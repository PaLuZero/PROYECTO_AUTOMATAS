"""Reloj global: oscilador DIA <-> NOCHE con periodo configurable.

Cada `periodo` ticks la fase cambia. Las tiendas y el mapa consultan
`fase_actual()` / `esta_abierto()`. Soporta observadores (callbacks).
"""

DIA = "DIA"
NOCHE = "NOCHE"


class RelojGlobal:
    def __init__(self, periodo=10, fase_inicial=DIA):
        if periodo < 1:
            raise ValueError("El periodo debe ser >= 1")
        if fase_inicial not in (DIA, NOCHE):
            raise ValueError("Fase inicial invalida")
        self.periodo = periodo
        self._fase_inicial = fase_inicial
        self.ticks = 0
        self._observadores = []

    # ---------- consulta ----------
    def fase_actual(self):
        ciclos = (self.ticks // self.periodo) % 2
        if self._fase_inicial == DIA:
            return DIA if ciclos == 0 else NOCHE
        return NOCHE if ciclos == 0 else DIA

    def esta_abierto(self):
        """Los comercios abren de DIA."""
        return self.fase_actual() == DIA

    def ticks_para_cambio(self):
        return self.periodo - (self.ticks % self.periodo)

    # ---------- avance ----------
    def tick(self, n=1):
        """Avanza n ticks y notifica si la fase cambio. Devuelve la fase."""
        for _ in range(n):
            antes = self.fase_actual()
            self.ticks += 1
            despues = self.fase_actual()
            if antes != despues:
                for cb in list(self._observadores):
                    cb(despues, self.ticks)
        return self.fase_actual()

    def reiniciar(self):
        self.ticks = 0

    # ---------- patron observador ----------
    def suscribir(self, callback):
        """callback(fase, ticks) se llama cada vez que cambia la fase."""
        self._observadores.append(callback)

    def desuscribir(self, callback):
        if callback in self._observadores:
            self._observadores.remove(callback)

    def __repr__(self):
        return f"RelojGlobal(ticks={self.ticks}, fase={self.fase_actual()}, periodo={self.periodo})"


# Instancia compartida por todo el mundo (mapa y tiendas)
RELOJ = RelojGlobal(periodo=10)


if __name__ == "__main__":
    r = RelojGlobal(periodo=3)
    r.suscribir(lambda fase, t: print(f"  >> Cambio de fase: {fase} (tick {t})"))
    for _ in range(8):
        print(r.tick(), "| ticks:", r.ticks, "| abierto:", r.esta_abierto())
