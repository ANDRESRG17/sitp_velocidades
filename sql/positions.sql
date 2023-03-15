DECLARE intervalo DATETIME DEFAULT TIMESTAMP_SUB(CURRENT_DATETIME('America/Bogota'), INTERVAL 60 MINUTE);
SELECT DISTINCT
    instante,
    fecha,
    (EXTRACT(TIME FROM CAST(instante AS TIMESTAMP))) AS hora,
    IFNULL(id_vehiculo, 0) AS id_vehiculo,
    IFNULL(id_ruta, 0) AS id_ruta,
    IFNULL(viaje, 0) AS viaje,
    coordx,
    coordy
FROM `transmilenio-dwh-shvpc.posicionbus.posicioneslog_buses`
WHERE fecha >= '2023-03-01' AND instante >= intervalo
ORDER BY
    id_vehiculo,
    id_ruta,
    viaje,
    instante