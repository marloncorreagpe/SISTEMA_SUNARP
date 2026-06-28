# -*- coding: utf-8 -*-
"""Funciones de conexion a MySQL/MariaDB."""

import mysql.connector
from mysql.connector import Error

from config import DB_CONFIG


def get_connection():
    """Crea una conexion nueva a la base SQL."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as exc:
        raise RuntimeError(
            "No se pudo conectar a MySQL/MariaDB. "
            "Verifique que XAMPP/MySQL este iniciado y que la base exista."
        ) from exc
