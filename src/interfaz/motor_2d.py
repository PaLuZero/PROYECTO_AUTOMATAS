import os
import sys
import time
import random
import json
import traceback
import pygame

RUTA_ACTUAL = os.path.dirname(os.path.abspath(__file__))
RUTA_SRC = os.path.abspath(os.path.join(RUTA_ACTUAL, ".."))
RUTA_RAIZ = os.path.abspath(os.path.join(RUTA_SRC, ".."))

if RUTA_SRC not in sys.path: sys.path.insert(0, RUTA_SRC)
if RUTA_ACTUAL not in sys.path: sys.path.insert(0, RUTA_ACTUAL)

from mundo.automata_pila import AutomataPilaMundo
from mundo.reloj_global import RelojMundo
from gramatica.glc_parser import ParserGLC
from narrativa.afn_motor import AFNNarrativo
from mundo.puzles_ciudad import GestorPuzlesCiudad
from mundo.dialogos_ciudad import ARBOLES_DIALOGO
from mundo.mapas_urbanos import MAPA_EXTERIOR_CIUDAD, INTERIOR_FORJA, INTERIOR_BIBLIOTECA, INTERIOR_BOTICA
from mundo.tienda_botica import CATALOGO_TIENDA, intentar_comprar
from mundo.tienda_armeria import CATALOGO_ARMERIA, intentar_comprar_armeria

from interfaz.animaciones_personaje import AnimadorPersonaje
from interfaz.render_edificios import GestorTilesetCiudad
from interfaz.render_menus import (
    dibujar_hud,
    dibujar_menu_mochila,
    dibujar_menu_tienda,
    dibujar_menu_formacion,
    dibujar_dialogo_overlay
)

try:
    from combate.sistema_batalla import BatallaTurnos
    from interfaz.render_combate import dibujar_overlay_batalla
except ModuleNotFoundError:
    try:
        from src.combate.sistema_batalla import BatallaTurnos
        from src.interfaz.render_combate import dibujar_overlay_batalla
    except ModuleNotFoundError:
        from sistema_batalla import BatallaTurnos
        from render_combate import dibujar_overlay_batalla

try:
    from interfaz.render_puzles import dibujar_overlay_puzle
except ModuleNotFoundError:
    from render_puzles import dibujar_overlay_puzle

ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TAMANO_TILE = 40
FPS = 60
VELOCIDAD_MOVIMIENTO_PIXELS = 4

COLOR_SUELO_NORMAL = (125, 175, 105)
COLOR_MURO_NORMAL = (90, 85, 95)
COLOR_PUERTA = (180, 110, 60)
COLOR_SALIDA = (220, 70, 70)
COLOR_PORTAL_REGIONES = (220, 180, 50)
COLOR_SANTUARIO = (100, 200, 240)

COLOR_SUELO_CREP = (45, 25, 60)
COLOR_MURO_CREP = (80, 20, 90)
COLOR_PORTAL_CREP = (180, 40, 220)

COLOR_HEROES_RESPALDO = {
    "Sidius Storm": (50, 120, 230),
    "Selene Moon": (210, 50, 70),
    "Noctis Reverie": (140, 60, 210),
    "Athina Nightwish": (40, 160, 110)
}

COLOR_NPC = (240, 200, 70)
COLOR_RECLUTABLE = (180, 100, 240)
COLOR_MISION_ACTIVA = (50, 220, 200)
COLOR_MISION_INACTIVA = (60, 80, 85)

COLOR_SUELO_BOTICA = (65, 45, 40)
COLOR_MOSTRADOR = (130, 80, 45)
COLOR_ESTANTERIA = (95, 60, 35)
COLOR_ALFOMBRA = (165, 40, 50)
COLOR_ALFOMBRA_BORDE = (225, 180, 60)
COLOR_CAMILLA = (220, 220, 230)
COLOR_CALDERO = (50, 50, 55)


class Juego2D:
    def __init__(self):
        try:
            pygame.mixer.pre_init(44100, -16, 2, 2048)
            pygame.mixer.init()
            pygame.mixer.music.set_volume(0.7)
            self.audio_disponible = True
            print("[AUDIO]: Mezclador de sonido iniciado con éxito.")
        except Exception as err:
            self.audio_disponible = False
            print(f"[AUDIO ERROR]: No se pudo inicializar mixer: {err}")

        pygame.init()
        pygame.font.init()
        self.pista_musical_actual = None

        self.pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
        pygame.display.set_caption("Hysteria: The Other Side - Ciudad Interactiva")
        self.reloj_fps = pygame.time.Clock()

        self.CATALOGO_TIENDA = CATALOGO_TIENDA
        self.CATALOGO_ARMERIA = CATALOGO_ARMERIA

        try:
            self.fuentes = {
                "texto": pygame.font.SysFont("Consolas", 15),
                "grande": pygame.font.SysFont("Consolas", 17, bold=True),
                "dialogo": pygame.font.SysFont("Consolas", 13),
                "puzle": pygame.font.SysFont("Consolas", 18, bold=True)
            }
        except Exception:
            f = pygame.font.Font(None, 18)
            self.fuentes = {"texto": f, "grande": f, "dialogo": f, "puzle": f}

        self.apd = AutomataPilaMundo()
        self.reloj = RelojMundo(duracion_fase=40)
        self.parser = ParserGLC()
        self.afn = AFNNarrativo()
        self.gestor_puzles = GestorPuzlesCiudad()

        self.mapa_actual = MAPA_EXTERIOR_CIUDAD
        self.zona_actual = "EXTERIOR_CIUDAD"
        self.pos_previa_exterior = (4, 5)

        # Líder
        self.jugador_x = 4
        self.jugador_y = 5
        self.pixel_x = float(self.jugador_x * TAMANO_TILE)
        self.pixel_y = float(self.jugador_y * TAMANO_TILE)
        self.destino_pixel_x = self.pixel_x
        self.destino_pixel_y = self.pixel_y
        self.en_movimiento = False
        self.direccion_mirada = "abajo"

        # Seguidor
        self.apoyo_x = 4
        self.apoyo_y = 6
        self.apoyo_pixel_x = float(self.apoyo_x * TAMANO_TILE)
        self.apoyo_pixel_y = float(self.apoyo_y * TAMANO_TILE)
        self.apoyo_destino_x = self.apoyo_pixel_x
        self.apoyo_destino_y = self.apoyo_pixel_y
        self.apoyo_en_movimiento = False
        self.apoyo_direccion = "abajo"

        self.animador_lider = AnimadorPersonaje(TAMANO_TILE)
        self.animador_apoyo = AnimadorPersonaje(TAMANO_TILE)
        self.gestor_edificios = GestorTilesetCiudad(TAMANO_TILE)

        self.stats_heroes = {
            "Sidius Storm": {
                "hp": 110, "max_hp": 110, "mp": 15, "max_mp": 15, "atk": 18, "def": 10, "atk_bono": 0,
                "nivel": 1, "exp": 0, "exp_sig": 50, "vinculo": "Materia",
                "equipo": {"arma": None, "armadura": None, "accesorio": None}
            },
            "Selene Moon": {
                "hp": 90, "max_hp": 90, "mp": 25, "max_mp": 25, "atk": 14, "def": 8, "atk_bono": 0,
                "nivel": 1, "exp": 0, "exp_sig": 50, "vinculo": "Memoria",
                "equipo": {"arma": None, "armadura": None, "accesorio": None}
            },
            "Noctis Reverie": {
                "hp": 95, "max_hp": 95, "mp": 20, "max_mp": 20, "atk": 16, "def": 9, "atk_bono": 0,
                "nivel": 1, "exp": 0, "exp_sig": 50, "vinculo": "Posibilidad",
                "equipo": {"arma": None, "armadura": None, "accesorio": None}
            },
            "Athina Nightwish": {
                "hp": 100, "max_hp": 100, "mp": 20, "max_mp": 20, "atk": 12, "def": 7, "atk_bono": 0,
                "nivel": 1, "exp": 0, "exp_sig": 50, "vinculo": "Sombra",
                "equipo": {"arma": None, "armadura": None, "accesorio": None}
            }
        }

        self.protagonista_inicial = "Sidius Storm"
        self.companeros_desbloqueados = [self.protagonista_inicial]
        self.pareja_activa = [self.protagonista_inicial, None]

        self.inventario_objetos = ["Poción Curativa", "Éter Místico", "Fragmento del Despertar"]
        self.monedas = 60

        self.puzle_activo = None
        self.conversacion_activa = None
        self.menu_formacion_activo = False
        self.menu_tienda_activo = False
        self.menu_mochila_activo = False
        self.indice_heroe_mochila = 0
        self.slot_formacion_seleccionando = 0
        self.indice_seleccion_fh = 0

        self.combate_activo = None
        self.enemigo_actual_objeto = None
        self.anim_timer_combate = 0

        # Estado del Jefe Final
        self.boss_invocado = False
        self.boss_derrotado = False
        self.boss_objeto = None
        self.estado_final_aceptado = None

        self.enemigos_crepusculares = [
            {"id": "sombra_1", "nombre": "Eco de Penumbra", "x": 6, "y": 6, "hp": 110, "max_hp": 110, "atk": 19, "oro": 35, "exp": 45, "derrotado": False, "es_grupo": False},
            {"id": "sombra_2", "nombre": "Espectro Fracturado", "x": 13, "y": 7, "hp": 150, "max_hp": 150, "atk": 25, "oro": 60, "exp": 75, "derrotado": False, "es_grupo": False},
            {
                "id": "sombra_duo",
                "nombre": "Vórtice Gemelo",
                "x": 10,
                "y": 8,
                "derrotado": False,
                "es_grupo": True,
                "oro": 80,
                "exp": 95,
                "enemigos": [
                    {"nombre": "Sombra Alfa", "hp": 85, "max_hp": 85, "atk": 16, "oro": 40, "exp": 45},
                    {"nombre": "Sombra Beta", "hp": 85, "max_hp": 85, "atk": 16, "oro": 40, "exp": 45}
                ]
            }
        ]
        self.ultimo_mov_enemigos = time.time()
        self.intervalo_mov_enemigos = 0.85

        carpetas_buscar = [
            os.path.join(RUTA_RAIZ, "assets", "sprites"),
            os.path.join(RUTA_RAIZ, "assets", "portraits"),
            os.path.join(RUTA_RAIZ, "assets"),
            RUTA_RAIZ,
            RUTA_ACTUAL
        ]

        def cargar_imagen_standee(nombres):
            for c in carpetas_buscar:
                for nom in nombres:
                    ruta = os.path.join(c, nom)
                    if os.path.exists(ruta):
                        try:
                            return pygame.image.load(ruta).convert_alpha()
                        except Exception:
                            pass
            return None

        def cargar_chibi(nombres):
            for c in carpetas_buscar:
                for nom in nombres:
                    for variante in [nom, nom.lower(), nom.capitalize()]:
                        ruta = os.path.join(c, variante)
                        if os.path.exists(ruta):
                            try:
                                img = pygame.image.load(ruta).convert_alpha()
                                return pygame.transform.scale(img, (TAMANO_TILE, TAMANO_TILE))
                            except Exception:
                                pass
            return None

        def cargar_fondo_habitacion(nombres):
            for carpeta in carpetas_buscar:
                for nom in nombres:
                    ruta = os.path.join(carpeta, nom)
                    if os.path.exists(ruta):
                        try:
                            img = pygame.image.load(ruta).convert()
                            return pygame.transform.scale(img, (ANCHO_VENTANA, ALTO_VENTANA))
                        except Exception:
                            pass
            return None

        self.fondo_botica = cargar_fondo_habitacion(["casa_vaelira.png", "botica_interior.png", "tileset_botica.png"])
        self.fondo_forja = cargar_fondo_habitacion(["herrería.png", "herreria.png", "forja_carlos.png", "forja.png", "tileset_forja.png"])

        self.retratos_heroes = {
            "Sidius Storm": cargar_imagen_standee(["sidius.png", "sidius_portrait.png"]),
            "Selene Moon": cargar_imagen_standee(["selene.png", "selene_portrait.png"]),
            "Noctis Reverie": cargar_imagen_standee(["noctis.png", "noctis_portrait.png"]),
            "Athina Nightwish": cargar_imagen_standee(["atina.png", "athina.png", "athina_portrait.png"])
        }

        def cargar_retrato_dialogo(nombres):
            for c in carpetas_buscar:
                for nom in nombres:
                    ruta = os.path.join(c, nom)
                    if os.path.exists(ruta):
                        try:
                            img = pygame.image.load(ruta).convert_alpha()
                            img.set_colorkey((0, 0, 0))
                            return img
                        except Exception:
                            pass
            return None

        # Retratos
        self.retrato_vaelira_normal = cargar_retrato_dialogo(["vaelira_portrait.png", "vaelira.png", "Valeria.jpg"])
        self.retrato_vaelira_crep = cargar_retrato_dialogo(["vaelira_crepuscular.png", "vaelira_crep.png", "vaelira_crep.jpg"])

        self.retrato_carlos_normal = cargar_retrato_dialogo(["carlos.png", "carlos_portrait.png"])
        self.retrato_carlos_crep = cargar_retrato_dialogo(["carlos_crepuscular.png", "carlos_crep.png", "carlos_crep.jpg"])
        self.retrato_carlos = self.retrato_carlos_normal

        self.chibi_vaelira_normal = cargar_chibi(["vaelira_chibi.png", "chibi_vaelira.png", "vaelira.png"])
        self.chibi_vaelira_crep = cargar_chibi(["vaelira_chibic.png", "vaelira_chibi_crep.png", "vaelira_crepuscular.png"])

        self.chibi_carlos_normal = cargar_chibi(["carlos_chibi.png", "chibi_carlos.png", "carlos.png"])
        self.chibi_carlos_crep = cargar_chibi(["carlos_chibi_crepuscular.png", "carlos_chibi_crep.png", "chibi_carlos_crepuscular.png"])
        self.chibi_carlos = self.chibi_carlos_normal

        for anim in [self.animador_lider, self.animador_apoyo]:
            anim.cargar_heroe("Sidius Storm", ["sidius_walk.png", "sidius_walk.jpg"], carpetas_buscar)
            anim.cargar_heroe("Selene Moon", ["selene_walk.png", "selene_walk.jpg"], carpetas_buscar)
            anim.cargar_heroe("Noctis Reverie", ["noctis_walk.png", "noctis_walk.jpg"], carpetas_buscar)
            anim.cargar_heroe("Athina Nightwish", ["athina_walk.png", "atina_walk.png"], carpetas_buscar)

        self.gestor_edificios.cargar(carpetas_buscar)

        self.sprites_npcs_normal = {}
        self.sprites_npcs_crep = {}

        def cargar_sheet(nombre):
            for c in carpetas_buscar:
                ruta = os.path.join(c, nombre)
                if os.path.exists(ruta):
                    try:
                        return pygame.image.load(ruta).convert_alpha()
                    except Exception:
                        pass
            return None

        sheet_norm = cargar_sheet("npc_normal.png")
        sheet_crep = cargar_sheet("npc_crepuscular.png")

        grid_npcs = [
            [("Alquimista_Eldrin", 0, 0), ("Tabernera_Marta", 1, 0), ("Viajero_Cael", 2, 0)],
            [("Aprendiz_Toby", 0, 1), ("Guardia_Vane", 1, 1), ("Nina_Lina", 2, 1)]
        ]

        for fila in grid_npcs:
            for id_npc, col_idx, fila_idx in fila:
                if sheet_norm:
                    w_sub = sheet_norm.get_width() // 3
                    h_sub = sheet_norm.get_height() // 2
                    rec = pygame.Rect(col_idx * w_sub, fila_idx * h_sub, w_sub, h_sub)
                    sub_img = sheet_norm.subsurface(rec)
                    self.sprites_npcs_normal[id_npc] = pygame.transform.scale(sub_img, (TAMANO_TILE, TAMANO_TILE))
                if sheet_crep:
                    w_sub = sheet_crep.get_width() // 3
                    h_sub = sheet_crep.get_height() // 2
                    rec = pygame.Rect(col_idx * w_sub, fila_idx * h_sub, w_sub, h_sub)
                    sub_img = sheet_crep.subsurface(rec)
                    self.sprites_npcs_crep[id_npc] = pygame.transform.scale(sub_img, (TAMANO_TILE, TAMANO_TILE))

        self.dialogo_linea1 = "Ciudad del Santuario. Pulsa [M] Mochila, [F] Estado/Grupo, [T] Tiendas."
        self.dialogo_linea2 = "WASD: Mover | [E/Espacio] Interactuar | [R] Rumor GLC | [G] Save-State"

        self.npcs_exterior = [
            {"id": "Alquimista_Eldrin", "nombre": "Eldrin el Alquimista", "x": 16, "y": 10},
            {"id": "Tabernera_Marta", "nombre": "Marta la Tabernera", "x": 11, "y": 6},
            {"id": "Viajero_Cael", "nombre": "Cael el Errante", "x": 10, "y": 11},
            {"id": "Aprendiz_Toby", "nombre": "Aprendiz Toby", "x": 4, "y": 7},
            {"id": "Guardia_Vane", "nombre": "Guardia Vane", "x": 7, "y": 1},
            {"id": "Nina_Lina", "nombre": "Pequeña Lina", "x": 17, "y": 4}
        ]

        self.portadores_en_mapa = [
            {"nombre": "Selene Moon", "vinculo": "Memoria", "x": 14, "y": 4, "reclutado": False, "dialogo": "Selene Moon: 'El reloj late fuera de fase. Mis artes de Memoria están a tu disposición para estabilizar el reino.'" },
            {"nombre": "Noctis Reverie", "vinculo": "Posibilidad", "x": 4, "y": 10, "reclutado": False, "dialogo": "Noctis Reverie: 'Cualquier línea temporal puede ser alterada si actuamos juntos. Te sigo los pasos.'" },
            {"nombre": "Athina Nightwish", "vinculo": "Sombra", "x": 17, "y": 2, "reclutado": False, "dialogo": "Athina Nightwish: 'Mi arco y mis destrezas curativas protegerán la vanguardia. Vamos a restaurar la paz.'" }
        ]

        self.npcs_interior_forja = [{"id_arbol": "Herrero_Doran", "x": 15, "y": 8}]
        self.npcs_interior_biblioteca = [{"id_arbol": "Cronista_Elowen", "x": 9, "y": 3}]
        self.npcs_interior_botica = [{"id_arbol": "Vaelira_Contriel", "x": 9, "y": 7}]

    # GESTOR DE AUDIO CON DIAGNÓSTICO EN CONSOLA
    def reproducir_musica(self, nombre_base, bucle=-1):
        if not getattr(self, "audio_disponible", False):
            return

        if self.pista_musical_actual == nombre_base:
            return

        extensiones = [".mp3", ".ogg", ".wav"]
        carpetas_audio = [
            os.path.join(RUTA_RAIZ, "assets", "audio"),
            os.path.join(RUTA_RAIZ, "assets"),
            RUTA_ACTUAL,
            os.path.join(RUTA_SRC, "assets", "audio"),
            os.getcwd()
        ]

        ruta_encontrada = None
        for carpeta in carpetas_audio:
            for ext in extensiones:
                candidato = os.path.join(carpeta, f"{nombre_base}{ext}")
                if os.path.exists(candidato):
                    ruta_encontrada = candidato
                    break
            if ruta_encontrada:
                break

        if ruta_encontrada:
            try:
                print(f"[AUDIO]: Cargando y reproduciendo: {ruta_encontrada}")
                pygame.mixer.music.load(ruta_encontrada)
                pygame.mixer.music.play(loops=bucle)
                self.pista_musical_actual = nombre_base
            except Exception as e:
                print(f"[AUDIO ERROR]: Falló la reproducción de {ruta_encontrada}: {e}")
        else:
            print(f"[AUDIO AVISO]: No se encontró el archivo para '{nombre_base}' (Buscado en: {carpetas_audio[0]})")

    def actualizar_musica_segun_estado(self):
        if not getattr(self, "audio_disponible", False):
            return

        # 1. Combate contra el Boss (Devorador del Cronos)
        if self.combate_activo and self.enemigo_actual_objeto and self.enemigo_actual_objeto.get("id") == "boss_cronos":
            self.reproducir_musica("boss")
        # 2. Combate regular contra Sombras
        elif self.combate_activo:
            self.reproducir_musica("combate")
        # 3. Exploración de la ciudad (Mundo Normal y Crepúsculo)
        else:
            self.reproducir_musica("ciudad")

    # MOVIMIENTO
    def actualizar_movimiento_suave(self):
        if self.en_movimiento:
            movido = False
            if abs(self.pixel_x - self.destino_pixel_x) > VELOCIDAD_MOVIMIENTO_PIXELS:
                self.pixel_x += VELOCIDAD_MOVIMIENTO_PIXELS if self.destino_pixel_x > self.pixel_x else -VELOCIDAD_MOVIMIENTO_PIXELS
                movido = True
            else:
                self.pixel_x = self.destino_pixel_x

            if abs(self.pixel_y - self.destino_pixel_y) > VELOCIDAD_MOVIMIENTO_PIXELS:
                self.pixel_y += VELOCIDAD_MOVIMIENTO_PIXELS if self.destino_pixel_y > self.pixel_y else -VELOCIDAD_MOVIMIENTO_PIXELS
                movido = True
            else:
                self.pixel_y = self.destino_pixel_y

            if not movido and self.pixel_x == self.destino_pixel_x and self.pixel_y == self.destino_pixel_y:
                self.en_movimiento = False

        self.animador_lider.actualizar(self.en_movimiento, self.direccion_mirada)

        if self.apoyo_en_movimiento:
            movido_apoyo = False
            if abs(self.apoyo_pixel_x - self.apoyo_destino_x) > VELOCIDAD_MOVIMIENTO_PIXELS:
                self.apoyo_pixel_x += VELOCIDAD_MOVIMIENTO_PIXELS if self.apoyo_destino_x > self.apoyo_pixel_x else -VELOCIDAD_MOVIMIENTO_PIXELS
                movido_apoyo = True
            else:
                self.apoyo_pixel_x = self.apoyo_destino_x

            if abs(self.apoyo_pixel_y - self.apoyo_destino_y) > VELOCIDAD_MOVIMIENTO_PIXELS:
                self.apoyo_pixel_y += VELOCIDAD_MOVIMIENTO_PIXELS if self.apoyo_destino_y > self.apoyo_pixel_y else -VELOCIDAD_MOVIMIENTO_PIXELS
                movido_apoyo = True
            else:
                self.apoyo_pixel_y = self.apoyo_destino_y

            if not movido_apoyo and self.apoyo_pixel_x == self.apoyo_destino_x and self.apoyo_pixel_y == self.apoyo_destino_y:
                self.apoyo_en_movimiento = False

        self.animador_apoyo.actualizar(self.apoyo_en_movimiento, self.apoyo_direccion)

    def sincronizar_posicion_instantanea(self, x, y, direccion="abajo"):
        self.jugador_x = x
        self.jugador_y = y
        self.pixel_x = float(x * TAMANO_TILE)
        self.pixel_y = float(y * TAMANO_TILE)
        self.destino_pixel_x = self.pixel_x
        self.destino_pixel_y = self.pixel_y
        self.en_movimiento = False
        self.direccion_mirada = direccion

        if direccion == "arriba":
            self.apoyo_x = x
            self.apoyo_y = y + 1
        elif direccion == "abajo":
            self.apoyo_x = x
            self.apoyo_y = y - 1
        else:
            self.apoyo_x = x - 1 if direccion == "derecha" else x + 1
            self.apoyo_y = y

        self.apoyo_pixel_x = float(self.apoyo_x * TAMANO_TILE)
        self.apoyo_pixel_y = float(self.apoyo_y * TAMANO_TILE)
        self.apoyo_destino_x = self.apoyo_pixel_x
        self.apoyo_destino_y = self.apoyo_pixel_y
        self.apoyo_en_movimiento = False
        self.apoyo_direccion = direccion

    def intentar_mover(self, dx, dy):
        if self.en_movimiento:
            return
        if self.puzle_activo or self.conversacion_activa or self.menu_formacion_activo or self.menu_tienda_activo or self.menu_mochila_activo or self.combate_activo or self.estado_final_aceptado:
            return

        if dy > 0: self.direccion_mirada = "abajo"
        elif dy < 0: self.direccion_mirada = "arriba"
        elif dx > 0: self.direccion_mirada = "derecha"
        elif dx < 0: self.direccion_mirada = "izquierda"

        nuevo_x = self.jugador_x + dx
        nuevo_y = self.jugador_y + dy

        st = self.reloj.obtener_estado()
        es_crep = st["es_crepusculo"]

        if es_crep and self.zona_actual == "EXTERIOR_CIUDAD":
            for e in self.enemigos_crepusculares:
                if not e["derrotado"] and e["x"] == nuevo_x and e["y"] == nuevo_y:
                    self.iniciar_combate_con(e)
                    return

        # Colisión con el Boss si está en el mapa
        if self.boss_objeto and not self.boss_objeto["derrotado"] and self.boss_objeto["x"] == nuevo_x and self.boss_objeto["y"] == nuevo_y:
            self.iniciar_combate_con(self.boss_objeto)
            return

        if 0 <= nuevo_y < len(self.mapa_actual) and 0 <= nuevo_x < len(self.mapa_actual[0]):
            tile_destino = self.mapa_actual[nuevo_y][nuevo_x]

            if tile_destino == 4:
                self.pos_previa_exterior = (self.jugador_x, self.jugador_y + 1 if dy <= 0 else self.jugador_y - 1)
                self.apd.transicion_delta("PUSH", "Interior: Forja de Carlos")
                self.mapa_actual = INTERIOR_FORJA
                self.zona_actual = "FORJA"
                self.sincronizar_posicion_instantanea(9, 12, direccion="arriba")
                self.dialogo_linea1 = "Entraste a la Forja de Carlos. Habla con Carlos a la derecha [E] o presiona [T]."
                return
            elif tile_destino == 5:
                self.pos_previa_exterior = (self.jugador_x, self.jugador_y + 1)
                self.apd.transicion_delta("PUSH", "Interior: Biblioteca de Elowen")
                self.mapa_actual = INTERIOR_BIBLIOTECA
                self.zona_actual = "BIBLIOTECA"
                self.sincronizar_posicion_instantanea(9, 9, direccion="arriba")
                self.dialogo_linea1 = "Entraste a la Biblioteca de Elowen. Acércate a los estantes [E]."
                return
            elif tile_destino == 6:
                self.pos_previa_exterior = (self.jugador_x, self.jugador_y + 1)
                self.apd.transicion_delta("PUSH", "Interior: Botica de Vaelira Contriel")
                self.mapa_actual = INTERIOR_BOTICA
                self.zona_actual = "BOTICA"
                self.sincronizar_posicion_instantanea(9, 12, direccion="arriba")
                self.dialogo_linea1 = "Entraste a la Botica. Habla con Vaelira en la alfombra [E] o presiona [T]."
                return
            elif tile_destino == 9:
                self.apd.transicion_delta("POP")
                self.mapa_actual = MAPA_EXTERIOR_CIUDAD
                self.zona_actual = "EXTERIOR_CIUDAD"
                self.sincronizar_posicion_instantanea(self.pos_previa_exterior[0], self.pos_previa_exterior[1], direccion="abajo")
                self.dialogo_linea1 = "Regresas a las calles de la Ciudad del Santuario."
                return

            if tile_destino not in [1, 7, 8, 10, 11]:
                if self.pareja_activa[1] is not None:
                    dx_apoyo = self.jugador_x - self.apoyo_x
                    dy_apoyo = self.jugador_y - self.apoyo_y
                    if abs(dx_apoyo) > abs(dy_apoyo):
                        self.apoyo_direccion = "derecha" if dx_apoyo > 0 else "izquierda"
                    elif dy_apoyo != 0:
                        self.apoyo_direccion = "abajo" if dy_apoyo > 0 else "arriba"

                    self.apoyo_x = self.jugador_x
                    self.apoyo_y = self.jugador_y
                    self.apoyo_destino_x = float(self.jugador_x * TAMANO_TILE)
                    self.apoyo_destino_y = float(self.jugador_y * TAMANO_TILE)
                    self.apoyo_en_movimiento = True

                self.jugador_x = nuevo_x
                self.jugador_y = nuevo_y
                self.destino_pixel_x = float(nuevo_x * TAMANO_TILE)
                self.destino_pixel_y = float(nuevo_y * TAMANO_TILE)
                self.en_movimiento = True

                mutacion, st_reloj = self.reloj.avanzar(1)
                if mutacion:
                    es_ahora_crep = st_reloj["es_crepusculo"]
                    rumor_glc = self.parser.generar_mision(es_ahora_crep)
                    self.dialogo_linea1 = f"¡MUTACIÓN TEMPORAL! Rumor: \"{rumor_glc}\""
                    print(f"\n[MUTACIÓN RELOJ - DERIVACIÓN GLC BNF]: {rumor_glc}")

                    if not es_ahora_crep:
                        for e in self.enemigos_crepusculares:
                            e["derrotado"] = False
                            if e.get("es_grupo"):
                                for sub_e in e["enemigos"]:
                                    sub_e["hp"] = sub_e["max_hp"]
                            else:
                                e["hp"] = e["max_hp"]

    # SISTEMA FORMAL: VOLCADO DE SAVE-STATE (DEFENSA DOCENTE)
    def trazar_save_state_formal(self):
        st_reloj = self.reloj.obtener_estado()
        misiones_resueltas = [m["id"] for m in self.gestor_puzles.misiones if m["resuelta"]]
        
        estado_afn_actual = "q_exploracion_exterior"
        if self.zona_actual != "EXTERIOR_CIUDAD":
            estado_afn_actual = f"q_interior_{self.zona_actual.lower()}"
        if self.combate_activo:
            estado_afn_actual = "q_combate_activo"
        if self.boss_invocado and not self.boss_derrotado:
            estado_afn_actual = "q_enfrentamiento_boss_final"

        traza = {
            "ESTADO_AFN_ACTUAL": estado_afn_actual,
            "PILA_APD_ZONAS (LIFO)": getattr(self.apd, "pila", [self.zona_actual]),
            "TOPE_PILA_APD": getattr(self.apd, "pila", [self.zona_actual])[-1],
            "FASE_RELOJ": st_reloj["nombre"],
            "ES_CREPUSCULO": st_reloj["es_crepusculo"],
            "VANGUARDIA": self.pareja_activa,
            "MISIONES_COMPLETADAS": len(misiones_resueltas),
            "LISTA_MISIONES": misiones_resueltas,
            "INVENTARIO": self.inventario_objetos,
            "TRANSICIONES_DISPONIBLES": [
                "delta(q, MOVER) -> q_exploracion",
                "delta(q, INTERACTUAR_FUENTE) -> q_invocar_boss",
                "delta(q, DERIVAR_GLC) -> Cadena_Sintactica_BNF",
                "delta(q, COMBATE_VICTORIA) -> q_level_up",
                "delta(q, ENTRAR_PUERTA) -> PUSH(Zona)",
                "delta(q, SALIR_TAPETE) -> POP(Zona)"
            ]
        }

        print("\n" + "=" * 65)
        print(" [TRAZA FORMAL DE SAVE-STATE - HYSTERIA: THE OTHER SIDE]")
        print("=" * 65)
        print(json.dumps(traza, indent=4, ensure_ascii=False))
        print("=" * 65 + "\n")
        self.dialogo_linea1 = "[SAVE-STATE]: Traza formal volcada con éxito a la consola."

    # COMBATE Y GESTIÓN DE EXP
    def iniciar_combate_con(self, enemigo):
        st = self.reloj.obtener_estado()
        es_crep = st["es_crepusculo"]

        heroes_reales = [h for h in self.pareja_activa if h]

        self.combate_activo = BatallaTurnos(heroes_reales, self.stats_heroes, enemigo, self.inventario_objetos)
        self.combate_activo.pareja_activa = heroes_reales
        self.combate_activo.stats_party = self.stats_heroes
        self.combate_activo.enemigo = enemigo
        self.combate_activo.enemigo_info = enemigo
        self.combate_activo.animador = self.animador_lider
        self.combate_activo.es_crepusculo = es_crep

        self.enemigo_actual_objeto = enemigo
        nombre_e = enemigo.get("nombre", "Enemigo") if isinstance(enemigo, dict) else getattr(enemigo, "nombre", "Enemigo")
        self.dialogo_linea1 = f"¡Combate iniciado contra {nombre_e}!"

    def procesar_victoria_combate(self, exp_ganada, oro_ganado):
        self.monedas += oro_ganado
        mensajes_subida = []

        heroes_activos = [h for h in self.pareja_activa if h]
        for heroe in heroes_activos:
            st = self.stats_heroes[heroe]
            if st["hp"] > 0:
                st["exp"] += exp_ganada

                subio = False
                while st["exp"] >= st.get("exp_sig", 50):
                    st["exp"] -= st["exp_sig"]
                    st["nivel"] += 1
                    st["exp_sig"] = int(st["exp_sig"] * 1.5)
                    st["max_hp"] += 15
                    st["hp"] = st["max_hp"]
                    st["max_mp"] += 5
                    st["mp"] = st["max_mp"]
                    st["atk"] += 3
                    st["def"] += 2
                    subio = True

                if subio:
                    mensajes_subida.append(f"¡{heroe} subió al Nivel {st['nivel']}!")

        # Si el enemigo derrotado era el Jefe Final, determinar el Estado de Aceptación
        if self.enemigo_actual_objeto and self.enemigo_actual_objeto.get("id") == "boss_cronos":
            self.boss_derrotado = True
            self.determinar_estado_de_aceptacion_final()
            return

        if mensajes_subida:
            self.dialogo_linea1 = f"¡Victoria! +{oro_ganado} monedas, +{exp_ganada} EXP. " + " ".join(mensajes_subida)
        else:
            self.dialogo_linea1 = f"¡Victoria! Ganaron {oro_ganado} monedas y {exp_ganada} EXP."

    def determinar_estado_de_aceptacion_final(self):
        """Evalúa las misiones resueltas y activa el desenlace narrativo correspondiente."""
        resueltas = sum(1 for m in self.gestor_puzles.misiones if m["resuelta"])

        if resueltas <= 1:
            self.estado_final_aceptado = {
                "titulo": "FINAL: EL COLAPSO DEL SANTUARIO",
                "color": (230, 60, 70),
                "misiones": resueltas,
                "texto_linea1": "Solo recuperaron fragmentos insuficientes del poder de los Vínculos.",
                "texto_linea2": "Aunque la bestia cayó, la grieta colapsó la ciudad entera en el vacío temporal.",
                "texto_linea3": "El reloj global se detuvo en cero. El Santuario ha desaparecido de la historia."
            }
        elif resueltas in [2, 3]:
            self.estado_final_aceptado = {
                "titulo": "FINAL: LA TREGUA INCIERTA",
                "color": (240, 200, 80),
                "misiones": resueltas,
                "texto_linea1": "Con la mitad de los catalizadores, lograron sellar al Devorador del Cronos.",
                "texto_linea2": "La ciudad sobrevive hoy, pero las fisuras volverán a abrirse con el próximo ciclo.",
                "texto_linea3": "Los portadores montan guardia eterna ante un Crepúsculo que jamás dormirá."
            }
        else:
            self.estado_final_aceptado = {
                "titulo": "FINAL: LA RESTAURACIÓN DE LA REALIDAD",
                "color": (100, 230, 140),
                "misiones": resueltas,
                "texto_linea1": "¡Los 4 Vínculos (Materia, Memoria, Posibilidad y Sombra) resonaron al unísono!",
                "texto_linea2": "La entidad del vacío fue purificada y la barrera del Santuario brilla con luz plena.",
                "texto_linea3": "El reloj sincroniza su compás perfecto. La fractura dimensional ha sido sellada."
            }

    def actualizar_animaciones_combate(self):
        if not self.combate_activo:
            return

        bat = self.combate_activo
        t_actual = pygame.time.get_ticks()

        if bat.anim_heroe_atacando:
            delta = t_actual - getattr(self, "anim_timer_combate", t_actual)

            if bat.anim_fase == 0 and delta > 160:
                bat.anim_fase = 1
                bat.anim_recibiendo_dano = True
                self.anim_timer_combate = t_actual

            elif bat.anim_fase == 1 and delta > 240:
                bat.anim_fase = 2
                bat.anim_recibiendo_dano = False
                self.anim_timer_combate = t_actual

            elif bat.anim_fase == 2 and delta > 140:
                bat.anim_heroe_atacando = None
                bat.anim_fase = 0

    def sincronizar_vida_enemigo_tras_accion(self):
        if not self.combate_activo:
            return

        b = self.combate_activo
        hp_vivo = getattr(b, "hp_enemigo", getattr(b, "hp_actual_enemigo", None))

        if hp_vivo is not None and self.enemigo_actual_objeto and isinstance(self.enemigo_actual_objeto, dict):
            self.enemigo_actual_objeto["hp"] = hp_vivo
            if "enemigo" in b.__dict__ and isinstance(b.enemigo, dict):
                b.enemigo["hp"] = hp_vivo
            if "enemigo_info" in b.__dict__ and isinstance(b.enemigo_info, dict):
                b.enemigo_info["hp"] = hp_vivo

    def actualizar_movimiento_enemigos(self):
        if self.zona_actual != "EXTERIOR_CIUDAD":
            return
        if self.combate_activo or self.conversacion_activa or self.puzle_activo or self.menu_formacion_activo or self.menu_tienda_activo or self.menu_mochila_activo or self.estado_final_aceptado:
            return

        st = self.reloj.obtener_estado()
        if not st["es_crepusculo"]:
            return

        ahora = time.time()
        if ahora - self.ultimo_mov_enemigos < self.intervalo_mov_enemigos:
            return

        self.ultimo_mov_enemigos = ahora
        direcciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        for e in self.enemigos_crepusculares:
            if e["derrotado"]:
                continue

            random.shuffle(direcciones)
            for dx, dy in direcciones:
                nx = e["x"] + dx
                ny = e["y"] + dy

                if (nx == self.jugador_x and ny == self.jugador_y) or (nx == self.apoyo_x and ny == self.apoyo_y):
                    self.iniciar_combate_con(e)
                    return

                if 0 <= ny < len(self.mapa_actual) and 0 <= nx < len(self.mapa_actual[0]):
                    tile = self.mapa_actual[ny][nx]
                    if tile in [0, 3, 13]:
                        otro_enemigo = any(
                            o != e and not o["derrotado"] and o["x"] == nx and o["y"] == ny
                            for o in self.enemigos_crepusculares
                        )
                        if not otro_enemigo:
                            e["x"] = nx
                            e["y"] = ny
                            break

    def curar_todo_el_equipo(self):
        for h in self.stats_heroes:
            self.stats_heroes[h]["hp"] = self.stats_heroes[h]["max_hp"]
            self.stats_heroes[h]["mp"] = self.stats_heroes[h]["max_mp"]

    def dejar_equipo_en_uno_hp(self):
        for h in self.stats_heroes:
            self.stats_heroes[h]["hp"] = 1

    # GESTIÓN DE EQUIPAMIENTO
    def equipar_objeto_a_heroe(self, nombre_heroe, nombre_item):
        item_info = next((it for it in CATALOGO_ARMERIA if it["nombre"] == nombre_item), None)
        if not item_info or nombre_item not in self.inventario_objetos:
            return False, "Objeto no válido para equipar."

        st = self.stats_heroes[nombre_heroe]
        ranura = item_info.get("ranura", "arma")
        bono = item_info.get("bono", 0)

        if st["equipo"].get(ranura) is not None:
            self.desequipar_objeto_de_heroe(nombre_heroe, ranura)

        self.inventario_objetos.remove(nombre_item)
        st["equipo"][ranura] = nombre_item

        if ranura == "arma":
            st["atk_bono"] = bono
        elif ranura == "armadura":
            st["max_hp"] += bono
            st["hp"] += bono
        elif ranura == "accesorio":
            st["max_mp"] += bono
            st["mp"] += bono

        return True, f"¡{nombre_heroe} se equipó [{nombre_item}]!"

    def desequipar_objeto_de_heroe(self, nombre_heroe, ranura):
        st = self.stats_heroes[nombre_heroe]
        item_previo = st["equipo"].get(ranura)
        if not item_previo:
            return

        item_info = next((it for it in CATALOGO_ARMERIA if it["nombre"] == item_previo), None)
        if item_info:
            bono = item_info.get("bono", 0)
            if ranura == "arma":
                st["atk_bono"] = 0
            elif ranura == "armadura":
                st["max_hp"] -= bono
                st["hp"] = min(st["hp"], st["max_hp"])
            elif ranura == "accesorio":
                st["max_mp"] -= bono
                st["mp"] = min(st["mp"], st["max_mp"])

        st["equipo"][ranura] = None
        self.inventario_objetos.append(item_previo)

    # INVOCACIÓN DEL BOSS EN LA FUENTE CENTRAL
    def abrir_menu_invocar_boss(self):
        misiones_hechas = sum(1 for m in self.gestor_puzles.misiones if m["resuelta"])
        self.conversacion_activa = {
            "id": "altar_fuente_boss",
            "nombre": "Fuente del Santuario",
            "saludo": f"El agua de la fuente refleja la anomalía del reloj. Misiones activas resueltas: {misiones_hechas}/4. ¿Deseas canalizar el sello para invocar al Devorador del Cronos?",
            "opciones": [
                {
                    "texto": "[1] SÍ: ¡Canalizar la energía y enfrentar a la Entidad!",
                    "heroe_requerido": None,
                    "disponible": True,
                    "es_invocar_boss": True,
                    "respuesta": "¡Un estruendo sacude la plaza! El Devorador del Cronos desciende sobre la fuente."
                },
                {
                    "texto": "[2] NO: Aún necesitamos prepararnos e investigar la ciudad.",
                    "heroe_requerido": None,
                    "disponible": True,
                    "es_invocar_boss": False,
                    "respuesta": "Decides retroceder. El sello continúa aguardando el momento propicio."
                }
            ],
            "respuesta_elegida": None
        }

    def ejecutar_invocacion_boss(self):
        self.boss_invocado = True
        misiones_hechas = sum(1 for m in self.gestor_puzles.misiones if m["resuelta"])

        hp_boss = max(180, 300 - (misiones_hechas * 30))
        atk_boss = max(18, 28 - (misiones_hechas * 2))

        self.boss_objeto = {
            "id": "boss_cronos",
            "nombre": "Devorador del Cronos",
            "x": 9,
            "y": 7,
            "hp": hp_boss,
            "max_hp": hp_boss,
            "atk": atk_boss,
            "oro": 150,
            "exp": 200,
            "derrotado": False,
            "es_grupo": False
        }

        self.iniciar_combate_con(self.boss_objeto)

    # ENTRADAS DE TECLADO
    def procesar_input_combate(self, tecla):
        b = self.combate_activo
        if not b: 
            return

        if b.fase_combate == "TERMINADO":
            if tecla in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_e]:
                if b.resultado == "VICTORIA":
                    oro_ganado = b.recompensas.get("oro", 0)
                    exp_ganada = b.recompensas.get("exp", 0)
                    if self.enemigo_actual_objeto:
                        self.enemigo_actual_objeto["derrotado"] = True
                    self.procesar_victoria_combate(exp_ganada, oro_ganado)
                elif b.resultado == "DERROTA":
                    self.dejar_equipo_en_uno_hp()
                    self.sincronizar_posicion_instantanea(4, 5, direccion="abajo")
                    self.dialogo_linea1 = "El grupo cayó ante las sombras. Despiertan heridos en la plaza con 1 HP."
                elif b.resultado == "HUIDA":
                    self.dialogo_linea1 = "Lograron romper el cerco y huir a un lugar seguro."

                self.combate_activo = None
                self.enemigo_actual_objeto = None
            return

        if getattr(b, "fase_combate", "") == "RESOLUCION":
            if tecla in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_e]:
                b.avanzar_evento_siguiente()
                self.sincronizar_vida_enemigo_tras_accion()
                self.anim_timer_combate = pygame.time.get_ticks()
            return

        if b.modo_menu == "PRINCIPAL":
            if tecla == pygame.K_1:
                b.ejecutar_ataque_basico()
                self.sincronizar_vida_enemigo_tras_accion()

            elif tecla == pygame.K_2:
                b.ejecutar_habilidad_vinculo()
                self.sincronizar_vida_enemigo_tras_accion()

            elif tecla == pygame.K_3:
                b.ejecutar_guardia()

            elif tecla == pygame.K_4:
                b.modo_menu = "OBJETOS"

            elif tecla == pygame.K_TAB:
                b.cambiar_objetivo()

            elif tecla == pygame.K_h:
                b.intentar_huir()

        elif b.modo_menu == "OBJETOS":
            if tecla == pygame.K_1:
                b.usar_item("Poción Curativa")
                b.modo_menu = "PRINCIPAL"
            elif tecla == pygame.K_2:
                b.usar_item("Éter Místico")
                b.modo_menu = "PRINCIPAL"
            elif tecla == pygame.K_3:
                b.usar_item("Fragmento del Despertar")
                b.modo_menu = "PRINCIPAL"
            elif tecla in [pygame.K_ESCAPE, pygame.K_0]:
                b.modo_menu = "PRINCIPAL"

    def procesar_input_mochila(self, tecla):
        if tecla in [pygame.K_ESCAPE, pygame.K_m]:
            self.menu_mochila_activo = False
            return

        if tecla == pygame.K_TAB:
            self.indice_heroe_mochila = (self.indice_heroe_mochila + 1) % len(self.companeros_desbloqueados)
            return

        heroe = self.companeros_desbloqueados[self.indice_heroe_mochila]
        piezas_disponibles = [it for it in self.inventario_objetos if any(eq["nombre"] == it for eq in CATALOGO_ARMERIA)]

        idx_pieza = None
        if tecla in [pygame.K_1, pygame.K_KP1] and len(piezas_disponibles) >= 1: idx_pieza = 0
        elif tecla in [pygame.K_2, pygame.K_KP2] and len(piezas_disponibles) >= 2: idx_pieza = 1
        elif tecla in [pygame.K_3, pygame.K_KP3] and len(piezas_disponibles) >= 3: idx_pieza = 2
        elif tecla in [pygame.K_4, pygame.K_KP4] and len(piezas_disponibles) >= 4: idx_pieza = 3
        elif tecla in [pygame.K_5, pygame.K_KP5] and len(piezas_disponibles) >= 5: idx_pieza = 4
        elif tecla in [pygame.K_6, pygame.K_KP6] and len(piezas_disponibles) >= 6: idx_pieza = 5

        if idx_pieza is not None:
            pieza = piezas_disponibles[idx_pieza]
            exito, msg = self.equipar_objeto_a_heroe(heroe, pieza)
            self.dialogo_linea1 = msg
            print(f"[EQUIPO]: {msg}")
        elif tecla == pygame.K_d:
            st = self.stats_heroes[heroe]
            for r in ["arma", "armadura", "accesorio"]:
                if st["equipo"].get(r):
                    self.desequipar_objeto_de_heroe(heroe, r)
            self.dialogo_linea1 = f"Se desequiparon todas las piezas de {heroe}."

    def procesar_input_tienda(self, tecla):
        if tecla in [pygame.K_ESCAPE, pygame.K_t]:
            self.menu_tienda_activo = False
            return

        idx = None
        if tecla == pygame.K_1: idx = 0
        elif tecla == pygame.K_2: idx = 1
        elif tecla == pygame.K_3: idx = 2

        if idx is not None:
            if self.zona_actual == "FORJA":
                exito, self.monedas, msg = intentar_comprar_armeria(idx, self.monedas, self.inventario_objetos)
            else:
                exito, self.monedas, msg = intentar_comprar(idx, self.monedas, self.inventario_objetos)
            self.dialogo_linea1 = msg

    def procesar_input_formacion(self, tecla):
        if tecla in [pygame.K_ESCAPE, pygame.K_f]:
            self.menu_formacion_activo = False
            return

        if tecla == pygame.K_TAB:
            self.slot_formacion_seleccionando = 1 - self.slot_formacion_seleccionando
            return

        if tecla in [pygame.K_a, pygame.K_LEFT]:
            self.indice_seleccion_fh = (self.indice_seleccion_fh - 1) % 4
            return
        elif tecla in [pygame.K_d, pygame.K_RIGHT]:
            self.indice_seleccion_fh = (self.indice_seleccion_fh + 1) % 4
            return

        if tecla == pygame.K_1: self.indice_seleccion_fh = 0
        elif tecla == pygame.K_2: self.indice_seleccion_fh = 1
        elif tecla == pygame.K_3: self.indice_seleccion_fh = 2
        elif tecla == pygame.K_4: self.indice_seleccion_fh = 3

        if tecla in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
            heroes_lista = ["Sidius Storm", "Selene Moon", "Noctis Reverie", "Athina Nightwish"]
            heroe_elegido = heroes_lista[self.indice_seleccion_fh]

            if heroe_elegido not in self.companeros_desbloqueados:
                self.dialogo_linea1 = f"¡{heroe_elegido} aún no ha sido reclutado en el Santuario!"
                return

            if self.slot_formacion_seleccionando == 0:
                if self.pareja_activa[1] == heroe_elegido:
                    self.pareja_activa[1] = self.pareja_activa[0]
                self.pareja_activa[0] = heroe_elegido
                self.dialogo_linea1 = f"¡{heroe_elegido} es ahora el Líder en el mapa (Posición 1)!"
            else:
                if heroe_elegido == self.pareja_activa[0]:
                    self.dialogo_linea1 = "Ese héroe ya está liderando. Elige a otro compañero de apoyo."
                    return
                self.pareja_activa[1] = heroe_elegido
                self.dialogo_linea1 = f"¡{heroe_elegido} te seguirá los pasos como Apoyo (Posición 2)!"

    def procesar_input_puzle(self, tecla):
        p = self.puzle_activo
        if not p: return
        m = p["mision"]

        if p["tipo"] == "TIMING_BARRA":
            if tecla == pygame.K_SPACE:
                zx, zw = p["zona_exito"]
                if zx <= p["pos_aguja"] <= zw:
                    self.concluir_puzle(m, True, "¡Sidius aplica la fuerza exacta en el pistón hidráulico!")
                else:
                    self.concluir_puzle(m, False, "El pistón vibró fuera de sincronía. Fallaste el intento.")

        elif p["tipo"] == "MEMORIA_RUNAS":
            if time.time() - p["tiempo_inicio"] > p["tiempo_memorizar"]:
                char = None
                if tecla == pygame.K_1: char = "1"
                elif tecla == pygame.K_2: char = "2"
                elif tecla == pygame.K_3: char = "3"
                elif tecla == pygame.K_4: char = "4"

                if char:
                    p["ingresado"].append(char)
                    idx = len(p["ingresado"]) - 1
                    if p["secuencia"][idx] != char:
                        self.concluir_puzle(m, False, "Runa incorrecta. Los ecos mnemónicos se disuelven.")
                    elif len(p["ingresado"]) == len(p["secuencia"]):
                        self.concluir_puzle(m, True, "¡Selene sintoniza los ecos de memoria en orden perfecto!")

        elif p["tipo"] == "REACCION_PARADOJA":
            char = None
            if tecla in [pygame.K_1, pygame.K_KP1]: char = "1"
            elif tecla in [pygame.K_2, pygame.K_KP2]: char = "2"
            elif tecla in [pygame.K_3, pygame.K_KP3]: char = "3"

            if char:
                if char == p["correcto"]:
                    self.concluir_puzle(m, True, f"¡Noctis sintoniza {p['simbolo_objetivo']} y colapsa la brecha cuántica!")
                else:
                    self.concluir_puzle(m, False, "Frecuencia desfasada. La línea temporal colapsó en paradoja.")

        elif p["tipo"] == "FAROLES_INTERRUPTORES":
            idx = None
            if tecla == pygame.K_1: idx = 0
            elif tecla == pygame.K_2: idx = 1
            elif tecla == pygame.K_3: idx = 2

            if idx is not None:
                p["estados"][idx] = not p["estados"][idx]
                if idx > 0: p["estados"][idx - 1] = not p["estados"][idx - 1]
                if idx < 2: p["estados"][idx + 1] = not p["estados"][idx + 1]

                if not any(p["estados"]):
                    self.concluir_puzle(m, True, "¡Athina extingue los prismas revelando el cofre en penumbra!")

    def concluir_puzle(self, mision, exito, mensaje):
        if exito:
            mision["resuelta"] = True
            self.inventario_objetos.append(mision["recompensa"])
            self.apd.transicion_delta("PUSH", f"OBJETO_{mision['recompensa']}")
            self.dialogo_linea1 = f"¡PUZLE RESUELTO! {mensaje}"
            self.dialogo_linea2 = f"Recompensa asegurada: [{mision['recompensa']}]."
        else:
            self.dialogo_linea1 = f"Intento fallido: {mensaje}"
            self.dialogo_linea2 = "Interactúa de nuevo para reintentar."
        self.puzle_activo = None

    def iniciar_conversacion(self, id_arbol):
        datos = ARBOLES_DIALOGO.get(id_arbol)
        if not datos:
            return

        st = self.reloj.obtener_estado()
        fase_clave = "crepusculo" if st["es_crepusculo"] else "normal"
        rama = datos[fase_clave]

        if id_arbol == "Vaelira_Contriel" and not st["es_crepusculo"]:
            if not datos.get("servicio_desbloqueado", False):
                saludo_mostrar = rama["saludo_inicial"]
                opciones_crudas = rama["opciones_introduccion"]
                es_primera_vez = True
            else:
                saludo_mostrar = rama["saludo_recurrente"]
                opciones_crudas = [rama["opcion_curar"], rama["opcion_conversar"], rama["opcion_extra"]]
                es_primera_vez = False
        else:
            saludo_mostrar = rama.get("saludo", "")
            opciones_crudas = rama.get("opciones", [])
            es_primera_vez = False

        # Inyección de rumor derivado por GLC en ciudadanos informantes
        if id_arbol in ["Tabernera_Marta", "Viajero_Cael", "Cronista_Elowen"]:
            mision_glc = self.parser.generar_mision(st["es_crepusculo"])
            saludo_mostrar = f"{saludo_mostrar} (Escuché un rumor: \"{mision_glc}\")"

        opciones_procesadas = []
        for opc in opciones_crudas:
            req = opc.get("heroe_requerido")
            disponible = (req is None) or (req in self.pareja_activa)
            opciones_procesadas.append({
                "texto": opc["texto"],
                "heroe_requerido": req,
                "disponible": disponible,
                "respuesta": opc["respuesta"],
                "cambio_animo": opc.get("cambio_animo"),
                "da_item": opc.get("da_item"),
                "es_sanacion": opc.get("es_sanacion", False)
            })

        self.conversacion_activa = {
            "id": id_arbol,
            "nombre": datos["nombre"],
            "saludo": saludo_mostrar,
            "opciones": opciones_procesadas,
            "respuesta_elegida": None,
            "es_primera_vez_vaelira": es_primera_vez
        }

    def procesar_input_conversacion(self, tecla):
        c = self.conversacion_activa
        if not c: return

        if c["respuesta_elegida"] is not None:
            if tecla in [pygame.K_SPACE, pygame.K_RETURN, pygame.K_e, pygame.K_ESCAPE]:
                if c.get("disparar_boss_al_cerrar"):
                    self.conversacion_activa = None
                    self.ejecutar_invocacion_boss()
                    return
                self.conversacion_activa = None
            return

        eleccion = None
        if tecla in [pygame.K_1, pygame.K_KP1] and len(c["opciones"]) >= 1: eleccion = 0
        elif tecla in [pygame.K_2, pygame.K_KP2] and len(c["opciones"]) >= 2: eleccion = 1
        elif tecla in [pygame.K_3, pygame.K_KP3] and len(c["opciones"]) >= 3: eleccion = 2
        elif tecla == pygame.K_ESCAPE:
            self.conversacion_activa = None
            return

        if eleccion is not None:
            opc = c["opciones"][eleccion]
            if not opc.get("disponible", True):
                self.dialogo_linea1 = f"¡Opción Bloqueada! Requiere a [{opc['heroe_requerido']}] en la vanguardia."
                self.dialogo_linea2 = "Abre la formación con [F] para rotar tu equipo."
                return

            if opc.get("es_invocar_boss"):
                c["respuesta_elegida"] = opc["respuesta"]
                c["disparar_boss_al_cerrar"] = True
                return
            elif opc.get("es_invocar_boss") is False:
                c["respuesta_elegida"] = opc["respuesta"]
                return

            datos_npc = ARBOLES_DIALOGO.get(c["id"], {})
            st = self.reloj.obtener_estado()

            if c.get("es_primera_vez_vaelira"):
                datos_npc["servicio_desbloqueado"] = True

            if opc.get("es_sanacion"):
                if st["es_crepusculo"]:
                    c["respuesta_elegida"] = opc["respuesta"]
                    self.dialogo_linea1 = "Vaelira está demasiado distraída por la niebla. ¡No hay sanación en el Crepúsculo!"
                    self.dialogo_linea2 = "Regresa cuando el reloj marque MUNDO NORMAL."
                else:
                    animo = datos_npc.get("estado_animo", "NEUTRAL")
                    if animo == "AMISTOSO":
                        self.curar_todo_el_equipo()
                        c["respuesta_elegida"] = "Vaelira: '¡Por ser tan amables y respetuosos, el servicio va por la casa! Cierren los ojos... ¡Listos como nuevos!'"
                        self.dialogo_linea1 = "¡Vaelira ha sanado al equipo GRATIS gracias a tu buen trato!"
                        self.dialogo_linea2 = "La vitalidad y energía (HP y MP) han sido restauradas al 100%."
                    elif animo == "HOSTIL":
                        costo = 25
                        if self.monedas >= costo:
                            self.monedas -= costo
                            self.curar_todo_el_equipo()
                            c["respuesta_elegida"] = f"Vaelira: 'Son {costo} monedas por las vendas y ungüentos. Tengan su medicina y procuren no volver a faltarme al respeto.'"
                            self.dialogo_linea1 = f"¡Vaelira te cobró {costo} monedas por sanar al grupo debido a tu actitud hostil!"
                            self.dialogo_linea2 = f"Monedas restantes: {self.monedas} oro. Equipo curado al 100%."
                        else:
                            c["respuesta_elegida"] = f"Vaelira: 'La sanación cuesta {costo} monedas para gente maleducada. Como no tienen suficiente dinero, ¡tendrán que aguantar el dolor allá afuera!'"
                            self.dialogo_linea1 = "¡Vaelira se negó a sanarte! No tienes suficiente oro para pagar su tarifa por hostilidad."
                            self.dialogo_linea2 = "Aprende a tratar mejor a los habitantes del pueblo."
                    else:
                        costo = 10
                        if self.monedas >= costo:
                            self.monedas -= costo
                            self.curar_todo_el_equipo()
                            c["respuesta_elegida"] = f"Vaelira: 'Son {costo} monedas por las gasas y hierbas. ¡Que tengan un buen viaje!'"
                            self.dialogo_linea1 = f"Vaelira te cobró {costo} monedas (tarifa estándar de botica)."
                            self.dialogo_linea2 = f"Monedas restantes: {self.monedas} oro. Equipo curado al 100%."
                        else:
                            c["respuesta_elegida"] = "Vaelira: 'Necesito al menos 10 monedas para cubrir el costo de las hierbas...'"
                            self.dialogo_linea1 = "No tienes monedas suficientes para la tarifa estándar de sanación."
            else:
                c["respuesta_elegida"] = opc["respuesta"]

            if opc.get("cambio_animo") and datos_npc:
                datos_npc["estado_animo"] = opc["cambio_animo"]

            if opc.get("da_item") and datos_npc and not datos_npc.get("recompensa_entregada", False):
                datos_npc["recompensa_entregada"] = True
                self.inventario_objetos.append(opc["da_item"])
                self.apd.transicion_delta("PUSH", f"OBJETO_{opc['da_item']}")
                self.dialogo_linea2 = f"¡Objeto recibido: [{opc['da_item']}]!"

    def interactuar(self):
        if self.en_movimiento or self.puzle_activo or self.conversacion_activa or self.menu_formacion_activo or self.menu_tienda_activo or self.menu_mochila_activo or self.combate_activo or self.estado_final_aceptado:
            return

        st = self.reloj.obtener_estado()
        es_crep = st["es_crepusculo"]

        if es_crep and self.zona_actual == "EXTERIOR_CIUDAD":
            for e in self.enemigos_crepusculares:
                if not e["derrotado"] and abs(e["x"] - self.jugador_x) + abs(e["y"] - self.jugador_y) <= 1:
                    self.iniciar_combate_con(e)
                    return

        if self.zona_actual == "EXTERIOR_CIUDAD":
            # Interacción con la fuente central para invocar al Jefe
            dist_fuente = abs(self.jugador_x - 9) + abs(self.jugador_y - 6)
            if dist_fuente <= 2:
                if not self.boss_derrotado:
                    self.abrir_menu_invocar_boss()
                    return
                else:
                    self.dialogo_linea1 = "La fuente fluye tranquila. El Devorador del Cronos ha sido purgado."
                    return

            vecinos = [
                self.mapa_actual[self.jugador_y - 1][self.jugador_x],
                self.mapa_actual[self.jugador_y + 1][self.jugador_x],
                self.mapa_actual[self.jugador_y][self.jugador_x - 1],
                self.mapa_actual[self.jugador_y][self.jugador_x + 1]
            ]
            if 3 in vecinos:
                self.menu_formacion_activo = True
                self.slot_formacion_seleccionando = 0
                return

            for m in self.gestor_puzles.misiones:
                if abs(m["x"] - self.jugador_x) + abs(m["y"] - self.jugador_y) <= 1:
                    acceso, motivo, detalle = self.gestor_puzles.verificar_acceso(m, es_crep, self.pareja_activa)
                    if not acceso:
                        self.dialogo_linea1 = detalle
                        self.dialogo_linea2 = "Avanza el tiempo o ajusta la formación con [F]."
                        return
                    self.puzle_activo = self.gestor_puzles.crear_estado_puzle(m)
                    return

            for p in self.portadores_en_mapa:
                if not p["reclutado"] and abs(p["x"] - self.jugador_x) + abs(p["y"] - self.jugador_y) <= 1:
                    p["reclutado"] = True
                    self.companeros_desbloqueados.append(p["nombre"])
                    if self.pareja_activa[1] is None:
                        self.pareja_activa[1] = p["nombre"]
                        self.apoyo_x = self.jugador_x
                        self.apoyo_y = self.jugador_y + 1
                        self.apoyo_pixel_x = float(self.apoyo_x * TAMANO_TILE)
                        self.apoyo_pixel_y = float(self.apoyo_y * TAMANO_TILE)
                        self.apoyo_destino_x = self.apoyo_pixel_x
                        self.apoyo_destino_y = self.apoyo_pixel_y

                    self.conversacion_activa = {
                        "id": f"reclutamiento_{p['nombre']}",
                        "nombre": p["nombre"],
                        "saludo": p["dialogo"],
                        "opciones": [
                            {
                                "texto": "[1] ¡Bienvenido al equipo! Cubre mi espalda y yo la tuya.",
                                "heroe_requerido": None,
                                "disponible": True,
                                "respuesta": f"{p['nombre']} asiente con firmeza: 'Trato hecho. No permitiré que las sombras rompan nuestra formación.'",
                                "cambio_animo": None,
                                "da_item": None,
                                "es_sanacion": False
                            },
                            {
                                "texto": f"[2] [Sidius] 'Tu vínculo de {p['vinculo']} será crucial para abrir los portales.'",
                                "heroe_requerido": "Sidius Storm",
                                "disponible": True,
                                "respuesta": f"{p['nombre']} sonríe con determinación: 'Juntos sincronizaremos el poder necesario para restaurar el tiempo.'",
                                "cambio_animo": None,
                                "da_item": "Poción Curativa",
                                "es_sanacion": False
                            },
                            {
                                "texto": "[3] Mantente alerta. Si el reloj suena, las cosas se pondrán feas.",
                                "heroe_requerido": None,
                                "disponible": True,
                                "respuesta": f"{p['nombre']} empuña su arma: 'He sobrevivido a la niebla antes. Estoy listo para lo que venga.'",
                                "cambio_animo": None,
                                "da_item": None,
                                "es_sanacion": False
                            }
                        ],
                        "respuesta_elegida": None,
                        "es_primera_vez_vaelira": False
                    }
                    self.dialogo_linea1 = f"¡{p['nombre']} se ha unido a la vanguardia!"
                    self.dialogo_linea2 = "Pulsa [F] en cualquier momento para configurar la formación."
                    return

            for n in self.npcs_exterior:
                if abs(n["x"] - self.jugador_x) + abs(n["y"] - self.jugador_y) <= 1:
                    self.iniciar_conversacion(n["id"])
                    return

        elif self.zona_actual in ["BOTICA", "FORJA", "BIBLIOTECA"]:
            lista_npcs = []
            if self.zona_actual == "BOTICA":
                lista_npcs = self.npcs_interior_botica
            elif self.zona_actual == "FORJA":
                lista_npcs = self.npcs_interior_forja
            elif self.zona_actual == "BIBLIOTECA":
                lista_npcs = self.npcs_interior_biblioteca

            for n in lista_npcs:
                dist_x = abs(n["x"] - self.jugador_x)
                dist_y = abs(n["y"] - self.jugador_y)
                if dist_x <= 2 and dist_y <= 2:
                    self.iniciar_conversacion(n["id_arbol"])
                    return

    # RENDERIZADO
    def dibujar_pantalla_final_aceptacion(self):
        f = self.estado_final_aceptado
        overlay = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        overlay.fill((8, 6, 12, 240))
        self.pantalla.blit(overlay, (0, 0))

        cx, cy = 60, 80
        cw, ch = ANCHO_VENTANA - 120, ALTO_VENTANA - 160
        pygame.draw.rect(self.pantalla, (18, 16, 26), (cx, cy, cw, ch))
        pygame.draw.rect(self.pantalla, f["color"], (cx, cy, cw, ch), 3)

        t_tit = self.fuentes["grande"].render(f["titulo"], True, f["color"])
        self.pantalla.blit(t_tit, (cx + 35, cy + 35))
        pygame.draw.line(self.pantalla, (60, 50, 75), (cx + 35, cy + 70), (cx + cw - 35, cy + 70), 1)

        t_mis = self.fuentes["texto"].render(f"Anomalías estabilizadas: {f['misiones']}/4", True, (240, 215, 90))
        self.pantalla.blit(t_mis, (cx + 35, cy + 95))

        t_l1 = self.fuentes["dialogo"].render(f["texto_linea1"], True, (240, 235, 240))
        t_l2 = self.fuentes["dialogo"].render(f["texto_linea2"], True, (240, 235, 240))
        t_l3 = self.fuentes["dialogo"].render(f["texto_linea3"], True, (240, 235, 240))
        self.pantalla.blit(t_l1, (cx + 35, cy + 150))
        self.pantalla.blit(t_l2, (cx + 35, cy + 185))
        self.pantalla.blit(t_l3, (cx + 35, cy + 220))

        t_pie = self.fuentes["texto"].render("Presiona [ESPACIO / ESC] para continuar", True, (130, 220, 255))
        self.pantalla.blit(t_pie, (cx + cw // 2 - t_pie.get_width() // 2, cy + ch - 45))

    def dibujar(self):
        st = self.reloj.obtener_estado()
        es_crep = st["es_crepusculo"]

        color_suelo = COLOR_SUELO_CREP if es_crep else COLOR_SUELO_NORMAL
        color_muro = COLOR_MURO_CREP if es_crep else COLOR_MURO_NORMAL

        self.pantalla.fill((0, 0, 0))

        fondo_activo = None
        if self.zona_actual == "BOTICA":
            fondo_activo = getattr(self, "fondo_botica", None)
        elif self.zona_actual == "FORJA":
            fondo_activo = getattr(self, "fondo_forja", None)

        if fondo_activo:
            self.pantalla.blit(fondo_activo, (0, 0))
            if es_crep:
                filtro = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
                filtro.fill((50, 20, 70, 110))
                self.pantalla.blit(filtro, (0, 0))

        zonas_edificios = [
            (2, 2, 3, 3), (15, 2, 3, 3), (2, 7, 3, 3), (15, 7, 3, 3), (6, 1, 8, 4)
        ]

        def es_zona_edificio(cx, cy):
            if self.zona_actual != "EXTERIOR_CIUDAD":
                return False
            for ex, ey, ew, eh in zonas_edificios:
                if ex <= cx < ex + ew and ey <= cy < ey + eh:
                    return True
            return False

        filas_tot = len(self.mapa_actual)
        cols_tot = len(self.mapa_actual[0])

        for fila in range(filas_tot):
            for col in range(cols_tot):
                tile = self.mapa_actual[fila][col]
                px = col * TAMANO_TILE
                py = fila * TAMANO_TILE
                rect = pygame.Rect(px, py, TAMANO_TILE, TAMANO_TILE)

                if self.zona_actual == "EXTERIOR_CIUDAD":
                    if es_zona_edificio(col, fila):
                        if not self.gestor_edificios.dibujar_terreno_tile(self.pantalla, "PASTO", px, py, es_crep):
                            pygame.draw.rect(self.pantalla, color_suelo, rect)
                        continue

                    if tile == 1:
                        self.gestor_edificios.dibujar_muro_procedural(self.pantalla, col, fila, cols_tot, filas_tot, es_crep)
                        continue
                    elif tile == 13:
                        if not self.gestor_edificios.dibujar_terreno_tile(self.pantalla, "CAMINO", px, py, es_crep):
                            pygame.draw.rect(self.pantalla, (215, 210, 195), rect)
                            pygame.draw.rect(self.pantalla, (185, 180, 165), rect, 1)
                        continue
                    elif tile in [0, 4, 5, 6]:
                        if not self.gestor_edificios.dibujar_terreno_tile(self.pantalla, "PASTO", px, py, es_crep):
                            pygame.draw.rect(self.pantalla, color_suelo, rect)
                        continue
                    elif tile == 2:
                        col_p = COLOR_PORTAL_CREP if es_crep else COLOR_PORTAL_REGIONES
                        pygame.draw.rect(self.pantalla, col_p, rect)
                        continue
                else:
                    if fondo_activo:
                        continue

                    if tile == 1:
                        pygame.draw.rect(self.pantalla, color_muro, rect)
                        pygame.draw.rect(self.pantalla, (20, 20, 20), rect, 1)
                    elif tile in [4, 5, 6]:
                        pygame.draw.rect(self.pantalla, COLOR_PUERTA, rect)
                    elif tile == 9:
                        pygame.draw.rect(self.pantalla, COLOR_SALIDA, rect)
                    elif tile == 7:
                        pygame.draw.rect(self.pantalla, COLOR_SUELO_BOTICA, rect)
                        pygame.draw.rect(self.pantalla, COLOR_MOSTRADOR, (rect.x, rect.y + 10, TAMANO_TILE, TAMANO_TILE - 10))
                        pygame.draw.rect(self.pantalla, (80, 50, 30), (rect.x, rect.y + 10, TAMANO_TILE, TAMANO_TILE - 10), 2)
                    elif tile == 8:
                        pygame.draw.rect(self.pantalla, COLOR_ESTANTERIA, rect)
                        pygame.draw.rect(self.pantalla, (55, 35, 20), rect, 2)
                    elif tile == 10:
                        pygame.draw.rect(self.pantalla, COLOR_SUELO_BOTICA, rect)
                        pygame.draw.rect(self.pantalla, COLOR_CAMILLA, (rect.x + 4, rect.y + 4, TAMANO_TILE - 8, TAMANO_TILE - 8))
                    elif tile == 11:
                        pygame.draw.rect(self.pantalla, COLOR_SUELO_BOTICA, rect)
                        pygame.draw.circle(self.pantalla, COLOR_CALDERO, rect.center, 15)
                    elif tile == 12:
                        pygame.draw.rect(self.pantalla, COLOR_SUELO_BOTICA, rect)
                        pygame.draw.rect(self.pantalla, COLOR_ALFOMBRA, rect)
                        pygame.draw.rect(self.pantalla, COLOR_ALFOMBRA_BORDE, rect, 2)
                    else:
                        suelo_pintar = COLOR_SUELO_BOTICA if self.zona_actual in ["BOTICA", "FORJA"] else color_suelo
                        pygame.draw.rect(self.pantalla, suelo_pintar, rect)

        self.gestor_edificios.dibujar_ciudad(self.pantalla, self.mapa_actual, self.zona_actual, es_crep)

        if self.zona_actual == "EXTERIOR_CIUDAD":
            # Indicador luminoso en la fuente central
            if not self.boss_derrotado:
                fx = 9 * TAMANO_TILE + TAMANO_TILE // 2
                fy = 6 * TAMANO_TILE + TAMANO_TILE // 2
                col_aura = (180, 60, 240) if es_crep else (100, 200, 255)
                pygame.draw.circle(self.pantalla, col_aura, (fx, fy), 18, 2)

            for m in self.gestor_puzles.misiones:
                if not m["resuelta"]:
                    mx, my = m["x"] * TAMANO_TILE + 10, m["y"] * TAMANO_TILE + 10
                    col_m = COLOR_MISION_ACTIVA if m["fase_requerida"] == es_crep else COLOR_MISION_INACTIVA
                    pygame.draw.rect(self.pantalla, col_m, (mx, my, TAMANO_TILE - 20, TAMANO_TILE - 20))

            if es_crep:
                for e in self.enemigos_crepusculares:
                    if not e["derrotado"]:
                        ex, ey = e["x"] * TAMANO_TILE + 6, e["y"] * TAMANO_TILE + 6
                        if e.get("es_grupo"):
                            pygame.draw.rect(self.pantalla, (45, 10, 25), (ex, ey, TAMANO_TILE - 12, TAMANO_TILE - 12))
                            pygame.draw.rect(self.pantalla, (220, 50, 80), (ex, ey, TAMANO_TILE - 12, TAMANO_TILE - 12), 2)
                            pygame.draw.circle(self.pantalla, (255, 80, 120), (ex + 10, ey + 14), 4)
                            pygame.draw.circle(self.pantalla, (200, 60, 240), (ex + 18, ey + 14), 4)
                        else:
                            pygame.draw.rect(self.pantalla, (25, 8, 35), (ex, ey, TAMANO_TILE - 12, TAMANO_TILE - 12))
                            pygame.draw.rect(self.pantalla, (160, 40, 210), (ex, ey, TAMANO_TILE - 12, TAMANO_TILE - 12), 1)
                            pygame.draw.circle(self.pantalla, (220, 80, 255), (ex + 14, ey + 14), 5)

            # Dibujar al Boss si fue invocado en el mapa
            if self.boss_objeto and not self.boss_objeto["derrotado"]:
                bx = self.boss_objeto["x"] * TAMANO_TILE
                by = self.boss_objeto["y"] * TAMANO_TILE
                pygame.draw.rect(self.pantalla, (35, 8, 45), (bx + 2, by + 2, TAMANO_TILE - 4, TAMANO_TILE - 4))
                pygame.draw.rect(self.pantalla, (240, 60, 60), (bx + 2, by + 2, TAMANO_TILE - 4, TAMANO_TILE - 4), 2)
                pygame.draw.circle(self.pantalla, (255, 40, 40), (bx + TAMANO_TILE // 2, by + TAMANO_TILE // 2), 10)

            # Ciudadanos exteriores 
            for n in self.npcs_exterior:
                nx = n["x"] * TAMANO_TILE
                ny = n["y"] * TAMANO_TILE
                dict_sprites = self.sprites_npcs_crep if es_crep else self.sprites_npcs_normal
                sprite_npc = dict_sprites.get(n["id"])

                if sprite_npc:
                    self.pantalla.blit(sprite_npc, (nx, ny))
                else:
                    col_npc = (160, 40, 90) if es_crep else COLOR_NPC
                    pygame.draw.rect(self.pantalla, col_npc, (nx + 8, ny + 8, TAMANO_TILE - 16, TAMANO_TILE - 16))

            # Protagonistas reclutables en mapa c
            for p in self.portadores_en_mapa:
                if not p["reclutado"]:
                    px = p["x"] * TAMANO_TILE
                    py = p["y"] * TAMANO_TILE
                    frame_chibi = self.animador_apoyo.obtener_frame(p["nombre"], "abajo")

                    if frame_chibi:
                        self.pantalla.blit(frame_chibi, (px, py))
                    else:
                        col_rec = COLOR_HEROES_RESPALDO.get(p["nombre"], COLOR_RECLUTABLE)
                        pygame.draw.rect(self.pantalla, col_rec, (px + 6, py + 6, TAMANO_TILE - 12, TAMANO_TILE - 12))
                        pygame.draw.rect(self.pantalla, (255, 255, 255), (px + 6, py + 6, TAMANO_TILE - 12, TAMANO_TILE - 12), 1)

                    pygame.draw.polygon(self.pantalla, (255, 220, 100), [
                        (px + TAMANO_TILE // 2, py - 4),
                        (px + TAMANO_TILE // 2 - 4, py - 10),
                        (px + TAMANO_TILE // 2 + 4, py - 10)
                    ])

        # Interiores
        elif self.zona_actual == "FORJA":
            for n in self.npcs_interior_forja:
                chibi_carlos_activo = self.chibi_carlos_crep if es_crep else self.chibi_carlos_normal
                nx, ny = n["x"] * TAMANO_TILE, n["y"] * TAMANO_TILE

                if chibi_carlos_activo:
                    self.pantalla.blit(chibi_carlos_activo, (nx, ny))
                else:
                    col_herrero = (150, 40, 60) if es_crep else (220, 120, 50)
                    pygame.draw.rect(self.pantalla, col_herrero, (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8))
                    pygame.draw.circle(self.pantalla, (255, 230, 200), (nx + TAMANO_TILE // 2, ny + 10), 6)
                    pygame.draw.rect(self.pantalla, (255, 255, 255), (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8), 1)

        elif self.zona_actual == "BIBLIOTECA":
            for n in self.npcs_interior_biblioteca:
                nx, ny = n["x"] * TAMANO_TILE, n["y"] * TAMANO_TILE
                pygame.draw.rect(self.pantalla, (100, 160, 230), (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8))
                pygame.draw.circle(self.pantalla, (255, 230, 200), (nx + TAMANO_TILE // 2, ny + 10), 6)
                pygame.draw.rect(self.pantalla, (255, 255, 255), (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8), 1)

        elif self.zona_actual == "BOTICA":
            for n in self.npcs_interior_botica:
                chibi_activo = self.chibi_vaelira_crep if es_crep else self.chibi_vaelira_normal
                nx = n["x"] * TAMANO_TILE
                ny = n["y"] * TAMANO_TILE

                if chibi_activo:
                    self.pantalla.blit(chibi_activo, (nx, ny))
                else:
                    col_v = (200, 80, 220) if es_crep else (120, 220, 160)
                    pygame.draw.rect(self.pantalla, col_v, (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8))
                    pygame.draw.circle(self.pantalla, (255, 230, 200), (nx + TAMANO_TILE // 2, ny + 10), 6)
                    pygame.draw.rect(self.pantalla, (255, 255, 255), (nx + 6, ny + 4, TAMANO_TILE - 12, TAMANO_TILE - 8), 1)

        # Dibujar Apoyo
        apoyo = self.pareja_activa[1]
        if apoyo is not None and self.stats_heroes[apoyo]["hp"] > 0:
            frame_apoyo = self.animador_apoyo.obtener_frame(apoyo, self.apoyo_direccion)
            if frame_apoyo:
                self.pantalla.blit(frame_apoyo, (int(self.apoyo_pixel_x), int(self.apoyo_pixel_y)))
            else:
                col_apoyo = COLOR_HEROES_RESPALDO.get(apoyo, (100, 200, 100))
                ax = int(self.apoyo_pixel_x) + 6
                ay = int(self.apoyo_pixel_y) + 6
                pygame.draw.rect(self.pantalla, col_apoyo, (ax, ay, TAMANO_TILE - 12, TAMANO_TILE - 12))
                pygame.draw.rect(self.pantalla, (255, 255, 255), (ax, ay, TAMANO_TILE - 12, TAMANO_TILE - 12), 1)

        # Dibujar Líder
        lider = self.pareja_activa[0]
        if self.stats_heroes[lider]["hp"] > 0:
            frame_lider = self.animador_lider.obtener_frame(lider, self.direccion_mirada)
            if frame_lider:
                self.pantalla.blit(frame_lider, (int(self.pixel_x), int(self.pixel_y)))
            else:
                col_lider = COLOR_HEROES_RESPALDO.get(lider, (50, 120, 230))
                jx = int(self.pixel_x) + 5
                jy = int(self.pixel_y) + 5
                pygame.draw.rect(self.pantalla, col_lider, (jx, jy, TAMANO_TILE - 10, TAMANO_TILE - 10))
                pygame.draw.rect(self.pantalla, (240, 210, 80), (jx, jy, TAMANO_TILE - 10, TAMANO_TILE - 10), 2)

        dibujar_hud(self.pantalla, self, ANCHO_VENTANA)

        # Overlays
        if self.estado_final_aceptado:
            self.dibujar_pantalla_final_aceptacion()
        elif self.combate_activo:
            self.actualizar_animaciones_combate()
            dibujar_overlay_batalla(self.pantalla, self.combate_activo, self.fuentes, ANCHO_VENTANA, ALTO_VENTANA)
        elif self.menu_mochila_activo:
            dibujar_menu_mochila(self.pantalla, self, ANCHO_VENTANA, ALTO_VENTANA)
        elif self.menu_tienda_activo:
            dibujar_menu_tienda(self.pantalla, self, ANCHO_VENTANA, ALTO_VENTANA)
        elif self.menu_formacion_activo:
            dibujar_menu_formacion(self.pantalla, self, ANCHO_VENTANA, ALTO_VENTANA)
        elif self.puzle_activo:
            if self.puzle_activo["tipo"] == "REACCION_PARADOJA":
                if time.time() - self.puzle_activo["tiempo_inicio"] >= self.puzle_activo["tiempo_limite"]:
                    self.concluir_puzle(self.puzle_activo["mision"], False, "Tiempo agotado. La brecha colapsó.")
            dibujar_overlay_puzle(self.pantalla, self.puzle_activo, self.fuentes, ANCHO_VENTANA, ALTO_VENTANA)
        elif self.conversacion_activa:
            dibujar_dialogo_overlay(self.pantalla, self, ANCHO_VENTANA, ALTO_VENTANA)

        pygame.display.flip()

    # BUCLE PRINCIPAL
    def ejecutar(self):
        ejecutando = True
        while ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    ejecutando = False
                elif evento.type == pygame.KEYDOWN:
                    if self.estado_final_aceptado:
                        if evento.key in [pygame.K_SPACE, pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_e]:
                            self.estado_final_aceptado = None
                    elif self.combate_activo:
                        self.procesar_input_combate(evento.key)
                    elif self.menu_mochila_activo:
                        self.procesar_input_mochila(evento.key)
                    elif self.menu_tienda_activo:
                        self.procesar_input_tienda(evento.key)
                    elif self.menu_formacion_activo:
                        self.procesar_input_formacion(evento.key)
                    elif self.conversacion_activa:
                        self.procesar_input_conversacion(evento.key)
                    elif self.puzle_activo:
                        self.procesar_input_puzle(evento.key)
                    else:
                        if evento.key in [pygame.K_w, pygame.K_UP]: self.intentar_mover(0, -1)
                        elif evento.key in [pygame.K_s, pygame.K_DOWN]: self.intentar_mover(0, 1)
                        elif evento.key in [pygame.K_a, pygame.K_LEFT]: self.intentar_mover(-1, 0)
                        elif evento.key in [pygame.K_d, pygame.K_RIGHT]: self.intentar_mover(1, 0)
                        elif evento.key in [pygame.K_e, pygame.K_SPACE]: self.interactuar()
                        elif evento.key == pygame.K_f:
                            self.menu_formacion_activo = True
                            self.slot_formacion_seleccionando = 0
                        elif evento.key == pygame.K_m:
                            self.menu_mochila_activo = True
                        elif evento.key == pygame.K_t:
                            if self.zona_actual in ["BOTICA", "FORJA"]:
                                self.menu_tienda_activo = True
                        # R: RGeneración GLC BNF en tiempo real
                        elif evento.key == pygame.K_r:
                            st = self.reloj.obtener_estado()
                            rumor = self.parser.generar_mision(st["es_crepusculo"])
                            self.dialogo_linea1 = f"[RUMOR GLC]: \"{rumor}\""
                            print(f"\n[GLC DERIVACIÓN BNF EN TIEMPO REAL]: {rumor}")
                        # G: Traza formal del Save-State
                        elif evento.key == pygame.K_g:
                            self.trazar_save_state_formal()

            self.actualizar_movimiento_suave()
            self.actualizar_movimiento_enemigos()
            self.actualizar_musica_segun_estado()
            self.dibujar()
            self.reloj_fps.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    try:
        juego = Juego2D()
        juego.ejecutar()
    except Exception:
        print("\n[ERROR CRÍTICO EN MOTOR 2D]:")
        traceback.print_exc()