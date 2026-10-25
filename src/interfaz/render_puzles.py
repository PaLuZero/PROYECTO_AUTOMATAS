import time
import math
import pygame

def dibujar_overlay_puzle(pantalla, puzle, fuentes, ancho_pantalla=800, alto_pantalla=600):
    if not puzle:
        return

    # Fondo semi-transparente
    overlay = pygame.Surface((ancho_pantalla, alto_pantalla), pygame.SRCALPHA)
    overlay.fill((10, 8, 16, 210))
    pantalla.blit(overlay, (0, 0))

    ancho_caja = 560
    alto_caja = 360
    cx = (ancho_pantalla - ancho_caja) // 2
    cy = (alto_pantalla - alto_caja) // 2

    caja = pygame.Rect(cx, cy, ancho_caja, alto_caja)
    pygame.draw.rect(pantalla, (20, 18, 28), caja)
    pygame.draw.rect(pantalla, (80, 180, 240), caja, 2)

    mision = puzle["mision"]
    txt_tit = fuentes["grande"].render(f"PUZLE: {mision['nombre'].upper()}", True, (255, 215, 80))
    pantalla.blit(txt_tit, (cx + 25, cy + 20))

    tipo = puzle["tipo"]

    # 1. TIMING DE BARRA (SIDIUS)
    if tipo == "TIMING_BARRA":
        txt_desc = fuentes["dialogo"].render("Presiona [ESPACIO] cuando la aguja entre en la zona verde.", True, (220, 220, 220))
        pantalla.blit(txt_desc, (cx + 25, cy + 65))

        # Actualizar aguja
        dt = 0.016
        puzle["pos_aguja"] += puzle["velocidad_aguja"] * puzle["direccion_aguja"] * dt
        if puzle["pos_aguja"] >= 1.0:
            puzle["pos_aguja"] = 1.0
            puzle["direccion_aguja"] = -1
        elif puzle["pos_aguja"] <= 0.0:
            puzle["pos_aguja"] = 0.0
            puzle["direccion_aguja"] = 1

        bw, bh = 460, 36
        bx, by = cx + 50, cy + 140
        pygame.draw.rect(pantalla, (40, 35, 50), (bx, by, bw, bh))

        # Zona verde de éxito
        zx1, zx2 = puzle["zona_exito"]
        verde_x = int(bx + zx1 * bw)
        verde_w = int((zx2 - zx1) * bw)
        pygame.draw.rect(pantalla, (50, 190, 90), (verde_x, by, verde_w, bh))
        pygame.draw.rect(pantalla, (200, 200, 200), (bx, by, bw, bh), 2)

        # Aguja móvil
        ax = int(bx + puzle["pos_aguja"] * bw)
        pygame.draw.line(pantalla, (255, 60, 60), (ax, by - 8), (ax, by + bh + 8), 4)

        lbl_espacio = fuentes["texto"].render("[ESPACIO] Aplicar Fuerza Hidráulica", True, (255, 255, 255))
        pantalla.blit(lbl_espacio, (cx + ancho_caja // 2 - lbl_espacio.get_width() // 2, cy + 240))

    # 2. MEMORIA DE RUNAS (SELENE)
    elif tipo == "MEMORIA_RUNAS":
        t_pasado = time.time() - puzle["tiempo_inicio"]
        t_memo = puzle["tiempo_memorizar"]

        if t_pasado < t_memo:
            txt_estado = fuentes["grande"].render("¡MEMORIZA LA SECUENCIA DE RUNAS!", True, (100, 220, 255))
            pantalla.blit(txt_estado, (cx + 25, cy + 65))

            secuencia_str = "   ".join([f"[{r}]" for r in puzle["secuencia"]])
            txt_sec = fuentes["puzle"].render(secuencia_str, True, (255, 215, 80))
            pantalla.blit(txt_sec, (cx + ancho_caja // 2 - txt_sec.get_width() // 2, cy + 145))

            pct_tiempo = max(0.0, 1.0 - (t_pasado / t_memo))
            pygame.draw.rect(pantalla, (40, 35, 50), (cx + 50, cy + 220, 460, 12))
            pygame.draw.rect(pantalla, (80, 200, 240), (cx + 50, cy + 220, int(460 * pct_tiempo), 12))
        else:
            txt_estado = fuentes["grande"].render("REPRODUCE EL ORDEN: Pulsa [1], [2], [3] o [4]", True, (240, 230, 140))
            pantalla.blit(txt_estado, (cx + 25, cy + 65))

            ingresado_str = "   ".join([f"[{r}]" for r in puzle["ingresado"]]) or "(Esperando primera runa...)"
            txt_ing = fuentes["texto"].render(f"Ingresadas: {ingresado_str}", True, (200, 240, 200))
            pantalla.blit(txt_ing, (cx + 50, cy + 150))

    # 3. REACCIÓN DE BRECHA CUÁNTICA CON SÍMBOLOS (NOCTIS)
    elif tipo == "REACCION_PARADOJA":
        t_restante = max(0.0, puzle["tiempo_limite"] - (time.time() - puzle["tiempo_inicio"]))
        pct_t = max(0.0, min(1.0, t_restante / puzle["tiempo_limite"]))

        txt_aviso = fuentes["texto"].render(f"COLAPSO DE BRECHA EN: {t_restante:.1f}s", True, (255, 80, 80) if t_restante < 1.0 else (240, 200, 80))
        pantalla.blit(txt_aviso, (cx + ancho_caja // 2 - txt_aviso.get_width() // 2, cy + 55))

        # Barra de tiempo regresiva
        pygame.draw.rect(pantalla, (35, 25, 45), (cx + 60, cy + 78, 440, 10))
        col_barra = (255, 60, 60) if t_restante < 1.0 else (200, 80, 240)
        pygame.draw.rect(pantalla, col_barra, (cx + 60, cy + 78, int(440 * pct_t), 10))

        txt_inst = fuentes["dialogo"].render("Sintoniza la frecuencia que estabiliza la anomalía detectada:", True, (210, 210, 220))
        pantalla.blit(txt_inst, (cx + 45, cy + 100))

        # Cuadro central con la anomalía detectada
        box_anomalia = pygame.Rect(cx + ancho_caja // 2 - 120, cy + 125, 240, 55)
        pygame.draw.rect(pantalla, (25, 15, 35), box_anomalia)
        pygame.draw.rect(pantalla, puzle["color_objetivo"], box_anomalia, 2)

        txt_simbolo = fuentes["puzle"].render(puzle["simbolo_objetivo"], True, puzle["color_objetivo"])
        pantalla.blit(txt_simbolo, (box_anomalia.centerx - txt_simbolo.get_width() // 2, box_anomalia.centery - txt_simbolo.get_height() // 2))

        # 3 Botones con sus frecuencias claras
        anch_b = 140
        for i, freq in enumerate(puzle["frecuencias"]):
            bx = cx + 55 + i * (anch_b + 25)
            by = cy + 215
            rect_btn = pygame.Rect(bx, by, anch_b, 65)

            pygame.draw.rect(pantalla, (30, 22, 40), rect_btn)
            pygame.draw.rect(pantalla, (120, 90, 150), rect_btn, 1)

            t_tecla = fuentes["grande"].render(f"[{freq['id']}]", True, (255, 255, 255))
            pantalla.blit(t_tecla, (rect_btn.centerx - t_tecla.get_width() // 2, rect_btn.y + 8))

            t_nom = fuentes["dialogo"].render(freq["simbolo"], True, freq["color"])
            pantalla.blit(t_nom, (rect_btn.centerx - t_nom.get_width() // 2, rect_btn.y + 35))

    # 4. FAROLES E INTERRUPTORES (ATHINA)
    elif tipo == "FAROLES_INTERRUPTORES":
        txt_desc = fuentes["dialogo"].render("Extingue todos los prismas. Cada interruptor altera a sus vecinos.", True, (220, 220, 220))
        pantalla.blit(txt_desc, (cx + 25, cy + 65))

        for i, encendido in enumerate(puzle["estados"]):
            fx = cx + 110 + i * 140
            fy = cy + 140
            pygame.draw.rect(pantalla, (40, 30, 50), (fx, fy, 70, 70))
            col_luz = (240, 200, 80) if encendido else (60, 50, 70)
            pygame.draw.circle(pantalla, col_luz, (fx + 35, fy + 35), 22)
            pygame.draw.rect(pantalla, (160, 140, 180), (fx, fy, 70, 70), 2)

            t_num = fuentes["grande"].render(f"[{i+1}]", True, (255, 255, 255))
            pantalla.blit(t_num, (fx + 22, fy + 80))