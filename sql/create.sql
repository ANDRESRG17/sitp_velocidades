CREATE TABLE IF NOT EXISTS dia_sin_carro.velocidades_sitp
(
    fecha date NOT NULL,
    hora integer NOT NULL,
    tid integer NOT NULL,
    corredor "char" NOT NULL,
    from_to "char" NOT NULL,
    sentido "char" NOT NULL,
    vel_kmh double precision NOT NULL
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE IF EXISTS dia_sin_carro.velocidades_sitp
    OWNER to central_datos_dim;
