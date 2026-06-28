# -*- coding: utf-8 -*-
"""Panel de uso simple para preparar, probar y operar el proyecto SQL."""

import subprocess
import sys
import time
import webbrowser
from datetime import datetime
from pathlib import Path

from config import DB_CONFIG


ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = ROOT / "sql"
MYSQL_DIR = Path("C:/xampp/mysql/bin")
MYSQLD = MYSQL_DIR / "mysqld.exe"
MYSQL = MYSQL_DIR / "mysql.exe"
MYSQLADMIN = MYSQL_DIR / "mysqladmin.exe"
MYINI = MYSQL_DIR / "my.ini"


def linea(caracter="-", largo=72):
    return caracter * largo


def pausar():
    try:
        input("\nPresione ENTER para continuar...")
    except EOFError:
        print()


def mysql_args(program, include_charset=False):
    args = [
        str(program),
        f"--host={DB_CONFIG['host']}",
        f"--port={DB_CONFIG['port']}",
        f"--user={DB_CONFIG['user']}",
    ]
    if DB_CONFIG.get("password"):
        args.append(f"--password={DB_CONFIG['password']}")
    if include_charset:
        args.append("--default-character-set=utf8mb4")
    return args


def ejecutar(cmd, cwd=ROOT, stdin_path=None):
    print("\n> " + " ".join(str(part) for part in cmd), flush=True)
    stdin = None
    try:
        if stdin_path:
            stdin = Path(stdin_path).open("rb")
        result = subprocess.run(cmd, cwd=str(cwd), stdin=stdin, text=False)
    finally:
        if stdin:
            stdin.close()
    return result.returncode == 0


def mysql_disponible():
    return MYSQL.exists() and MYSQLADMIN.exists()


def verificar_mysql():
    print(linea("="))
    print("ESTADO RAPIDO")
    print(linea("="))
    if not mysql_disponible():
        print("No se encontro MySQL/MariaDB en C:\\xampp\\mysql\\bin.")
        print("Instale XAMPP o ajuste las rutas del proyecto.")
        return False

    ping = subprocess.run(
        mysql_args(MYSQLADMIN) + ["ping"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    print(ping.stdout.strip() or "Sin respuesta de mysqladmin.")
    if ping.returncode != 0:
        print("MySQL/MariaDB no parece estar iniciado.")
        return False

    try:
        from database import get_connection

        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """
            SELECT
              COUNT(*) AS total,
              SUM(CASE WHEN titulo IS NOT NULL THEN 1 ELSE 0 END) AS con_titulo,
              SUM(CASE WHEN partida IS NOT NULL OR partida_web IS NOT NULL THEN 1 ELSE 0 END) AS con_partida,
              SUM(CASE WHEN pdf_descargado <> 'NO' THEN 1 ELSE 0 END) AS con_pdf
            FROM titulos_registrales
            """
        )
        resumen = cursor.fetchone()
        print(
            "Base: {db} | titulos: {total} | con titulo: {con_titulo} | "
            "con partida: {con_partida} | con PDF: {con_pdf}".format(
                db=DB_CONFIG["database"],
                total=resumen["total"] or 0,
                con_titulo=resumen["con_titulo"] or 0,
                con_partida=resumen["con_partida"] or 0,
                con_pdf=resumen["con_pdf"] or 0,
            )
        )
        cursor.execute(
            """
            SELECT estado_sunarp, cantidad, porcentaje
            FROM vw_resumen_estado
            ORDER BY cantidad DESC, estado_sunarp
            """
        )
        print("\nEstados:")
        for row in cursor.fetchall():
            print(
                f"  {row['estado_sunarp']:<24} "
                f"{row['cantidad']:>5} ({row['porcentaje']}%)"
            )
        cursor.close()
        connection.close()
        return True
    except Exception as exc:
        print("MySQL responde, pero no pude leer la base academica.")
        print(f"Detalle: {exc}")
        return False


def iniciar_mysql():
    if verificar_mysql():
        print("\nMySQL/MariaDB ya esta listo.")
        return
    if not MYSQLD.exists():
        print("\nNo se encontro C:\\xampp\\mysql\\bin\\mysqld.exe.")
        return

    print("\nIniciando MySQL/MariaDB de XAMPP...")
    cmd = [str(MYSQLD), f"--defaults-file={MYINI}", "--standalone"]
    subprocess.Popen(
        cmd,
        cwd=str(MYSQL_DIR),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    time.sleep(4)
    verificar_mysql()


def instalar_dependencias():
    ejecutar([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])


def cargar_base_demo():
    if not mysql_disponible():
        print("No se encontro MySQL/MariaDB en C:\\xampp\\mysql\\bin.")
        return

    archivos = [
        SQL_DIR / "01_schema.sql",
        SQL_DIR / "04_migracion_partida_en_base.sql",
        SQL_DIR / "02_seed_demo.sql",
    ]
    for archivo in archivos:
        if not archivo.exists():
            print(f"No existe {archivo}")
            return

    print(linea("="))
    print("CARGA / ACTUALIZACION DE BASE")
    print(linea("="))
    for archivo in archivos:
        print(f"\nAplicando {archivo.name}...")
        ok = ejecutar(mysql_args(MYSQL, include_charset=True), stdin_path=archivo)
        if not ok:
            print("No se pudo completar la carga.")
            return
    print("\nBase cargada correctamente.")
    verificar_mysql()


def abrir_menu_crud():
    ejecutar([sys.executable, str(ROOT / "src" / "main.py")])


def importar_csv():
    print(linea("="))
    print("IMPORTAR CSV A SQL")
    print(linea("="))
    print("Pegue la ruta del resultados_full.csv o archivo equivalente.")
    raw_path = input("Ruta CSV: ").strip().strip('"')
    if not raw_path:
        print("Importacion cancelada.")
        return

    path_csv = Path(raw_path)
    if not path_csv.exists():
        print(f"No existe el archivo: {path_csv}")
        return

    default_lote = "PANEL_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    lote = input(f"Nombre de lote [{default_lote}]: ").strip() or default_lote
    ejecutar(
        [
            sys.executable,
            str(ROOT / "src" / "importar_resultados_csv.py"),
            str(path_csv),
            "--lote",
            lote,
        ]
    )
    verificar_mysql()


def ejecutar_pruebas():
    ejecutar([sys.executable, "-m", "unittest", "tests.test_integracion_sql", "-v"])


def generar_evidencia_profesor():
    ejecutar([sys.executable, str(ROOT / "src" / "demo_profesor.py")])


def abrir_phpmyadmin():
    webbrowser.open("http://localhost/phpmyadmin/")
    print("Abriendo phpMyAdmin en el navegador.")


def abrir_formularios():
    print("Abriendo formularios graficos (CREATE / READ / UPDATE)...")
    ejecutar([sys.executable, str(ROOT / "src" / "formularios.py")])


def mostrar_menu():
    print("\n" + linea("*"))
    print("  SUNARP SQL - USO SIMPLE")
    print(linea("*"))
    print("  1. Ver estado de MySQL y resumen de la base")
    print("  2. Iniciar MySQL/MariaDB de XAMPP")
    print("  3. Instalar dependencias Python")
    print("  4. Crear/actualizar base demo SQL")
    print("  5. Abrir menu CRUD del sistema")
    print("  6. Importar resultados_full.csv a SQL")
    print("  7. Ejecutar pruebas automaticas")
    print("  8. Generar evidencia tecnica")
    print("  9. Abrir phpMyAdmin")
    print("  10. Abrir formularios graficos (CREATE/READ/UPDATE)")
    print("  0. Salir")


def leer_opcion():
    while True:
        try:
            opcion = input("Seleccione una opcion: ").strip()
        except EOFError:
            return 0
        if opcion.isdigit() and 0 <= int(opcion) <= 10:
            return int(opcion)
        print("Ingrese un numero entre 0 y 10.")


def main():
    acciones = {
        1: verificar_mysql,
        2: iniciar_mysql,
        3: instalar_dependencias,
        4: cargar_base_demo,
        5: abrir_menu_crud,
        6: importar_csv,
        7: ejecutar_pruebas,
        8: generar_evidencia_profesor,
        9: abrir_phpmyadmin,
        10: abrir_formularios,
    }
    while True:
        mostrar_menu()
        opcion = leer_opcion()
        if opcion == 0:
            print("Fin del panel simple.")
            return
        try:
            acciones[opcion]()
        except KeyboardInterrupt:
            print("\nOperacion interrumpida.")
        except Exception as exc:
            print(f"\nNo se pudo completar la opcion: {exc}")
        pausar()


if __name__ == "__main__":
    main()
