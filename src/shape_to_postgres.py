import datetime
import pandas as pd
import geopandas as gpd
from sqlalchemy import create_engine
#from geoalchemy2 import Geometry, WKTElement
from shapely.geometry import  MultiLineString, MultiPolygon
from shapely import wkt
from pathlib import Path
import yaml




def conection():
    
    cwd = Path.cwd()
    credentials_postgresql = None
    with open(cwd / 'config.yaml') as file:
        credentials_postgresql = yaml.load(file, Loader=yaml.SafeLoader)['postgres_db']
    
    user     = credentials_postgresql['user']
    password = credentials_postgresql['password']
    host     = credentials_postgresql['host']
    db_name  = credentials_postgresql['db']
    port     = str(credentials_postgresql['port'])
    admin    = credentials_postgresql['admin']
    
    engine = create_engine(f'{admin}://{user}:{password}@{host}:{port}/{db_name}')
    
    return engine

def get_shape():
    
    cwd = Path.cwd()
    s = gpd.read_file(cwd / 'shape_wst/shape_malla_wst_2023_01_31.shp')
    s.loc[((s['corredor']=='TV85,CL65BIS,KR85J') & (s['corr_14']==1)), 'corr_14'] = 0
    s.loc[((s['corredor']=='CL.26.SUR') & (s['corr_14']==1)), 'corr_14'] = 0
    s.loc[(s['tid'].apply(lambda x: x in ['1000766', '1000767', '1000768', '1000769', '1000770', '1000771', '1001207', '1001208', '1001209', '1001210', '1001211', '1001212', '1001990', '1001991'])), 'corredor'] = 'AV.AUTOSUR'
    s['corredor'] = s['corredor'].apply(lambda x: x.replace('NQS', 'AV.NQS').replace('CL.26', 'AV.CL.26').replace('AUTONORTE', 'AV.AUTONORTE').replace('AV.68', 'AV.KR.68'))
    # s['geome'] = s['geometry'].apply(lambda x: MultiPolygon([x]))
    # s['geometry'] = s['geometry'].apply(lambda x: wkt.dumps(x))

    # # s['geometry'] = s['geometry'].apply(lambda x: WKTElement(x.wkt, srid=32618))
    s['version'] = '2023-02-15'
    s = s.drop(columns = ['FID_', 'SHAPE_Leng', 'SHAPE_Area', 'nom_corr'])
    
    return s



def load():
    
    engine = conection()
    shape = get_shape()

    shape.to_postgis(
        name='shape_unificado',
        schema='test',
        con = engine,
        if_exists='replace',
        index=False,
        dtype={'geometry': 'MULTILINESTRING'}
        )


load()
