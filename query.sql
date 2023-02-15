SET TIMEZONE = 'America/Bogota';
WITH base AS (

    SELECT *, CURRENT_DATE as actual 
    FROM snap.sensor_vol
    
)
SELECT *
FROM base
WHERE fecha IN (actual)