# Velocidades en tiempo real del componente Zonal

Cálculo de las velocidades del SITP a partir de las posiciones log

## Ajustes pendientes:
 * Es necesario trabajar en la rama main, y eliminar la rama master. Tener cuidado al realizar eso!!!. Por eso es aconsejable realizar ese procedimiento al iniciar el repositorio. (Ok)
 
 * Es necesario utilizar rutas relativas a los arcchivos, de lo contarios no se podrá acceder a los recursos. P.ej.:
 
 -- En requierements: geopandas @ file:///mnt/c/Users/aarin/OneDrive/Documentos/work/maquina_virtual/sitp_velocidades/geopandas (Ok)
 
 * El job.sh no es necesario. Tener presente que no se utilizará crontab para ejecutar el script. (Ok)
 
 * Ubicar todos los archivos .sql dentro de la carpeta sql, me refiero al query.sql que está en la raiz del directorio. (Ok)

 * Ubicar los notebooks dentro de la carpeta notebooks (Ok)
 
 * Es necesario documentar las funciones doc strings y usar type hints para los parametros de funciones (no para otras variables).
 
 * Reemplazar los comentarios de este readme con información que complemente la documentación del código, por ejemplo debe decir cada cuanto se ejecuta el script, cada cuanto se actualiza la información geográfica, problemas detectados que se deban corregir, consideraciones a tener en cuenta y que no son evidentes al leer el código, etc
 
 * Así mismo se deberá incluir un indice del repositorio, al final dejo un ejemplo.

 * Se realizan algunos ajustes en varios archivos y se dejan algunos comentarios con inquietudes. Es necesario realizar un pull y revisar los ajustes y al final eliminar los comentarios.



########################




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
