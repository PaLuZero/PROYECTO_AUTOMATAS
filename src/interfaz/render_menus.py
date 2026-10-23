import pygame

# 1. HUD INFERIOR EXACTO A LA REFERENCIA
def dibujar_hud(pantalla, juego, ancho_pantalla):
    y_hud = 480
    alto_hud = 120

    rect_hud = pygame.Rect(0, y_hud, ancho_pantalla, alto_hud)
    pygame.draw.rect(pantalla, (10, 10, 14), rect_hud)
    pygame.draw.line(pantalla, (45, 45, 60), (0, y_hud), (ancho_pantalla, y_hud), 2)

    st = juego.reloj.obtener_estado()
    es_crep = st["es_crepusculo"]

    # Fila 1: FASE (izq) y ZONA (der)
    col_fase = (240, 100, 160) if es_crep else (100, 240, 140)
    txt_fase = juego.fuentes["texto"].render(f"FASE: {st['nombre']}  [{st['barra']}]", True, col_fase)
    pantalla.blit(txt_fase, (16, y_hud + 8))

    txt_zona = juego.fuentes["texto"].render(f"ZONA: {juego.zona_actual}", True, (200, 200, 215))
    pantalla.blit(txt_zona, (ancho_pantalla - txt_zona.get_width() - 20, y_hud + 8))

    # Fila 2: Oro, Mochila y Atajos
    t_oro = f"ORO: {juego.monedas}"
    t_mochila = f"MOCHILA: {len(juego.inventario_objetos)} items"
    t_equipo = "[M]: EQUIPO"
    t_grupo = "[F]: ESTADO / GRUPO"
    linea2 = f"{t_oro}   |   {t_mochila}   |   {t_equipo}   |   {t_grupo}"
    txt_l2 = juego.fuentes["texto"].render(linea2, True, (245, 205, 80))
    pantalla.blit(txt_l2, (16, y_hud + 34))

    # Fila 3: Stats de la Vanguardia (Líder y Apoyo)
    lider = juego.pareja_activa[0]
    st_lid = juego.stats_heroes[lider]
    txt_lid_str = f"LÍDER: {lider} [Nv.{st_lid['nivel']} | {st_lid['hp']}/{st_lid['max_hp']} HP | {st_lid['mp']} MP]"
    txt_lid = juego.fuentes["texto"].render(txt_lid_str, True, (100, 215, 255))
    pantalla.blit(txt_lid, (16, y_hud + 60))

    apoyo = juego.pareja_activa[1]
    if apoyo:
        st_ap = juego.stats_heroes[apoyo]
        txt_ap_str = f"APOYO: {apoyo} [Nv.{st_ap['nivel']} | {st_ap['hp']}/{st_ap['max_hp']} HP | {st_ap['mp']} MP]"
    else:
        txt_ap_str = "APOYO: (Sin asignar)"
    txt_ap = juego.fuentes["texto"].render(txt_ap_str, True, (100, 215, 255))
    pantalla.blit(txt_ap, (415, y_hud + 60))

    # Fila 4: Bitácora de diálogo e indicaciones
    txt_d1 = juego.fuentes["dialogo"].render(juego.dialogo_linea1, True, (240, 235, 230))
    pantalla.blit(txt_d1, (16, y_hud + 88))

# 2. MENÚ DE FORMACIÓN 
CITAS_HEROES = {
    "Sidius Storm": "\"La materia obedece a la voluntad inquebrantable. Ninguna espada romperá mi resolución.\"",
    "Selene Moon": "\"Los recuerdos nos anclan a la realidad. Olvidar es la verdadera derrota ante el vacío.\"",
    "Noctis Reverie": "\"Cada instante es una bifurcación de infinitas posibilidades. Elegiremos la que nos salve.\"",
    "Athina Nightwish": "\"Athina observa desde la penumbra. Las sombras son su refugio.\""
}

def dibujar_menu_formacion(pantalla, juego, ancho_pantalla, alto_pantalla):
    pantalla.fill((10, 8, 14))

    # Sidebar izquierda con atajos
    sidebar_x = 10
    sidebar_y = 50
    botones_nav = [
        ("[F]", "Grupo"),
        ("[M]", "Mochila"),
        ("[TAB]", "Puesto"),
        ("[ESC]", "Salir")
    ]
    for i, (tecla, etiqueta) in enumerate(botones_nav):
        by = sidebar_y + i * 58
        t_k = juego.fuentes["grande"].render(tecla, True, (240, 200, 90))
        pantalla.blit(t_k, (sidebar_x + 12, by))
        t_lbl = juego.fuentes["dialogo"].render(etiqueta, True, (160, 160, 180))
        pantalla.blit(t_lbl, (sidebar_x + 8, by + 20))

    # Encabezado superior
    rol_txt = "LÍDER (Pos. 1)" if juego.slot_formacion_seleccionando == 0 else "APOYO (Pos. 2)"
    txt_header = f"ASIGNANDO A: {rol_txt}   |   [TAB: Alternar Puesto   |   ESPACIO/ENTER: Asignar Héroe]"
    lbl_h = juego.fuentes["grande"].render(txt_header, True, (245, 215, 80))
    pantalla.blit(lbl_h, (95, 16))
    pygame.draw.line(pantalla, (45, 45, 60), (95, 42), (ancho_pantalla - 15, 42), 1)

    todos_heroes = ["Sidius Storm", "Selene Moon", "Noctis Reverie", "Athina Nightwish"]
    inicio_x = 95
    ancho_total = ancho_pantalla - inicio_x - 15
    ancho_col = ancho_total // 4

    for i, h_nom in enumerate(todos_heroes):
        col_x = inicio_x + i * ancho_col
        esta_sel = (i == juego.indice_seleccion_fh)
        desbloqueado = h_nom in juego.companeros_desbloqueados
        st = juego.stats_heroes[h_nom]

        # Marco de selección dorado de la columna completa
        if esta_sel:
            rect_sel = pygame.Rect(col_x + 3, 50, ancho_col - 6, 424)
            pygame.draw.rect(pantalla, (235, 185, 55), rect_sel, 2)

        # Nombre corto
        nom_corto = h_nom.split()[0]
        t_nom = juego.fuentes["grande"].render(nom_corto, True, (255, 255, 255) if desbloqueado else (90, 85, 95))
        pantalla.blit(t_nom, (col_x + ancho_col // 2 - t_nom.get_width() // 2, 58))

        # Rol actual: LÍDER / APOYO / RESERVA / BLOQUEADO
        if not desbloqueado:
            rol_etiqueta = "[ BLOQUEADO ]"
            col_rol = (100, 90, 105)
        elif juego.pareja_activa[0] == h_nom:
            rol_etiqueta = "[ LÍDER ]"
            col_rol = (100, 220, 255)
        elif juego.pareja_activa[1] == h_nom:
            rol_etiqueta = "[ APOYO ]"
            col_rol = (100, 240, 150)
        else:
            rol_etiqueta = "[ RESERVA ]"
            col_rol = (170, 165, 180)
        t_rol = juego.fuentes["dialogo"].render(rol_etiqueta, True, col_rol)
        pantalla.blit(t_rol, (col_x + ancho_col // 2 - t_rol.get_width() // 2, 78))

        # Vínculo (solo si está reclutado)
        if desbloqueado:
            t_vinc = juego.fuentes["dialogo"].render(f"Vínculo {st['vinculo']}", True, (180, 140, 230))
            pantalla.blit(t_vinc, (col_x + ancho_col // 2 - t_vinc.get_width() // 2, 96))

        # Cuerpo completo a escala real grande 
        img_standee = juego.retratos_heroes.get(h_nom)
        if img_standee and desbloqueado:
            rw, rh = img_standee.get_size()
            alto_max = 280
            ancho_calc = int(alto_max * (rw / rh))
            img_esc = pygame.transform.scale(img_standee, (ancho_calc, alto_max))
            pos_y_standee = 390 - alto_max
            pantalla.blit(img_esc, (col_x + ancho_col // 2 - ancho_calc // 2, pos_y_standee))
        else:
            t_bloq = juego.fuentes["dialogo"].render("[ NO RECLUTADO ]", True, (100, 85, 110))
            pantalla.blit(t_bloq, (col_x + ancho_col // 2 - t_bloq.get_width() // 2, 230))

        # BARRAS DE ATRIBUTOS: Solo si el héroe está desbloqueado
        if desbloqueado:
            y_barras = 390
            bw = ancho_col - 16
            bx = col_x + 8

            # Barra de Cuerpo (HP) - Roja
            pct_hp = max(0.0, min(1.0, st["hp"] / max(1, st["max_hp"])))
            pygame.draw.rect(pantalla, (45, 15, 20), (bx, y_barras, bw, 13))
            pygame.draw.rect(pantalla, (215, 45, 55), (bx, y_barras, int(bw * pct_hp), 13))
            txt_hp = juego.fuentes["dialogo"].render(f"Cuerpo  {st['hp']}/{st['max_hp']}", True, (255, 255, 255))
            pantalla.blit(txt_hp, (bx + 3, y_barras - 1))

            # Barra de Mente (MP) - Azul
            pct_mp = max(0.0, min(1.0, st["mp"] / max(1, st["max_mp"])))
            pygame.draw.rect(pantalla, (15, 25, 45), (bx, y_barras + 16, bw, 13))
            pygame.draw.rect(pantalla, (45, 125, 230), (bx, y_barras + 16, int(bw * pct_mp), 13))
            txt_mp = juego.fuentes["dialogo"].render(f"Mente   {st['mp']}/{st['max_mp']}", True, (255, 255, 255))
            pantalla.blit(txt_mp, (bx + 3, y_barras + 15))

            # Barra de EXP 
            exp_req = st.get("exp_sig", 50)
            pct_exp = max(0.0, min(1.0, st["exp"] / max(1, exp_req)))
            pygame.draw.rect(pantalla, (35, 30, 20), (bx, y_barras + 32, bw, 13))
            pygame.draw.rect(pantalla, (160, 130, 45), (bx, y_barras + 32, int(bw * pct_exp), 13))
            txt_exp = juego.fuentes["dialogo"].render(f"Nv.{st['nivel']}   EXP {st['exp']}/{exp_req}", True, (255, 255, 255))
            pantalla.blit(txt_exp, (bx + 3, y_barras + 31))

            # Estado del arma
            arma = st["equipo"].get("arma")
            txt_arma = f"Arma: {arma}" if arma else f"Arma: Desarmado (+{st['atk_bono']} ATK)"
            lbl_arma = juego.fuentes["dialogo"].render(txt_arma, True, (150, 150, 165))
            pantalla.blit(lbl_arma, (bx, y_barras + 49))

    # Panel inferior de cita y descripción temática
    heroe_activo = todos_heroes[juego.indice_seleccion_fh]
    desbloqueado_activo = heroe_activo in juego.companeros_desbloqueados

    rect_cita = pygame.Rect(95, 482, ancho_total, 102)
    pygame.draw.rect(pantalla, (16, 14, 22), rect_cita)
    pygame.draw.rect(pantalla, (45, 45, 60), rect_cita, 1)

    if desbloqueado_activo:
        t_nom_cita = juego.fuentes["grande"].render(f"{heroe_activo.upper()}:", True, (245, 215, 80))
        pantalla.blit(t_nom_cita, (rect_cita.x + 18, rect_cita.y + 12))

        cita_str = CITAS_HEROES.get(heroe_activo, "\"La vanguardia avanza sin vacilar.\"")
        t_cita = juego.fuentes["texto"].render(cita_str, True, (220, 215, 230))
        pantalla.blit(t_cita, (rect_cita.x + 18, rect_cita.y + 38))
    else:
        t_nom_cita = juego.fuentes["grande"].render(f"PORTADOR NO RECLUTADO", True, (160, 140, 170))
        pantalla.blit(t_nom_cita, (rect_cita.x + 18, rect_cita.y + 12))
        t_cita = juego.fuentes["texto"].render("Explora las calles y recintos del Santuario para reclutar a este compañero.", True, (130, 120, 140))
        pantalla.blit(t_cita, (rect_cita.x + 18, rect_cita.y + 38))


# 3. OVERLAY DE DIÁLOGOS
def dibujar_dialogo_overlay(pantalla, juego, ancho_pantalla=800, alto_pantalla=600):
    c = juego.conversacion_activa
    if not c:
        return

    filtro_oscuro = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
    filtro_oscuro.fill((0, 0, 0, 150))
    pantalla.blit(filtro_oscuro, (0, 0))

    st = juego.reloj.obtener_estado()
    es_crep = st["es_crepusculo"]

    retrato_dibujar = None
    id_conversacion = c.get("id", "")
    nombre_hablante = c.get("nombre", "")

    # Selector dinámico
    if id_conversacion == "Vaelira_Contriel":
        retrato_dibujar = juego.retrato_vaelira_crep if es_crep else juego.retrato_vaelira_normal
    elif id_conversacion in ["Herrero_Doran", "carlos", "Carlos"]:
        retrato_dibujar = juego.retrato_carlos_crep if es_crep else juego.retrato_carlos_normal
    elif nombre_hablante in juego.retratos_heroes:
        retrato_dibujar = juego.retratos_heroes.get(nombre_hablante)
    else:
        for heroe_nombre in juego.retratos_heroes:
            if heroe_nombre in id_conversacion or heroe_nombre in nombre_hablante:
                retrato_dibujar = juego.retratos_heroes[heroe_nombre]
                break

    if not retrato_dibujar and hasattr(juego, "sprites_npcs_normal"):
        dict_sp = juego.sprites_npcs_crep if es_crep else juego.sprites_npcs_normal
        retrato_dibujar = dict_sp.get(id_conversacion)

    caja_ancho = 720
    caja_alto = 430
    cx = (ancho_pantalla - caja_ancho) // 2
    cy = 28

    rect_caja = pygame.Rect(cx, cy, caja_ancho, caja_alto)
    pygame.draw.rect(pantalla, (20, 20, 32), rect_caja)
    pygame.draw.rect(pantalla, (230, 185, 60), rect_caja, 3)

    txt_titulo = juego.fuentes["grande"].render(f"HABLANDO CON: {nombre_hablante.upper()}", True, (245, 215, 80))
    pantalla.blit(txt_titulo, (cx + 25, cy + 18))

    frame_ancho = 185
    frame_alto = 345
    frame_x = cx + 25
    frame_y = cy + 55

    rect_frame = pygame.Rect(frame_x, frame_y, frame_ancho, frame_alto)
    pygame.draw.rect(pantalla, (12, 12, 20), rect_frame)
    pygame.draw.rect(pantalla, (220, 120, 45), rect_frame, 2)

    if retrato_dibujar:
        rw, rh = retrato_dibujar.get_size()
        max_h = frame_alto - 16
        max_w = frame_ancho - 16
        escala = min(max_w / rw, max_h / rh)
        nw = int(rw * escala)
        nh = int(rh * escala)

        img_esc = pygame.transform.scale(retrato_dibujar, (nw, nh))
        pos_img_x = frame_x + (frame_ancho - nw) // 2
        pos_img_y = frame_y + (frame_alto - nh) // 2
        pantalla.blit(img_esc, (pos_img_x, pos_img_y))
    else:
        txt_sin_img = juego.fuentes["dialogo"].render("[Sin Retrato]", True, (130, 120, 140))
        pantalla.blit(txt_sin_img, (frame_x + frame_ancho // 2 - txt_sin_img.get_width() // 2, frame_y + frame_alto // 2))

    texto_x = frame_x + frame_ancho + 25
    texto_w = caja_ancho - frame_ancho - 65
    texto_y = frame_y + 10

    if c.get("respuesta_elegida"):
        texto_resp = c["respuesta_elegida"]
        palabras = texto_resp.split(" ")
        lineas = []
        linea_act = ""
        for p in palabras:
            prueba = linea_act + p + " "
            if juego.fuentes["dialogo"].size(prueba)[0] < texto_w:
                linea_act = prueba
            else:
                lineas.append(linea_act)
                linea_act = p + " "
        lineas.append(linea_act)

        for i, l in enumerate(lineas):
            lbl_linea = juego.fuentes["dialogo"].render(l, True, (245, 240, 245))
            pantalla.blit(lbl_linea, (texto_x, texto_y + i * 22))

        pygame.draw.line(pantalla, (55, 60, 85), (texto_x, cy + caja_alto - 65), (cx + caja_ancho - 25, cy + caja_alto - 65), 1)
        txt_continuar = juego.fuentes["texto"].render("[ESPACIO / ENTER / E] Continuar", True, (120, 215, 255))
        pantalla.blit(txt_continuar, (texto_x, cy + caja_alto - 45))

    else:
        txt_saludo = c.get("saludo", "")
        palabras = txt_saludo.split(" ")
        lineas = []
        linea_act = ""
        for p in palabras:
            prueba = linea_act + p + " "
            if juego.fuentes["dialogo"].size(prueba)[0] < texto_w:
                linea_act = prueba
            else:
                lineas.append(linea_act)
                linea_act = p + " "
        lineas.append(linea_act)

        for i, l in enumerate(lineas[:3]):
            lbl_l = juego.fuentes["dialogo"].render(l, True, (235, 230, 240))
            pantalla.blit(lbl_l, (texto_x, texto_y + i * 22))

        y_div = texto_y + max(70, len(lineas[:3]) * 24 + 5)
        pygame.draw.line(pantalla, (55, 60, 85), (texto_x, y_div), (cx + caja_ancho - 25, y_div), 1)

        txt_prompt = juego.fuentes["texto"].render("Elige tu opción con [1], [2] o [3]:", True, (100, 200, 245))
        pantalla.blit(txt_prompt, (texto_x, y_div + 15))

        y_opc = y_div + 45
        for i, opc in enumerate(c.get("opciones", [])):
            disponible = opc.get("disponible", True)
            col_opc = (245, 245, 250) if disponible else (130, 95, 105)
            txt_opc = juego.fuentes["dialogo"].render(opc["texto"], True, col_opc)
            pantalla.blit(txt_opc, (texto_x, y_opc + i * 36))


# 4. MENÚ DE MOCHILA (SEPARACIÓN CLARA ENTRE CONSUMIBLES Y EQUIPO)
def dibujar_menu_mochila(pantalla, juego, ancho_pantalla, alto_pantalla):
    overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
    overlay.fill((12, 10, 18, 230))
    pantalla.blit(overlay, (0, 0))

    cx, cy = 60, 45
    cw, ch = ancho_pantalla - 120, alto_pantalla - 90
    pygame.draw.rect(pantalla, (22, 18, 28), (cx, cy, cw, ch))
    pygame.draw.rect(pantalla, (110, 95, 140), (cx, cy, cw, ch), 2)

    tit = juego.fuentes["grande"].render("ALFORJA Y EQUIPAMIENTO DE VANGUARDIA", True, (255, 215, 90))
    pantalla.blit(tit, (cx + 25, cy + 18))
    pygame.draw.line(pantalla, (70, 60, 90), (cx + 25, cy + 44), (cx + cw - 25, cy + 44), 1)

    heroe = juego.companeros_desbloqueados[juego.indice_heroe_mochila]
    st = juego.stats_heroes[heroe]
    txt_h = juego.fuentes["texto"].render(f"HÉROE: {heroe} (Nv. {st['nivel']}) - [TAB] Cambiar Héroe", True, (130, 220, 255))
    pantalla.blit(txt_h, (cx + 25, cy + 54))

    eq = st["equipo"]
    y_eq = cy + 85
    txt_arma = juego.fuentes["dialogo"].render(f"Arma: {eq.get('arma') or 'Ninguna (+0 ATK)'}", True, (220, 220, 220))
    txt_armad = juego.fuentes["dialogo"].render(f"Armadura: {eq.get('armadura') or 'Ninguna (+0 HP)'}", True, (220, 220, 220))
    txt_acc = juego.fuentes["dialogo"].render(f"Accesorio: {eq.get('accesorio') or 'Ninguno (+0 MP)'}", True, (220, 220, 220))
    pantalla.blit(txt_arma, (cx + 25, y_eq))
    pantalla.blit(txt_armad, (cx + 25, y_eq + 20))
    pantalla.blit(txt_acc, (cx + 25, y_eq + 40))

    pygame.draw.line(pantalla, (70, 60, 90), (cx + 25, y_eq + 68), (cx + cw - 25, y_eq + 68), 1)

    # Identificar piezas equipables en la bolsa
    piezas_equipables = [it for it in juego.inventario_objetos if any(eq_i["nombre"] == it for eq_i in juego.CATALOGO_ARMERIA)]
    consumibles = [it for it in juego.inventario_objetos if it not in piezas_equipables]

    # Columna Izquierda: EQUIPAMIENTO INTERACTIVO 
    lbl_eq = juego.fuentes["texto"].render("PIEZAS PARA EQUIPAR (Presiona el número):", True, (240, 215, 90))
    pantalla.blit(lbl_eq, (cx + 25, y_eq + 78))

    if not piezas_equipables:
        pantalla.blit(juego.fuentes["dialogo"].render("(No tienes armaduras ni armas en la bolsa)", True, (130, 125, 140)), (cx + 25, y_eq + 104))
    else:
        for idx, pieza in enumerate(piezas_equipables[:6]):
            info_eq = next((eq_i for eq_i in juego.CATALOGO_ARMERIA if eq_i["nombre"] == pieza), {})
            ranura = info_eq.get("ranura", "equipo").upper()
            bono = info_eq.get("bono", 0)
            lbl_p = juego.fuentes["dialogo"].render(f"[{idx+1}] {pieza}  ({ranura} +{bono})", True, (120, 240, 160))
            pantalla.blit(lbl_p, (cx + 25, y_eq + 104 + idx * 24))

    # Columna Derecha: CONSUMIBLES
    col_der_x = cx + 360
    lbl_con = juego.fuentes["texto"].render("CONSUMIBLES (Uso en Combate):", True, (180, 200, 230))
    pantalla.blit(lbl_con, (col_der_x, y_eq + 78))

    if not consumibles:
        pantalla.blit(juego.fuentes["dialogo"].render("(Sin pociones ni elixires)", True, (130, 125, 140)), (col_der_x, y_eq + 104))
    else:
        for idx, con in enumerate(consumibles[:8]):
            lbl_c = juego.fuentes["dialogo"].render(f"• {con}", True, (220, 215, 230))
            pantalla.blit(lbl_c, (col_der_x, y_eq + 104 + idx * 22))

    lbl_cerrar = juego.fuentes["dialogo"].render("[ESC/M] Cerrar Mochila   [D] Desequipar Todo de " + heroe.split()[0], True, (160, 160, 170))
    pantalla.blit(lbl_cerrar, (cx + 25, cy + ch - 26))

# MENÚ DE TIENDA
def dibujar_menu_tienda(pantalla, juego, ancho_pantalla, alto_pantalla):
    overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
    overlay.fill((12, 10, 18, 225))
    pantalla.blit(overlay, (0, 0))

    cx, cy = 80, 55
    cw, ch = ancho_pantalla - 160, alto_pantalla - 110
    pygame.draw.rect(pantalla, (22, 18, 28), (cx, cy, cw, ch))
    pygame.draw.rect(pantalla, (180, 140, 80), (cx, cy, cw, ch), 2)

    es_forja = juego.zona_actual == "FORJA"
    titulo = "ARMERÍA DE CARLOS" if es_forja else "BOTICA DE SUMINISTROS"
    catalogo = juego.CATALOGO_ARMERIA if es_forja else juego.CATALOGO_TIENDA

    t_tit = juego.fuentes["grande"].render(titulo, True, (255, 215, 90))
    pantalla.blit(t_tit, (cx + 25, cy + 18))
    t_oro = juego.fuentes["texto"].render(f"Oro Disponible: {juego.monedas} monedas", True, (255, 230, 110))
    pantalla.blit(t_oro, (cx + cw - t_oro.get_width() - 25, cy + 20))
    pygame.draw.line(pantalla, (80, 65, 50), (cx + 25, cy + 44), (cx + cw - 25, cy + 44), 1)

    for i, it in enumerate(catalogo):
        y_pos = cy + 62 + i * 55
        rect_it = pygame.Rect(cx + 20, y_pos, cw - 40, 46)
        pygame.draw.rect(pantalla, (32, 26, 38), rect_it)
        pygame.draw.rect(pantalla, (70, 60, 80), rect_it, 1)

        t_nom = juego.fuentes["texto"].render(f"[{i+1}] {it['nombre']}", True, (240, 235, 240))
        pantalla.blit(t_nom, (rect_it.x + 15, rect_it.y + 6))
        t_desc = juego.fuentes["dialogo"].render(it.get("desc", ""), True, (170, 165, 180))
        pantalla.blit(t_desc, (rect_it.x + 15, rect_it.y + 24))
        t_costo = juego.fuentes["texto"].render(f"{it['precio']} oro", True, (255, 215, 90))
        pantalla.blit(t_costo, (rect_it.right - t_costo.get_width() - 15, rect_it.y + 12))

    lbl_cerrar = juego.fuentes["dialogo"].render("[ESC/T] Salir de la Tienda", True, (160, 160, 170))
    pantalla.blit(lbl_cerrar, (cx + 25, cy + ch - 26))