import os
import time
import pygame

class AnimadorPersonaje:
    def __init__(self, tamano_tile=40):
        self.tamano_tile = tamano_tile
        self.banco_sprites = {}
        self.direccion_actual = "abajo"
        self.frame_actual = 0
        self.ultimo_cambio_tiempo = time.time()
        self.intervalo_frame = 0.12

    def cargar_heroe(self, nombre_heroe, nombres_archivo, carpetas_buscar):
        hoja_img = None
        for c in carpetas_buscar:
            for nom in nombres_archivo:
                ruta = os.path.join(c, nom)
                if os.path.exists(ruta):
                    try:
                        hoja_img = pygame.image.load(ruta).convert_alpha()
                        break
                    except Exception:
                        pass
            if hoja_img:
                break

        if not hoja_img:
            return False

        if hoja_img.get_alpha() is None:
            color_fondo = hoja_img.get_at((0, 0))[:3]
            hoja_img.set_colorkey(color_fondo)

        w_total, h_total = hoja_img.get_size()
        frame_w = w_total // 4
        frame_h = h_total // 4

        pad_x = 2
        pad_y = 2

        def recortar_y_escalar(col, fila):
            rx = col * frame_w + pad_x
            ry = fila * frame_h + pad_y
            rw = frame_w - (pad_x * 2)
            rh = frame_h - (pad_y * 2)
            sub = hoja_img.subsurface(pygame.Rect(rx, ry, rw, rh)).copy()
            return pygame.transform.scale(sub, (self.tamano_tile, self.tamano_tile))

        sprites_heroe = {"abajo": [], "izquierda": [], "derecha": [], "arriba": []}

        for col in range(4):
            sprites_heroe["abajo"].append(recortar_y_escalar(col, 0))

        for col in range(4):
            f_izq = recortar_y_escalar(col, 1)
            sprites_heroe["izquierda"].append(f_izq)
            f_der = pygame.transform.flip(f_izq, True, False)
            sprites_heroe["derecha"].append(f_der)

        for col in range(4):
            sprites_heroe["arriba"].append(recortar_y_escalar(col, 3))

        self.banco_sprites[nombre_heroe] = sprites_heroe
        return True

    def actualizar(self, en_movimiento, direccion):
        self.direccion_actual = direccion
        if en_movimiento:
            ahora = time.time()
            if ahora - self.ultimo_cambio_tiempo >= self.intervalo_frame:
                self.ultimo_cambio_tiempo = ahora
                self.frame_actual = (self.frame_actual + 1) % 4
        else:
            self.frame_actual = 0

    def obtener_frame(self, nombre_heroe, direccion=None):
        dir_usar = direccion if direccion else self.direccion_actual
        if nombre_heroe in self.banco_sprites:
            frames = self.banco_sprites[nombre_heroe].get(dir_usar, [])
            if frames and len(frames) == 4:
                return frames[self.frame_actual]
        return None