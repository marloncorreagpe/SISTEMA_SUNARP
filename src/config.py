# -*- coding: utf-8 -*-
"""Configuracion de conexion SQL para el proyecto academico SUNARP."""

import os

DB_ENGINE = os.getenv("SUNARP_DB_ENGINE", "mssql").lower()

MYSQL_CONFIG = {
    "host": os.getenv("SUNARP_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("SUNARP_DB_PORT", "3306")),
    "user": os.getenv("SUNARP_DB_USER", "root"),
    "password": os.getenv("SUNARP_DB_PASSWORD", ""),
    "database": os.getenv("SUNARP_DB_NAME", "sunarp_academico"),
}

SQLSERVER_CONFIG = {
    "server": os.getenv("SUNARP_SQLSERVER", r"localhost\SQLEXPRESS"),
    "database": os.getenv("SUNARP_DB_NAME", "sunarp_academico"),
    "trusted_connection": os.getenv("SUNARP_SQLSERVER_TRUSTED", "yes"),
    "driver": os.getenv("SUNARP_SQLSERVER_DRIVER", "ODBC Driver 18 for SQL Server"),
    "username": os.getenv("SUNARP_SQLSERVER_USER", ""),
    "password": os.getenv("SUNARP_SQLSERVER_PASSWORD", ""),
}


ESTADOS_VALIDOS = [
    "INSCRITO",
    "OBSERVADO",
    "TACHADO",
    "PENDIENTE",
    "CALIFICACION",
    "NO_ENCONTRADO",
    "RESERVADO",
    "FUERA_ALCANCE_REGISTRO",
]

OFICINAS_VALIDAS = ["LIMA", "CALLAO", "HUACHO", "BARRANCA"]
