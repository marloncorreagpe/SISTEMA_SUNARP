# -*- coding: utf-8 -*-
"""Repositorio SQL: aqui viven las operaciones CRUD y reportes."""

import csv
from pathlib import Path

try:
    from mysql.connector import IntegrityError as MySqlIntegrityError
except Exception:  # noqa: BLE001
    MySqlIntegrityError = type("MySqlIntegrityError", (Exception,), {})

try:
    import pyodbc
except Exception:  # noqa: BLE001
    pyodbc = None


EXPORT_FIELDS = [
    "item",
    "bloque",
    "oficina",
    "oficio",
    "titulo",
    "nombre",
    "dni_ruc",
    "partida",
    "partida_web",
    "estado_sunarp",
    "fecha_presentacion",
    "fecha_vencimiento",
    "pdf_descargado",
]


class TituloRepository:
    def __init__(self, connection):
        self.connection = connection
        self.engine = getattr(connection, "engine", "mysql")

    def _ph(self):
        return "?" if self.engine == "mssql" else "%s"

    def _cursor_dict(self):
        if self.engine == "mssql":
            return self.connection.cursor()
        return self.connection.cursor(dictionary=True)

    def _fetchall_dict(self, cursor):
        if self.engine != "mssql":
            return cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def _integrity_errors(self):
        errors = [MySqlIntegrityError]
        if pyodbc is not None:
            errors.append(pyodbc.IntegrityError)
        return tuple(errors)

    def registrar(self, data):
        fields = (
            "item", "bloque", "oficina", "anio_consulta", "oficio", "titulo",
            "nombre", "dni_ruc", "partida", "estado_sunarp",
            "fecha_presentacion", "fecha_vencimiento", "pdf_descargado",
        )
        if self.engine == "mssql":
            placeholders = ", ".join("?" for _ in fields)
            sql = f"""
                INSERT INTO titulos_registrales
                ({", ".join(fields)})
                VALUES ({placeholders})
            """
            params = tuple(data[field] for field in fields)
        else:
            sql = """
                INSERT INTO titulos_registrales
                (item, bloque, oficina, anio_consulta, oficio, titulo, nombre,
                 dni_ruc, partida, estado_sunarp, fecha_presentacion,
                 fecha_vencimiento, pdf_descargado)
                VALUES
                (%(item)s, %(bloque)s, %(oficina)s, %(anio_consulta)s,
                 %(oficio)s, %(titulo)s, %(nombre)s, %(dni_ruc)s, %(partida)s,
                 %(estado_sunarp)s, %(fecha_presentacion)s,
                 %(fecha_vencimiento)s, %(pdf_descargado)s)
            """
            params = data
        try:
            cursor = self.connection.cursor()
            cursor.execute(sql, params)
            cursor.close()
            self.connection.commit()
            return True, "Titulo registrado correctamente."
        except self._integrity_errors():
            self.connection.rollback()
            return False, "Ese numero de titulo ya existe en la base de datos."

    def listar(self):
        sql = """
            SELECT item, bloque, oficina, oficio, titulo, nombre,
                   dni_ruc, partida, partida_web, estado_sunarp, fecha_presentacion,
                   fecha_vencimiento, pdf_descargado
            FROM titulos_registrales
            ORDER BY item
        """
        cursor = self._cursor_dict()
        cursor.execute(sql)
        rows = self._fetchall_dict(cursor)
        cursor.close()
        return rows

    def _buscar_detalle(self, where_sql, params):
        sql = f"""
            SELECT id, item, bloque, oficina, anio_consulta, oficio, titulo,
                   nombre, dni_ruc, partida, estado_base, estado_sunarp,
                   tipo_registro, partida_web, fecha_presentacion,
                   hora_presentacion, fecha_vencimiento, pdf_descargado,
                   pdf_observacion, pdf_inscripcion, error, actualizado
            FROM titulos_registrales
            WHERE {where_sql}
            ORDER BY item
        """
        cursor = self._cursor_dict()
        cursor.execute(sql, params)
        rows = self._fetchall_dict(cursor)
        cursor.close()
        return rows

    def buscar_por_titulo(self, titulo):
        rows = self._buscar_detalle(f"titulo = {self._ph()}", (titulo,))
        return rows[0] if rows else None

    def buscar_por_partida(self, partida):
        """Busqueda interna SQL; no representa una consulta en SUNARP."""
        return self._buscar_detalle(
            f"(partida = {self._ph()} OR partida_web = {self._ph()})",
            (partida, partida),
        )

    def actualizar_estado(self, titulo, nuevo_estado, observacion=""):
        actual = self.buscar_por_titulo(titulo)
        if actual is None:
            return False, "No existe un titulo con ese numero."

        sql_update = """
            UPDATE titulos_registrales
            SET estado_sunarp = {ph}, error = NULL
            WHERE id = {ph}
        """
        sql_hist = """
            INSERT INTO historial_estados
            (titulo_id, estado_anterior, estado_nuevo, observacion)
            VALUES ({ph}, {ph}, {ph}, {ph})
        """
        ph = self._ph()
        cursor = self.connection.cursor()
        cursor.execute(sql_update.format(ph=ph), (nuevo_estado, actual["id"]))
        cursor.execute(
            sql_hist.format(ph=ph),
            (actual["id"], actual["estado_sunarp"], nuevo_estado, observacion),
        )
        cursor.close()
        self.connection.commit()
        return True, "Estado actualizado y registrado en historial."

    def eliminar(self, titulo):
        cursor = self.connection.cursor()
        cursor.execute(f"DELETE FROM titulos_registrales WHERE titulo = {self._ph()}", (titulo,))
        filas = cursor.rowcount
        cursor.close()
        self.connection.commit()
        if filas == 0:
            return False, "No existe un titulo con ese numero."
        return True, "Titulo eliminado correctamente."

    def estadisticas_por_estado(self):
        sql = """
            SELECT estado_sunarp, cantidad, porcentaje
            FROM vw_resumen_estado
            ORDER BY cantidad DESC, estado_sunarp
        """
        cursor = self._cursor_dict()
        cursor.execute(sql)
        rows = self._fetchall_dict(cursor)
        cursor.close()
        return rows

    def reporte_por_bloque(self):
        sql = """
            SELECT bloque, procesados, total, avance
            FROM vw_avance_bloque
            ORDER BY bloque
        """
        cursor = self._cursor_dict()
        cursor.execute(sql)
        rows = self._fetchall_dict(cursor)
        cursor.close()
        return rows

    def historial_por_titulo(self, titulo):
        actual = self.buscar_por_titulo(titulo)
        if actual is None:
            return []

        sql = """
            SELECT h.estado_anterior, h.estado_nuevo, h.observacion,
                   h.fecha_cambio
            FROM historial_estados h
            WHERE h.titulo_id = {ph}
            ORDER BY h.fecha_cambio DESC, h.id DESC
        """
        cursor = self._cursor_dict()
        cursor.execute(sql.format(ph=self._ph()), (actual["id"],))
        rows = self._fetchall_dict(cursor)
        cursor.close()
        return rows

    def exportar_csv(self, output_path):
        rows = self.listar()
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=EXPORT_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        return path
