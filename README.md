# Velocidades en tiempo real del componente Zonal

Cálculo de las velocidades del SITP a partir de las posiciones log


# Gestor de flujos de trabajo de Procesos ETL y pipelines de proyectos de Machine Learning.

## Descripción
Este repositorio contiene la configuración de un ambiente de desarrollo y producción para el gestor de flujos de trabajo de **Apache Airflow**.
El ambiente de desarrollo y de producción se construye con docker y docker-compose.
Es necesario instalar y configurar Nginx para crer un proxy inverso y poder acceder a la interfaz web de Airflow [Airflow GUI](http://20.110.226.237/airflow/).
El despliegue e integración continua (CI/CD) se realiza con Github Actions, el runner se encuentra dentro de la misma máquina virtual donde se despliega el ambiente de producción. 
Una vez que se despliega el ambiente de producción no es necesario realizar ninguna configuración adicional, los cambios que se realicen en el repositorio en la rama "main" se reflejarán automáticamente.

## Archivos de configuración de conexiones y variables de ambiente
* [.env](./.env)
* [config.yaml](./scripts/config.yaml)

## Archivo con el listado de dependencias
* [requirements.txt](./requirements.txt)

## Archivo de configuración para construir la imagen de Airflow personalizada
* [Dockerfile](./Dockerfile)

## Archivo de configuración para construir las imagenes y los contenedores de Airflow (postgres, redis, airflow)
* [docker-compose.yaml](./docker-compose.yaml)

## Configuración del ambiente de desarrollo
* Verificar que EL UID del usuario que ejecutará el contenedor de airflow sea el mismo el archivo [.env](./.env) con el comando `id -u`.
* Ejecutar el archivo [build.sh](./build.sh)

## Configuración del ambiente de producción
* Descomentar las lineas 5 y 6 del archivo [Dockerfile](./Dockerfile)
* Descomentar las lineas 3 y 4 del archivo [.env](./.env)
* Verificar que EL UID del usuario que ejecutará el contenedor de airflow sea el mismo el archivo [.env](./.env) con el comando `id -u`.
* Ejecutar el archivo [build.sh](./build.sh)

## Procesamiento de los datos

Para el procesamiento de los datos en primer lugar debe realizarse el query de la base de datos de 
de Transmilenio para obtener el listado de las posiciones log de los vehículos del componente zonal en el periodo de tiempo especificado.

Despues de lo anterior se procede a emparejar los datos con su respectivo siguinete, por ello se agrupa por vehículo, ruta y viaje. Y se calculan variables de distancia, tiempo y velocidad entre los puntos consecutivos. Posterior a esto, se determina si los deltas son positivos o negativos para clasificar los puntos en cuadrantes (esto se hace para evitar el uso de la función atan2 que en reiteradas pruebas consumio bastante tiempo en el cálculo de los ángulos o Bearings de los segmentos por lo cual para garantizar los mismos resultados se relizan los ajustes y correcciones a los ángulos de 0°, 180° y 360°).

Y se realiza el cálculo de los cuartos de hora que es la unidad mínima de tiempo en la que se agruparía la información.

En cuando al procesamiento geo espacial, la metodología que se emplea para el cruce con el shape de la malla vial es que el centro de gravedad se encuentre dentro del póligono y como en un segmento el centro de gravedad está en el punto medio, se calcula el punto medio como elemento geométrico.


## Shape de la Malla Vial

Este es el shape de los corredores principales y vías a las que tanto Waze como Traffic Now (sensores) hacen seguimiento, el shape comprende los poligonos de los tramos viales divididos en subtramos a los que se les puede calcular una orientación clave para el Bearing de los segmentos con el que se debe comparar para que ambos coincidan en este parámetro.
Este shape también contiene información referente a los corredores preferenciales.
Y la última actualialización es del dia 15 de marzo del 2023. Esta información se actualiza dependiendo del requerimiento o cambios considerables que puedan afectar los resultados de los diferentes análisis.
