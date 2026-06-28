@echo off
cd /d "%~dp0"
set SUNARP_DB_ENGINE=mysql
python src\main.py
pause
