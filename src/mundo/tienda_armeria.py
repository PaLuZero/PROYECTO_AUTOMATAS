"""Armeria (armas y armaduras). Reutiliza la clase Tienda de tienda_botica."""

try:
    from .tienda_botica import Tienda, Jugador
    from .reloj_global import RELOJ
except ImportError:  # ejecucion directa del archivo
    from tienda_botica import Tienda, Jugador
    from reloj_global import RELOJ


def crear_armeria(reloj=None):
    return Tienda(
        "Armeria",
        [
            ("espada de hierro", 60, 3),
            ("arco corto", 50, 3),
            ("daga", 25, 5),
            ("escudo de madera", 40, 4),
            ("armadura de cuero", 70, 2),
            ("armadura de acero", 150, 1),
        ],
        reloj=reloj,
    )


if __name__ == "__main__":
    armeria = crear_armeria()
    heroe = Jugador("Hugo", oro=200)
    armeria.listar()
    print(armeria.comprar("espada de hierro", heroe))
    print(armeria.comprar("escudo de madera", heroe))
    print(armeria.comprar("armadura de acero", heroe))   # oro insuficiente
    print("Inventario:", heroe.inventario.elementos(), "| oro:", heroe.oro)
    print(armeria.deshacer_compra(heroe))                # saca el escudo (LIFO)
    print(armeria.vender("espada de hierro", heroe))
    print("Inventario:", heroe.inventario.elementos(), "| oro:", heroe.oro)
