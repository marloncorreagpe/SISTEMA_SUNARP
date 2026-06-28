USE sunarp_academico;

INSERT INTO lotes_seguimiento (nombre_lote, descripcion)
VALUES ('DEMO_2026_01', 'Lote academico de 50 titulos SUNARP para pruebas')
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

SET @lote_demo := (SELECT id FROM lotes_seguimiento WHERE nombre_lote = 'DEMO_2026_01');

INSERT INTO titulos_registrales
(lote_id, item, bloque, oficina, anio_consulta, oficio, titulo, nombre, dni_ruc, partida, estado_sunarp, fecha_presentacion, fecha_vencimiento, pdf_descargado, source_row)
VALUES
(@lote_demo, 1, '01', 'LIMA', 2026, 'OF-2026-1001', '393004', 'Juan Perez', '12345678', 'P03010001', 'INSCRITO', '2026-05-02', '2026-06-20', 'SI', 2),
(@lote_demo, 2, '01', 'CALLAO', 2026, 'OF-2026-1002', '393011', 'Maria Quispe', '23456789', 'P03010002', 'OBSERVADO', '2026-05-04', '2026-06-22', 'SI', 3),
(@lote_demo, 3, '01', 'HUACHO', 2026, 'OF-2026-1003', '393018', 'Luis Ramos', '34567890', 'P03010003', 'PENDIENTE', '2026-05-05', '2026-06-23', 'NO', 4),
(@lote_demo, 4, '01', 'BARRANCA', 2026, 'OF-2026-1004', '393026', 'Ana Torres', '45678901', 'P03010004', 'CALIFICACION', '2026-05-06', '2026-06-24', 'NO_REQUIERE', 5),
(@lote_demo, 5, '01', 'LIMA', 2026, 'OF-2026-1005', '393033', 'Carlos Flores', '56789012', 'P03010005', 'TACHADO', '2026-05-07', '2026-06-25', 'NO_REQUIERE', 6),
(@lote_demo, 6, '02', 'CALLAO', 2026, 'OF-2026-1006', '393039', 'Rosa Diaz', '67890123', 'P03010006', 'NO_ENCONTRADO', '2026-05-08', NULL, 'NO_REQUIERE', 7),
(@lote_demo, 7, '02', 'HUACHO', 2026, 'OF-2026-1007', '393047', 'Pedro Castro', '78901234', 'P03010007', 'INSCRITO', '2026-05-09', '2026-06-26', 'SI', 8),
(@lote_demo, 8, '02', 'BARRANCA', 2026, 'OF-2026-1008', '393055', 'Elena Vargas', '89012345', 'P03010008', 'OBSERVADO', '2026-05-10', '2026-06-27', 'SI', 9),
(@lote_demo, 9, '02', 'LIMA', 2026, 'OF-2026-1009', '393061', 'Jorge Mendoza', '90123456', 'P03010009', 'PENDIENTE', '2026-05-11', '2026-06-28', 'NO', 10),
(@lote_demo, 10, '02', 'CALLAO', 2026, 'OF-2026-1010', '393069', 'Lucia Rojas', '10234567', 'P03010010', 'CALIFICACION', '2026-05-12', '2026-06-29', 'NO_REQUIERE', 11),
(@lote_demo, 11, '03', 'HUACHO', 2026, 'OF-2026-1011', '393076', 'Miguel Salas', '11234567', 'P03010011', 'INSCRITO', '2026-05-13', '2026-06-30', 'SI', 12),
(@lote_demo, 12, '03', 'BARRANCA', 2026, 'OF-2026-1012', '393083', 'Carmen Rios', '12234567', 'P03010012', 'TACHADO', '2026-05-14', '2026-07-01', 'NO_REQUIERE', 13),
(@lote_demo, 13, '03', 'LIMA', 2026, 'OF-2026-1013', '393091', 'Juan Perez', '13234567', 'P03010013', 'OBSERVADO', '2026-05-15', '2026-07-02', 'SI', 14),
(@lote_demo, 14, '03', 'CALLAO', 2026, 'OF-2026-1014', '393098', 'Maria Quispe', '14234567', 'P03010014', 'PENDIENTE', '2026-05-16', '2026-07-03', 'NO', 15),
(@lote_demo, 15, '03', 'HUACHO', 2026, 'OF-2026-1015', '393106', 'Luis Ramos', '15234567', 'P03010015', 'CALIFICACION', '2026-05-17', '2026-07-04', 'NO_REQUIERE', 16),
(@lote_demo, 16, '04', 'BARRANCA', 2026, 'OF-2026-1016', '393112', 'Ana Torres', '16234567', 'P03010016', 'INSCRITO', '2026-05-18', '2026-07-05', 'SI', 17),
(@lote_demo, 17, '04', 'LIMA', 2026, 'OF-2026-1017', '393119', 'Carlos Flores', '17234567', 'P03010017', 'NO_ENCONTRADO', '2026-05-19', NULL, 'NO_REQUIERE', 18),
(@lote_demo, 18, '04', 'CALLAO', 2026, 'OF-2026-1018', '393126', 'Rosa Diaz', '18234567', 'P03010018', 'OBSERVADO', '2026-05-20', '2026-07-06', 'SI', 19),
(@lote_demo, 19, '04', 'HUACHO', 2026, 'OF-2026-1019', '393134', 'Pedro Castro', '19234567', 'P03010019', 'PENDIENTE', '2026-05-21', '2026-07-07', 'NO', 20),
(@lote_demo, 20, '04', 'BARRANCA', 2026, 'OF-2026-1020', '393141', 'Elena Vargas', '20234567', 'P03010020', 'TACHADO', '2026-05-22', '2026-07-08', 'NO_REQUIERE', 21),
(@lote_demo, 21, '05', 'LIMA', 2026, 'OF-2026-1021', '393149', 'Jorge Mendoza', '21234567', 'P03010021', 'INSCRITO', '2026-05-03', '2026-06-21', 'SI', 22),
(@lote_demo, 22, '05', 'CALLAO', 2026, 'OF-2026-1022', '393156', 'Lucia Rojas', '22234567', 'P03010022', 'CALIFICACION', '2026-05-04', '2026-06-22', 'NO_REQUIERE', 23),
(@lote_demo, 23, '05', 'HUACHO', 2026, 'OF-2026-1023', '393164', 'Miguel Salas', '23234567', 'P03010023', 'PENDIENTE', '2026-05-05', '2026-06-23', 'NO', 24),
(@lote_demo, 24, '05', 'BARRANCA', 2026, 'OF-2026-1024', '393171', 'Carmen Rios', '24234567', 'P03010024', 'OBSERVADO', '2026-05-06', '2026-06-24', 'SI', 25),
(@lote_demo, 25, '05', 'LIMA', 2026, 'OF-2026-1025', '393178', 'Juan Perez', '25234567', 'P03010025', 'INSCRITO', '2026-05-07', '2026-06-25', 'SI', 26),
(@lote_demo, 26, '06', 'CALLAO', 2026, 'OF-2026-1026', '393186', 'Maria Quispe', '26234567', 'P03010026', 'TACHADO', '2026-05-08', '2026-06-26', 'NO_REQUIERE', 27),
(@lote_demo, 27, '06', 'HUACHO', 2026, 'OF-2026-1027', '393193', 'Luis Ramos', '27234567', 'P03010027', 'PENDIENTE', '2026-05-09', '2026-06-27', 'NO', 28),
(@lote_demo, 28, '06', 'BARRANCA', 2026, 'OF-2026-1028', '393201', 'Ana Torres', '28234567', 'P03010028', 'NO_ENCONTRADO', '2026-05-10', NULL, 'NO_REQUIERE', 29),
(@lote_demo, 29, '06', 'LIMA', 2026, 'OF-2026-1029', '393208', 'Carlos Flores', '29234567', 'P03010029', 'CALIFICACION', '2026-05-11', '2026-06-28', 'NO_REQUIERE', 30),
(@lote_demo, 30, '06', 'CALLAO', 2026, 'OF-2026-1030', '393216', 'Rosa Diaz', '30234567', 'P03010030', 'INSCRITO', '2026-05-12', '2026-06-29', 'SI', 31),
(@lote_demo, 31, '07', 'HUACHO', 2026, 'OF-2026-1031', '393223', 'Pedro Castro', '31234567', 'P03010031', 'OBSERVADO', '2026-05-13', '2026-06-30', 'SI', 32),
(@lote_demo, 32, '07', 'BARRANCA', 2026, 'OF-2026-1032', '393231', 'Elena Vargas', '32234567', 'P03010032', 'PENDIENTE', '2026-05-14', '2026-07-01', 'NO', 33),
(@lote_demo, 33, '07', 'LIMA', 2026, 'OF-2026-1033', '393238', 'Jorge Mendoza', '33234567', 'P03010033', 'TACHADO', '2026-05-15', '2026-07-02', 'NO_REQUIERE', 34),
(@lote_demo, 34, '07', 'CALLAO', 2026, 'OF-2026-1034', '393246', 'Lucia Rojas', '34234567', 'P03010034', 'INSCRITO', '2026-05-16', '2026-07-03', 'SI', 35),
(@lote_demo, 35, '07', 'HUACHO', 2026, 'OF-2026-1035', '393253', 'Miguel Salas', '35234567', 'P03010035', 'CALIFICACION', '2026-05-17', '2026-07-04', 'NO_REQUIERE', 36),
(@lote_demo, 36, '08', 'BARRANCA', 2026, 'OF-2026-1036', '393261', 'Carmen Rios', '36234567', 'P03010036', 'OBSERVADO', '2026-05-18', '2026-07-05', 'SI', 37),
(@lote_demo, 37, '08', 'LIMA', 2026, 'OF-2026-1037', '393268', 'Juan Perez', '37234567', 'P03010037', 'PENDIENTE', '2026-05-19', '2026-07-06', 'NO', 38),
(@lote_demo, 38, '08', 'CALLAO', 2026, 'OF-2026-1038', '393276', 'Maria Quispe', '38234567', 'P03010038', 'NO_ENCONTRADO', '2026-05-20', NULL, 'NO_REQUIERE', 39),
(@lote_demo, 39, '08', 'HUACHO', 2026, 'OF-2026-1039', '393283', 'Luis Ramos', '39234567', 'P03010039', 'INSCRITO', '2026-05-21', '2026-07-07', 'SI', 40),
(@lote_demo, 40, '08', 'BARRANCA', 2026, 'OF-2026-1040', '393291', 'Ana Torres', '40234567', 'P03010040', 'TACHADO', '2026-05-22', '2026-07-08', 'NO_REQUIERE', 41),
(@lote_demo, 41, '09', 'LIMA', 2026, 'OF-2026-1041', '393298', 'Carlos Flores', '41234567', 'P03010041', 'CALIFICACION', '2026-05-03', '2026-06-21', 'NO_REQUIERE', 42),
(@lote_demo, 42, '09', 'CALLAO', 2026, 'OF-2026-1042', '393306', 'Rosa Diaz', '42234567', 'P03010042', 'PENDIENTE', '2026-05-04', '2026-06-22', 'NO', 43),
(@lote_demo, 43, '09', 'HUACHO', 2026, 'OF-2026-1043', '393313', 'Pedro Castro', '43234567', 'P03010043', 'OBSERVADO', '2026-05-05', '2026-06-23', 'SI', 44),
(@lote_demo, 44, '09', 'BARRANCA', 2026, 'OF-2026-1044', '393321', 'Elena Vargas', '44234567', 'P03010044', 'INSCRITO', '2026-05-06', '2026-06-24', 'SI', 45),
(@lote_demo, 45, '09', 'LIMA', 2026, 'OF-2026-1045', '393328', 'Jorge Mendoza', '45234567', 'P03010045', 'TACHADO', '2026-05-07', '2026-06-25', 'NO_REQUIERE', 46),
(@lote_demo, 46, '10', 'CALLAO', 2026, 'OF-2026-1046', '393336', 'Lucia Rojas', '46234567', 'P03010046', 'PENDIENTE', '2026-05-08', '2026-06-26', 'NO', 47),
(@lote_demo, 47, '10', 'HUACHO', 2026, 'OF-2026-1047', '393343', 'Miguel Salas', '47234567', 'P03010047', 'NO_ENCONTRADO', '2026-05-09', NULL, 'NO_REQUIERE', 48),
(@lote_demo, 48, '10', 'BARRANCA', 2026, 'OF-2026-1048', '393351', 'Carmen Rios', '48234567', 'P03010048', 'CALIFICACION', '2026-05-10', '2026-06-27', 'NO_REQUIERE', 49),
(@lote_demo, 49, '10', 'LIMA', 2026, 'OF-2026-1049', '393358', 'Juan Perez', '49234567', 'P03010049', 'OBSERVADO', '2026-05-11', '2026-06-28', 'SI', 50),
(@lote_demo, 50, '10', 'CALLAO', 2026, 'OF-2026-1050', '393366', 'Maria Quispe', '50234567', 'P03010050', 'INSCRITO', '2026-05-12', '2026-06-29', 'SI', 51)
ON DUPLICATE KEY UPDATE
  estado_sunarp = VALUES(estado_sunarp),
  fecha_presentacion = VALUES(fecha_presentacion),
  fecha_vencimiento = VALUES(fecha_vencimiento),
  pdf_descargado = VALUES(pdf_descargado),
  actualizado = CURRENT_TIMESTAMP;

INSERT INTO historial_estados
(titulo_id, estado_anterior, estado_nuevo, observacion)
SELECT
  t.id,
  'PENDIENTE',
  t.estado_sunarp,
  'Carga inicial demo para trazabilidad'
FROM titulos_registrales t
WHERE t.titulo = '393011'
  AND NOT EXISTS (
    SELECT 1
    FROM historial_estados h
    WHERE h.titulo_id = t.id
      AND h.observacion = 'Carga inicial demo para trazabilidad'
  );
