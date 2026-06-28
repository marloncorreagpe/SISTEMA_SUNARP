# -*- coding: utf-8 -*-
"""Importa un resultados_full.csv a la base SQL academica.

Uso:
    python src/importar_resultados_csv.py ruta/al/resultados_full.csv
    python src/importar_resultados_csv.py ruta/al/resultados_full.csv --lote LOTE_2026_01
"""

import argparse
import csv
from datetime import datetime
from pathlib import Path

from database import get_connection


HEADERS_ESPERADOS = {
    "item",
    "bloque",
    "oficio",
    "titulo",
    "nombre",
    "dni_ruc",
    "partida",
    "estado_sunarp",
    "anio_consulta",
    "tipo_registro",
    "partida_web",
    "acto_descripcion",
    "criterio_validacion",
    "fecha_presentacion",
    "hora_presentacion",
    "fecha_vencimiento",
    "pdf_descargado",
    "pdf_observacion",
    "pdf_inscripcion",
    "error",
    "source_row",
    "source_error",
    "actualizado",
}


def empty_to_none(value):
    text = str(value or "").strip()
    return text if text else None


def to_int(value, default=None):
    text = str(value or "").strip()
    return int(text) if text.isdigit() else default


def normalizar_fecha(value):
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return datetime.strptime(text, fmt).date().isoformat()
        except ValueError:
            continue
    return None


def normalizar_hora(value):
    text = str(value or "").strip()
    if not text:
        return None
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(text, fmt).time().isoformat()
        except ValueError:
            continue
    return None


def crear_o_buscar_lote(connection, nombre_lote):
    sql_insert = """
        INSERT INTO lotes_seguimiento (nombre_lote, descripcion)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion)
    """
    sql_select = "SELECT id FROM lotes_seguimiento WHERE nombre_lote = %s"
    cursor = connection.cursor()
    cursor.execute(
        sql_insert,
        (nombre_lote, "Importacion CSV para pruebas SQL academicas"),
    )
    cursor.execute(sql_select, (nombre_lote,))
    lote_id = cursor.fetchone()[0]
    cursor.close()
    return lote_id


def normalizar_fila(row, lote_id, indice):
    source_row = to_int(row.get("source_row"), indice)
    item = to_int(row.get("item"), source_row)
    estado_base = empty_to_none(row.get("estado_base"))
    estado_sunarp = (
        empty_to_none(row.get("estado_sunarp"))
        or estado_base
        or "PENDIENTE"
    )
    return {
        "lote_id": lote_id,
        "item": item,
        "bloque": empty_to_none(row.get("bloque")) or "00",
        "oficina": empty_to_none(row.get("oficina")) or "LIMA",
        "anio_consulta": to_int(row.get("anio_consulta"), 2026),
        "oficio": empty_to_none(row.get("oficio")) or "SIN_OFICIO",
        "titulo": empty_to_none(row.get("titulo")),
        "nombre": empty_to_none(row.get("nombre")) or "SIN_NOMBRE",
        "dni_ruc": empty_to_none(row.get("dni_ruc")) or "00000000",
        "partida": empty_to_none(row.get("partida")),
        "estado_base": estado_base,
        "observacion_base": empty_to_none(row.get("observacion_base")),
        "estado_sunarp": estado_sunarp,
        "tipo_registro": empty_to_none(row.get("tipo_registro")),
        "partida_web": empty_to_none(row.get("partida_web")),
        "acto_descripcion": empty_to_none(row.get("acto_descripcion")),
        "criterio_validacion": empty_to_none(row.get("criterio_validacion")),
        "fecha_presentacion": normalizar_fecha(row.get("fecha_presentacion"))
        or normalizar_fecha(row.get("fecha_presentacion_base")),
        "hora_presentacion": normalizar_hora(row.get("hora_presentacion")),
        "fecha_vencimiento": normalizar_fecha(row.get("fecha_vencimiento"))
        or normalizar_fecha(row.get("fecha_vencimiento_base")),
        "pdf_descargado": empty_to_none(row.get("pdf_descargado")) or "NO",
        "pdf_observacion": empty_to_none(row.get("pdf_observacion")),
        "pdf_inscripcion": empty_to_none(row.get("pdf_inscripcion")),
        "error": empty_to_none(row.get("error")),
        "source_row": source_row,
        "source_error": empty_to_none(row.get("source_error")),
    }


def fila_importable(row):
    return bool(empty_to_none(row.get("titulo")) or empty_to_none(row.get("partida")))


def importar(path_csv, nombre_lote=None):
    nombre_lote = nombre_lote or f"CSV_{Path(path_csv).stem.upper()}"
    sql = """
        INSERT INTO titulos_registrales
        (lote_id, item, bloque, oficina, anio_consulta, oficio, titulo, nombre,
         dni_ruc, partida, estado_base, observacion_base, estado_sunarp,
         tipo_registro, partida_web, acto_descripcion, criterio_validacion,
         fecha_presentacion, hora_presentacion, fecha_vencimiento,
         pdf_descargado, pdf_observacion, pdf_inscripcion, error,
         source_row, source_error)
        VALUES
        (%(lote_id)s, %(item)s, %(bloque)s, %(oficina)s, %(anio_consulta)s,
         %(oficio)s, %(titulo)s, %(nombre)s, %(dni_ruc)s, %(partida)s,
         %(estado_base)s, %(observacion_base)s, %(estado_sunarp)s,
         %(tipo_registro)s, %(partida_web)s, %(acto_descripcion)s,
         %(criterio_validacion)s, %(fecha_presentacion)s,
         %(hora_presentacion)s, %(fecha_vencimiento)s,
         %(pdf_descargado)s, %(pdf_observacion)s, %(pdf_inscripcion)s,
         %(error)s, %(source_row)s, %(source_error)s)
        ON DUPLICATE KEY UPDATE
          lote_id = VALUES(lote_id),
          item = VALUES(item),
          bloque = VALUES(bloque),
          oficina = VALUES(oficina),
          anio_consulta = VALUES(anio_consulta),
          oficio = VALUES(oficio),
          titulo = VALUES(titulo),
          nombre = VALUES(nombre),
          dni_ruc = VALUES(dni_ruc),
          partida = VALUES(partida),
          estado_base = VALUES(estado_base),
          observacion_base = VALUES(observacion_base),
          estado_sunarp = VALUES(estado_sunarp),
          tipo_registro = VALUES(tipo_registro),
          partida_web = VALUES(partida_web),
          acto_descripcion = VALUES(acto_descripcion),
          criterio_validacion = VALUES(criterio_validacion),
          fecha_presentacion = VALUES(fecha_presentacion),
          hora_presentacion = VALUES(hora_presentacion),
          fecha_vencimiento = VALUES(fecha_vencimiento),
          pdf_descargado = VALUES(pdf_descargado),
          pdf_observacion = VALUES(pdf_observacion),
          pdf_inscripcion = VALUES(pdf_inscripcion),
          error = VALUES(error),
          source_row = VALUES(source_row),
          source_error = VALUES(source_error)
    """
    with Path(path_csv).open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        headers = set(reader.fieldnames or [])
        if not {"titulo", "partida"} & headers:
            raise ValueError(
                "El CSV debe incluir titulo para consulta SUNARP "
                "o partida para conservar control SQL."
            )

        raw_rows = list(reader)

    connection = get_connection()
    try:
        lote_id = crear_o_buscar_lote(connection, nombre_lote)
        rows = [
            normalizar_fila(row, lote_id, indice)
            for indice, row in enumerate(raw_rows, start=1)
            if fila_importable(row)
        ]
        cursor = connection.cursor()
        if rows:
            cursor.executemany(sql, rows)
        connection.commit()
        cursor.close()
    finally:
        connection.close()
    return {
        "leidas": len(raw_rows),
        "importadas": len(rows),
        "omitidas": len(raw_rows) - len(rows),
        "lote": nombre_lote,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", help="Ruta del resultados_full.csv o fuente equivalente")
    parser.add_argument("--lote", default=None, help="Nombre del lote de importacion")
    args = parser.parse_args()

    resultado = importar(args.csv, args.lote)
    print(
        "Importacion completada: "
        f"{resultado['importadas']} filas insertadas/actualizadas, "
        f"{resultado['omitidas']} omitidas, lote={resultado['lote']}."
    )


if __name__ == "__main__":
    main()
