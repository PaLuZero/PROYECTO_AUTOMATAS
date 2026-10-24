import os
import math
import random
import pygame

_SPRITES_COMBATE = {}

def obtener_sprite_combate(heroe, estado, carpetas_buscar):
    clave = f"{heroe}_{estado}"
    if clave in _SPRITES_COMBATE:
        return _SPRITES_COMBATE[clave]

    nombre_limpio = str(heroe).lower().split()[0]
    nombres_alias = [nombre_limpio]
    if nombre_limpio in ["athina", "atina"]:
        nombres_alias = ["athina", "atina"]

    posibles_archivos = []
    for na in nombres_alias:
        if estado == "guardia":
            posibles_archivos.extend([
                f"{na}_battle_back.png",
                f"{na}_back_battle.png",
                f"{na}_back.png"
            ])
        else:
            posibles_archivos.extend([
                f"{na}_battle_back2.png",
                f"{na}_battle_back.2jpg.png",
                f"{na}_back_battle2.png",
                f"{na}_attack_back.png"
            ])

    directorio_script = os.path.dirname(os.path.abspath(__file__))
    raiz_proyecto = os.path.abspath(os.path.join(directorio_script, "..", ".."))

    rutas_base = list(carpetas_buscar)
    rutas_base.extend([
        os.path.join(raiz_proyecto, "assets", "sprites"),
        os.path.join(raiz_proyecto, "assets"),
        os.path.join(raiz_proyecto, "sprites"),
        "assets/sprites",
        "assets"
    ])

    for carpeta in rutas_base:
        for nombre in posibles_archivos:
            ruta = os.path.join(carpeta, nombre)
            if os.path.exists(ruta):
                try:
                    img = pygame.image.load(ruta).convert_alpha()
                    w, h = img.get_size()
                    alto_fijo = 250
                    ancho_calc = int(alto_fijo * (w / h))
                    img_escalada = pygame.transform.scale(img, (ancho_calc, alto_fijo))
                    _SPRITES_COMBATE[clave] = img_escalada
                    return img_escalada
                except Exception:
                    pass
    return None


def dibujar_overlay_batalla(pantalla, batalla, fuentes, ancho_pantalla=800, alto_pantalla=600):
    carpetas_buscar = ["assets/sprites", "assets", "sprites"]

    # --------------------------------------------------------------------------
    # 1. DATOS EN VIVO DEL ENEMIGO
    # --------------------------------------------------------------------------
    e_obj = getattr(batalla, "enemigo_info", None) or getattr(batalla, "enemigo", None)

    nombre_enemigo = getattr(batalla, "nombre_enemigo", "Sombra Hostil")
    hp_actual = getattr(batalla, "hp_enemigo", e_obj.get("hp", 0) if isinstance(e_obj, dict) else 0)
    max_hp = getattr(batalla, "max_hp_enemigo", e_obj.get("max_hp", 100) if isinstance(e_obj, dict) else 100)
    es_grupo = getattr(batalla, "es_grupo", False)
    indice_obj = getattr(batalla, "indice_objetivo", 0)

    fase_combate = getattr(batalla, "fase_combate", "")
    resultado = getattr(batalla, "resultado", "")
    if fase_combate == "TERMINADO" and resultado == "VICTORIA":
        hp_actual = 0

    val_hp = max(0, int(hp_actual))
    val_max = max(1, int(max_hp))

    # 2. FONDO OSCURO Y EFECTOS
    fondo_batalla = pygame.Surface((ancho_pantalla, alto_pantalla))
    fondo_batalla.fill((12, 10, 16))
    pantalla.blit(fondo_batalla, (0, 0))

    tiempo_ms = pygame.time.get_ticks()
    shake_x, shake_y = 0, 0
    if getattr(batalla, "anim_recibiendo_dano", False):
        shake_x = random.randint(-8, 8)
        shake_y = random.randint(-4, 4)

    tinte_dano = getattr(batalla, "anim_recibiendo_dano", False) and (tiempo_ms % 150 < 75)
    esta_cargando = getattr(batalla, "enemigo_cargando_ataque", False)

    # 3. DIBUJAR ENEMIGO (A LA DERECHA)
    if not es_grupo:
        ex = 540 + shake_x
        ey = 160 + shake_y

        pulso_sombra = int(math.sin(tiempo_ms * 0.003) * 5)
        sombra_enemigo = pygame.Surface((220 + pulso_sombra, 50), pygame.SRCALPHA)
        pygame.draw.ellipse(sombra_enemigo, (0, 0, 0, 130), (0, 0, 220 + pulso_sombra, 50))
        pantalla.blit(sombra_enemigo, (ex - (110 + pulso_sombra // 2), ey + 50))

        if esta_cargando:
            radio_aura = 68 + int(math.sin(tiempo_ms * 0.015) * 8)
            pygame.draw.circle(pantalla, (255, 40, 40), (ex, ey), radio_aura, 3)
            txt_aviso = fuentes["puzle"].render("¡PREPARANDO GOLPE DEVASTADOR!", True, (255, 60, 60))
            pantalla.blit(txt_aviso, (ex - txt_aviso.get_width() // 2, ey - 125))

        col_cuerpo = (180, 20, 20) if tinte_dano else (40, 15, 50)
        col_borde = (255, 100, 100) if tinte_dano else ((255, 50, 50) if esta_cargando else (160, 40, 180))
        pygame.draw.circle(pantalla, col_cuerpo, (ex, ey), 55)
        pygame.draw.circle(pantalla, col_borde, (ex, ey), 55, 4 if esta_cargando else 3)
        pygame.draw.circle(pantalla, (230, 80, 255), (ex - 12, ey - 10), 8)
        pygame.draw.circle(pantalla, (230, 80, 255), (ex + 12, ey - 10), 8)
        pygame.draw.circle(pantalla, (255, 255, 255), (ex - 12, ey - 10), 3)
        pygame.draw.circle(pantalla, (255, 255, 255), (ex + 12, ey - 10), 3)

        txt_nom = fuentes["grande"].render(str(nombre_enemigo), True, (240, 220, 240))
        pantalla.blit(txt_nom, (ex - txt_nom.get_width() // 2, ey - 95))

        bw, bh = 180, 10
        bx, by = ex - bw // 2, ey - 65
        pct = max(0.0, min(1.0, val_hp / val_max))
        pygame.draw.rect(pantalla, (30, 20, 30), (bx, by, bw, bh))
        pygame.draw.rect(pantalla, (190, 40, 60), (bx, by, int(bw * pct), bh))
        pygame.draw.rect(pantalla, (120, 80, 110), (bx, by, bw, bh), 1)

        txt_hp = fuentes["dialogo"].render(f"{val_hp}/{val_max}", True, (220, 220, 220))
        pantalla.blit(txt_hp, (bx + bw + 8, by - 2))

    else:
        enemigos = getattr(batalla, "enemigos", [])
        spacing = 150
        start_x = 440

        for i, sub_e in enumerate(enemigos):
            cx = start_x + i * spacing + (shake_x if i == indice_obj else 0)
            cy = 160 + (shake_y if i == indice_obj else 0)
            esta_activo = (i == indice_obj)
            tinte_sub = esta_activo and tinte_dano

            pygame.draw.ellipse(pantalla, (0, 0, 0, 110), (cx - 45, cy + 35, 90, 30))

            col_borde = (255, 80, 100) if esta_activo else (130, 40, 120)
            col_cuerpo = (180, 20, 20) if tinte_sub else (45, 12, 30)
            pygame.draw.circle(pantalla, col_cuerpo, (cx, cy), 42)
            pygame.draw.circle(pantalla, col_borde, (cx, cy), 42, 3 if esta_activo else 2)
            pygame.draw.circle(pantalla, (240, 80, 120), (cx, cy - 8), 6)

            nom_txt = fuentes["texto"].render(str(sub_e.get("nombre", f"Sombra {i+1}")), True, (240, 220, 230))
            pantalla.blit(nom_txt, (cx - nom_txt.get_width() // 2, cy - 85))

            bw = 110
            bx, by = cx - bw // 2, cy - 62
            sub_max = max(1, sub_e.get("max_hp", 60))
            sub_hp = max(0, sub_e.get("hp", 60))
            pct = max(0.0, min(1.0, sub_hp / sub_max))

            pygame.draw.rect(pantalla, (30, 15, 20), (bx, by, bw, 9))
            pygame.draw.rect(pantalla, (200, 40, 60), (bx, by, int(bw * pct), 9))
            pygame.draw.rect(pantalla, (120, 80, 90), (bx, by, bw, 9), 1)

            txt_num_sub = fuentes["dialogo"].render(f"{sub_hp}/{sub_max}", True, (220, 220, 220))
            pantalla.blit(txt_num_sub, (cx - txt_num_sub.get_width() // 2, by - 16))

    # 4. RENDERIZADO DE LOS HÉROES
    heroes_pos = [
        (90, 175),   # Líder
        (225, 190)   # Apoyo
    ]

    pareja_cruda = getattr(batalla, "pareja_activa", ["Sidius Storm"])
    # Filtrado estricto contra valores None o vacíos
    pareja = [h for h in pareja_cruda if h]
    stats_party = getattr(batalla, "stats_party", {})
    heroe_activo_decision = batalla.obtener_heroe_activo_turno() if hasattr(batalla, "obtener_heroe_activo_turno") else None

    for idx, heroe in enumerate(pareja):
        if not heroe or idx >= len(heroes_pos):
            continue

        st_h = stats_party.get(heroe, {})
        if st_h.get("hp", 1) <= 0:
            continue

        hx, hy = heroes_pos[idx]

        pygame.draw.ellipse(pantalla, (0, 0, 0, 120), (hx + 20, hy + 230, 85, 20))

        if heroe == heroe_activo_decision and fase_combate == "TURNO_JUGADOR":
            pulso_pie = int(math.sin(tiempo_ms * 0.008) * 4)
            pygame.draw.ellipse(pantalla, (255, 215, 100), (hx + 15, hy + 225 - pulso_pie // 2, 95, 26 + pulso_pie), 2)

        offset_y = 0
        offset_x = 0
        estado_sprite = "guardia"

        es_atacante = getattr(batalla, "anim_heroe_atacando", None) == heroe
        if es_atacante:
            fase = getattr(batalla, "anim_fase", 0)
            if fase in [0, 1]:
                offset_y = -35
                offset_x = 18
                estado_sprite = "ataque"
            elif fase == 2:
                offset_y = -10
                offset_x = 5
                estado_sprite = "guardia"
        else:
            offset_y = int(math.sin(tiempo_ms * 0.003 + (idx * 1.5)) * 3)

        sprite_heroe = obtener_sprite_combate(heroe, estado_sprite, carpetas_buscar)
        if sprite_heroe:
            pantalla.blit(sprite_heroe, (hx + offset_x, hy + offset_y))

    # 5. BITÁCORA Y REGISTRO EN PANTALLA
    log_rect = pygame.Rect(40, 385, ancho_pantalla - 80, 32)
    pygame.draw.rect(pantalla, (20, 16, 25), log_rect)
    pygame.draw.rect(pantalla, (70, 60, 80), log_rect, 1)

    msg_actual = getattr(batalla, "mensaje_en_pantalla", "¡Combate en curso!")
    txt_log = fuentes["dialogo"].render(str(msg_actual), True, (245, 230, 210))
    pantalla.blit(txt_log, (log_rect.x + 12, log_rect.y + 8))

    # 6. PANELES DE COMANDOS Y ESTADO DEL GRUPO
    h_panel = 160
    y_panel = alto_pantalla - h_panel - 15

    rect_cmd = pygame.Rect(30, y_panel, 260, h_panel)
    pygame.draw.rect(pantalla, (18, 14, 22), rect_cmd)
    pygame.draw.rect(pantalla, (110, 100, 120), rect_cmd, 2)

    modo_menu = getattr(batalla, "modo_menu", "PRINCIPAL")

    if fase_combate == "TERMINADO":
        t_fin = fuentes["grande"].render(f"¡{resultado}!", True, (255, 215, 80))
        pantalla.blit(t_fin, (rect_cmd.x + 20, rect_cmd.y + 45))
        t_cont = fuentes["dialogo"].render("[ESPACIO] Salir de Combate", True, (200, 200, 200))
        pantalla.blit(t_cont, (rect_cmd.x + 20, rect_cmd.y + 85))

    elif fase_combate == "RESOLUCION":
        txt_res = fuentes["grande"].render("RESOLVIENDO...", True, (255, 215, 110))
        pantalla.blit(txt_res, (rect_cmd.x + 20, rect_cmd.y + 35))
        t_cont = fuentes["dialogo"].render("[ESPACIO] Siguiente Acción", True, (130, 220, 255))
        pantalla.blit(t_cont, (rect_cmd.x + 20, rect_cmd.y + 75))

    elif modo_menu == "OBJETOS":
        lbl_tit = fuentes["dialogo"].render("Usar Objeto:", True, (240, 220, 140))
        pantalla.blit(lbl_tit, (rect_cmd.x + 15, rect_cmd.y + 36))
        items = ["[1] Poción (+50 HP)", "[2] Éter (+15 MP)", "[ESC] Volver"]
        for i, it in enumerate(items):
            lbl = fuentes["dialogo"].render(it, True, (220, 220, 220))
            pantalla.blit(lbl, (rect_cmd.x + 15, rect_cmd.y + 58 + i * 20))

    else:
        tit_turno = f"TURNO: {heroe_activo_decision}" if heroe_activo_decision else "ACCIONES"
        txt_tit_cmd = fuentes["texto"].render(tit_turno, True, (255, 215, 110))
        pantalla.blit(txt_tit_cmd, (rect_cmd.x + 15, rect_cmd.y + 10))
        pygame.draw.line(pantalla, (70, 60, 80), (rect_cmd.x + 15, rect_cmd.y + 30), (rect_cmd.right - 15, rect_cmd.y + 30), 1)

        opciones = [
            ("[1] Atacar", (240, 240, 240)),
            ("[2] Habilidad Vínculo", (130, 200, 255)),
            ("[3] Guardia / Bloqueo", (110, 230, 160)),
            ("[4] Objetos", (220, 180, 100)),
            ("[H] Huir", (180, 180, 180))
        ]
        if es_grupo:
            opciones.append(("[TAB] Cambiar Objetivo", (255, 130, 160)))

        for i, (txt, col) in enumerate(opciones):
            lbl = fuentes["dialogo"].render(txt, True, col)
            pantalla.blit(lbl, (rect_cmd.x + 15, rect_cmd.y + 36 + i * 20))

    # Estado del Grupo
    rect_party = pygame.Rect(305, y_panel, ancho_pantalla - 335, h_panel)
    pygame.draw.rect(pantalla, (18, 14, 22), rect_party)
    pygame.draw.rect(pantalla, (110, 100, 120), rect_party, 2)

    txt_tit_party = fuentes["texto"].render("ESTADO DE VANGUARDIA", True, (200, 180, 160))
    pantalla.blit(txt_tit_party, (rect_party.x + 15, rect_party.y + 10))
    pygame.draw.line(pantalla, (70, 60, 80), (rect_party.x + 15, rect_party.y + 30), (rect_party.right - 15, rect_party.y + 30), 1)

    for i, heroe in enumerate(pareja):
        if not heroe:
            continue
        st_h = stats_party.get(heroe, {"hp": 110, "max_hp": 110, "mp": 15, "max_mp": 15})
        y_pos = rect_party.y + 40 + i * 50

        rol = "Líder" if i == 0 else "Apoyo"
        esta_vivo = st_h.get("hp", 0) > 0

        if esta_vivo:
            color_nombre = (240, 235, 240)
            texto_etiqueta = f"[{rol}] {heroe}"
        else:
            color_nombre = (160, 60, 60)
            texto_etiqueta = f"[{rol}] {heroe} (CAÍDO)"

        txt_h_nom = fuentes["texto"].render(texto_etiqueta, True, color_nombre)
        pantalla.blit(txt_h_nom, (rect_party.x + 15, y_pos))

        max_hp_h = max(1, st_h.get("max_hp", 100))
        hp_h = max(0, st_h.get("hp", 100))
        pct_hp = max(0.0, min(1.0, hp_h / max_hp_h))
        pygame.draw.rect(pantalla, (40, 15, 20), (rect_party.x + 180, y_pos + 4, 110, 10))
        pygame.draw.rect(pantalla, (210, 50, 60), (rect_party.x + 180, y_pos + 4, int(110 * pct_hp), 10))
        pygame.draw.rect(pantalla, (100, 80, 90), (rect_party.x + 180, y_pos + 4, 110, 10), 1)

        txt_hp = fuentes["dialogo"].render(f"HP {hp_h}/{max_hp_h}", True, (220, 220, 220))
        pantalla.blit(txt_hp, (rect_party.x + 300, y_pos + 1))

        max_mp_h = max(1, st_h.get("max_mp", 15))
        mp_h = max(0, st_h.get("mp", 15))
        pct_mp = max(0.0, min(1.0, mp_h / max_mp_h))
        pygame.draw.rect(pantalla, (15, 25, 45), (rect_party.x + 180, y_pos + 20, 110, 8))
        pygame.draw.rect(pantalla, (50, 140, 230), (rect_party.x + 180, y_pos + 20, int(110 * pct_mp), 8))
        pygame.draw.rect(pantalla, (80, 90, 110), (rect_party.x + 180, y_pos + 20, 110, 8), 1)

        txt_mp = fuentes["dialogo"].render(f"MP {mp_h}/{max_mp_h}", True, (170, 200, 240))
        pantalla.blit(txt_mp, (rect_party.x + 300, y_pos + 17))