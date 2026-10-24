"""Automata de Pila Determinista (APD) formal: (Q, Sigma, Gamma, delta, q0, Z0, F).

La pila es LIFO (ultimo en entrar, primero en salir) y se reutiliza en el
resto del mundo: inventario de las tiendas y recorrido del mapa (backtracking).
"""


class AutomataPila:
    def __init__(self, estados, alfabeto, transiciones, inicial,
                 simbolo_fondo="Z", finales=None):
        self.estados = set(estados)                 # Q
        self.alfabeto = set(alfabeto)               # Sigma
        self.delta = dict(transiciones)             # {(q, a, tope): (q2, [apilar])}
        self.inicial = inicial                      # q0
        self.simbolo_fondo = simbolo_fondo          # Z0
        self.finales = set(finales or [])           # F

        # Gamma: simbolos de pila usados por delta (mas el fondo)
        self.gamma = {simbolo_fondo}
        for (_, _, tope), (_, apilar) in self.delta.items():
            self.gamma.add(tope)
            self.gamma.update(apilar)

        self._validar()
        self.estado = inicial
        self.pila = [simbolo_fondo]

    # ---------- validacion ----------
    def _validar(self):
        if self.inicial not in self.estados:
            raise ValueError("El estado inicial no pertenece a Q")
        if not self.finales <= self.estados:
            raise ValueError("Hay estados finales que no pertenecen a Q")
        # Determinismo: al ser un dict, cada (q, a, tope) tiene UNA sola
        # transicion. Solo comprobamos que todo sea coherente con Q y Sigma.
        for (q, a, _), (q2, _) in self.delta.items():
            if q not in self.estados or q2 not in self.estados:
                raise ValueError(f"Transicion con estado desconocido: {q}->{q2}")
            if a not in self.alfabeto:
                raise ValueError(f"Simbolo fuera del alfabeto: {a}")

    # ---------- operaciones de pila ----------
    def push(self, x):
        self.pila.append(x)

    def pop(self):
        """Saca el tope. El simbolo de fondo nunca se saca (devuelve None)."""
        return self.pila.pop() if len(self.pila) > 1 else None

    def peek(self):
        return self.pila[-1]

    def esta_vacia(self):
        """Vacia = solo queda el simbolo de fondo."""
        return len(self.pila) == 1

    def elementos(self):
        """Contenido sin el fondo, del tope hacia abajo."""
        return list(reversed(self.pila[1:]))

    def __len__(self):
        return len(self.pila) - 1

    # ---------- funcion de transicion ----------
    def transitar(self, simbolo):
        """delta(estado, simbolo, tope) -> (nuevo_estado, simbolos a apilar).

        El primer simbolo de la lista queda en el tope de la pila.
        Devuelve False si no hay transicion (la cadena se rechaza).
        """
        clave = (self.estado, simbolo, self.peek())
        if clave not in self.delta:
            return False
        nuevo_estado, apilar = self.delta[clave]
        self.estado = nuevo_estado
        self.pila.pop()
        for s in reversed(apilar):
            self.pila.append(s)
        return True

    def reiniciar(self):
        self.estado = self.inicial
        self.pila = [self.simbolo_fondo]

    def procesar(self, entrada):
        """True si la cadena se acepta: termina en estado final y con la pila
        en su fondo. False si se rechaza."""
        self.reiniciar()
        for simbolo in entrada:
            if simbolo not in self.alfabeto or not self.transitar(simbolo):
                return False
        return self.estado in self.finales and self.esta_vacia()


# ---------- fabricas utiles ----------
def pila_simple():
    """Pila LIFO sin transiciones: sirve de inventario o historial."""
    return AutomataPila({"q0"}, set(), {}, "q0", finales={"q0"})


def apd_an_bn():
    """APD que acepta el lenguaje a^n b^n (n >= 0)."""
    delta = {
        ("q0", "a", "Z"): ("q0", ["A", "Z"]),
        ("q0", "a", "A"): ("q0", ["A", "A"]),
        ("q0", "b", "A"): ("q1", []),
        ("q1", "b", "A"): ("q1", []),
    }
    return AutomataPila({"q0", "q1"}, {"a", "b"}, delta, "q0",
                        finales={"q0", "q1"})


def apd_parentesis():
    """APD que acepta cadenas de parentesis balanceados."""
    delta = {
        ("q0", "(", "Z"): ("q0", ["P", "Z"]),
        ("q0", "(", "P"): ("q0", ["P", "P"]),
        ("q0", ")", "P"): ("q0", []),
    }
    return AutomataPila({"q0"}, {"(", ")"}, delta, "q0", finales={"q0"})


if __name__ == "__main__":
    apd = apd_an_bn()
    for cadena in ["", "ab", "aabb", "aaabbb", "aab", "abb", "ba", "abab"]:
        print(f"a^n b^n  {cadena!r:10} -> {'ACEPTA' if apd.procesar(cadena) else 'RECHAZA'}")
    par = apd_parentesis()
    for cadena in ["()", "(())()", "(()", "())"]:
        print(f"parentesis {cadena!r:10} -> {'ACEPTA' if par.procesar(cadena) else 'RECHAZA'}")

    p = pila_simple()
    p.push("espada"); p.push("pocion")
    print("Pila:", p.elementos(), "| pop:", p.pop(), "| tope:", p.peek())
