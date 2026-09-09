"""
====================================================================
 GUI (Tkinter): PLAYLIST - LISTA DOBLEMENTE ENLAZADA
====================================================================

Este archivo SOLO se encarga de la ventana: dibuja botones, lee lo
que escribe el usuario y llama a los metodos de la clase Playlist
que esta en logica.py. No tiene ninguna regla de negocio aqui.
"""

import tkinter as tk
from tkinter import ttk, messagebox

from logica import Playlist


class PlaylistApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lista Doblemente Enlazada - Playlist")
        self.root.geometry("480x560")
        self.root.resizable(True, True)

        self.playlist = Playlist("Favoritas para programar")
        # nodo -> indice en el Listbox, para poder resaltar el actual
        self.nodos_en_orden = []

        self._construir_interfaz()
        self._cargar_canciones_iniciales()

    # ------------------------------------------------------
    def _construir_interfaz(self):
        titulo = ttk.Label(
            self.root, text="🎵 Playlist (Lista Doblemente Enlazada)",
            font=("Segoe UI", 14, "bold")
        )
        titulo.pack(pady=10)

        # --- Formulario para agregar canciones (en filas verticales,
        # para que quepa sin importar el ancho de la ventana) ---
        frame_form = ttk.Frame(self.root)
        frame_form.pack(pady=5, fill="x", padx=20)
        frame_form.columnconfigure(1, weight=1)

        ttk.Label(frame_form, text="Título:").grid(row=0, column=0, sticky="w", pady=3)
        self.entry_titulo = ttk.Entry(frame_form)
        self.entry_titulo.grid(row=0, column=1, sticky="ew", padx=5, pady=3)

        ttk.Label(frame_form, text="Artista:").grid(row=1, column=0, sticky="w", pady=3)
        self.entry_artista = ttk.Entry(frame_form)
        self.entry_artista.grid(row=1, column=1, sticky="ew", padx=5, pady=3)

        btn_agregar = ttk.Button(frame_form, text="➕ Agregar",
                                  command=self.agregar_cancion)
        btn_agregar.grid(row=2, column=0, columnspan=2, pady=8)

        # --- Lista visual de canciones (representa los nodos) ---
        self.listbox = tk.Listbox(
            self.root, width=60, height=12, font=("Consolas", 10),
            selectbackground="#4a90d9"
        )
        self.listbox.pack(pady=10, padx=20)

        # --- Botones de eliminar ---
        btn_eliminar = ttk.Button(
            self.root, text="🗑 Eliminar canción seleccionada",
            command=self.eliminar_cancion
        )
        btn_eliminar.pack(pady=(0, 10))

        # --- Reproductor: anterior / actual / siguiente ---
        frame_reproductor = ttk.Frame(self.root)
        frame_reproductor.pack(pady=5)

        btn_anterior = ttk.Button(frame_reproductor, text="⏮ Anterior",
                                   command=self.anterior)
        btn_anterior.grid(row=0, column=0, padx=10)

        btn_siguiente = ttk.Button(frame_reproductor, text="Siguiente ⏭",
                                    command=self.siguiente)
        btn_siguiente.grid(row=0, column=1, padx=10)

        self.label_actual = ttk.Label(
            self.root, text="", font=("Segoe UI", 11, "bold"),
            foreground="#1565c0"
        )
        self.label_actual.pack(pady=10)

    # ------------------------------------------------------
    def _cargar_canciones_iniciales(self):
        for titulo, artista in [
            ("Bohemian Rhapsody", "Queen"),
            ("Billie Jean", "Michael Jackson"),
            ("Clocks", "Coldplay"),
            ("Africa", "Toto"),
        ]:
            self.playlist.agregar_cancion(titulo, artista)
        self._refrescar_vista()

    # ------------------------------------------------------
    # Vuelve a dibujar el Listbox recorriendo la lista enlazada
    # desde la cabeza. Esto es un RECORRIDO clasico de lista enlazada.
    # ------------------------------------------------------
    def _refrescar_vista(self):
        self.listbox.delete(0, tk.END)
        self.nodos_en_orden = []

        for i, nodo in enumerate(self.playlist.recorrer(), start=1):
            marca = "  ▶ SONANDO" if nodo is self.playlist.cancion_actual else ""
            self.listbox.insert(tk.END, f"{i}. {nodo}{marca}")
            self.nodos_en_orden.append(nodo)

            if nodo is self.playlist.cancion_actual:
                self.listbox.itemconfig(i - 1, {"bg": "#dff0d8"})

        if self.playlist.cancion_actual is not None:
            self.label_actual.config(
                text=f"🎧 Reproduciendo ahora: {self.playlist.cancion_actual}"
            )
        else:
            self.label_actual.config(text="La playlist está vacía")

    # ------------------------------------------------------
    def agregar_cancion(self):
        titulo = self.entry_titulo.get().strip()
        artista = self.entry_artista.get().strip()

        if not titulo or not artista:
            messagebox.showwarning("Datos incompletos",
                                    "Escribe título y artista.")
            return

        self.playlist.agregar_cancion(titulo, artista)
        self.entry_titulo.delete(0, tk.END)
        self.entry_artista.delete(0, tk.END)
        self._refrescar_vista()

    def eliminar_cancion(self):
        seleccion = self.listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Nada seleccionado",
                                    "Selecciona una canción de la lista.")
            return

        indice = seleccion[0]
        nodo = self.nodos_en_orden[indice]
        self.playlist.eliminar_cancion(nodo)
        self._refrescar_vista()

    def siguiente(self):
        self.playlist.reproducir_siguiente()
        self._refrescar_vista()

    def anterior(self):
        self.playlist.reproducir_anterior()
        self._refrescar_vista()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistApp(root)
    root.mainloop()
