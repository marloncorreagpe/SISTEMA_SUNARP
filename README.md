# Sistema SUNARP

Este repositorio contiene el proyecto final del curso **Fundamentos de Programacion - CIIN1205P**.

El trabajo nace de un problema observado en el seguimiento de titulos registrales. El control se realizaba de forma manual, revisando datos uno por uno y anotando resultados en hojas de calculo. Con ese metodo era facil perder tiempo, duplicar informacion o confundir datos importantes como titulo, oficio o partida.

Por eso se desarrollo un sistema en Python que permite llevar el control de los titulos desde una sola aplicacion. El programa registra informacion, consulta titulos, actualiza estados, muestra reportes por bloque, genera estadisticas y exporta resultados para dejar evidencia del avance.

## Datos generales

- Curso: Fundamentos de Programacion - CIIN1205P
- Lenguaje usado: Python
- Base de datos recomendada para revision: SQL Server 2022
- Ejecucion alternativa: MySQL/MariaDB con XAMPP
- Interfaz: menu en consola y formularios en Tkinter

## Carpetas principales

```text
src/        Codigo fuente del sistema
sql/        Scripts para crear y cargar la base de datos
sql_sqlserver/ Scripts listos para SQL Server 2022
tests/      Pruebas automatizadas
docs/       Documentacion tecnica del proyecto
salidas/    Evidencias y archivos generados
```

## Ejecucion recomendada con SQL Server 2022

Esta es la ruta pensada para que el proyecto pueda revisarse en una PC con Visual Studio y SQL Server 2022.

1. Instalar lo necesario:

- Python 3.10 o superior.
- Visual Studio 2022 con soporte para Python.
- SQL Server 2022, por ejemplo la instancia `localhost\SQLEXPRESS`.
- ODBC Driver 18 for SQL Server.
- Microsoft Command Line Utilities for SQL Server, para tener el comando `sqlcmd`.

2. Instalar dependencias de Python desde la carpeta del proyecto.

```bash
pip install -r requirements.txt
```

3. Cargar la base demo en SQL Server 2022.

```bat
CARGAR_SQLSERVER_2022.bat
```

Si la instancia tiene otro nombre, se puede indicar asi:

```bat
CARGAR_SQLSERVER_2022.bat localhost\SQLEXPRESS
```

4. Abrir los formularios conectados a SQL Server 2022.

```bat
FORMULARIOS_SQLSERVER_2022.bat
```

5. Si se prefiere usar el menu de consola:

```bat
EJECUTAR_MENU_SQLSERVER_2022.bat
```

En Visual Studio tambien se puede abrir `sistema.sln`. El archivo de inicio configurado es `src\formularios.py`.
Por defecto el proyecto apunta a SQL Server 2022 con la instancia `localhost\SQLEXPRESS`.

## Ejecucion alternativa con XAMPP

1. Instalar las dependencias de Python.

```bash
pip install -r requirements.txt
```

2. Iniciar MySQL/MariaDB desde XAMPP.

Los scripts SQL para esta opcion estan en la carpeta `sql/`.

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

Para SQL Server 2022 se debe usar la carpeta `sql_sqlserver/`:

- `01_schema_sqlserver_2022.sql`: crea la base, tablas, indices y vistas.
- `02_seed_demo_sqlserver_2022.sql`: carga los 50 registros de demostracion.

Para MySQL/MariaDB se debe usar la carpeta `sql/`:

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
