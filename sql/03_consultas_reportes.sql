USE sunarp_academico;

-- 1. Listado general para revision del profesor.
SELECT
  item,
  bloque,
  oficina,
  oficio,
  titulo,
  partida,
  nombre,
  dni_ruc,
  estado_sunarp,
  fecha_presentacion,
  fecha_vencimiento,
  pdf_descargado
FROM titulos_registrales
ORDER BY item;

-- 2. Buscar un titulo especifico.
SELECT *
FROM titulos_registrales
WHERE titulo = '393004';

-- 3. Validacion interna SQL por partida.
-- Importante: esta consulta es para la base de datos, no para SUNARP.
SELECT item, bloque, oficio, titulo, partida, nombre, estado_sunarp
FROM titulos_registrales
WHERE partida = 'P03010001';

-- 4. Resumen por estado SUNARP.
SELECT *
FROM vw_resumen_estado
ORDER BY cantidad DESC;

-- 5. Avance por bloque o lote.
SELECT *
FROM vw_avance_bloque
ORDER BY bloque;

-- 6. Titulos pendientes de seguimiento.
SELECT item, bloque, oficio, titulo, partida, nombre, estado_sunarp
FROM titulos_registrales
WHERE estado_sunarp IN ('PENDIENTE', 'CALIFICACION')
ORDER BY bloque, item;

-- 7. Historial de cambios de estado.
SELECT
  t.titulo,
  t.partida,
  t.nombre,
  h.estado_anterior,
  h.estado_nuevo,
  h.observacion,
  h.fecha_cambio
FROM historial_estados h
JOIN titulos_registrales t ON t.id = h.titulo_id
ORDER BY h.fecha_cambio DESC;

-- 8. Evidencia de integridad general.
SELECT
  COUNT(*) AS total_registros,
  SUM(CASE WHEN titulo IS NOT NULL THEN 1 ELSE 0 END) AS registros_con_titulo,
  SUM(CASE WHEN partida IS NOT NULL OR partida_web IS NOT NULL THEN 1 ELSE 0 END) AS registros_con_partida,
  SUM(CASE WHEN estado_sunarp <> 'PENDIENTE' THEN 1 ELSE 0 END) AS registros_procesados
FROM titulos_registrales;

-- 9. Lotes registrados y cantidad por lote.
SELECT
  l.nombre_lote,
  l.fecha_creacion,
  COUNT(t.id) AS total_titulos
FROM lotes_seguimiento l
LEFT JOIN titulos_registrales t ON t.lote_id = l.id
GROUP BY l.id, l.nombre_lote, l.fecha_creacion
ORDER BY l.fecha_creacion DESC;

-- 10. Verificacion de duplicados por titulo consultable.
SELECT titulo, COUNT(*) AS repeticiones
FROM titulos_registrales
WHERE titulo IS NOT NULL
GROUP BY titulo
HAVING COUNT(*) > 1;
