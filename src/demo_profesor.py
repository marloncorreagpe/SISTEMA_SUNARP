# -*- coding: utf-8 -*-
"""Genera una evidencia tecnica reproducible del funcionamiento."""

from datetime import datetime
from pathlib import Path

from database import get_connection
from repository import TituloRepository


ROOT = Path(__file__).resolve().parents[1]
DEMO_TITLE = "999999991"
DEMO_NAME = "REGISTRO TEMPORAL DEMO SQL"


def _fetch_one(cursor, sql, params=None):
    cursor.execute(sql, params or ())
    return cursor.fetchone()


def _fetch_all(cursor, sql, params=None):
    cursor.execute(sql, params or ())
    return cursor.fetchall()


def generar_evidencia(output_path=None):
    output = Path(output_path or ROOT / "salidas" / "evidencia_demo_profesor.txt")
    output.parent.mkdir(parents=True, exist_ok=True)

    connection = get_connection()
    repo = TituloRepository(connection)
    lines = []
    try:
        cursor = connection.cursor(dictionary=True)
        lines.append("EVIDENCIA TECNICA - SUNARP SQL")
        lines.append("=" * 72)
        lines.append(f"Fecha de generacion: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")

        resumen = _fetch_one(
            cursor,
            """
            SELECT
              COUNT(*) AS total,
              SUM(CASE WHEN titulo IS NOT NULL THEN 1 ELSE 0 END) AS con_titulo,
              SUM(CASE WHEN partida IS NOT NULL OR partida_web IS NOT NULL THEN 1 ELSE 0 END) AS con_partida,
              SUM(CASE WHEN estado_sunarp <> 'PENDIENTE' THEN 1 ELSE 0 END) AS procesados
            FROM titulos_registrales
            """,
        )
        lines.append("1. Resumen general de la base")
        lines.append(
            "   total={total}, con_titulo={con_titulo}, con_partida={con_partida}, "
            "procesados={procesados}".format(**resumen)
        )
        lines.append("")

        estados = _fetch_all(
            cursor,
            """
            SELECT estado_sunarp, cantidad, porcentaje
            FROM vw_resumen_estado
            ORDER BY cantidad DESC, estado_sunarp
            """,
        )
        lines.append("2. Resumen por estado")
        for row in estados:
            lines.append(
                f"   {row['estado_sunarp']:<24} {row['cantidad']:>5} ({row['porcentaje']}%)"
            )
        lines.append("")

        titulo = repo.buscar_por_titulo("393004")
        if titulo is None:
            raise RuntimeError(
                "No se encontro el titulo demo 393004. "
                "Ejecute primero la carga de base demo."
            )
        lines.append("3. Busqueda operativa por titulo SUNARP")
        lines.append(
            "   titulo=393004 -> item={item}, partida={partida}, estado={estado_sunarp}".format(
                **titulo
            )
        )
        lines.append("")

        partidas = repo.buscar_por_partida("P03010001")
        lines.append("4. Validacion interna por partida SQL")
        lines.append("   partida=P03010001 -> coincidencias={}".format(len(partidas)))
        for row in partidas:
            lines.append(
                "   item={item}, titulo={titulo}, estado={estado_sunarp}".format(**row)
            )
        lines.append("   Nota: SUNARP se consulta por titulo; partida es control interno.")
        lines.append("")

        existing = repo.buscar_por_titulo(DEMO_TITLE)
        if existing and existing["nombre"] != DEMO_NAME:
            raise RuntimeError(
                f"El titulo temporal {DEMO_TITLE} ya existe con otros datos."
            )
        if existing:
            repo.eliminar(DEMO_TITLE)

        data = {
            "item": 999991,
            "bloque": "99",
            "oficina": "LIMA",
            "anio_consulta": 2026,
            "oficio": "DEMO-SQL-001",
            "titulo": DEMO_TITLE,
            "nombre": DEMO_NAME,
            "dni_ruc": "99999999",
            "partida": "PDEMO999",
            "estado_sunarp": "PENDIENTE",
            "fecha_presentacion": None,
            "fecha_vencimiento": None,
            "pdf_descargado": "NO",
        }
        ok, message = repo.registrar(data)
        if not ok:
            raise RuntimeError(message)
        repo.actualizar_estado(DEMO_TITLE, "OBSERVADO", "Demo CRUD controlada")
        actualizado = repo.buscar_por_titulo(DEMO_TITLE)
        historial = repo.historial_por_titulo(DEMO_TITLE)
        eliminado_ok, eliminado_msg = repo.eliminar(DEMO_TITLE)

        lines.append("5. Prueba CRUD temporal")
        lines.append(f"   CREATE: {message}")
        lines.append(
            "   READ/UPDATE: titulo={titulo}, estado={estado_sunarp}, partida={partida}".format(
                **actualizado
            )
        )
        lines.append(f"   HISTORIAL: {len(historial)} cambio(s) registrado(s)")
        lines.append(f"   DELETE: {eliminado_msg if eliminado_ok else 'No eliminado'}")
        lines.append("")

        pendientes = _fetch_all(
            cursor,
            """
            SELECT bloque, COUNT(*) AS total
            FROM titulos_registrales
            WHERE estado_sunarp IN ('PENDIENTE', 'CALIFICACION')
            GROUP BY bloque
            ORDER BY bloque
            LIMIT 10
            """,
        )
        lines.append("6. Pendientes por bloque")
        for row in pendientes:
            lines.append(f"   bloque={row['bloque']} -> {row['total']} pendiente(s)")
        lines.append("")
        lines.append("Resultado: evidencia generada sin dejar registros temporales.")
        cursor.close()
    finally:
        connection.close()

    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output


def main():
    path = generar_evidencia()
    print(f"Evidencia generada: {path}")


if __name__ == "__main__":
    main()
