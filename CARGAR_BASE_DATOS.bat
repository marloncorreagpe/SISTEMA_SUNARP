@echo off
cd /d "%~dp0"
set MYSQL=C:\xampp\mysql\bin\mysql.exe

if not exist "%MYSQL%" (
  echo No se encontro MySQL en C:\xampp.
  echo Instale XAMPP o ajuste la ruta en este archivo.
  pause
  exit /b 1
)

echo Cargando estructura SQL...
"%MYSQL%" -uroot --default-character-set=utf8mb4 < sql\01_schema.sql
if errorlevel 1 goto error

echo Aplicando migracion de partida en base...
"%MYSQL%" -uroot --default-character-set=utf8mb4 < sql\04_migracion_partida_en_base.sql
if errorlevel 1 goto error

echo Cargando 50 registros demo...
"%MYSQL%" -uroot --default-character-set=utf8mb4 < sql\02_seed_demo.sql
if errorlevel 1 goto error

echo.
echo Base sunarp_academico cargada correctamente.
"%MYSQL%" -uroot --default-character-set=utf8mb4 -D sunarp_academico -e "SELECT COUNT(*) AS total_titulos FROM titulos_registrales; SELECT * FROM vw_resumen_estado ORDER BY cantidad DESC;"
pause
exit /b 0

:error
echo.
echo No se pudo cargar la base. Verifique que MySQL/MariaDB este iniciado en XAMPP.
pause
exit /b 1
