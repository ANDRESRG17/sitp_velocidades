with q1 as (   
    SELECT 
        *, (EXTRACT(TIME FROM CAST(A.instante AS TIMESTAMP))) as hora, CURRENT_TIME('America/Bogota') as hora2
    FROM 
        `transmilenio-dwh-shvpc.posicionbus.posicioneslog_buses` A
    WHERE
        A.fecha >= 'previous_date'
), q2 as (
    SELECT
        *, TIME_DIFF(hora2, hora, SECOND) as diff
    FROM q1
)
SELECT DISTINCT
    UNIX_SECONDS(CAST(instante AS TIMESTAMP)) AS datetime1, 
    IFNULL(id_vehiculo, 0) AS id_vehiculo,
    IFNULL(id_ruta, 0) AS id_ruta,
    IFNULL(viaje, 0) AS viaje,
    instante,
    hora,
    fecha,   
    coordx AS coordx,
    coordy AS coordy
FROM q2
WHERE diff <= 1*12*5*60
ORDER BY
    id_vehiculo,
    id_ruta,
    viaje,
    datetime1