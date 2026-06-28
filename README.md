# Sistema SUNARP

Este repositorio contiene el proyecto final del curso **Fundamentos de Programacion - CIIN1205P**.

El trabajo nace de un problema observado en el seguimiento de titulos registrales. El control se realizaba de forma manual, revisando datos uno por uno y anotando resultados en hojas de calculo. Con ese metodo era facil perder tiempo, duplicar informacion o confundir datos importantes como titulo, oficio o partida.

Por eso se desarrollo un sistema en Python que permite llevar el control de los titulos desde una sola aplicacion. El programa registra informacion, consulta titulos, actualiza estados, muestra reportes por bloque, genera estadisticas y exporta resultados para dejar evidencia del avance.

## Datos generales

- Curso: Fundamentos de Programacion - CIIN1205P
- Lenguaje usado: Python
- Base de datos: SQL 2022 como referencia academica del proyecto
- Ejecucion local probada: MySQL/MariaDB con XAMPP
- Interfaz: menu en consola y formularios en Tkinter

## Carpetas principales

```text
src/        Codigo fuente del sistema
sql/        Scripts para crear y cargar la base de datos
tests/      Pruebas automatizadas
docs/       Documentacion tecnica del proyecto
salidas/    Evidencias y archivos generados
```

## Como ejecutar

1. Instalar las dependencias de Python.

```bash
pip install -r requirements.txt
```

2. Iniciar el servicio de base de datos.

Para la prueba local se uso XAMPP con MySQL/MariaDB. Los scripts SQL estan en la carpeta `sql/`.

3. Cargar la base de datos.

```bat
CARGAR_BASE_DATOS.bat
```

4. Abrir el menu principal.

```bat
EJECUTAR_MENU.bat
```

5. Abrir los formularios graficos.

```bat
FORMULARIOS.bat
```

## Que permite hacer

- Registrar un nuevo titulo.
- Listar los titulos guardados.
- Buscar un titulo SUNARP.
- Actualizar el estado de un titulo.
- Eliminar un registro cuando corresponde.
- Ver estadisticas por estado.
- Revisar el avance por bloque.
- Exportar resultados a CSV.
- Consultar partida como dato interno de control.
- Revisar el historial de cambios.

## Base de datos

Los archivos de base de datos se encuentran en `sql/`:

- `01_schema.sql`: crea la estructura principal.
- `02_seed_demo.sql`: carga registros de demostracion.
- `03_consultas_reportes.sql`: contiene consultas para reportes.
- `04_migracion_partida_en_base.sql`: agrega el manejo de partida como dato interno.

## Pruebas

La matriz de pruebas esta en:

```text
docs/MATRIZ_PRUEBAS_10_CASOS.txt
```

Las pruebas automatizadas estan en:

```text
tests/test_integracion_sql.py
```

## Integrantes

- Marlon Correa
- Luis Melendez Bao
- Gianluca Renato Hurtado Malca

