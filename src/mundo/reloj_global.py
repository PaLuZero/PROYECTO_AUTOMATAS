class RelojMundo:
    def __init__(self, duracion_fase=40):
        self.pasos_totales = 0
        self.duracion_fase = duracion_fase  # Pasos antes de cambiar de fase (duplicado para más tiempo)
        self.es_crepusculo = False

    def avanzar(self, pasos=1):
        """Avanza el reloj y retorna si hubo cambio de fase."""
        self.pasos_totales += pasos
        nuevo_crepusculo = (self.pasos_totales // self.duracion_fase) % 2 == 1
        cambio = (nuevo_crepusculo != self.es_crepusculo)
        self.es_crepusculo = nuevo_crepusculo
        return cambio, self.obtener_estado()

    def obtener_estado(self):
        pasos_en_fase = self.pasos_totales % self.duracion_fase
        progreso = pasos_en_fase / self.duracion_fase
        bloques = int(progreso * 6)
        barra = "[" + "#" * bloques + "-" * (6 - bloques) + "]"

        if self.es_crepusculo:
            nombre = "CREPÚSCULO (Inestable)"
        else:
            nombre = "MUNDO NORMAL (Estable)"

        return {
            "es_crepusculo": self.es_crepusculo,
            "nombre": nombre,
            "pasos_fase": pasos_en_fase,
            "duracion": self.duracion_fase,
            "barra": barra
        }