
import random

class BatallaTurnos:
    def __init__(self, pareja_activa, stats_heroes, enemigo, inventario_objetos):
        # Filtro de entrada de cualquier valor nulo o inválido
        self.pareja_activa = [h for h in pareja_activa if h and h in stats_heroes]
        if not self.pareja_activa:
            self.pareja_activa = ["Sidius Storm"]

        self.stats_party = stats_heroes
        self.inventario_objetos = inventario_objetos

        # Configuración del enemigo
        self.enemigo_info = enemigo
        self.nombre_enemigo = enemigo.get("nombre", "Eco de Penumbra")
        self.es_grupo = enemigo.get("es_grupo", False)

        if not self.es_grupo:
            base_hp = enemigo.get("hp", 120)
            self.max_hp_enemigo = int(base_hp * 1.5)
            self.hp_enemigo = self.max_hp_enemigo
            self.atk_enemigo = int(enemigo.get("atk", 18) * 1.3)
            self.enemigos = []
            self.indice_objetivo = 0
        else:
            self.enemigos = []
            for sub in enemigo.get("enemigos", []):
                m_hp = int(sub.get("max_hp", 70) * 1.4)
                self.enemigos.append({
                    "nombre": sub["nombre"],
                    "hp": m_hp,
                    "max_hp": m_hp,
                    "atk": int(sub.get("atk", 15) * 1.25)
                })
            self.indice_objetivo = 0
            self.atk_enemigo = self.enemigos[0]["atk"] if self.enemigos else 15
            self.max_hp_enemigo = sum(e["max_hp"] for e in self.enemigos)
            self.hp_enemigo = sum(e["hp"] for e in self.enemigos)

        self.en_guardia = {h: False for h in self.pareja_activa}
        self.enemigo_cargando_ataque = False

        # Flujo por turnos
        self.indice_heroe_turno = 0
        self.acciones_planificadas = []

        # Cola de eventos cinemáticos
        self.cola_eventos = []
        self.evento_actual = None

        self.anim_heroe_atacando = None
        self.anim_fase = 0
        self.anim_recibiendo_dano = False

        self.fase_combate = "TURNO_JUGADOR"
        self.modo_menu = "PRINCIPAL"
        self.resultado = ""
        self.mensaje_en_pantalla = f"¡Ha aparecido {self.nombre_enemigo}!"
        self.mensajes_log = [self.mensaje_en_pantalla]
        self.recompensas = {"oro": enemigo.get("oro", 30), "exp": enemigo.get("exp", 25)}

    def obtener_heroe_activo_turno(self):
        """Devuelve el héroe activo con HP > 0; omite valores None y caídos."""
        heroes_vivos = [
            h for h in self.pareja_activa 
            if h and h in self.stats_party and self.stats_party[h].get("hp", 0) > 0
        ]
        
        while self.indice_heroe_turno < len(self.pareja_activa):
            heroe_actual = self.pareja_activa[self.indice_heroe_turno]
            if heroe_actual and heroe_actual in self.stats_party and self.stats_party[heroe_actual].get("hp", 0) > 0:
                return heroe_actual
            self.indice_heroe_turno += 1

        return heroes_vivos[0] if heroes_vivos else (self.pareja_activa[0] if self.pareja_activa else "Sidius Storm")

    def fijar_mensaje(self, texto):
        self.mensaje_en_pantalla = texto
        self.mensajes_log.append(texto)
        if len(self.mensajes_log) > 8:
            self.mensajes_log.pop(0)

    
    # PLanificacion de las Acciones del jugador
  
    def encolar_accion(self, tipo_accion, dato_extra=None):
        if self.fase_combate != "TURNO_JUGADOR":
            return

        heroe_actual = self.obtener_heroe_activo_turno()
        self.acciones_planificadas.append({
            "heroe": heroe_actual,
            "tipo": tipo_accion,
            "extra": dato_extra
        })

        # Buscar al siguiente héroe con vida para el turno
        self.indice_heroe_turno += 1
        while (self.indice_heroe_turno < len(self.pareja_activa) and 
               self.stats_party[self.pareja_activa[self.indice_heroe_turno]]["hp"] <= 0):
            self.indice_heroe_turno += 1

        # Si aún queda un integrante por decidir
        if self.indice_heroe_turno < len(self.pareja_activa):
            siguiente = self.pareja_activa[self.indice_heroe_turno]
            self.fijar_mensaje(f"Turno de {siguiente}. Elige su acción.")
        else:
            self.generar_cola_resolucion()

    def ejecutar_ataque_basico(self):
        self.encolar_accion("ATACAR")

    def ejecutar_habilidad_vinculo(self):
        heroe = self.obtener_heroe_activo_turno()
        st = self.stats_party[heroe]
        if st["mp"] < 8:
            self.fijar_mensaje(f"¡{heroe} no tiene suficiente MP (requiere 8 MP)!")
            return
        self.encolar_accion("HABILIDAD")

    def ejecutar_guardia(self):
        self.encolar_accion("GUARDIA")

    def usar_item(self, nombre_item):
        if nombre_item in self.inventario_objetos:
            self.encolar_accion("ITEM", nombre_item)

    def cambiar_objetivo(self):
        if not self.es_grupo:
            return
        vivos = [i for i, e in enumerate(self.enemigos) if e["hp"] > 0]
        if vivos:
            try:
                curr_idx = vivos.index(self.indice_objetivo)
                self.indice_objetivo = vivos[(curr_idx + 1) % len(vivos)]
            except ValueError:
                self.indice_objetivo = vivos[0]

    def intentar_huir(self):
        if random.random() < 0.6:
            self.fase_combate = "TERMINADO"
            self.resultado = "HUIDA"
            self.fijar_mensaje("¡Lograron romper la formación enemiga y escapar!")
        else:
            self.fijar_mensaje("¡No pudieron escapar! Las sombras cierran el paso.")
            self.generar_contraataque_enemigo_solitario()

    
    # Cosntruccion de la Secuencia de Resolucion
    
    def generar_cola_resolucion(self):
        self.cola_eventos = []

        for plan in self.acciones_planificadas:
            heroe = plan["heroe"]
            tipo = plan["tipo"]

            if self.stats_party[heroe]["hp"] <= 0:
                continue

            if tipo == "ATACAR":
                st = self.stats_party[heroe]
                atk_base = st.get("atk", 16) + st.get("atk_bono", 0)
                dano = max(8, int(atk_base * random.uniform(1.05, 1.35)))
                nombre_tec = "Tajo de Acero" if "Sidius" in heroe else "Estocada Furtiva"
                self.cola_eventos.append({
                    "tipo": "ATAQUE_HEROE",
                    "heroe": heroe,
                    "dano": dano,
                    "tecnica": nombre_tec
                })

            elif tipo == "HABILIDAD":
                st = self.stats_party[heroe]
                st["mp"] = max(0, st["mp"] - 8)
                dano = int(st.get("atk", 14) * 2.2)
                nombre_hab = "Destello de Vínculo" if "Selene" in heroe else "Falla Dimensional"
                self.cola_eventos.append({
                    "tipo": "HABILIDAD_HEROE",
                    "heroe": heroe,
                    "dano": dano,
                    "tecnica": nombre_hab
                })

            elif tipo == "GUARDIA":
                self.en_guardia[heroe] = True
                self.cola_eventos.append({
                    "tipo": "GUARDIA_HEROE",
                    "heroe": heroe
                })

            elif tipo == "ITEM":
                self.cola_eventos.append({
                    "tipo": "ITEM_HEROE",
                    "heroe": heroe,
                    "item": plan["extra"]
                })

        self.construir_evento_enemigo()

        self.fase_combate = "RESOLUCION"
        self.acciones_planificadas = []
        self.indice_heroe_turno = 0
        self.avanzar_evento_siguiente()

    def construir_evento_enemigo(self):
        heroes_vivos = [h for h in self.pareja_activa if self.stats_party[h]["hp"] > 0]
        if not heroes_vivos:
            return

        if not self.es_grupo:
            obj_nom = random.choice(heroes_vivos)
            if self.enemigo_cargando_ataque:
                self.enemigo_cargando_ataque = False
                dano = int(self.atk_enemigo * 2.4)
                self.cola_eventos.append({
                    "tipo": "ATAQUE_ENEMIGO",
                    "atacante": self.nombre_enemigo,
                    "objetivo": obj_nom,
                    "dano": dano,
                    "tecnica": "Impacto de Ruina Fracturada",
                    "es_cargado": True
                })
            else:
                if random.random() < 0.40:
                    self.enemigo_cargando_ataque = True
                    self.cola_eventos.append({
                        "tipo": "CARGA_ENEMIGO",
                        "atacante": self.nombre_enemigo
                    })
                else:
                    dano = int(self.atk_enemigo * random.uniform(0.9, 1.25))
                    self.cola_eventos.append({
                        "tipo": "ATAQUE_ENEMIGO",
                        "atacante": self.nombre_enemigo,
                        "objetivo": obj_nom,
                        "dano": dano,
                        "tecnica": "Zarpazo Umbrío",
                        "es_cargado": False
                    })
        else:
            for sub in self.enemigos:
                if sub["hp"] > 0:
                    heroes_vivos = [h for h in self.pareja_activa if self.stats_party[h]["hp"] > 0]
                    if not heroes_vivos:
                        break
                    obj_nom = random.choice(heroes_vivos)
                    dano = int(sub.get("atk", 14) * random.uniform(0.85, 1.15))
                    self.cola_eventos.append({
                        "tipo": "ATAQUE_ENEMIGO",
                        "atacante": sub["nombre"],
                        "objetivo": obj_nom,
                        "dano": dano,
                        "tecnica": "Ataque Espectral",
                        "es_cargado": False
                    })

    def generar_contraataque_enemigo_solitario(self):
        self.cola_eventos = []
        self.construir_evento_enemigo()
        self.fase_combate = "RESOLUCION"
        self.avanzar_evento_siguiente()

    
    # Resolucion paso a paso con [ESPACIO]
    
    def avanzar_evento_siguiente(self):
        if not self.cola_eventos:
            for h in self.en_guardia:
                self.en_guardia[h] = False

            if all(self.stats_party[h]["hp"] <= 0 for h in self.pareja_activa):
                self.fase_combate = "TERMINADO"
                self.resultado = "DERROTA"
                self.fijar_mensaje("¡El grupo ha colapsado ante la oscuridad!")
                return

            self.fase_combate = "TURNO_JUGADOR"
            self.anim_heroe_atacando = None
            self.indice_heroe_turno = 0
            self.fijar_mensaje(f"Nueva ronda. Turno de {self.obtener_heroe_activo_turno()}.")
            return

        ev = self.cola_eventos.pop(0)
        self.evento_actual = ev
        tipo = ev["tipo"]

        heroe_ev = ev.get("heroe")
        if heroe_ev and self.stats_party[heroe_ev]["hp"] <= 0:
            self.fijar_mensaje(f"¡{heroe_ev} ha caído y no puede actuar!")
            self.anim_heroe_atacando = None
            return

        if tipo == "ATAQUE_HEROE":
            h = ev["heroe"]
            d = ev["dano"]
            tec = ev["tecnica"]
            self.anim_heroe_atacando = h
            self.anim_fase = 0

            if not self.es_grupo:
                self.hp_enemigo = max(0, self.hp_enemigo - d)
                self.enemigo_info["hp"] = self.hp_enemigo
                self.fijar_mensaje(f"{h} usó {tec} causando {d} de daño a {self.nombre_enemigo}.")
                if self.hp_enemigo <= 0:
                    self.finalizar_victoria()
                    return
            else:
                obj = self.enemigos[self.indice_objetivo]
                obj["hp"] = max(0, obj["hp"] - d)
                self.fijar_mensaje(f"{h} usó {tec} causando {d} de daño a {obj['nombre']}.")
                if obj["hp"] <= 0:
                    vivos = [e for e in self.enemigos if e["hp"] > 0]
                    if not vivos:
                        self.finalizar_victoria()
                        return
                    else:
                        self.cambiar_objetivo()

        elif tipo == "HABILIDAD_HEROE":
            h = ev["heroe"]
            d = ev["dano"]
            tec = ev["tecnica"]
            self.anim_heroe_atacando = h
            self.anim_fase = 0

            if not self.es_grupo:
                self.hp_enemigo = max(0, self.hp_enemigo - d)
                self.enemigo_info["hp"] = self.hp_enemigo
                self.fijar_mensaje(f"¡{h} usó {tec} causando {d} de daño mágico a {self.nombre_enemigo}!")
                if self.hp_enemigo <= 0:
                    self.finalizar_victoria()
                    return
            else:
                for sub in self.enemigos:
                    if sub["hp"] > 0:
                        sub["hp"] = max(0, sub["hp"] - int(d * 0.75))
                self.fijar_mensaje(f"¡{h} usó {tec} en área causando {int(d * 0.75)} de daño!")
                if not any(e["hp"] > 0 for e in self.enemigos):
                    self.finalizar_victoria()
                    return

        elif tipo == "GUARDIA_HEROE":
            self.anim_heroe_atacando = None
            self.fijar_mensaje(f"{ev['heroe']} asume postura de Bloqueo defensivo.")

        elif tipo == "ITEM_HEROE":
            self.anim_heroe_atacando = None
            h = ev["heroe"]
            it = ev["item"]
            if it in self.inventario_objetos:
                self.inventario_objetos.remove(it)
                if it == "Poción Curativa":
                    self.stats_party[h]["hp"] = min(self.stats_party[h]["max_hp"], self.stats_party[h]["hp"] + 50)
                    self.fijar_mensaje(f"{h} usó Poción Curativa (+50 HP).")
                elif it == "Éter Místico":
                    self.stats_party[h]["mp"] = min(self.stats_party[h]["max_mp"], self.stats_party[h]["mp"] + 15)
                    self.fijar_mensaje(f"{h} usó Éter Místico (+15 MP).")

        elif tipo == "CARGA_ENEMIGO":
            self.anim_heroe_atacando = None
            self.fijar_mensaje(f"¡ALERTA! ¡{ev['atacante']} acumula energía caótica! (¡USA BLOQUEO [3] EL SIGUIENTE TURNO!)")

        elif tipo == "ATAQUE_ENEMIGO":
            self.anim_heroe_atacando = None
            atc = ev["atacante"]
            obj = ev["objetivo"]
            d_base = ev["dano"]
            tec = ev["tecnica"]
            st_obj = self.stats_party[obj]

            if self.en_guardia.get(obj, False):
                if random.random() < 0.35:
                    d_final = max(1, int(d_base * 0.15))
                    self.fijar_mensaje(f"¡BLOQUEO PERFECTO! {obj} desvió {tec} de {atc} (Solo {d_final} de daño).")
                else:
                    d_final = max(3, int(d_base * 0.50))
                    self.fijar_mensaje(f"{obj} bloqueó {tec} de {atc} reduciendo a {d_final} de daño.")
            else:
                d_final = d_base
                self.fijar_mensaje(f"{atc} usó {tec} causando {d_final} de daño a {obj}.")

            st_obj["hp"] = max(0, st_obj["hp"] - d_final)

            if all(self.stats_party[h]["hp"] <= 0 for h in self.pareja_activa):
                self.cola_eventos = []
                self.fase_combate = "TERMINADO"
                self.resultado = "DERROTA"
                self.fijar_mensaje("¡El grupo ha sido derrotado!")

    def finalizar_victoria(self):
        self.cola_eventos = []
        self.fase_combate = "TERMINADO"
        self.resultado = "VICTORIA"
        self.hp_enemigo = 0
        if "hp" in self.enemigo_info:
            self.enemigo_info["hp"] = 0
        self.fijar_mensaje(f"¡{self.nombre_enemigo} ha sido derrotado con éxito!")