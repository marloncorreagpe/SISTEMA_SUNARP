# -*- coding: utf-8 -*-
"""Pruebas de integracion SQL para el proyecto academico SUNARP.

Estas pruebas usan una base separada: sunarp_academico_test.
La consulta operativa se valida por titulo; partida se valida como dato SQL.
"""

import csv
import os
import sys
import tempfile
import unittest
from pathlib import Path

import mysql.connector


PROJECT_DIR = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_DIR / "src"
SQL_DIR = PROJECT_DIR / "sql"
TEST_DB = "sunarp_academico_test"

os.environ["SUNARP_DB_HOST"] = os.getenv("SUNARP_DB_HOST", "127.0.0.1")
os.environ["SUNARP_DB_PORT"] = os.getenv("SUNARP_DB_PORT", "3306")
os.environ["SUNARP_DB_USER"] = os.getenv("SUNARP_DB_USER", "root")
os.environ["SUNARP_DB_PASSWORD"] = os.getenv("SUNARP_DB_PASSWORD", "")
os.environ["SUNARP_DB_NAME"] = TEST_DB
sys.path.insert(0, str(SRC_DIR))

from database import get_connection  # noqa: E402
from demo_profesor import DEMO_TITLE, generar_evidencia  # noqa: E402
from importar_resultados_csv import importar  # noqa: E402
from repository import TituloRepository  # noqa: E402


def server_connection():
    return mysql.connector.connect(
        host=os.environ["SUNARP_DB_HOST"],
        port=int(os.environ["SUNARP_DB_PORT"]),
        user=os.environ["SUNARP_DB_USER"],
        password=os.environ["SUNARP_DB_PASSWORD"],
    )


def run_sql_file(connection, path):
    raw_sql = path.read_text(encoding="utf-8").replace("sunarp_academico", TEST_DB)
    sql = "\n".join(
        line for line in raw_sql.splitlines()
        if not line.strip().startswith("--")
    )
    cursor = connection.cursor()
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            cursor.execute(statement)
            if cursor.with_rows:
                cursor.fetchall()
    cursor.close()
    connection.commit()


class SunarpSqlIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        connection = server_connection()
        cursor = connection.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB}")
        cursor.close()
        run_sql_file(connection, SQL_DIR / "01_schema.sql")
        run_sql_file(connection, SQL_DIR / "04_migracion_partida_en_base.sql")
        run_sql_file(connection, SQL_DIR / "02_seed_demo.sql")
        connection.close()

    def setUp(self):
        self.connection = get_connection()
        self.repo = TituloRepository(self.connection)

    def tearDown(self):
        self.connection.close()

    def test_busqueda_operativa_es_por_titulo_y_muestra_partida(self):
        row = self.repo.buscar_por_titulo("393004")

        self.assertIsNotNone(row)
        self.assertEqual(row["titulo"], "393004")
        self.assertEqual(row["partida"], "P03010001")
        self.assertEqual(row["estado_sunarp"], "INSCRITO")

    def test_partida_se_puede_validar_en_sql_sin_ser_consulta_sunarp(self):
        rows = self.repo.buscar_por_partida("P03010001")

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["titulo"], "393004")
        self.assertEqual(rows[0]["partida"], "P03010001")

    def test_actualizar_estado_usa_titulo_y_graba_historial(self):
        ok, message = self.repo.actualizar_estado(
            "393018",
            "OBSERVADO",
            "prueba automatica por titulo",
        )

        self.assertTrue(ok, message)
        row = self.repo.buscar_por_titulo("393018")
        self.assertEqual(row["estado_sunarp"], "OBSERVADO")

        cursor = self.connection.cursor()
        cursor.execute(
            """
            SELECT COUNT(*)
            FROM historial_estados h
            JOIN titulos_registrales t ON t.id = h.titulo_id
            WHERE t.titulo = %s AND h.estado_nuevo = %s
            """,
            ("393018", "OBSERVADO"),
        )
        total = cursor.fetchone()[0]
        cursor.close()
        self.assertGreaterEqual(total, 1)

    def test_historial_por_titulo_devuelve_trazabilidad(self):
        self.repo.actualizar_estado(
            "393026",
            "PENDIENTE",
            "prueba de historial academico",
        )

        historial = self.repo.historial_por_titulo("393026")

        self.assertGreaterEqual(len(historial), 1)
        self.assertEqual(historial[0]["estado_nuevo"], "PENDIENTE")
        self.assertEqual(historial[0]["observacion"], "prueba de historial academico")

    def test_exportar_csv_incluye_partida(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "test_resultados_seguimiento_sql.csv"
            path = self.repo.exportar_csv(output)

            with path.open(newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                first = next(reader)

        self.assertIn("partida", reader.fieldnames)
        self.assertEqual(first["titulo"], "393004")
        self.assertEqual(first["partida"], "P03010001")

    def test_importar_csv_con_titulos_y_partidas_reales_de_control(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture = Path(tmpdir) / "fixture_importacion_partidas.csv"
            rows = [
                {
                    "item": "9001",
                    "bloque": "99",
                    "oficio": "OF-TEST-01",
                    "titulo": "990001",
                    "source_row": "1",
                    "nombre": "CASO TEST CON TITULO",
                    "dni_ruc": "12345678",
                    "partida": "PTEST001",
                    "estado_base": "",
                    "observacion_base": "",
                    "source_error": "",
                    "estado_sunarp": "PENDIENTE",
                    "anio_consulta": "2026",
                    "tipo_registro": "",
                    "partida_web": "",
                    "acto_descripcion": "",
                    "criterio_validacion": "",
                    "fecha_presentacion": "22/01/2026",
                    "hora_presentacion": "08:15",
                    "fecha_vencimiento": "20/04/2026",
                    "pdf_descargado": "NO",
                    "pdf_observacion": "",
                    "pdf_inscripcion": "",
                    "error": "",
                    "actualizado": "",
                },
                {
                    "item": "9002",
                    "bloque": "99",
                    "oficio": "OF-TEST-02",
                    "titulo": "",
                    "source_row": "2",
                    "nombre": "CASO TEST SOLO PARTIDA",
                    "dni_ruc": "87654321",
                    "partida": "PTEST002",
                    "estado_base": "NO_REQUIERE",
                    "observacion_base": "fila sin titulo consultable",
                    "source_error": "FUENTE: fila en Excel sin numero de titulo",
                    "estado_sunarp": "",
                    "anio_consulta": "2026",
                    "tipo_registro": "",
                    "partida_web": "",
                    "acto_descripcion": "",
                    "criterio_validacion": "",
                    "fecha_presentacion": "",
                    "hora_presentacion": "",
                    "fecha_vencimiento": "",
                    "pdf_descargado": "NO",
                    "pdf_observacion": "",
                    "pdf_inscripcion": "",
                    "error": "",
                    "actualizado": "",
                },
            ]
            with fixture.open("w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
                writer.writeheader()
                writer.writerows(rows)

            result = importar(fixture, "TEST_IMPORT_PARTIDAS")
            result_again = importar(fixture, "TEST_IMPORT_PARTIDAS")

        self.assertEqual(result["importadas"], 2)
        self.assertEqual(result_again["importadas"], 2)
        self.assertEqual(self.repo.buscar_por_titulo("990001")["partida"], "PTEST001")
        self.assertIsNone(self.repo.buscar_por_titulo("PTEST002"))
        self.assertEqual(self.repo.buscar_por_partida("PTEST002")[0]["titulo"], None)

    def test_formularios_graficos_construyen_y_consultan(self):
        try:
            import tkinter as tk
        except Exception as exc:  # pragma: no cover
            self.skipTest(f"tkinter no disponible: {exc}")
        try:
            root = tk.Tk()
        except tk.TclError as exc:  # pragma: no cover
            self.skipTest(f"sin entorno grafico disponible: {exc}")
        root.withdraw()
        try:
            import formularios as forms

            consulta = forms.FormularioConsulta(root)
            consulta.update()
            self.assertEqual(len(consulta.tabla.get_children()), 50)
            consulta.entry_titulo.insert(0, "393004")
            consulta._buscar()
            consulta.update()
            self.assertEqual(consulta.lbl_estado.cget("text"), "INSCRITO")
            consulta.destroy()

            actualizacion = forms.FormularioActualizacion(root)
            actualizacion.entry_titulo.insert(0, "393033")
            actualizacion._cargar()
            actualizacion.update()
            self.assertEqual(actualizacion.combo_estado.get(), "TACHADO")
            actualizacion.destroy()

            forms.FormularioRegistro(root).destroy()
        finally:
            root.destroy()

    def test_generar_evidencia_profesor_crea_archivo_y_limpia_demo(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "evidencia_demo_profesor.txt"
            path = generar_evidencia(output)
            content = path.read_text(encoding="utf-8")

        self.assertIn("EVIDENCIA TECNICA - SUNARP SQL", content)
        self.assertIn("Busqueda operativa por titulo SUNARP", content)
        self.assertIn("Validacion interna por partida SQL", content)
        self.assertIn("Prueba CRUD temporal", content)
        self.assertIsNone(self.repo.buscar_por_titulo(DEMO_TITLE))


if __name__ == "__main__":
    unittest.main(verbosity=2)
