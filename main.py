from src.get_data import conexion_bigquery, get_data_positions, get_speeds, get_shape, union, insert_function
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')


def sitp_speeds_workflow():
  """
    Esta función consolida el algoritmo de get_data y carga los datos en la base de datos
  """
  conexion       = conexion_bigquery()
  raw_data       = get_data_positions(conexion)
  geo_info       = get_shape()
  data_processed = get_speeds(raw_data)
  data_speeds    = union(data_processed, geo_info)
  insert_function(data_speeds)

if __name__ == "__main__":
  sitp_speeds_workflow()
  
