@echo off
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
set SUNARP_DB_ENGINE=mssql
if "%SUNARP_SQLSERVER%"=="" set SUNARP_SQLSERVER=localhost\SQLEXPRESS
if "%SUNARP_DB_NAME%"=="" set SUNARP_DB_NAME=sunarp_academico
python src\formularios.py
pause

