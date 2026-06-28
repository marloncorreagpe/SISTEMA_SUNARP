# -*- coding: utf-8 -*-
"""Funciones de conexion SQL para MySQL/MariaDB o SQL Server 2022."""

from config import DB_ENGINE, MYSQL_CONFIG, SQLSERVER_CONFIG


class DbConnection:
    def __init__(self, raw_connection, engine):
        self.raw = raw_connection
        self.engine = engine

    def cursor(self, *args, **kwargs):
        if self.engine == "mssql":
            return self.raw.cursor()
        return self.raw.cursor(*args, **kwargs)

    def commit(self):
        return self.raw.commit()

    def rollback(self):
        return self.raw.rollback()

    def close(self):
        return self.raw.close()


def get_connection():
    """Crea una conexion nueva a la base SQL seleccionada."""
    if DB_ENGINE == "mssql":
        return _get_sqlserver_connection()
    return _get_mysql_connection()


def _get_mysql_connection():
    try:
        import mysql.connector
        from mysql.connector import Error

        return DbConnection(mysql.connector.connect(**MYSQL_CONFIG), "mysql")
    except Error as exc:
        raise RuntimeError(
            "No se pudo conectar a MySQL/MariaDB. "
            "Verifique que XAMPP/MySQL este iniciado y que la base exista."
        ) from exc


def _get_sqlserver_connection():
    try:
        import pyodbc

        cfg = SQLSERVER_CONFIG
        if cfg["username"]:
            auth = f"UID={cfg['username']};PWD={cfg['password']};"
        else:
            auth = f"Trusted_Connection={cfg['trusted_connection']};"
        conn_str = (
            f"DRIVER={{{cfg['driver']}}};"
            f"SERVER={cfg['server']};"
            f"DATABASE={cfg['database']};"
            f"{auth}"
            "TrustServerCertificate=yes;"
        )
        return DbConnection(pyodbc.connect(conn_str), "mssql")
    except Exception as exc:  # noqa: BLE001
        raise RuntimeError(
            "No se pudo conectar a SQL Server 2022. "
            "Verifique que SQL Server este iniciado, que exista la base "
            "sunarp_academico y que este instalado el ODBC Driver 18."
        ) from exc
