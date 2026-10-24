class AutomataPilaMundo:
    def __init__(self):
        self.simbolo_fondo = "Z0_SANTUARIO_CENTRAL"
        self.pila = [self.simbolo_fondo]
        self.inventario_fragmentos = set()
        self.registro_misericordia = {}

    def transicion_delta(self, accion, argumento=None):
        """
        Función formal delta(q, a, X) -> (p, gamma)
        """
        tope = self.pila[-1] if self.pila else None

        if accion == "PUSH" and argumento:
            self.pila.append(argumento)
            return True, f"APD PUSH: '{argumento}' apilado sobre '{tope}'."
        elif accion == "POP":
            if len(self.pila) > 1:
                removido = self.pila.pop()
                return True, f"APD POP: Retorno a '{self.pila[-1]}'. Desapilado: '{removido}'."
            return False, "APD ERROR: Imposible desapilar el símbolo inicial Z0."
        elif accion == "PEEK":
            return True, tope
        return False, "Acción APD no válida."

    def registrar_decision(self, subordinado, fue_perdonado):
        self.registro_misericordia[subordinado] = fue_perdonado

    def agregar_fragmento(self, nombre):
        self.inventario_fragmentos.add(nombre)

    def tope(self):
        return self.pila[-1]

    def obtener_traza_pila(self):
        return list(reversed(self.pila))