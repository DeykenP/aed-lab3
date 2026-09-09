"""
====================================================================
 LOGICA: LISTA SIMPLEMENTE ENLAZADA
 Ejemplo de la vida real: TREN DE CARGA (locomotora + vagones)
====================================================================

Este archivo SOLO contiene la estructura de datos, sin nada de
tkinter. Por eso lo puede usar gui.py sin duplicar codigo.

Por que lista SIMPLEMENTE enlazada (no doble)?
Porque un tren real solo se puede RECORRER/INSPECCIONAR hacia
adelante: desde la locomotora hacia el ultimo vagon. Cada vagon
solo conoce al vagon de ATRAS de el (su "siguiente"), no le hace
falta conocer al de adelante. No hay boton de "retroceder" porque
un tren no funciona asi.

    [Locomotora] -> [Vagon1] -> [Vagon2] -> [Vagon3] -> None

Esto contrasta con la playlist (lista DOBLE) del otro ejemplo,
donde si se necesitaba ir en las dos direcciones.
"""


# --------------------------------------------------------------
# 1. NODO: un vagon del tren.
#    Un nodo simple solo tiene DATOS + referencia al SIGUIENTE
#    (a diferencia del nodo doble de la playlist, aqui no hay
#    referencia hacia atras).
# --------------------------------------------------------------
class Vagon:
    def __init__(self, carga):
        self.carga = carga        # que transporta el vagon, ej. "Granos"
        self.siguiente = None     # apunta al vagon de atras (o None)

    def __str__(self):
        return f"Vagón de {self.carga}"


# --------------------------------------------------------------
# 2. LISTA SIMPLEMENTE ENLAZADA: el tren completo
# --------------------------------------------------------------
class Tren:
    def __init__(self, nombre):
        self.nombre = nombre
        self.locomotora = None    # primer vagon de la fila
        self.ultimo_vagon = None  # ultimo vagon, para agregar rapido

    # ------------------------------------------------------
    # Agregar SIEMPRE al final: engancharlo despues del que
    # hasta ahora era el ultimo vagon.
    # ------------------------------------------------------
    def enganchar_vagon(self, carga):
        nuevo = Vagon(carga)

        if self.locomotora is None:
            # el tren estaba vacio -> este vagon es el unico
            self.locomotora = nuevo
            self.ultimo_vagon = nuevo
            return nuevo

        self.ultimo_vagon.siguiente = nuevo
        self.ultimo_vagon = nuevo
        return nuevo

    # ------------------------------------------------------
    # Quitar un vagon. Como cada vagon SOLO conoce al de
    # adelante, hay que recorrer desde la locomotora para
    # encontrar quien va justo antes del que se quiere quitar
    # (esa busqueda extra es la desventaja de la lista simple
    # frente a la doble, que ya tiene ese dato guardado).
    # ------------------------------------------------------
    def desenganchar_vagon(self, vagon):
        anterior = None
        actual = self.locomotora

        # Paso 1: buscar el vagon y recordar quien iba antes de el
        while actual is not None and actual is not vagon:
            anterior = actual
            actual = actual.siguiente

        if actual is None:
            return False   # el vagon no esta en este tren

        # Paso 2: saltar el vagon encontrado, uniendo sus vecinos
        if anterior is None:
            self.locomotora = actual.siguiente   # se quito la locomotora
        else:
            anterior.siguiente = actual.siguiente

        if actual is self.ultimo_vagon:
            self.ultimo_vagon = anterior          # se quito el ultimo vagon

        return True

    # ------------------------------------------------------
    # Recorrido clasico: empezar en la locomotora y avanzar
    # con "siguiente" hasta llegar a None. Solo se puede ir
    # hacia adelante (no existe forma de retroceder).
    # ------------------------------------------------------
    def recorrer(self):
        vagones = []
        actual = self.locomotora
        while actual is not None:
            vagones.append(actual)
            actual = actual.siguiente
        return vagones
