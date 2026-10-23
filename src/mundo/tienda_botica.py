"""Tienda base + Botica (pociones y antidotos).

Cada compra se apila en el inventario del jugador (LIFO), por lo que
`deshacer_compra()` saca siempre el ultimo item comprado.
El jugador solo necesita los atributos `oro` e `inventario` (una pila).
"""

try:
    from .automata_pila import pila_simple
    from .reloj_global import RELOJ, DIA
except ImportError:  # ejecucion directa del archivo
    from automata_pila import pila_simple
    from reloj_global import RELOJ, DIA


class Jugador:
    """Jugador minimo para probar. Si ya tienen uno, basta con que tenga
    `oro` (int) e `inventario` (pila con push/pop/peek/esta_vacia)."""

    def __init__(self, nombre="Heroe", oro=100):
        self.nombre = nombre
        self.oro = oro
        self.inventario = pila_simple()


class Tienda:
    def __init__(self, nombre, catalogo, reloj=None, fases_abierta=(DIA,)):
        # catalogo: lista de (nombre, precio, stock)
        self.nombre = nombre
        self.catalogo = {n: {"precio": p, "stock": s} for n, p, s in catalogo}
        self.reloj = reloj or RELOJ
        self.fases_abierta = tuple(fases_abierta)

    def esta_abierta(self):
        return self.reloj.fase_actual() in self.fases_abierta

    def listar(self):
        estado = "ABIERTA" if self.esta_abierta() else "CERRADA"
        lineas = [f"== {self.nombre} ({estado}) =="]
        for n, d in self.catalogo.items():
            lineas.append(f"- {n}: {d['precio']} oro (stock {d['stock']})")
        texto = "\n".join(lineas)
        print(texto)
        return texto

    def comprar(self, item, jugador):
        """Devuelve (ok, mensaje)."""
        if not self.esta_abierta():
            return False, f"{self.nombre} esta cerrada ({self.reloj.fase_actual()})."
        if item not in self.catalogo:
            return False, f"'{item}' no se vende aqui."
        datos = self.catalogo[item]
        if datos["stock"] <= 0:
            return False, f"'{item}' esta agotado."
        if jugador.oro < datos["precio"]:
            return False, f"Oro insuficiente: necesitas {datos['precio']} y tienes {jugador.oro}."
        jugador.oro -= datos["precio"]
        datos["stock"] -= 1
        jugador.inventario.push(item)       # LIFO
        return True, f"Compraste {item} por {datos['precio']} oro."

    def vender(self, item, jugador):
        """El jugador vende un item de su inventario por el 50% del precio."""
        if not self.esta_abierta():
            return False, f"{self.nombre} esta cerrada ({self.reloj.fase_actual()})."
        if item not in self.catalogo:
            return False, f"{self.nombre} no compra '{item}'."
        # Buscar el item en la pila: se sacan los de arriba y se devuelven.
        temporal = []
        encontrado = False
        while not jugador.inventario.esta_vacia():
            tope = jugador.inventario.pop()
            if tope == item:
                encontrado = True
                break
            temporal.append(tope)
        for x in reversed(temporal):        # restaurar el orden original
            jugador.inventario.push(x)
        if not encontrado:
            return False, f"No tienes '{item}' en el inventario."
        pago = self.catalogo[item]["precio"] // 2
        jugador.oro += pago
        self.catalogo[item]["stock"] += 1
        return True, f"Vendiste {item} por {pago} oro."

    def deshacer_compra(self, jugador):
        """Saca el ultimo item del inventario y devuelve el oro completo."""
        if not self.esta_abierta():
            return False, f"{self.nombre} esta cerrada ({self.reloj.fase_actual()})."
        if jugador.inventario.esta_vacia():
            return False, "No hay compras que deshacer."
        ultimo = jugador.inventario.peek()
        if ultimo not in self.catalogo:
            return False, f"El ultimo item ('{ultimo}') no es de {self.nombre}."
        jugador.inventario.pop()
        precio = self.catalogo[ultimo]["precio"]
        jugador.oro += precio
        self.catalogo[ultimo]["stock"] += 1
        return True, f"Compra deshecha: {ultimo} (+{precio} oro)."


def crear_botica(reloj=None):
    return Tienda(
        "Botica",
        [
            ("pocion de vida", 25, 5),
            ("pocion de mana", 30, 4),
            ("antidoto", 20, 6),
            ("elixir mayor", 80, 2),
        ],
        reloj=reloj,
    )


if __name__ == "__main__":
    botica = crear_botica()
    heroe = Jugador("Hugo", oro=100)
    botica.listar()
    print(botica.comprar("pocion de vida", heroe))
    print(botica.comprar("antidoto", heroe))
    print("Inventario:", heroe.inventario.elementos(), "| oro:", heroe.oro)
    print(botica.deshacer_compra(heroe))
    print(botica.vender("pocion de vida", heroe))
    print(botica.comprar("elixir mayor", heroe))
    RELOJ.tick(10)                          # cae la noche
    print(botica.comprar("antidoto", heroe))
