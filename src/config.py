# -*- coding: utf-8 -*-
"""Configuracion de conexion SQL para el proyecto academico SUNARP."""

import os


DB_CONFIG = {
    "host": os.getenv("SUNARP_DB_HOST", "127.0.0.1"),
    "port": int(os.getenv("SUNARP_DB_PORT", "3306")),
    "user": os.getenv("SUNARP_DB_USER", "root"),
    "password": os.getenv("SUNARP_DB_PASSWORD", ""),
    "database": os.getenv("SUNARP_DB_NAME", "sunarp_academico"),
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
