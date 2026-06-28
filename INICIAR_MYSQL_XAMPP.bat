@echo off
set MYSQLD=C:\xampp\mysql\bin\mysqld.exe
set MYINI=C:\xampp\mysql\bin\my.ini

if not exist "%MYSQLD%" (
  echo No se encontro MariaDB en C:\xampp.
  pause
  exit /b 1
)

echo Iniciando MySQL/MariaDB de XAMPP...
start "SUNARP SQL - MariaDB" /min "%MYSQLD%" --defaults-file="%MYINI%" --standalone
timeout /t 4 >nul
C:\xampp\mysql\bin\mysqladmin.exe -uroot ping
pause
