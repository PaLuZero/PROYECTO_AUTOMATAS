"""
MÓDULO: Diálogos de Ciudad - Hysteria: The Other Side
- Estructura fija de 3 opciones por interacción [1], [2] y [3].
- Diálogos naturales, cercanos y expresivos.
- Opciones especiales de reacción con héroes de la vanguardia.
- Fases Mundo Normal y Crepúsculo diferenciadas.
"""

ARBOLES_DIALOGO = {
    # --------------------------------------------------------------------------
    # 1. BOTICA: Vaelira Contriel
    # --------------------------------------------------------------------------
    "Vaelira_Contriel": {
        "nombre": "Vaelira Contriel",
        "estado_animo": "NEUTRAL",
        "servicio_desbloqueado": False,
        "recompensa_entregada": False,
        "normal": {
            "saludo_inicial": "Vaelira: '¡Hey, bienvenidos a la botica! El aire afuera huele a flores... y a problemas serios. ¿Qué se les ofrece?'",
            "saludo_recurrente": "Vaelira: '¡De vuelta enteros! ¿Vienen por parches para los golpes, pociones frescas o solo a saludar?'",
            "opciones_introduccion": [
                {
                    "texto": "[1] Un gusto, Vaelira. Venimos a prepararnos para lo que acecha afuera.",
                    "heroe_requerido": None,
                    "cambio_animo": "AMISTOSO",
                    "respuesta": "Vaelira: '¡Esa es la actitud! Da gusto hablar con gente educada. Cuenten conmigo para parcharles las heridas.'",
                    "es_sanacion": False
                },
                {
                    "texto": "[2] [Selene] 'Hacía tiempo que no olía lavanda pura. Tienes un santuario hermoso.'",
                    "heroe_requerido": "Selene Moon",
                    "cambio_animo": "AMISTOSO",
                    "da_item": "Éter Místico",
                    "respuesta": "Vaelira sonríe encantada: '¡Selene! Qué lindo tenerte aquí. Guarda este frasco de éter concentrado, ¡te servirá para tus hechizos!'",
                    "es_sanacion": False
                },
                {
                    "texto": "[3] Solo danos lo que tengas en stock y ahórrate la charla.",
                    "heroe_requerido": None,
                    "cambio_animo": "HOSTIL",
                    "respuesta": "Vaelira cruza los brazos con mala cara: 'Menudo humor... si vas a ser grosero, mis ungüentos te van a costar el doble.'",
                    "es_sanacion": False
                }
            ],
            "opcion_curar": {
                "texto": "[1] Necesitamos tratamiento médico para todo el equipo.",
                "heroe_requerido": None,
                "es_sanacion": True,
                "respuesta": ""
            },
            "opcion_conversar": {
                "texto": "[2] Cuéntanos qué notas de raro cuando el reloj empieza a sonar.",
                "heroe_requerido": None,
                "es_sanacion": False,
                "respuesta": "Vaelira se pone seria: 'El agua del caldero empieza a girar al revés y siento murmullos en la nuca... Cuídense mucho allá afuera.'"
            },
            "opcion_extra": {
                "texto": "[3] [Athina] 'Revisemos tus reservas de hierbas medicinales antes de salir.'",
                "heroe_requerido": "Athina Nightwish",
                "es_sanacion": False,
                "da_item": "Poción Curativa",
                "respuesta": "Vaelira: '¡Buena idea, Athina! Llévate esta poción curativa extra, nunca sobra cuando las sombras atacan.'"
            }
        },
        "crepusculo": {
            "saludo": "Vaelira suelta una risita con ojos brillantes: '¡Ji, ji, ji! ¿Oyen eso? Las botellas están cantando desafinadas... ¿vienen a jugar o quieren té de hongos?'",
            "opciones": [
                {
                    "texto": "[1] Vaelira, vuelve en ti. ¡Necesitamos curación ahora!",
                    "heroe_requerido": None,
                    "es_sanacion": True,
                    "respuesta": "Vaelira ríe a carcajadas: '¡Ni hablar! Las vendas están vivas y muerden los dedos... ¡vuelvan de día, ji, ji!'"
                },
                {
                    "texto": "[2] [Selene] 'Mírame a los ojos, Vaelira. Recuerda tu voz real.'",
                    "heroe_requerido": "Selene Moon",
                    "es_sanacion": False,
                    "cambio_animo": "AMISTOSO",
                    "da_item": "Fragmento del Despertar",
                    "respuesta": "Vaelira parpadea despejada un momento: 'Selene... tu voz me ancló... Toma esto rápido, antes de que la niebla me vuelva a confundir.'"
                },
                {
                    "texto": "[3] Esta chica está completamente chiflada por la niebla, vámonos.",
                    "heroe_requerido": None,
                    "es_sanacion": False,
                    "respuesta": "Vaelira se ríe en un rincón: '¡Chiflada tu abuela en bicicleta! ¡Ji, ji, ji!'"
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 2. FORJA: Carlos el Herrero
    # --------------------------------------------------------------------------
    "Herrero_Doran": {
        "nombre": "Carlos el Herrero",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Carlos: '¡Cuidado con las chispas! El carbón está al rojo vivo. ¿Vienen a equiparse como se debe o solo a hacer sombra?'",
            "opciones": [
                {
                    "texto": "[1] Enséñanos lo más duro y resistente que tengas forjado.",
                    "heroe_requerido": None,
                    "respuesta": "Carlos: 'Abre el catálogo con [T] y mira tú mismo. Nada de hojalata barata, aquí todo aguanta mamporros.'"
                },
                {
                    "texto": "[2] [Sidius] 'Ese balance en las empuñaduras es de maestro, Carlos.'",
                    "heroe_requerido": "Sidius Storm",
                    "cambio_animo": "AMISTOSO",
                    "da_item": "Poción Curativa",
                    "respuesta": "Carlos ríe orgulloso: '¡Vaya ojo tienes, muchacho! Toma esto de cortesía, un buen filo no sirve si caes desangrado.'"
                },
                {
                    "texto": "[3] ¿Por qué tanto calor aquí adentro? Es insoportable.",
                    "heroe_requerido": None,
                    "respuesta": "Carlos suelta un bufido: '¡Pues claro que hace calor, novato! ¡Es una fragua, no una heladería!'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Carlos martilla frenético con chispas azules: '¡El hierro no se enfría! ¡Siento que si dejo de golpear, la pared se me viene encima!'",
            "opciones": [
                {
                    "texto": "[1] ¡Carlos, detén el martillo un segundo! Vas a partir el yunque.",
                    "heroe_requerido": None,
                    "respuesta": "Carlos jadea con los nudillos blancos: '¡No puedo parar! Si suelto el mango, las sombras entrarán por el tiro del fuego...'"
                },
                {
                    "texto": "[2] [Noctis] 'El calor de tu mente supera al del fuego. Respira, es una ilusión.'",
                    "heroe_requerido": "Noctis Reverie",
                    "respuesta": "Carlos baja el martillo despacio: 'Uff... esa calma tuya es contagiosa, chaval. Casi apagas el zumbido de mi cráneo.'"
                },
                {
                    "texto": "[3] Déjalo que siga martillando, está en trance.",
                    "heroe_requerido": None,
                    "respuesta": "Carlos sigue golpeando sin mirar a nadie, envuelto en humo metálico."
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 3. BIBLIOTECA: Cronista Elowen
    # --------------------------------------------------------------------------
    "Cronista_Elowen": {
        "nombre": "Cronista Elowen",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Elowen: 'Buenas tardes, caminantes. Cuiden el tono de voz; los ecos de la biblioteca son sensibles a la imprudencia.'",
            "opciones": [
                {
                    "texto": "[1] Buscamos entender por qué el cielo se tiñe de violeta cada tanto.",
                    "heroe_requerido": None,
                    "respuesta": "Elowen: 'La fractura temporal del Santuario. Cada 40 campanadas, la realidad pierde su sostén y el crepúsculo se filtra.'"
                },
                {
                    "texto": "[2] [Selene] 'He sentido cómo las memorias flotan en estas estanterías.'",
                    "heroe_requerido": "Selene Moon",
                    "da_item": "Éter Místico",
                    "respuesta": "Elowen asiente conmovida: 'Tu vínculo es afinado, Selene. Toma esta esencia arcana para nutrir tu poder.'"
                },
                {
                    "texto": "[3] ¿No tienes algún libro con mapas de escape o atajos?",
                    "heroe_requerido": None,
                    "respuesta": "Elowen sonríe levemente: 'No hay atajos en un laberinto en constante mutación, viajero.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Elowen hojea un libro en blanco con horror: '¡La tinta se escurre de las hojas! ¡Los nombres de nuestros ancestros se borraron!'",
            "opciones": [
                {
                    "texto": "[1] ¡Cálmate! Los libros materiales se pueden reescribir.",
                    "heroe_requerido": None,
                    "respuesta": "Elowen: '¿Reescribir? ¿Cómo vamos a reescribir lo que ya nadie recuerda haber vivido?!'"
                },
                {
                    "texto": "[2] [Noctis] 'Lo que desaparece aquí existe en otra posibilidad. No desesperes.'",
                    "heroe_requerido": "Noctis Reverie",
                    "respuesta": "Elowen se aferra al tomo: 'Ojalá tengas razón... tu voz suena como si vinieras de un mañana más firme.'"
                },
                {
                    "texto": "[3] Mejor salgamos de aquí antes de que los estantes colapsen.",
                    "heroe_requerido": None,
                    "respuesta": "Elowen no responde, perdida mirando las páginas translúcidas."
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 4. EXTERIOR: Anciano Alquimista Eldrin
    # --------------------------------------------------------------------------
    "Alquimista_Eldrin": {
        "nombre": "Eldrin el Alquimista",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Eldrin te mira por encima de sus gafas: '¡Ah, jóvenes con prisa! Miren este frasco, un buen destilado de raíz amarga mantiene a raya el cansancio.'",
            "opciones": [
                {
                    "texto": "[1] ¿Tienes algo que nos dé ventaja contra las sombras de afuera?",
                    "heroe_requerido": None,
                    "respuesta": "Eldrin: 'El mejor truco es no dejarse arrinconar. Y si las cosas se ponen feas, ¡usen guardia para frenar el impacto!'"
                },
                {
                    "texto": "[2] [Athina] 'Esa raíz que tienes en la mano es cicuta estelar, ¿verdad?'",
                    "heroe_requerido": "Athina Nightwish",
                    "da_item": "Poción Curativa",
                    "respuesta": "Eldrin abre los ojos asombrado: '¡Caramba, qué buen ojo! Pocos reconocen las hierbas raras. ¡Toma esta muestra de regalo!'"
                },
                {
                    "texto": "[3] Huele a hierba quemada por aquí, abuelo.",
                    "heroe_requerido": None,
                    "respuesta": "Eldrin se ríe con picardía: '¡Es el perfume del progreso, muchacho! Mejor eso que oler a pantano podrido.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Eldrin tiembla con un frasco de líquido violeta burbujeante: '¡Me habla! El frasco tiene voz y me dice que si lo bebo podré volar por encima del muro...'",
            "opciones": [
                {
                    "texto": "[1] ¡Ni se te ocurra beber eso, es veneno dimensional puro!",
                    "heroe_requerido": None,
                    "respuesta": "Eldrin suelta un respingo y baja el brazo: 'Uff... gracias... por un segundo juré que era vino dulce.'"
                },
                {
                    "texto": "[2] [Sidius] 'Dame ese frasco, anciano. Yo me encargo de deshacerme de él.'",
                    "heroe_requerido": "Sidius Storm",
                    "respuesta": "Eldrin te entrega el tubo con alivio: 'Tómalo, hijo... tus manos son más firmes que mis viejos huesos.'"
                },
                {
                    "texto": "[3] Da un paso atrás, no quiero que esa porquería salpique.",
                    "heroe_requerido": None,
                    "respuesta": "Eldrin abraza el frasco susurrando cosas incomprensibles en la penumbra."
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 5. EXTERIOR: Tabernera Marta
    # --------------------------------------------------------------------------
    "Tabernera_Marta": {
        "nombre": "Marta la Tabernera",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Marta limpia una jarra de barro con una sonrisa: '¡Pasen, pasen! El guiso está en el fuego y la sidra bien fría. ¿Cómo los trata el camino?'",
            "opciones": [
                {
                    "texto": "[1] Agotados, pero firmes. ¿Cómo van las cosas por el vecindario?",
                    "heroe_requerido": None,
                    "respuesta": "Marta: 'La gente anda con miedo por el reloj, pero mientras no falte pan caliente y compañía, nos mantendremos en pie.'"
                },
                {
                    "texto": "[2] [Sidius] 'Un brindis por la gente que aún mantiene vivo este pueblo.'",
                    "heroe_requerido": "Sidius Storm",
                    "cambio_animo": "AMISTOSO",
                    "respuesta": "Marta le guiña un ojo: '¡Ese es mi líder! Da gusto ver a alguien que no se olvida de la gente común. ¡Fuerza allá afuera!'"
                },
                {
                    "texto": "[3] No tenemos tiempo para comer, solo estamos de paso.",
                    "heroe_requerido": None,
                    "respuesta": "Marta suspira: 'Vayan con cuidado entonces... el estómago vacío hace temblar la espada.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Marta aprieta la jarra con nudillos pálidos y ojos fijos: 'El caldo... el caldo se volvió negro como tinta... y nadie entra por la puerta...'",
            "opciones": [
                {
                    "texto": "[1] Marta, atranca bien las puertas y quédate adentro hasta que pase.",
                    "heroe_requerido": None,
                    "respuesta": "Marta asiente temblando: 'Sí... sí, pondré el pestillo. No quiero ver qué rostros tienen los que caminan en la niebla.'"
                },
                {
                    "texto": "[2] [Selene] 'El calor de tu hogar es más fuerte que esta oscuridad, Marta.'",
                    "heroe_requerido": "Selene Moon",
                    "da_item": "Poción Curativa",
                    "respuesta": "Marta suspira aliviada: 'Qué linda eres, niña... toma esta botella de licor curativo que guardaba para emergencias.'"
                },
                {
                    "texto": "[3] El pueblo entero parece una pesadilla viviente.",
                    "heroe_requerido": None,
                    "respuesta": "Marta mira la pared sin parpadear: 'Una pesadilla... de la que no sé si vamos a despertar...'"
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 6. EXTERIOR: Viajero Encapuchado Cael
    # --------------------------------------------------------------------------
    "Viajero_Cael": {
        "nombre": "Cael el Errante",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Cael alza su farol con calma: 'He visto reinos enteros consumirse por no prestar atención a las grietas. Ustedes cargan con un peso peligroso.'",
            "opciones": [
                {
                    "texto": "[1] ¿Qué clase de peligros aguardan más allá de las puertas?",
                    "heroe_requerido": None,
                    "respuesta": "Cael: 'Criaturas que no atacan tu carne, sino tu certeza. Cuando la duda te gana, el crepúsculo ya venció.'"
                },
                {
                    "texto": "[2] [Noctis] 'Ese farol tuyo no arde con aceite corriente, ¿verdad?'",
                    "heroe_requerido": "Noctis Reverie",
                    "da_item": "Fragmento del Despertar",
                    "respuesta": "Cael sonríe con misterio: 'Bien visto, portador de Posibilidad. Arde con fragmentos de tiempo puro. Toma uno, te abrirá caminos.'"
                },
                {
                    "texto": "[3] Te ves bastante siniestro para ser un simple viajero.",
                    "heroe_requerido": None,
                    "respuesta": "Cael: 'En un mundo que se cae a pedazos, la desconfianza es la primera virtud. No te culpo, viajero.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "La lámpara de Cael brilla con un fuego azul fantasmal: 'Ya empezó... las siluetas del páramo están cruzando los muros. ¿Sienten el frío en los dedos?'",
            "opciones": [
                {
                    "texto": "[1] Nuestras armas están listas. No daremos ni un paso atrás.",
                    "heroe_requerido": None,
                    "respuesta": "Cael asiente con respeto: 'Entonces apunten directo al núcleo de los espectros. No duden ni un segundo.'"
                },
                {
                    "texto": "[2] [Athina] 'Tu luz nos protege. Mantén el farol en alto, Cael.'",
                    "heroe_requerido": "Athina Nightwish",
                    "respuesta": "Cael: 'Mientras mi brazo aguante, la sombra no tocará esta esquina de la plaza.'"
                },
                {
                    "texto": "[3] Esto pinta muy mal, deberíamos refugiarnos.",
                    "heroe_requerido": None,
                    "respuesta": "Cael niega con la cabeza: 'No hay refugio cuando la noche te busca por dentro.'"
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 7. EXTERIOR: Aprendiz Toby
    # --------------------------------------------------------------------------
    "Aprendiz_Toby": {
        "nombre": "Aprendiz Toby",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Toby carga un martillo grande con ambas manos: '¡Hola! El maestro Carlos me tiene puliendo herraduras, pero yo quiero forjar mandobles legendarios.'",
            "opciones": [
                {
                    "texto": "[1] Todo gran herrero empezó limpiando carbón, muchacho.",
                    "heroe_requerido": None,
                    "respuesta": "Toby se anima: '¡Eso mismo me dice mi mamá! No voy a aflojar hasta hacer una espada que corte piedras.'"
                },
                {
                    "texto": "[2] [Sidius] 'La postura de tus pies al martillar es clave. Planta bien los talones.'",
                    "heroe_requerido": "Sidius Storm",
                    "cambio_animo": "AMISTOSO",
                    "da_item": "Poción Curativa",
                    "respuesta": "Toby corrige su pose fascinado: '¡Guau, se siente mucho más firme! ¡Toma esta poción que me dio Carlos, te la ganaste!'"
                },
                {
                    "texto": "[3] Ten cuidado no vayas a aplastarte un pie con eso.",
                    "heroe_requerido": None,
                    "respuesta": "Toby bufa orgulloso: '¡Para tu información, solo se me ha caído tres veces esta semana!'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Toby está acurrucado tras un barril, pálido como el papel: '¡El fuego de la forja se apagó de golpe y escuché rasguños bajo las tablas del suelo!'",
            "opciones": [
                {
                    "texto": "[1] Tranquilo, Toby. Quédate aquí agachado, nosotros vigilamos.",
                    "heroe_requerido": None,
                    "respuesta": "Toby traga saliva: 'Por favor... no dejen que esas cosas con garras se acerquen al taller.'"
                },
                {
                    "texto": "[2] [Athina] 'Respira despacio conmigo, Toby. Es solo el viento en los tejados.'",
                    "heroe_requerido": "Athina Nightwish",
                    "respuesta": "Toby se calma un poco: 'Tu voz es muy dulce... gracias, señorita. Ya no siento tanto temblor.'"
                },
                {
                    "texto": "[3] ¡Levántate y empuña el martillo por si acaso!",
                    "heroe_requerido": None,
                    "respuesta": "Toby aprieta los ojos con miedo: '¡Pesa demasiado cuando me tiemblan las manos!'"
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 8. EXTERIOR: Guardia Vane
    # --------------------------------------------------------------------------
    "Guardia_Vane": {
        "nombre": "Guardia Vane",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Vane ajusta su guantelete de metal: 'Entrada norte despejada. La barrera del Santuario funciona como un reloj mientras haya luz de día.'",
            "opciones": [
                {
                    "texto": "[1] ¿Qué recomiendas hacer si nos sorprende la noche afuera?",
                    "heroe_requerido": None,
                    "respuesta": "Vane: 'Correr hacia la plaza. Las sombras son territoriales y se desorientan cerca del monumento central.'"
                },
                {
                    "texto": "[2] [Sidius] 'Firme guardia, soldado. La vanguardia te respalda.'",
                    "heroe_requerido": "Sidius Storm",
                    "cambio_animo": "AMISTOSO",
                    "respuesta": "Vane golpea su peto con el puño: '¡Es un honor tener guerreros de su temple en la ciudad, comandante!'"
                },
                {
                    "texto": "[3] Espero que esa armadura pesada no te haga lento si toca correr.",
                    "heroe_requerido": None,
                    "respuesta": "Vane sonríe de lado: 'Un guardia del Santuario no huye, camarada. Aguanta el golpe y responde el doble.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Vane desenvaina su espada abollada con la respiración entrecortada: '¡La niebla cruzó los arcos! ¡Veo siluetas caminando por las sombras del callejón!'",
            "opciones": [
                {
                    "texto": "[1] ¡Calma, Vane! Somos nosotros, mantén la posición defensiva.",
                    "heroe_requerido": None,
                    "respuesta": "Vane pestañea aliviado y baja la punta: 'Cielos... por un segundo juré que eran espectros arrastrándose.'"
                },
                {
                    "texto": "[2] [Noctis] 'No ataques a las sombras sueltas, busca el vórtice central.'",
                    "heroe_requerido": "Noctis Reverie",
                    "respuesta": "Vane: 'Entendido. Cuidaré la puerta para que no los rodeen por la espalda.'"
                },
                {
                    "texto": "[3] Si la cosa se pone fea, nosotros abriremos el paso.",
                    "heroe_requerido": None,
                    "respuesta": "Vane: 'Cuento con ustedes. ¡Por el Santuario!'"
                }
            ]
        }
    },

    # --------------------------------------------------------------------------
    # 9. EXTERIOR: Pequeña Lina
    # --------------------------------------------------------------------------
    "Nina_Lina": {
        "nombre": "Pequeña Lina",
        "estado_animo": "NEUTRAL",
        "recompensa_entregada": False,
        "normal": {
            "saludo": "Lina abraza una muñeca de trapo vieja: 'Hola... a mi muñeca le gusta ver sus armaduras brillantes. Dice que parecen caballeros de cuento.'",
            "opciones": [
                {
                    "texto": "[1] Dile a tu muñeca que cuidaremos de que no le pase nada al pueblo.",
                    "heroe_requerido": None,
                    "respuesta": "Lina sonríe contenta: '¡Dice que muchas gracias! Y que huelen a aventuras lejanas.'"
                },
                {
                    "texto": "[2] [Athina] 'Qué linda muñeca, Lina. ¿Tiene nombre?'",
                    "heroe_requerido": "Athina Nightwish",
                    "da_item": "Fragmento del Despertar",
                    "respuesta": "Lina: '¡Se llama Chispa! Toma, encontramos esta piedra violeta en la arena y Chispa quiere que sea tuya.'"
                },
                {
                    "texto": "[3] Deberías estar con tus padres jugando adentro, niña.",
                    "heroe_requerido": None,
                    "respuesta": "Lina hace un puchero: 'Mamá está tejiendo y no me deja hacer ruido adentro... solo estaba mirando las flores.'"
                }
            ]
        },
        "crepusculo": {
            "saludo": "Lina mira fijamente al suelo con la mirada perdida y voz temblorosa: 'La muñeca... la muñeca empezó a pestañear sola... y me dijo que me escondiera.'",
            "opciones": [
                {
                    "texto": "[1] Corre a la botica con Vaelira de inmediato, Lina. ¡Ya mismo!",
                    "heroe_requerido": None,
                    "respuesta": "Lina asiente con lágrimas en los ojos: '¡Sí, voy corriendo! ¡Tengan cuidado con los monstruos!'"
                },
                {
                    "texto": "[2] [Selene] 'Dame la mano, Lina. Cierra los ojos y escucha mi voz tranquila.'",
                    "heroe_requerido": "Selene Moon",
                    "respuesta": "Lina aprieta la mano de Selene: 'Tu mano está calientita... ya no escucho los ruidos feos del viento.'"
                },
                {
                    "texto": "[3] ¡Tira esa muñeca si está embrujada!",
                    "heroe_requerido": None,
                    "respuesta": "Lina la abraza con más fuerza asustada: '¡No! ¡Chispa solo tiene miedo igual que yo!'"
                }
            ]
        }
    }
}