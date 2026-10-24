"""
Generador sintáctico en BNF con derivación sensible a la fase temporal.
"""
import random

class ParserGLC:
    def __init__(self):
        self.reglas_normal = {
            "<MISION>": [["<EMISOR>", "<VERBO>", "<OBJETO>", "<UBICACION>"]],
            "<EMISOR>": [["Un", "artesano", "preocupado"], ["El", "cronista", "del", "santuario"], ["Una", "guardia", "desesperada"]],
            "<VERBO>": [["solicita", "rescatar"], ["ruega", "localizar"], ["pide", "proteger"]],
            "<OBJETO>": [["un", "mineral", "de", "alta", "pureza"], ["un", "canto", "ancestral", "grabado"], ["las", "llaves", "de", "las", "catacumbas"]],
            "<UBICACION>": [["en", "los", "callejones", "del", "mercado."], ["en", "la", "frontera", "de", "las", "minas."], ["dentro", "del", "viejo", "acueducto."]]
        }
        self.reglas_crepusculo = {
            "<MISION>": [["<EMISOR>", "<VERBO>", "<OBJETO>", "<UBICACION>"]],
            "<EMISOR>": [["Un", "eco", "del", "pasado"], ["Una", "sombra", "distorsionada"], ["Un", "reflejo", "del", "espejo", "roto"]],
            "<VERBO>": [["exige", "sellar"], ["susurra", "purgar"], ["advierte", "evacuar"]],
            "<OBJETO>": [["la", "memoria", "corrupta"], ["el", "nexo", "de", "la", "paradoja"], ["el", "rastro", "de", "la", "entidad"]],
            "<UBICACION>": [["en", "la", "niebla", "de", "la", "grieta."], ["donde", "las", "paredes", "sangran", "sombras."], ["en", "el", "abismo", "sin", "retorno."]]
        }

    def derivar(self, simbolo, es_crepusculo):
        reglas = self.reglas_crepusculo if es_crepusculo else self.reglas_normal
        if simbolo not in reglas:
            return [simbolo]
        produccion = random.choice(reglas[simbolo])
        cadena = []
        for elem in produccion:
            cadena.extend(self.derivar(elem, es_crepusculo))
        return cadena

    def generar_mision(self, es_crepusculo):
        tokens = self.derivar("<MISION>", es_crepusculo)
        return " ".join(tokens)
