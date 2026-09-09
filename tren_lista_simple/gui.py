"""
====================================================================
 GUI (Tkinter): TREN DE CARGA - LISTA SIMPLEMENTE ENLAZADA
====================================================================

Este archivo SOLO se encarga de la ventana: dibuja botones, lee lo
que escribe el usuario y llama a los metodos de la clase Tren que
esta en logica.py. No tiene ninguna regla de negocio aqui.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from logica import Tren


class TrenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista Simplemente Enlazada - Tren de Carga")
        self.root.geometry("480x580")
        self.root.resizable(True, True)

        self.tren = Tren("Tren de carga Sur-Norte")
        self.vagon_en_inspeccion = None   # puntero de recorrido (solo avanza)
        self.vagones_en_orden = []

        self._construir_interfaz()
        self._cargar_vagones_iniciales()

    # ------------------------------------------------------
    def _construir_interfaz(self):
        titulo = ttk.Label(
            self.root, text="🚂 Tren de Carga (Lista Simplemente Enlazada)",
            font=("Segoe UI", 13, "bold")
        )
        titulo.pack(pady=10)

        # --- Formulario para enganchar vagones (en filas verticales,
        # para que quepa sin importar el ancho de la ventana) ---
        frame_form = ttk.Frame(self.root)
        frame_form.pack(pady=5, fill="x", padx=20)

        ttk.Label(frame_form, text="Carga del vagón:").pack(anchor="w")
        self.entry_carga = ttk.Entry(frame_form)
        self.entry_carga.pack(fill="x", pady=3)

        btn_enganchar = ttk.Button(frame_form, text="🔗 Enganchar al final",
                                    command=self.enganchar_vagon)
        btn_enganchar.pack(pady=5)

        # --- Lista visual del tren ---
        self.listbox = tk.Listbox(
            self.root, width=60, height=12, font=("Consolas", 10),
            selectbackground="#4a90d9"
        )
        self.listbox.pack(pady=10, padx=20)

        btn_eliminar = ttk.Button(
            self.root, text="✂ Desenganchar vagón seleccionado",
            command=self.desenganchar_vagon
        )
        btn_eliminar.pack(pady=(0, 15))

        # --- Inspeccion: solo se puede avanzar (como un tren real) ---
        separador = ttk.Separator(self.root, orient="horizontal")
        separador.pack(fill="x", padx=20, pady=5)

        ttk.Label(
            self.root, text="Inspección del tren (solo hacia adelante):",
            font=("Segoe UI", 10, "italic")
        ).pack()

        frame_inspeccion = ttk.Frame(self.root)
        frame_inspeccion.pack(pady=8)

        btn_iniciar = ttk.Button(frame_inspeccion, text="🔁 Empezar en locomotora",
                                  command=self.iniciar_inspeccion)
        btn_iniciar.grid(row=0, column=0, padx=8)

        btn_avanzar = ttk.Button(frame_inspeccion, text="➡ Avanzar un vagón",
                                  command=self.avanzar_inspeccion)
        btn_avanzar.grid(row=0, column=1, padx=8)

        self.label_inspeccion = ttk.Label(
            self.root, text="", font=("Segoe UI", 11, "bold"),
            foreground="#b71c1c"
        )
        self.label_inspeccion.pack(pady=10)

    # ------------------------------------------------------
    def _cargar_vagones_iniciales(self):
        for carga in ["Granos", "Contenedores", "Madera", "Automóviles"]:
            self.tren.enganchar_vagon(carga)
        self._refrescar_vista()

    # ------------------------------------------------------
    def _refrescar_vista(self):
        self.listbox.delete(0, tk.END)
        self.vagones_en_orden = []

        for i, vagon in enumerate(self.tren.recorrer(), start=1):
            etiqueta = "Locomotora + " if i == 1 else f"Vagón {i - 1}: "
            marca = "  🔍 INSPECCIONANDO" if vagon is self.vagon_en_inspeccion else ""
            self.listbox.insert(tk.END, f"{etiqueta}{vagon}{marca}")
            self.vagones_en_orden.append(vagon)

            if vagon is self.vagon_en_inspeccion:
                self.listbox.itemconfig(i - 1, {"bg": "#ffe0b2"})

    # ------------------------------------------------------
    def enganchar_vagon(self):
        carga = self.entry_carga.get().strip()
        if not carga:
            messagebox.showwarning("Dato incompleto",
                                    "Escribe qué transporta el vagón.")
            return
        self.tren.enganchar_vagon(carga)
        self.entry_carga.delete(0, tk.END)
        self._refrescar_vista()

    def desenganchar_vagon(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Nada seleccionado",
                                    "Selecciona un vagón de la lista.")
            return

        indice = seleccion[0]
        vagon = self.vagones_en_orden[indice]

        if vagon is self.vagon_en_inspeccion:
            self.vagon_en_inspeccion = None
            self.label_inspeccion.config(text="")

        self.tren.desenganchar_vagon(vagon)
        self._refrescar_vista()

    def iniciar_inspeccion(self):
        self.vagon_en_inspeccion = self.tren.locomotora
        if self.vagon_en_inspeccion is None:
            self.label_inspeccion.config(text="El tren no tiene vagones")
        else:
            self.label_inspeccion.config(
                text=f"🔍 Inspeccionando: {self.vagon_en_inspeccion}"
            )
        self._refrescar_vista()

    def avanzar_inspeccion(self):
        if self.vagon_en_inspeccion is None:
            messagebox.showinfo("Aviso",
                                 "Primero presiona 'Empezar en locomotora'.")
            return

        if self.vagon_en_inspeccion.siguiente is not None:
            self.vagon_en_inspeccion = self.vagon_en_inspeccion.siguiente
            self.label_inspeccion.config(
                text=f"🔍 Inspeccionando: {self.vagon_en_inspeccion}"
            )
        else:
            self.label_inspeccion.config(
                text="🏁 Llegaste al último vagón (fin del tren, no hay 'atrás')"
            )

        self._refrescar_vista()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrenApp(root)
    root.mainloop()
