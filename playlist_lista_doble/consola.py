"""
====================================================================
 DEMO DE CONSOLA: PLAYLIST - LISTA DOBLEMENTE ENLAZADA
====================================================================

Version de terminal (sin ventana) del mismo ejemplo. Usa la MISMA
logica de logica.py que usa gui.py - aqui solo agregamos los
"print" para poder ver los pasos en la consola.
"""

from logica import Playlist


def mostrar_playlist(playlist):
    canciones = playlist.recorrer()
    print(f"\n--- Playlist: {playlist.nombre} ({len(canciones)} canciones) ---")
    for posicion, cancion in enumerate(canciones, start=1):
        marca = " <-- sonando" if cancion is playlist.cancion_actual else ""
        print(f"  {posicion}. {cancion}{marca}")
    print("-" * 45)


if __name__ == "__main__":
    mi_playlist = Playlist("Favoritas para programar")

    mi_playlist.agregar_cancion("Bohemian Rhapsody", "Queen")
    mi_playlist.agregar_cancion("Billie Jean", "Michael Jackson")
    mi_playlist.agregar_cancion("Clocks", "Coldplay")
    mi_playlist.agregar_cancion("Africa", "Toto")

    mostrar_playlist(mi_playlist)

    print("\n>> El usuario le da 'siguiente' dos veces:")
    mi_playlist.reproducir_siguiente()
    mi_playlist.reproducir_siguiente()
    mostrar_playlist(mi_playlist)

    print("\n>> El usuario elimina 'Billie Jean':")
    segunda_cancion = mi_playlist.recorrer()[1]
    mi_playlist.eliminar_cancion(segunda_cancion)
    mostrar_playlist(mi_playlist)

    print("\n>> El usuario le da 'anterior':")
    mi_playlist.reproducir_anterior()
    mostrar_playlist(mi_playlist)
