@echo off
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
set SUNARP_DB_ENGINE=mysql
python src\formularios.py
pause
