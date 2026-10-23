import os
import pygame

class GestorTilesetCiudad:
    def __init__(self, tamano_tile=40):
        self.tamano_tile = tamano_tile
        self.cargado = False

        self.casa_forja = None
        self.casa_biblioteca = None
        self.casa_botica = None
        self.casa_taller = None
        self.santuario_central = None

        self.tile_pasto = None
        self.tile_adoquin = None

    def cargar(self, carpetas_buscar):
        tw = self.tamano_tile

        def cargar_sprite(nombres, w_px, h_px):
            for c in carpetas_buscar:
                for nom in nombres:
                    ruta = os.path.join(c, nom)
                    if os.path.exists(ruta):
                        try:
                            img = pygame.image.load(ruta).convert_alpha()
                            return pygame.transform.scale(img, (int(w_px), int(h_px)))
                        except Exception:
                            pass
            return None

        # 1. Casas 
        b3 = tw * 3
        self.casa_forja = cargar_sprite(["House_Hay_4_Purple.png", "house_hay_4_purple.png"], b3, b3)
        self.casa_biblioteca = cargar_sprite(["House_Hay_3.png", "house_hay_3.png"], b3, b3)
        self.casa_botica = cargar_sprite(["House_Hay_2.png", "house_hay_2.png"], b3, b3)
        self.casa_taller = cargar_sprite(["House_Hay_1.png", "house_hay_1.png"], b3, b3)

        # 2. Gran Santuario Central 
        self.santuario_central = cargar_sprite(
            ["santuario_central.png", "santuario.png", "santuario_central.PNG"],
            tw * 8,
            int(tw * 4.5)
        )

        # 3. Tileset de Terreno 
        hoja_suelo = None
        for c in carpetas_buscar:
            for nom in ["suelo_tileset.png", "suelo_tileset.PNG", "suelo_tileset.jpg"]:
                ruta = os.path.join(c, nom)
                if os.path.exists(ruta):
                    try:
                        hoja_suelo = pygame.image.load(ruta).convert_alpha()
                        break
                    except Exception:
                        pass
            if hoja_suelo:
                break

        if hoja_suelo:
            sw, sh = hoja_suelo.get_size()
            cw = sw / 10.0
            ch = sh / 8.0

            def cortar(cx, cy):
                rx = int(cx * cw)
                ry = int(cy * ch)
                rect = pygame.Rect(rx, ry, int(cw), int(ch))
                sub = hoja_suelo.subsurface(rect).copy()
                return pygame.transform.scale(sub, (tw, tw))

            self.tile_pasto = cortar(6.5, 1.0)
            self.tile_adoquin = cortar(4.5, 3.5)

        self.cargado = any([self.casa_forja, self.casa_biblioteca, self.santuario_central])
        return self.cargado

    def aplicar_tinte_crepuscular(self, superficie):
        s = superficie.copy()
        filtro = pygame.Surface(s.get_size(), pygame.SRCALPHA)
        filtro.fill((65, 30, 95, 95))
        s.blit(filtro, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        return s

    def dibujar_muro_procedural(self, pantalla, col, fila, total_cols, total_filas, es_crepusculo):
        tw = self.tamano_tile
        rect = pygame.Rect(col * tw, fila * tw, tw, tw)

        es_sup = (fila == 0)
        es_inf = (fila == total_filas - 1)
        es_izq = (col == 0)
        es_der = (col == total_cols - 1)

        # Paleta tomada directamente de las casas
        col_piedra_base = (205, 198, 180) if not es_crepusculo else (85, 70, 90)
        col_piedra_oscura = (175, 168, 150) if not es_crepusculo else (65, 50, 75)
        col_linea_junta = (130, 120, 105) if not es_crepusculo else (45, 35, 55)
        col_madera = (145, 95, 55) if not es_crepusculo else (70, 45, 50)
        col_madera_borde = (95, 60, 35) if not es_crepusculo else (40, 25, 35)

        # 1. Base de piedra
        pygame.draw.rect(pantalla, col_piedra_base, rect)

        # 2. Esquinas
        if (es_sup or es_inf) and (es_izq or es_der):
            p_rect = pygame.Rect(rect.x + 4, rect.y + 4, tw - 8, tw - 8)
            pygame.draw.rect(pantalla, col_madera, p_rect)
            pygame.draw.rect(pantalla, col_madera_borde, p_rect, 2)
            pygame.draw.circle(pantalla, (60, 50, 45), rect.center, 3)
            return

        # 3. Muros horizontales
        if es_sup or es_inf:
            # Líneas de sillares de piedra
            pygame.draw.line(pantalla, col_linea_junta, (rect.left, rect.y + 20), (rect.right, rect.y + 20), 1)
            offset_junta = 20 if (col % 2 == 0) else 0
            pygame.draw.line(pantalla, col_linea_junta, (rect.x + offset_junta, rect.top), (rect.x + offset_junta, rect.y + 20), 1)
            pygame.draw.line(pantalla, col_linea_junta, (rect.x + 40 - offset_junta, rect.y + 20), (rect.x + 40 - offset_junta, rect.bottom), 1)

            # Viga de madera horizontal que recorre la parte superior
            viga_y = rect.y if es_sup else rect.y + 28
            viga_rect = pygame.Rect(rect.left, viga_y, tw, 12)
            pygame.draw.rect(pantalla, col_madera, viga_rect)
            pygame.draw.rect(pantalla, col_madera_borde, viga_rect, 1)

        # 4. Muros verticales 
        elif es_izq or es_der:
            pygame.draw.line(pantalla, col_linea_junta, (rect.x + 20, rect.top), (rect.x + 20, rect.bottom), 1)
            offset_junta = 20 if (fila % 2 == 0) else 0
            pygame.draw.line(pantalla, col_linea_junta, (rect.left, rect.y + offset_junta), (rect.x + 20, rect.y + offset_junta), 1)
            pygame.draw.line(pantalla, col_linea_junta, (rect.x + 20, rect.y + 40 - offset_junta), (rect.right, rect.y + 40 - offset_junta), 1)

            # Viga de madera vertical lateral
            viga_x = rect.x if es_izq else rect.x + 28
            viga_rect = pygame.Rect(viga_x, rect.top, 12, tw)
            pygame.draw.rect(pantalla, col_madera, viga_rect)
            pygame.draw.rect(pantalla, col_madera_borde, viga_rect, 1)

        # Sombra sutil de profundidad
        pygame.draw.rect(pantalla, (0, 0, 0, 40), rect, 1)

    def dibujar_terreno_tile(self, pantalla, tile_tipo, px, py, es_crepusculo):
        img = None
        if tile_tipo == "CAMINO" and self.tile_adoquin:
            img = self.tile_adoquin
        elif tile_tipo == "PASTO" and self.tile_pasto:
            img = self.tile_pasto

        if img:
            sprite = self.aplicar_tinte_crepuscular(img) if es_crepusculo else img
            pantalla.blit(sprite, (px, py))
            return True
        return False

    def dibujar_ciudad(self, pantalla, mapa_actual, zona_actual, es_crepusculo):
        if not self.cargado or zona_actual != "EXTERIOR_CIUDAD":
            return False

        tw = self.tamano_tile

        def dibujar_con_efecto(img, x, y):
            if img:
                sprite = self.aplicar_tinte_crepuscular(img) if es_crepusculo else img
                pantalla.blit(sprite, (x, y))

        # 1. Forja de Carlos
        dibujar_con_efecto(self.casa_forja, 2 * tw, 2 * tw)
        # 2. Biblioteca de Elowen
        dibujar_con_efecto(self.casa_biblioteca, 15 * tw, 2 * tw)
        # 3. Botica de Vaelira
        dibujar_con_efecto(self.casa_botica, 2 * tw, 7 * tw)
        # 4. Taller Sureste
        dibujar_con_efecto(self.casa_taller, 15 * tw, 7 * tw)

        # 5. Gran Santuario Central
        if self.santuario_central:
            pos_x = (800 - self.santuario_central.get_width()) // 2
            pos_y = int(1.15 * tw)
            dibujar_con_efecto(self.santuario_central, pos_x, pos_y)

        return True