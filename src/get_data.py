### Importe de las librerías a utilizar

import numpy as np
import datetime
import pandas as pd
import geopandas as gpd
from google.cloud import bigquery
from google.oauth2 import service_account
from datetime import date
from math import degrees, atan
from shapely.geometry import Point
import yaml
from pathlib import Path
import logging

logging.basicConfig(filename='speeds.log', level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


t = datetime.datetime.now()
n = t.strftime('%Y-%m-%d') + '--' + t.strftime('%H')
dir = f'/home/administrador/monitoreo/sitp_speeds_new/Dia_sin_carro/data/{n}.csv'


def conexion_bq():
    
    cwd = Path.cwd()
    logging.info('Conectando a las base de TMSA ...')
    key_path = cwd / 'helios/smart-helios-3.json'
    credentials = service_account.Credentials.from_service_account_file(key_path,scopes=["https://www.googleapis.com/auth/cloud-platform"])
    client = bigquery.Client(credentials=credentials, project='transmilenio-dwh-shvpc')

    return client


def positions():
    
    cwd = Path.cwd()
    logging.info('Realizando la consulta de las posiciones ...')
    file = open(cwd / 'sql/positions.sql', 'r')
    q = file.read()
    file.close()
    q = q.replace('previous_date', datetime.datetime.strftime(date.today(), '%Y-%m-%d'))
    df = (conexion_bq().query(q).result().to_dataframe(create_bqstorage_client=True))

    return df


def speeds():
    
    logging.info('Cargando las posiciones en un df ...')
    df = positions()
    df['seconds'] = df['datetime1']+5*3600
    df = df.drop(columns=['datetime1'])

    ### Emparejamiento con el punto siguiente

    logging.info(f'Emparejamiento con posición anterior ...')
    df1 = df.groupby(['id_vehiculo', 'id_ruta', 'viaje'])[['seconds', 'coordx', 'coordy']].shift(1)
    df1 = df1.rename(columns = {'seconds':'t1', 'coordx':'x1', 'coordy':'y1'})
    df = pd.concat([df, df1], axis=1)
    df = df.rename(columns={'seconds': 't2', 'coordx': 'x2', 'coordy': 'y2'})
    df = df.dropna()    

    ### Cálculo de variables distancia, tiempo y velocidad entre puntos consecutivos

    logging.info(f'Cálculo de variables de distancia, tiempo y velocidad ...')
    df['delta_t'] = df['t2'] - df['t1']
    df['delta_d'] = round(((df.x2-df.x1)**2 + (df.y2-df.y1)**2)**0.5,4)
    df['vel'] = df['delta_d']/df['delta_t']
    df = df[(df.vel>0.3)&(df.vel<17)]

    ### Variables de confirmación

    logging.info(f'Cálculo de variables de confirmación ...')
    df['delta_y>0'] = df['y2']>df['y1']
    df['delta_x>0'] = df['x2']>df['x1']
    df['delta_y=0'] = df['y2']==df['y1']
    df['delta_x=0'] = df['x2']==df['x1']

    # Cálculo de los cuadrantes para los Bearings

    logging.info(f'Cálculo de cuadrantes ...')
    df['cuad'] = None
    df.loc[(df['delta_y>0'] == True)  & (df['delta_x>0'] == True),  'cuad'] = 1
    df.loc[(df['delta_y>0'] == True)  & (df['delta_x>0'] == False), 'cuad'] = 2
    df.loc[(df['delta_y>0'] == False) & (df['delta_x>0'] == False), 'cuad'] = 3
    df.loc[(df['delta_y>0'] == False) & (df['delta_x>0'] == True),  'cuad'] = 4

    # Cálculo de los Bearings

    logging.info(f'Cálculo de los bearings: ...')
    df['bearing'] = (df['y2']-df['y1'])/(df['x2']-df['x1'])
    df['bearing'] = df['bearing'].apply(lambda x: round(degrees(atan(x)),0))

    # Ajuste de los ángulos

    logging.info(f'Ajuste y corrección de los ángulos ...')
    df['bear'] = None
    df.loc[df.cuad == 1, 'bear'] = (90 - df.bearing)%360
    df.loc[df.cuad == 2, 'bear'] = (90 - (df.bearing + 180))%360
    df.loc[df.cuad == 3, 'bear'] = (90 - (df.bearing + 180))%360
    df.loc[df.cuad == 4, 'bear'] = (90 - (df.bearing + 360))%360

    df.loc[(df['delta_x=0']==True)&(df['cuad']==2), 'bear'] = 0
    df.loc[(df['delta_x=0']==True)&(df['cuad']==3), 'bear'] = 180
    df.loc[(df['bearing']==-90)&(df['cuad']==2), 'bear'] = 360

    # Quarter

    logging.info(f'Cálculo de los cuartos de hora ...')
    df['quarter'] = df['instante'].apply(lambda x: '23:45-00:00' if (x.hour == 23)&(x.minute>=45) else f'{x.hour:02}:{(x.minute//15)*15:02}-{(x.hour+1):02}:00' if x.minute>=45 else f'{x.hour:02}:{(x.minute//15)*15:02}-{x.hour:02}:{(x.minute//15+1)*15:02}').replace({'24':'00'})

    ### Elementos geoespaciales

    logging.info(f'Obtención de los puntos geoespaciales ...')    
    point = []
    df['x_m'] = (df['x1'] + df['x2'])*0.5
    df['y_m'] = (df['y1'] + df['y2'])*0.5
    a = np.array(df[['x_m', 'y_m']])

    for j in range(len(a)):

        point.append(Point(a[j][0],a[j][1]))


    ### Transformación a un geodataframe

    logging.info('Transformación a un geodataframe ...')
    dfg = gpd.GeoDataFrame(df, geometry=point, crs="EPSG:32618")

    return dfg


def shape():
    
    logging.info('Cargue del shape ...')
    df = gpd.read_file('/home/administrador/monitoreo/sitp_speeds_new/congestion/Último_08.01.23/polygons_projected_230108.shp')
    
    df.loc[((df['corredor']=='TV85,CL65BIS,KR85J') & (df['corr_14']==1)), 'corr_14'] = '0'
    df.loc[((df['corredor']=='CL.26.SUR') & (df['corr_14']==1)), 'corr_14'] = '0'
    df.loc[(df['tid'].apply(lambda x: x in ['1000766', '1000767', '1000768', '1000769', '1000770', '1000771', '1001207', '1001208', '1001209', '1001210', '1001211', '1001212', '1001990', '1001991'])), 'corredor'] = 'AV.AUTOSUR'  
    df['corredor'] = df['corredor'].apply(lambda x: x.replace('NQS', 'AV.NQS').replace('CL.26', 'AV.CL.26').replace('AUTONORTE', 'AV.AUTONORTE').replace('AV.68', 'AV.KR.68'))

    return df


def union():

    logging.info('Unión de las posiciones con el shape ...')
    un = gpd.sjoin(speeds(), shape())
    un['dif_bear'] = abs(un['bear']-un['bearing_right'])
    un = un[un.dif_bear<=30]
    un = un[un['corr_14']==1]
    un['hora'] = un['quarter'].apply(lambda x: int(x[:2]))
    un['vel_kmh'] = un['vel']*3.6

    ### Selección de variables definitivas

    logging.info('Selección de las variables definitivas y agrupación: ...')
    un = un.loc[:,['fecha', 'hora', 'tid', 'corredor', 'from_to', 'sentido', 'vel_kmh']]
    un = un.groupby(['fecha', 'hora', 'tid', 'corredor', 'from_to', 'sentido'])['vel_kmh'].mean().reset_index()
     
    return un


def insert_function():
    
    credentials_postgresql = None
    with open(r'/home/administrador/monitoreo/sitp_speeds_new/Dia_sin_carro/credentials_postgresql.yaml') as file:
        credentials_postgresql = yaml.load(file, Loader=yaml.FullLoader)
        
    user     = credentials_postgresql['user']
    password = credentials_postgresql['password']
    host     = credentials_postgresql['host']
    db_name  = credentials_postgresql['db']
    port     = str(credentials_postgresql['port'])
    
    SQLALCHEMY_CONNECTION = f'postgresql://{user}:{password}@{host}:{port}/{db_name}'

    chunksize = 10000
    i1 = 1
    i2 = chunksize
    
    for chunk in pd.read_csv(dir, decimal=',', sep='|', chunksize=chunksize):
        
        i1 = i1 + chunksize
        i2 = i2 + chunksize
        
        try:
            
            chunk.columns = ["fecha", "hora", "tid", "corredor", "from_to", "sentido", "vel_kmh"]
            chunk.to_sql(name='velocidades_sitp', con=SQLALCHEMY_CONNECTION, schema='dia_sin_carro', if_exists='append', method='multi', index=False)
            
        except:
            logging.info("DB operational Error: ")


# df = union()

# df.to_csv(dir, index=False, decimal=',', sep='|')

# df = pd.read_csv(dir, decimal=',', sep='|')

# insert_function()


print(speeds())