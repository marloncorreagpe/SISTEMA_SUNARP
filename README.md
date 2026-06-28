# Sistema SUNARP - Seguimiento Automatizado de Titulos Registrales

Proyecto final del curso **Fundamentos de Programacion - CIIN1205P**.

El sistema automatiza el seguimiento de titulos registrales SUNARP que antes se controlaba manualmente en hojas de calculo. Permite registrar, listar, buscar, actualizar estados, eliminar registros, generar estadisticas, reportar avance por bloque, exportar resultados a CSV, validar partidas internas en SQL y revisar historial de cambios.

## Tecnologia

- Lenguaje: Python
- Base de datos: MySQL/MariaDB
- Interfaz: consola y formularios Tkinter
- Pruebas: unittest

## Estructura

```text
src/        Codigo fuente principal
sql/        Scripts de base de datos, carga demo y consultas
tests/      Pruebas automatizadas
docs/       Documentacion, pseudocodigo, matriz de pruebas y evidencias
salidas/    Archivos de salida generados por el sistema
*.bat       Accesos rapidos para Windows
```

## Instalacion rapida

1. Instalar dependencias:

```bash
pip install -r requirements.txt
```

2. Iniciar MySQL/MariaDB, por ejemplo desde XAMPP.

3. Cargar la base de datos:

```bat
CARGAR_BASE_DATOS.bat
```

4. Ejecutar el menu principal:

```bat
EJECUTAR_MENU.bat
```

5. Ejecutar formularios graficos:

```bat
FORMULARIOS.bat
```

## Funciones principales

- Registrar nuevo titulo.
- Listar titulos.
- Buscar titulo SUNARP.
- Actualizar estado por titulo.
- Eliminar titulo.
- Ver estadisticas por estado.
- Generar reporte por bloque.
- Exportar CSV desde SQL.
- Validar partida como control interno SQL.
- Ver historial de cambios.

## Base de datos

Los scripts SQL estan en la carpeta `sql/`:

- `01_schema.sql`: crea tablas, vistas e indices.
- `02_seed_demo.sql`: carga registros de demostracion.
- `03_consultas_reportes.sql`: consultas de reporte.
- `04_migracion_partida_en_base.sql`: migracion para conservar partida como control interno.

## Pruebas

La matriz de 10 pruebas esta documentada en:

```text
docs/MATRIZ_PRUEBAS_10_CASOS.txt
```

Las pruebas automatizadas estan en:

```text
tests/test_integracion_sql.py
```

## Autores

- Marlon Correa
- Luis Melendez Bao
- Gianluca Renato Hurtado Malca

