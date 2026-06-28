IF DB_ID(N'sunarp_academico') IS NULL
BEGIN
    CREATE DATABASE sunarp_academico;
END
GO

USE sunarp_academico;
GO

IF OBJECT_ID(N'historial_estados', N'U') IS NOT NULL DROP TABLE historial_estados;
IF OBJECT_ID(N'titulos_registrales', N'U') IS NOT NULL DROP TABLE titulos_registrales;
IF OBJECT_ID(N'lotes_seguimiento', N'U') IS NOT NULL DROP TABLE lotes_seguimiento;
GO

CREATE TABLE lotes_seguimiento (
    id INT IDENTITY(1,1) PRIMARY KEY,
    nombre_lote VARCHAR(80) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NULL,
    fecha_creacion DATETIME2 NOT NULL DEFAULT SYSDATETIME()
);

CREATE TABLE titulos_registrales (
    id INT IDENTITY(1,1) PRIMARY KEY,
    lote_id INT NULL,
    item INT NOT NULL,
    bloque VARCHAR(10) NOT NULL DEFAULT '00',
    oficina VARCHAR(40) NOT NULL,
    anio_consulta INT NOT NULL,
    oficio VARCHAR(40) NOT NULL,
    titulo VARCHAR(40) NULL,
    nombre VARCHAR(120) NOT NULL,
    dni_ruc VARCHAR(11) NOT NULL,
    partida VARCHAR(40) NULL,
    estado_base VARCHAR(30) NULL,
    observacion_base VARCHAR(255) NULL,
    estado_sunarp VARCHAR(30) NOT NULL DEFAULT 'PENDIENTE',
    tipo_registro VARCHAR(80) NULL,
    partida_web VARCHAR(40) NULL,
    acto_descripcion VARCHAR(180) NULL,
    criterio_validacion VARCHAR(180) NULL,
    fecha_presentacion DATE NULL,
    hora_presentacion TIME NULL,
    fecha_vencimiento DATE NULL,
    pdf_descargado VARCHAR(20) NOT NULL DEFAULT 'NO',
    pdf_observacion VARCHAR(255) NULL,
    pdf_inscripcion VARCHAR(255) NULL,
    error VARCHAR(MAX) NULL,
    source_row INT NULL,
    source_error VARCHAR(255) NULL,
    actualizado DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT uq_titulo UNIQUE (titulo),
    CONSTRAINT uq_lote_item UNIQUE (lote_id, item),
    CONSTRAINT fk_titulos_lote FOREIGN KEY (lote_id)
        REFERENCES lotes_seguimiento(id)
        ON UPDATE CASCADE
        ON DELETE SET NULL
);

CREATE INDEX idx_titulos_partida ON titulos_registrales(partida);
CREATE INDEX idx_titulos_partida_web ON titulos_registrales(partida_web);

CREATE TABLE historial_estados (
    id INT IDENTITY(1,1) PRIMARY KEY,
    titulo_id INT NOT NULL,
    estado_anterior VARCHAR(30) NULL,
    estado_nuevo VARCHAR(30) NOT NULL,
    observacion VARCHAR(255) NULL,
    fecha_cambio DATETIME2 NOT NULL DEFAULT SYSDATETIME(),
    CONSTRAINT fk_historial_titulo FOREIGN KEY (titulo_id)
        REFERENCES titulos_registrales(id)
        ON UPDATE CASCADE
        ON DELETE CASCADE
);
GO

CREATE OR ALTER VIEW vw_resumen_estado AS
SELECT
    estado_sunarp,
    COUNT(*) AS cantidad,
    CAST(ROUND(COUNT(*) * 100.0 / NULLIF((SELECT COUNT(*) FROM titulos_registrales), 0), 2) AS DECIMAL(10,2)) AS porcentaje
FROM titulos_registrales
GROUP BY estado_sunarp;
GO

CREATE OR ALTER VIEW vw_avance_bloque AS
SELECT
    bloque,
    COUNT(*) AS total,
    SUM(CASE WHEN estado_sunarp <> 'PENDIENTE' THEN 1 ELSE 0 END) AS procesados,
    CAST(ROUND(SUM(CASE WHEN estado_sunarp <> 'PENDIENTE' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS DECIMAL(10,2)) AS avance
FROM titulos_registrales
GROUP BY bloque;
GO
