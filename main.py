from src.get_data import positions, shape, speeds, union, insert_function ######> ajustar nombrees de funciones de acuerdo a los cambios en get_data()
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s:%(levelname)s:%(message)s')

######> en este archivo se deberian traer las fucniones de get_data y orquestar el fuljo de trabajo, algo así:


def sitp_speeds_workflow():
  """
  docuementar...
  """
  raw_data       = positions()
  geo_info       = shape()
  data_processed = speeds(raw_data)
  data_speeds    = union(data_processed, geo_info)
  insert_function(data_speeds)

if __name__ == "__main__":
  sitp_speeds_workflow()
  
