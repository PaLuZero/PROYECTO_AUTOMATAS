"""
MÓDULO: Motor Narrativo AFN
Gestiona el grafo global de escenas y transiciones formales hacia los múltiples finales.
"""

class AFNNarrativo:
    def __init__(self):
        self.estados = {
            "q0": "Inicio de la Crisis",
            "q1": "Espejo Quebrado en la Ciudad",
            "q2": "Exploración de las 4 Regiones",
            "q3": "Espejo Restaurado en el Santuario",
            "q4": "Umbral del Crepúsculo",
            "q_final_a": "Final A: El Equilibrio",
            "q_final_b": "Final B: Sacrificio de los Vínculos",
            "q_final_c": "Final C: Crepúsculo Eterno",
            "q_final_d": "Final D: Los Cuatro Guardianes (Secreto)"
        }
        self.estado_actual = "q0"
        self.estados_aceptacion = {"q_final_a", "q_final_b", "q_final_c", "q_final_d"}

    def transicion(self, accion, contexto=None):
        if self.estado_actual == "q0" and accion == "ROMPER_ESPEJO":
            self.estado_actual = "q1"
        elif self.estado_actual == "q1" and accion == "REUNIR_GRUPO":
            self.estado_actual = "q2"
        elif self.estado_actual == "q2" and accion == "COMPLETAR_FRAGMENTOS":
            self.estado_actual = "q3"
        elif self.estado_actual == "q3" and accion == "CRUZAR_ESPEJO":
            self.estado_actual = "q4"
        elif self.estado_actual == "q4" and accion == "RESOLUCION":
            resultado_combate, perdonados = contexto
            if resultado_combate == "DERROTA":
                self.estado_actual = "q_final_c"
            elif resultado_combate == "SACRIFICIO":
                self.estado_actual = "q_final_b"
            elif resultado_combate == "VICTORIA":
                # Validación matemática del final secreto: 4 subordinados perdonados[cite: 8, 13]
                if len(perdonados) == 4 and all(perdonados.values()):
                    self.estado_actual = "q_final_d"
                else:
                    self.estado_actual = "q_final_a"

        return self.estado_actual

    def trazas_alcanzabilidad(self):
        return {
            "Final A (El Equilibrio)": ["q0", "q1", "q2", "q3", "q4", "q_final_a"],
            "Final B (Sacrificio)": ["q0", "q1", "q2", "q3", "q4", "q_final_b"],
            "Final C (Crepúsculo Eterno)": ["q0", "q1", "q2", "q3", "q4", "q_final_c"],
            "Final D (Cuatro Guardianes)": ["q0", "q1", "q2", "q3", "q4", "q_final_d"]
        }