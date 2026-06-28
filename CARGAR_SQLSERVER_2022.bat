@echo off
cd /d "%~dp0"
setlocal

set SERVER=localhost\SQLEXPRESS
if not "%~1"=="" set SERVER=%~1

where sqlcmd >nul 2>nul
if errorlevel 1 (
  echo No se encontro sqlcmd.
  echo Instale SQL Server 2022 y Microsoft Command Line Utilities for SQL Server.
  echo Tambien puede abrir los archivos de sql_sqlserver en SQL Server Management Studio.
  pause
  exit /b 1
)

echo Cargando base sunarp_academico en SQL Server 2022...
sqlcmd -S "%SERVER%" -E -i "sql_sqlserver\01_schema_sqlserver_2022.sql"
if errorlevel 1 goto error

echo Cargando 50 registros de demostracion...
sqlcmd -S "%SERVER%" -E -i "sql_sqlserver\02_seed_demo_sqlserver_2022.sql"
if errorlevel 1 goto error

echo.
echo Base cargada correctamente en %SERVER%.
pause
exit /b 0

:error
echo.
echo No se pudo cargar la base en SQL Server.
echo Revise que el servicio este iniciado y que el servidor sea correcto.
echo Ejemplo: CARGAR_SQLSERVER_2022.bat localhost\SQLEXPRESS
pause
exit /b 1

