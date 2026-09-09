# --------------------------------------------------------------
# 1. NODO: una cancion dentro de la playlist.
#    Un nodo siempre es lo mismo: DATOS + REFERENCIAS a sus vecinos.
# --------------------------------------------------------------
class Cancion:
    def __init__(self, titulo, artista):
        self.titulo = titulo
        self.artista = artista
        self.siguiente = None   # apunta a la cancion de despues (o None)
        self.anterior = None    # apunta a la cancion de antes (o None)

    def __str__(self):
        return f"{self.titulo} - {self.artista}"


# --------------------------------------------------------------
# 2. LISTA DOBLEMENTE ENLAZADA: la playlist completa.
#    Esta clase solo guarda 3 punteros y sabe moverlos.
# --------------------------------------------------------------
class Playlist:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cabeza = None          # primera cancion de la lista
        self.cola = None            # ultima cancion de la lista
        self.cancion_actual = None  # cancion que se esta reproduciendo

    # ------------------------------------------------------
    # Agregar SIEMPRE al final: crear el nodo y enlazarlo con
    # el que hasta ahora era el ultimo (la cola).
    # ------------------------------------------------------
    def agregar_cancion(self, titulo, artista):
        nueva = Cancion(titulo, artista)

        if self.cabeza is None:
            # la playlist estaba vacia -> la nueva cancion es unica
            self.cabeza = nueva
            self.cola = nueva
            self.cancion_actual = nueva
            return nueva

        # engancha la nueva cancion despues de la actual ultima
        nueva.anterior = self.cola
        self.cola.siguiente = nueva
        self.cola = nueva
        return nueva

    # ------------------------------------------------------
    # Eliminar: "saltar" el nodo uniendo a su anterior con su
    # siguiente, para que la cadena quede sin huecos.
    # ------------------------------------------------------
    def eliminar_cancion(self, cancion):
        anterior = cancion.anterior
        siguiente = cancion.siguiente

        # Paso 1: conectar al vecino de la izquierda con el de la derecha
        if anterior is not None:
            anterior.siguiente = siguiente
        else:
            self.cabeza = siguiente     # se elimino la primera cancion

        # Paso 2: conectar al vecino de la derecha con el de la izquierda
        if siguiente is not None:
            siguiente.anterior = anterior
        else:
            self.cola = anterior        # se elimino la ultima cancion

        # Paso 3: si borramos la que sonaba, hay que "saltar" a otra
        if self.cancion_actual is cancion:
            if siguiente is not None:
                self.cancion_actual = siguiente
            else:
                self.cancion_actual = anterior

    # ------------------------------------------------------
    # Mover el puntero "cancion_actual" una posicion adelante
    # ------------------------------------------------------
    def reproducir_siguiente(self):
        if self.cancion_actual is None:
            return
        if self.cancion_actual.siguiente is not None:
            self.cancion_actual = self.cancion_actual.siguiente
        else:
            self.cancion_actual = self.cabeza   # reinicia la playlist

    # ------------------------------------------------------
    # Mover el puntero "cancion_actual" una posicion atras
    # ------------------------------------------------------
    def reproducir_anterior(self):
        if self.cancion_actual is None:
            return
        if self.cancion_actual.anterior is not None:
            self.cancion_actual = self.cancion_actual.anterior
        else:
            self.cancion_actual = self.cola     # se va a la ultima

    # ------------------------------------------------------
    # Recorrido clasico de una lista enlazada: empezar en la
    # cabeza e ir avanzando con "siguiente" hasta llegar a None.
    # ------------------------------------------------------
    def recorrer(self):
        canciones = []
        actual = self.cabeza
        while actual is not None:
            canciones.append(actual)
            actual = actual.siguiente
        return canciones
