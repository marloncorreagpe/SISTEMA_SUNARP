@echo off
cd /d "%~dp0"
set PYTHONDONTWRITEBYTECODE=1
echo ============================================
echo   Validacion tecnica SUNARP SQL
echo ============================================
echo.
echo [1/2] Ejecutando pruebas automaticas...
python -m unittest tests.test_integracion_sql -v
if errorlevel 1 goto error

echo.
echo [2/2] Generando evidencia tecnica...
python src\demo_profesor.py
if errorlevel 1 goto error

echo.
echo Validacion completada correctamente.
pause
exit /b 0

:error
echo.
echo La validacion encontro un problema. Revise MySQL/MariaDB y la base demo.
pause
exit /b 1
