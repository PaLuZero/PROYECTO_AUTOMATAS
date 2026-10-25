import time
import random

class GestorPuzlesCiudad:
    def __init__(self):
        self.misiones = [
            {
                "id": "puzle_sidius",
                "nombre": "Pistón de Vapor de la Forja",
                "x": 3, "y": 4,
                "heroe_requerido": "Sidius Storm",
                "fase_requerida": False,  # Día/Normal
                "tipo": "TIMING_BARRA",
                "resuelta": False,
                "recompensa": "Fragmento de Acero Templado",
                "descripcion": "Sidius debe usar su fuerza y vínculo de Materia para calibrar el pistón."
            },
            {
                "id": "puzle_selene",
                "nombre": "Altar de Ecos Mnemónicos",
                "x": 15, "y": 3,
                "heroe_requerido": "Selene Moon",
                "fase_requerida": False,  # Día/Normal
                "tipo": "MEMORIA_RUNAS",
                "resuelta": False,
                "recompensa": "Gema de Recuerdo Antiguo",
                "descripcion": "Selene debe sintonizar la secuencia de runas resonantes en su orden exacto."
            },
            {
                "id": "puzle_noctis",
                "nombre": "Brecha de Posibilidades Fracturadas",
                "x": 12, "y": 9,
                "heroe_requerido": "Noctis Reverie",
                "fase_requerida": True,   # Crepúsculo
                "tipo": "REACCION_PARADOJA",
                "resuelta": False,
                "recompensa": "Cronocristal Inestable",
                "descripcion": "Noctis debe colapsar la brecha cuántica pulsando la frecuencia que coincide con la anomalía."
            },
            {
                "id": "puzle_athina",
                "nombre": "Faroles de Penumbra Sellados",
                "x": 5, "y": 11,
                "heroe_requerido": "Athina Nightwish",
                "fase_requerida": True,   # Crepúsculo
                "tipo": "FAROLES_INTERRUPTORES",
                "resuelta": False,
                "recompensa": "Pluma Umbría Bendecida",
                "descripcion": "Athina debe apagar los faroles enlazados para disipar la barrera oscura."
            }
        ]

    def verificar_acceso(self, mision, es_crepusculo, pareja_activa):
        if mision["resuelta"]:
            return False, "RESUELTA", "Esta anomalía ya ha sido estabilizada y reclamaste su recompensa."

        if mision["fase_requerida"] != es_crepusculo:
            req = "CREPÚSCULO" if mision["fase_requerida"] else "MUNDO NORMAL (Día)"
            return False, "FASE_INCORRECTA", f"Esta anomalía solo resuena durante el {req}."

        heroes_presentes = [h for h in pareja_activa if h]
        if mision["heroe_requerido"] not in heroes_presentes:
            return False, "HEROE_FALTANTE", f"Requiere la presencia de [{mision['heroe_requerido']}] en la vanguardia [F]."

        return True, "ACCESO_CONCEDIDO", "Sintonización establecida."

    def crear_estado_puzle(self, mision):
        tipo = mision["tipo"]

        if tipo == "TIMING_BARRA":
            return {
                "tipo": "TIMING_BARRA",
                "mision": mision,
                "pos_aguja": 0.0,
                "velocidad_aguja": 1.75,
                "direccion_aguja": 1,
                "zona_exito": (0.65, 0.85)
            }

        elif tipo == "MEMORIA_RUNAS":
            runas_posibles = ["1", "2", "3", "4"]
            secuencia = [random.choice(runas_posibles) for _ in range(4)]
            return {
                "tipo": "MEMORIA_RUNAS",
                "mision": mision,
                "secuencia": secuencia,
                "ingresado": [],
                "tiempo_inicio": time.time(),
                "tiempo_memorizar": 2.5
            }

        elif tipo == "REACCION_PARADOJA":
            frecuencias = [
                {"id": "1", "nombre": "Frecuencia Alfa", "simbolo": "▲ ALFA", "color": (80, 200, 255)},
                {"id": "2", "nombre": "Frecuencia Beta", "simbolo": "◆ BETA", "color": (230, 80, 255)},
                {"id": "3", "nombre": "Frecuencia Gamma", "simbolo": "● GAMMA", "color": (80, 255, 140)}
            ]
            objetivo = random.choice(frecuencias)

            return {
                "tipo": "REACCION_PARADOJA",
                "mision": mision,
                "tiempo_inicio": time.time(),
                "tiempo_limite": 3.0,
                "correcto": objetivo["id"],
                "simbolo_objetivo": objetivo["simbolo"],
                "color_objetivo": objetivo["color"],
                "frecuencias": frecuencias
            }

        elif tipo == "FAROLES_INTERRUPTORES":
            return {
                "tipo": "FAROLES_INTERRUPTORES",
                "mision": mision,
                "estados": [True, False, True]
            }

        return None