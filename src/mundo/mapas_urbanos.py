"""Mapas urbanos como matrices (list[list[str]]) con backtracking por pila.

Leyenda: '#' pared, '.' calle, 'B' botica, 'A' armeria, '@' jugador.
Coordenadas: x = columna, y = fila.
"""

try:
    from .automata_pila import pila_simple
except ImportError:  # ejecucion directa del archivo
    from automata_pila import pila_simple

LEYENDA = {"#": "pared", ".": "calle", "B": "botica", "A": "armeria", "@": "jugador"}

DIRECCIONES = {
    "w": (0, -1), "arriba": (0, -1), "norte": (0, -1),
    "s": (0, 1), "abajo": (0, 1), "sur": (0, 1),
    "a": (-1, 0), "izquierda": (-1, 0), "oeste": (-1, 0),
    "d": (1, 0), "derecha": (1, 0), "este": (1, 0),
}

MAPA_CIUDAD = [
    "###########",
    "#@..#.....#",
    "#.#.#.###.#",
    "#.#...#B..#",
    "#.#####.###",
    "#...A...#.#",
    "###########",
]


class MapaUrbano:
    def __init__(self, filas=None):
        self.base = []                  # matriz sin el jugador
        self.x = 0
        self.y = 0
        self.historial = pila_simple()  # pila LIFO de posiciones visitadas
        self.cargar_mapa(filas or MAPA_CIUDAD)

    def cargar_mapa(self, filas):
        """Carga una matriz (lista de strings o de listas). Busca '@' como inicio."""
        matriz = [list(f) for f in filas]
        inicio = None
        for y, fila in enumerate(matriz):
            for x, c in enumerate(fila):
                if c == "@":
                    inicio = (x, y)
                    matriz[y][x] = "."
        if inicio is None:
            raise ValueError("El mapa debe tener un '@' como posicion inicial")
        self.base = matriz
        self.x, self.y = inicio
        self.historial = pila_simple()
        self.historial.push(inicio)

    def es_transitable(self, x, y):
        if y < 0 or y >= len(self.base) or x < 0 or x >= len(self.base[y]):
            return False
        return self.base[y][x] != "#"

    def mover(self, direccion):
        """Mueve al jugador. Guarda la posicion previa en la pila. True si se movio."""
        d = DIRECCIONES.get(str(direccion).lower())
        if d is None:
            return False
        nx, ny = self.x + d[0], self.y + d[1]
        if not self.es_transitable(nx, ny):
            return False
        self.historial.push((nx, ny))
        self.x, self.y = nx, ny
        return True

    def volver_atras(self):
        """Backtracking: desapila la posicion actual y regresa a la anterior."""
        if len(self.historial) <= 1:        # solo queda la posicion inicial
            return False
        self.historial.pop()
        self.x, self.y = self.historial.peek()
        return True

    def edificio_actual(self):
        """'B' si esta en la botica, 'A' en la armeria, None en otro caso."""
        c = self.base[self.y][self.x]
        return c if c in ("B", "A") else None

    def posicion(self):
        return (self.x, self.y)

    def a_texto(self):
        filas = []
        for y, fila in enumerate(self.base):
            filas.append("".join("@" if (x, y) == (self.x, self.y) else c
                                 for x, c in enumerate(fila)))
        return "\n".join(filas)

    def mostrar_mapa(self):
        print(self.a_texto())


if __name__ == "__main__":
    m = MapaUrbano()
    m.mostrar_mapa()
    for paso in ["d", "d", "s", "s", "d"]:
        print(f"\nmover({paso}) ->", m.mover(paso))
    m.mostrar_mapa()
    print("\nVolver atras 2 veces:", m.volver_atras(), m.volver_atras(), m.posicion())
    m.mostrar_mapa()
