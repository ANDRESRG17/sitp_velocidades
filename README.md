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
