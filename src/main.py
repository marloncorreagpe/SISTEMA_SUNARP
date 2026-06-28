# -*- coding: utf-8 -*-
"""Sistema academico de seguimiento de titulos registrales SUNARP con SQL."""

from datetime import date

from config import ESTADOS_VALIDOS, OFICINAS_VALIDAS
from database import get_connection
from repository import TituloRepository


def linea(caracter="-", largo=78):
    return caracter * largo


def pausar():
    input("\nPresione ENTER para continuar...")


def leer_texto(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        print("  [!] El dato no puede estar vacio.")


def leer_titulo(mensaje):
    while True:
        valor = leer_texto(mensaje)
        if valor.isdigit():
            return valor
        print("  [!] El titulo SUNARP debe ingresarse solo con numeros.")


def leer_bloque():
    numero = leer_entero("Bloque (1-99): ", 1, 99)
    return str(numero).zfill(2)


def leer_oficina():
    print("\nOficinas validas:")
    for index, oficina in enumerate(OFICINAS_VALIDAS, start=1):
        print(f"  {index}. {oficina}")
    opcion = leer_entero("Seleccione oficina: ", 1, len(OFICINAS_VALIDAS))
    return OFICINAS_VALIDAS[opcion - 1]


def leer_partida():
    valor = input("Partida registral (opcional, control interno SQL): ").strip()
    return valor.upper() if valor else None


def leer_entero(mensaje, minimo=None, maximo=None):
    while True:
        entrada = input(mensaje).strip()
        if not entrada.isdigit():
            print("  [!] Debe ingresar un numero entero.")
            continue
        numero = int(entrada)
        if minimo is not None and numero < minimo:
            print(f"  [!] El valor debe ser mayor o igual a {minimo}.")
        elif maximo is not None and numero > maximo:
            print(f"  [!] El valor debe ser menor o igual a {maximo}.")
        else:
            return numero


def leer_fecha(mensaje):
    while True:
        valor = input(mensaje).strip()
        if not valor:
            return None
        try:
            return date.fromisoformat(valor)
        except ValueError:
            print("  [!] Use formato AAAA-MM-DD o deje vacio.")


def leer_dni_ruc(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit() and len(valor) in (8, 11):
            return valor
        print("  [!] DNI debe tener 8 digitos o RUC 11 digitos.")


def leer_estado():
    print("\nEstados validos:")
    for index, estado in enumerate(ESTADOS_VALIDOS, start=1):
        print(f"  {index}. {estado}")
    opcion = leer_entero("Seleccione estado: ", 1, len(ESTADOS_VALIDOS))
    return ESTADOS_VALIDOS[opcion - 1]


def registrar_titulo(repo):
    print(linea())
    print("REGISTRAR TITULO")
    print(linea())
    data = {
        "item": leer_entero("Item operativo: ", 1),
        "bloque": leer_bloque(),
        "oficina": leer_oficina(),
        "anio_consulta": leer_entero("Anio de consulta: ", 2000, 2100),
        "oficio": leer_texto("Nro. de oficio: "),
        "titulo": leer_titulo("Nro. de titulo SUNARP: "),
        "nombre": leer_texto("Nombre del solicitante: "),
        "dni_ruc": leer_dni_ruc("DNI o RUC: "),
        "partida": leer_partida(),
        "estado_sunarp": leer_estado(),
        "fecha_presentacion": leer_fecha("Fecha presentacion AAAA-MM-DD (opcional): "),
        "fecha_vencimiento": leer_fecha("Fecha vencimiento AAAA-MM-DD (opcional): "),
        "pdf_descargado": "NO",
    }
    ok, mensaje = repo.registrar(data)
    print(("  [OK] " if ok else "  [!] ") + mensaje)


def listar_titulos(repo):
    rows = repo.listar()
    print(linea("=", 136))
    print(
        f"{'ITEM':<6}{'BLOQUE':<8}{'OFICINA':<10}{'OFICIO':<15}"
        f"{'TITULO':<12}{'PARTIDA':<14}{'NOMBRE':<28}{'DNI/RUC':<13}"
        f"{'ESTADO':<18}{'PDF':<12}"
    )
    print(linea("=", 136))
    for row in rows:
        print(
            f"{row['item']:<6}{row['bloque']:<8}{row['oficina']:<10}"
            f"{row['oficio']:<15}{str(row['titulo'] or ''):<12}"
            f"{str(row['partida'] or row['partida_web'] or ''):<14}{row['nombre']:<28}"
            f"{row['dni_ruc']:<13}{row['estado_sunarp']:<18}{row['pdf_descargado']:<12}"
        )
    print(linea("=", 136))
    print(f"Total de titulos: {len(rows)}")


def imprimir_ficha(row):
    print(linea())
    print("FICHA DEL TITULO")
    print(linea())
    for clave, valor in row.items():
        print(f"{clave:<20}: {valor if valor is not None else ''}")


def buscar_titulo(repo):
    titulo = leer_titulo("Nro. de titulo SUNARP a buscar: ")
    row = repo.buscar_por_titulo(titulo)
    if row is None:
        print("  [X] No se encontro el titulo.")
        return
    imprimir_ficha(row)


def buscar_partida_interna(repo):
    partida = leer_texto("Partida a validar solo en SQL: ").upper()
    rows = repo.buscar_por_partida(partida)
    if not rows:
        print("  [X] No se encontro la partida en la base SQL.")
        return
    print(linea("=", 116))
    print(f"{'ITEM':<6}{'BLOQUE':<8}{'OFICIO':<15}{'TITULO':<12}{'PARTIDA':<14}{'NOMBRE':<28}{'ESTADO':<18}")
    print(linea("=", 116))
    for row in rows:
        partida_row = row["partida"] or row["partida_web"] or ""
        print(
            f"{row['item']:<6}{row['bloque']:<8}{row['oficio']:<15}"
            f"{str(row['titulo'] or ''):<12}{partida_row:<14}"
            f"{row['nombre']:<28}{row['estado_sunarp']:<18}"
        )
    print(linea("=", 116))
    print("Nota: esta busqueda es interna de SQL; SUNARP se consulta por titulo.")


def actualizar_estado(repo):
    titulo = leer_titulo("Nro. de titulo SUNARP a actualizar: ")
    nuevo_estado = leer_estado()
    observacion = input("Observacion del cambio (opcional): ").strip()
    ok, mensaje = repo.actualizar_estado(titulo, nuevo_estado, observacion)
    print(("  [OK] " if ok else "  [!] ") + mensaje)


def eliminar_titulo(repo):
    titulo = leer_texto("Nro. de titulo a eliminar: ")
    confirmar = input(f"Confirmar eliminacion del titulo {titulo} (S/N): ").strip().upper()
    if confirmar != "S":
        print("Operacion cancelada.")
        return
    ok, mensaje = repo.eliminar(titulo)
    print(("  [OK] " if ok else "  [!] ") + mensaje)


def mostrar_estadisticas(repo):
    print(linea())
    print("ESTADISTICAS POR ESTADO")
    print(linea())
    for row in repo.estadisticas_por_estado():
        print(
            f"{row['estado_sunarp']:<24}"
            f"{row['cantidad']:>4} titulos  {row['porcentaje']:>6}%"
        )


def reporte_por_bloque(repo):
    print(linea())
    print("REPORTE POR BLOQUE")
    print(linea())
    print(f"{'BLOQUE':<10}{'PROCESADOS':<16}{'TOTAL':<10}{'AVANCE'}")
    for row in repo.reporte_por_bloque():
        print(
            f"{row['bloque']:<10}{row['procesados']:<16}"
            f"{row['total']:<10}{row['avance']}%"
        )


def exportar_csv(repo):
    path = repo.exportar_csv("salidas/resultados_seguimiento_sql.csv")
    print(f"  [OK] Exportado a {path}")


def ver_historial(repo):
    titulo = leer_titulo("Nro. de titulo SUNARP para ver historial: ")
    rows = repo.historial_por_titulo(titulo)
    if not rows:
        print("  [X] No hay historial registrado para ese titulo.")
        return
    print(linea("=", 100))
    print(f"{'ANTERIOR':<18}{'NUEVO':<18}{'FECHA':<22}{'OBSERVACION'}")
    print(linea("=", 100))
    for row in rows:
        print(
            f"{str(row['estado_anterior'] or ''):<18}"
            f"{row['estado_nuevo']:<18}"
            f"{str(row['fecha_cambio']):<22}"
            f"{str(row['observacion'] or '')}"
        )


def mostrar_menu():
    print("\n" + linea("*"))
    print("  SISTEMA DE SEGUIMIENTO DE TITULOS REGISTRALES - SUNARP SQL")
    print(linea("*"))
    print("  1. Registrar nuevo titulo")
    print("  2. Listar titulos")
    print("  3. Buscar titulo SUNARP")
    print("  4. Actualizar estado por titulo")
    print("  5. Eliminar titulo")
    print("  6. Estadisticas por estado")
    print("  7. Reporte por bloque")
    print("  8. Exportar CSV desde SQL")
    print("  9. Validar partida en SQL (control interno)")
    print("  10. Ver historial de cambios por titulo")
    print("  0. Salir")


def main():
    connection = get_connection()
    try:
        repo = TituloRepository(connection)
        opcion = -1
        while opcion != 0:
            mostrar_menu()
            opcion = leer_entero("Seleccione una opcion: ", 0, 10)
            if opcion == 1:
                registrar_titulo(repo)
            elif opcion == 2:
                listar_titulos(repo)
            elif opcion == 3:
                buscar_titulo(repo)
            elif opcion == 4:
                actualizar_estado(repo)
            elif opcion == 5:
                eliminar_titulo(repo)
            elif opcion == 6:
                mostrar_estadisticas(repo)
            elif opcion == 7:
                reporte_por_bloque(repo)
            elif opcion == 8:
                exportar_csv(repo)
            elif opcion == 9:
                buscar_partida_interna(repo)
            elif opcion == 10:
                ver_historial(repo)
            elif opcion == 0:
                print("Fin del programa.")
            if opcion != 0:
                pausar()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
