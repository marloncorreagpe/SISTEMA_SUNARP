# -*- coding: utf-8 -*-
"""Formularios graficos (Tkinter) para el sistema SUNARP SQL.

Incluye los tres formularios exigidos por la rubrica, todos conectados a la
misma base SQL y reutilizando la logica de TituloRepository:

  1. Formulario de Registro de Titulo        (CREATE)
  2. Formulario de Consulta y Seguimiento     (READ + diferenciacion de estado)
  3. Formulario de Actualizacion de Estado    (UPDATE + historial)

Regla operativa: la consulta SUNARP se realiza por numero de titulo.
La partida se conserva como dato interno de control en SQL.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from config import DB_ENGINE, ESTADOS_VALIDOS, OFICINAS_VALIDAS
from database import get_connection
from repository import TituloRepository


# Colores por estado: permiten "ver" que el sistema diferencia cada resultado.
COLORES_ESTADO = {
    "INSCRITO": ("#1b7f3b", "#d7f3e1"),
    "OBSERVADO": ("#8a6d00", "#fff3c4"),
    "TACHADO": ("#9b1c1c", "#fde2e2"),
    "PENDIENTE": ("#1f4e79", "#dbe7f3"),
    "CALIFICACION": ("#5b21b6", "#ede4fb"),
    "NO_ENCONTRADO": ("#444444", "#e6e6e6"),
    "RESERVADO": ("#0f766e", "#d4f1ee"),
    "FUERA_ALCANCE_REGISTRO": ("#7c2d12", "#f6e0d4"),
}
COLOR_DEFECTO = ("#222222", "#f0f0f0")


def color_estado(estado):
    return COLORES_ESTADO.get((estado or "").upper(), COLOR_DEFECTO)


def operar(accion):
    """Ejecuta una accion con una conexion fresca y la cierra siempre.

    Devuelve (ok, resultado_o_error). Evita conexiones colgadas durante la demo
    y muestra un mensaje claro si la base SQL no esta disponible.
    """
    try:
        connection = get_connection()
    except Exception as exc:  # noqa: BLE001
        motor = "SQL Server 2022" if DB_ENGINE == "mssql" else "MySQL/MariaDB"
        detalle = (
            "Verifique que SQL Server este iniciado y que la base demo este cargada."
            if DB_ENGINE == "mssql"
            else "Verifique que XAMPP este iniciado y que la base demo este cargada."
        )
        messagebox.showerror(
            "Sin conexion a la base",
            f"No se pudo conectar a {motor}.\n\n"
            f"{detalle}\n\n"
            f"Detalle: {exc}",
        )
        return False, exc
    try:
        return True, accion(TituloRepository(connection))
    finally:
        connection.close()


# ---------------------------------------------------------------------------
# 1. FORMULARIO DE REGISTRO (CREATE)
# ---------------------------------------------------------------------------
class FormularioRegistro(tk.Toplevel):
    TITULO = "Formulario 1 - Registro de titulo"

    def __init__(self, master):
        super().__init__(master)
        self.title(self.TITULO)
        self.resizable(False, False)
        self._construir()

    def _construir(self):
        cont = ttk.Frame(self, padding=16)
        cont.grid(row=0, column=0)
        ttk.Label(
            cont, text="Registro de titulo registral", font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        self.vars = {}

        def fila(etiqueta, clave, widget):
            r = len(self.vars) + 1
            ttk.Label(cont, text=etiqueta).grid(row=r, column=0, sticky="w", pady=3, padx=(0, 10))
            widget.grid(row=r, column=1, sticky="we", pady=3)
            self.vars[clave] = widget

        ent = lambda: ttk.Entry(cont, width=34)

        fila("Item operativo:", "item", ent())
        fila("Bloque (1-99):", "bloque", ent())
        combo_of = ttk.Combobox(cont, values=OFICINAS_VALIDAS, state="readonly", width=32)
        combo_of.set(OFICINAS_VALIDAS[0])
        fila("Oficina:", "oficina", combo_of)
        anio = ent(); anio.insert(0, "2026")
        fila("Anio de consulta:", "anio_consulta", anio)
        fila("Nro. de oficio:", "oficio", ent())
        fila("Nro. de titulo (solo numeros):", "titulo", ent())
        fila("Nombre del solicitante:", "nombre", ent())
        fila("DNI (8) o RUC (11):", "dni_ruc", ent())
        fila("Partida (opcional, control SQL):", "partida", ent())
        combo_est = ttk.Combobox(cont, values=ESTADOS_VALIDOS, state="readonly", width=32)
        combo_est.set("PENDIENTE")
        fila("Estado SUNARP:", "estado_sunarp", combo_est)
        fila("Fecha presentacion (AAAA-MM-DD):", "fecha_presentacion", ent())
        fila("Fecha vencimiento (AAAA-MM-DD):", "fecha_vencimiento", ent())

        self.mensaje = ttk.Label(cont, text="", foreground="#1f4e79")
        self.mensaje.grid(row=len(self.vars) + 1, column=0, columnspan=2, sticky="w", pady=(10, 4))

        barra = ttk.Frame(cont)
        barra.grid(row=len(self.vars) + 2, column=0, columnspan=2, sticky="e", pady=(8, 0))
        ttk.Button(barra, text="Limpiar", command=self._limpiar).grid(row=0, column=0, padx=6)
        ttk.Button(barra, text="Guardar", command=self._guardar).grid(row=0, column=1)

        cont.columnconfigure(1, weight=1)

    def _val(self, clave):
        return self.vars[clave].get().strip()

    def _limpiar(self, limpiar_mensaje=True):
        for clave, widget in self.vars.items():
            if isinstance(widget, ttk.Combobox):
                continue
            widget.delete(0, tk.END)
        self.vars["anio_consulta"].insert(0, "2026")
        if limpiar_mensaje:
            self.mensaje.config(text="", foreground="#1f4e79")

    def _validar(self):
        if not self._val("item").isdigit():
            return "El item operativo debe ser un numero."
        if not (self._val("bloque").isdigit() and 1 <= int(self._val("bloque")) <= 99):
            return "El bloque debe ser un numero entre 1 y 99."
        if not (self._val("anio_consulta").isdigit() and 2000 <= int(self._val("anio_consulta")) <= 2100):
            return "El anio de consulta debe estar entre 2000 y 2100."
        if not self._val("oficio"):
            return "El numero de oficio no puede estar vacio."
        if not self._val("titulo").isdigit():
            return "El numero de titulo SUNARP debe ingresarse solo con numeros."
        if not self._val("nombre"):
            return "El nombre del solicitante no puede estar vacio."
        if not (self._val("dni_ruc").isdigit() and len(self._val("dni_ruc")) in (8, 11)):
            return "DNI debe tener 8 digitos o RUC 11 digitos."
        for campo in ("fecha_presentacion", "fecha_vencimiento"):
            valor = self._val(campo)
            if valor and not _fecha_valida(valor):
                return f"La {campo.replace('_', ' ')} debe usar formato AAAA-MM-DD."
        return None

    def _guardar(self):
        error = self._validar()
        if error:
            self.mensaje.config(text="[!] " + error, foreground="#9b1c1c")
            return
        data = {
            "item": int(self._val("item")),
            "bloque": self._val("bloque").zfill(2),
            "oficina": self._val("oficina"),
            "anio_consulta": int(self._val("anio_consulta")),
            "oficio": self._val("oficio"),
            "titulo": self._val("titulo"),
            "nombre": self._val("nombre"),
            "dni_ruc": self._val("dni_ruc"),
            "partida": (self._val("partida").upper() or None),
            "estado_sunarp": self._val("estado_sunarp"),
            "fecha_presentacion": self._val("fecha_presentacion") or None,
            "fecha_vencimiento": self._val("fecha_vencimiento") or None,
            "pdf_descargado": "NO",
        }
        ok, resultado = operar(lambda repo: repo.registrar(data))
        if not ok:
            return
        exito, mensaje = resultado
        if exito:
            self._limpiar(limpiar_mensaje=False)
            self.mensaje.config(text="[OK] " + mensaje, foreground="#1b7f3b")
        else:
            self.mensaje.config(text="[!] " + mensaje, foreground="#9b1c1c")


# ---------------------------------------------------------------------------
# 2. FORMULARIO DE CONSULTA Y SEGUIMIENTO (READ + diferenciacion de estado)
# ---------------------------------------------------------------------------
class FormularioConsulta(tk.Toplevel):
    TITULO = "Formulario 2 - Consulta y seguimiento"

    def __init__(self, master):
        super().__init__(master)
        self.title(self.TITULO)
        self.minsize(820, 520)
        self._construir()
        self._cargar_listado()

    def _construir(self):
        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)

        ttk.Label(
            cont, text="Consulta de titulo y seguimiento por estado",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        # --- Busqueda operativa por titulo ---
        barra = ttk.Frame(cont)
        barra.pack(fill="x")
        ttk.Label(barra, text="Buscar por Nro. de titulo:").pack(side="left")
        self.entry_titulo = ttk.Entry(barra, width=18)
        self.entry_titulo.pack(side="left", padx=6)
        self.entry_titulo.bind("<Return>", lambda _e: self._buscar())
        ttk.Button(barra, text="Buscar", command=self._buscar).pack(side="left")

        ttk.Label(barra, text="   Filtrar listado:").pack(side="left", padx=(18, 4))
        self.filtro = ttk.Combobox(
            barra, values=["(TODOS)"] + ESTADOS_VALIDOS, state="readonly", width=20
        )
        self.filtro.set("(TODOS)")
        self.filtro.pack(side="left")
        self.filtro.bind("<<ComboboxSelected>>", lambda _e: self._cargar_listado())

        # --- Ficha con estado destacado ---
        ficha = ttk.LabelFrame(cont, text="Resultado de la busqueda", padding=10)
        ficha.pack(fill="x", pady=10)
        self.lbl_estado = tk.Label(
            ficha, text="ESTADO", font=("Segoe UI", 14, "bold"),
            width=20, padx=8, pady=6,
        )
        self.lbl_estado.grid(row=0, column=0, rowspan=3, padx=(0, 14))
        self.lbl_detalle = ttk.Label(ficha, text="Ingrese un numero de titulo y presione Buscar.",
                                     justify="left")
        self.lbl_detalle.grid(row=0, column=1, sticky="w")
        self._pintar_estado(None)

        # --- Listado coloreado por estado ---
        cols = ("item", "bloque", "oficio", "titulo", "partida", "nombre", "estado", "pdf")
        self.tabla = ttk.Treeview(cont, columns=cols, show="headings", height=12)
        anchos = (50, 60, 120, 80, 100, 180, 130, 90)
        encabezados = ("Item", "Bloque", "Oficio", "Titulo", "Partida", "Nombre", "Estado", "PDF")
        for c, e, a in zip(cols, encabezados, anchos):
            self.tabla.heading(c, text=e)
            self.tabla.column(c, width=a, anchor="w")
        for estado, (fg, bg) in COLORES_ESTADO.items():
            self.tabla.tag_configure(estado, background=bg, foreground=fg)
        self.tabla.pack(fill="both", expand=True)

        self.lbl_total = ttk.Label(cont, text="")
        self.lbl_total.pack(anchor="w", pady=(6, 0))

    def _pintar_estado(self, estado):
        fg, bg = color_estado(estado)
        self.lbl_estado.config(text=(estado or "—"), fg=fg, bg=bg)

    def _buscar(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo.isdigit():
            messagebox.showinfo("Dato invalido", "El titulo SUNARP se ingresa solo con numeros.")
            return
        ok, row = operar(lambda repo: repo.buscar_por_titulo(titulo))
        if not ok:
            return
        if row is None:
            self._pintar_estado(None)
            self.lbl_detalle.config(text=f"No se encontro el titulo {titulo} en la base SQL.")
            return
        self._pintar_estado(row["estado_sunarp"])
        self.lbl_detalle.config(
            text=(
                f"Titulo: {row['titulo']}      Item: {row['item']}      Bloque: {row['bloque']}\n"
                f"Oficina: {row['oficina']}      Oficio: {row['oficio']}\n"
                f"Solicitante: {row['nombre']}      DNI/RUC: {row['dni_ruc']}\n"
                f"Partida (control interno SQL): {row['partida'] or row['partida_web'] or '—'}\n"
                f"PDF: {row['pdf_descargado']}      "
                f"Presentacion: {row['fecha_presentacion'] or '—'}      "
                f"Vencimiento: {row['fecha_vencimiento'] or '—'}"
            )
        )

    def _cargar_listado(self):
        ok, rows = operar(lambda repo: repo.listar())
        if not ok:
            return
        filtro = self.filtro.get()
        if filtro and filtro != "(TODOS)":
            rows = [r for r in rows if r["estado_sunarp"] == filtro]
        self.tabla.delete(*self.tabla.get_children())
        for r in rows:
            self.tabla.insert(
                "", "end",
                values=(
                    r["item"], r["bloque"], r["oficio"], r["titulo"] or "",
                    r["partida"] or r["partida_web"] or "", r["nombre"],
                    r["estado_sunarp"], r["pdf_descargado"],
                ),
                tags=(r["estado_sunarp"],),
            )
        self.lbl_total.config(text=f"Registros mostrados: {len(rows)}")


# ---------------------------------------------------------------------------
# 3. FORMULARIO DE ACTUALIZACION DE ESTADO (UPDATE + historial)
# ---------------------------------------------------------------------------
class FormularioActualizacion(tk.Toplevel):
    TITULO = "Formulario 3 - Actualizacion de estado"

    def __init__(self, master):
        super().__init__(master)
        self.title(self.TITULO)
        self.minsize(720, 480)
        self._construir()

    def _construir(self):
        cont = ttk.Frame(self, padding=14)
        cont.pack(fill="both", expand=True)
        ttk.Label(
            cont, text="Actualizacion de estado con trazabilidad",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 10))

        barra = ttk.Frame(cont)
        barra.pack(fill="x")
        ttk.Label(barra, text="Nro. de titulo:").pack(side="left")
        self.entry_titulo = ttk.Entry(barra, width=18)
        self.entry_titulo.pack(side="left", padx=6)
        self.entry_titulo.bind("<Return>", lambda _e: self._cargar())
        ttk.Button(barra, text="Cargar", command=self._cargar).pack(side="left")

        self.lbl_actual = ttk.Label(cont, text="Cargue un titulo para ver su estado actual.")
        self.lbl_actual.pack(anchor="w", pady=10)

        cambio = ttk.Frame(cont)
        cambio.pack(fill="x")
        ttk.Label(cambio, text="Nuevo estado:").grid(row=0, column=0, sticky="w")
        self.combo_estado = ttk.Combobox(cambio, values=ESTADOS_VALIDOS, state="readonly", width=24)
        self.combo_estado.grid(row=0, column=1, sticky="w", padx=6)
        ttk.Label(cambio, text="Observacion:").grid(row=1, column=0, sticky="w", pady=6)
        self.entry_obs = ttk.Entry(cambio, width=52)
        self.entry_obs.grid(row=1, column=1, sticky="we", padx=6, pady=6)
        ttk.Button(cambio, text="Actualizar estado", command=self._actualizar).grid(
            row=0, column=2, rowspan=2, padx=12
        )

        self.mensaje = ttk.Label(cont, text="")
        self.mensaje.pack(anchor="w", pady=(2, 8))

        ttk.Label(cont, text="Historial de cambios:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        cols = ("anterior", "nuevo", "fecha", "observacion")
        self.tabla = ttk.Treeview(cont, columns=cols, show="headings", height=9)
        for c, e, a in zip(cols, ("Anterior", "Nuevo", "Fecha", "Observacion"), (130, 130, 160, 260)):
            self.tabla.heading(c, text=e)
            self.tabla.column(c, width=a, anchor="w")
        self.tabla.pack(fill="both", expand=True, pady=(4, 0))

    def _cargar(self):
        titulo = self.entry_titulo.get().strip()
        if not titulo.isdigit():
            messagebox.showinfo("Dato invalido", "El titulo SUNARP se ingresa solo con numeros.")
            return
        ok, row = operar(lambda repo: repo.buscar_por_titulo(titulo))
        if not ok:
            return
        if row is None:
            self.lbl_actual.config(text=f"No existe el titulo {titulo}.", foreground="#9b1c1c")
            self.combo_estado.set("")
            self.tabla.delete(*self.tabla.get_children())
            return
        fg, _ = color_estado(row["estado_sunarp"])
        self.lbl_actual.config(
            text=f"Titulo {row['titulo']}  |  estado actual: {row['estado_sunarp']}  |  "
                 f"solicitante: {row['nombre']}",
            foreground=fg,
        )
        self.combo_estado.set(row["estado_sunarp"])
        self._cargar_historial(titulo)

    def _cargar_historial(self, titulo):
        ok, historial = operar(lambda repo: repo.historial_por_titulo(titulo))
        if not ok:
            return
        self.tabla.delete(*self.tabla.get_children())
        for h in historial:
            self.tabla.insert(
                "", "end",
                values=(h["estado_anterior"] or "", h["estado_nuevo"],
                        str(h["fecha_cambio"]), h["observacion"] or ""),
            )

    def _actualizar(self):
        titulo = self.entry_titulo.get().strip()
        nuevo = self.combo_estado.get().strip()
        if not titulo.isdigit():
            messagebox.showinfo("Dato invalido", "Primero cargue un titulo valido.")
            return
        if not nuevo:
            messagebox.showinfo("Dato invalido", "Seleccione el nuevo estado.")
            return
        obs = self.entry_obs.get().strip()
        ok, resultado = operar(lambda repo: repo.actualizar_estado(titulo, nuevo, obs))
        if not ok:
            return
        exito, mensaje = resultado
        self.mensaje.config(
            text=("[OK] " if exito else "[!] ") + mensaje,
            foreground="#1b7f3b" if exito else "#9b1c1c",
        )
        if exito:
            self.entry_obs.delete(0, tk.END)
            self._cargar()


# ---------------------------------------------------------------------------
# VENTANA PRINCIPAL: menu de los tres formularios
# ---------------------------------------------------------------------------
class MenuFormularios(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SUNARP SQL - Formularios")
        self.resizable(False, False)
        cont = ttk.Frame(self, padding=24)
        cont.pack()
        ttk.Label(
            cont, text="Sistema SUNARP SQL", font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 4))
        ttk.Label(cont, text="Formularios de gestion de titulos registrales").pack(pady=(0, 18))

        botones = [
            ("1.  Registrar titulo  (CREATE)", FormularioRegistro),
            ("2.  Consulta y seguimiento  (READ)", FormularioConsulta),
            ("3.  Actualizar estado  (UPDATE)", FormularioActualizacion),
        ]
        for texto, clase in botones:
            ttk.Button(
                cont, text=texto, width=42,
                command=lambda c=clase: c(self),
            ).pack(pady=5, ipady=4)

        ttk.Separator(cont).pack(fill="x", pady=14)
        ttk.Label(
            cont,
            text="Nota: la consulta SUNARP es por numero de titulo;\n"
                 "la partida es dato interno de control en SQL.",
            foreground="#555555", justify="center",
        ).pack()
        ttk.Button(cont, text="Salir", command=self.destroy).pack(pady=(14, 0))


def _fecha_valida(texto):
    from datetime import date
    try:
        date.fromisoformat(texto)
        return True
    except ValueError:
        return False


def main():
    MenuFormularios().mainloop()


if __name__ == "__main__":
    main()
