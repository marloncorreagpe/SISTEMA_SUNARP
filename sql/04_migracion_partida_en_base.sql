USE sunarp_academico;

-- Permite conservar filas reales que tienen partida aunque aun no tengan titulo.
-- La consulta operativa SUNARP sigue siendo por titulo; partida queda como dato SQL.
ALTER TABLE titulos_registrales
  MODIFY titulo VARCHAR(40) NULL;

SET @idx_partida := (
  SELECT COUNT(*)
  FROM information_schema.statistics
  WHERE table_schema = DATABASE()
    AND table_name = 'titulos_registrales'
    AND index_name = 'idx_titulos_partida'
);
SET @sql_idx_partida := IF(
  @idx_partida = 0,
  'CREATE INDEX idx_titulos_partida ON titulos_registrales (partida)',
  'SET @noop_idx_partida := 0'
);
PREPARE stmt_idx_partida FROM @sql_idx_partida;
EXECUTE stmt_idx_partida;
DEALLOCATE PREPARE stmt_idx_partida;

SET @idx_partida_web := (
  SELECT COUNT(*)
  FROM information_schema.statistics
  WHERE table_schema = DATABASE()
    AND table_name = 'titulos_registrales'
    AND index_name = 'idx_titulos_partida_web'
);
SET @sql_idx_partida_web := IF(
  @idx_partida_web = 0,
  'CREATE INDEX idx_titulos_partida_web ON titulos_registrales (partida_web)',
  'SET @noop_idx_partida_web := 0'
);
PREPARE stmt_idx_partida_web FROM @sql_idx_partida_web;
EXECUTE stmt_idx_partida_web;
DEALLOCATE PREPARE stmt_idx_partida_web;
