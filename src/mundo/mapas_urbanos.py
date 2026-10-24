# 0 = Suelo Pasto
# 1 = Muro Perimetral
# 2 = Portal dimensional / salida
# 3 = Núcleo del Santuario
# 4 = Puerta Forja
# 5 = Puerta Biblioteca
# 6 = Puerta Botica
# 13 = Camino de adoquines de piedra

MAPA_EXTERIOR_CIUDAD = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 4, 1, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 1, 5, 1, 0, 1],
    [1, 0, 0, 13, 0, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 0, 13, 0, 0, 1],
    [1, 0, 0, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 0, 1, 6, 1, 13, 13, 13, 13, 13, 13, 13, 13, 13, 13, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 13, 13, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# INTERIOR FORJA / ARMERÍA (Muros, yunque y mostradores)
# 20 columnas x 15 filas (800x600 px a escala de 40 px por tile)
# 1 = Paredes, horno de fundición, barriles, lingotes y yunques (SÓLIDO)
# 7 = Mostrador largo de herrería (bloquea el paso pero permite interactuar con [E])
# 9 = Tapete rojo de salida hacia la ciudad
# 0 = Suelo de piedra transitable

INTERIOR_FORJA = [
    # 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 0: Muro superior
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 1: Estantes altos
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 2: Armas y chimenea
    [ 1,  1,  1,  1,  1,  1,  0,  1,  1,  0,  1,  1,  0,  0,  1,  1,  1,  1,  1,  1], # 3: Yunques (x=7,8 y x=10,11)
    [ 1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1], # 4: Pasillo de Carlos (Carlos en x=12, y=4)
    [ 1,  1,  1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1,  1], # 5: Detrás del mostrador
    [ 1,  1,  1,  0,  0,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  0,  0,  1,  1,  1], # 6: Mostrador de herramientas
    [ 1,  1,  1,  0,  0,  7,  7,  7,  7,  7,  7,  7,  7,  7,  7,  0,  0,  1,  1,  1], # 7: Cajas de minerales
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1], # 8: Suelo frente al mostrador
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1], # 9: Suelo transitable
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1], # 10: Placa de metal en el suelo
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1], # 11: Mesa de forja derecha
    [ 1,  1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1,  1], # 12: Pasillo hacia la puerta
    [ 1,  1,  1,  1,  1,  1,  1,  1,  9,  9,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 13: Tapete de salida
    [ 1,  1,  1,  1,  1,  1,  1,  1,  9,  9,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]  # 14: Muro inferior
]

# INTERIOR BIBLIOTECA DE ELOWEN
INTERIOR_BIBLIOTECA = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Matriz calibrada a la imagen: 20 columnas (x=0..19) x 15 filas (y=0..14)
# 1 = Muros, repisas superiores, chimenea, caldero y camas (SÓLIDO)
# 7 = Mostrador de Vaelira (bloquea el paso pero permite interactuar con [E])
# 9 = Alfombra de salida inferior hacia la ciudad
# 0 = Suelo de madera y alfombra roja central (TRANSITABLE)

INTERIOR_BOTICA = [
    # 0   1   2   3   4   5   6   7   8   9  10  11  12  13  14  15  16  17  18  19
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 0: Techo y vigas
    [ 1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 1: Estantes altos
    [ 1,  1,  1,  1,  1,  1,  0,  0,  0,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 2: Pasillo interior Vaelira (x=6..8)
    [ 1,  1,  1,  7,  7,  7,  7,  7,  7,  7,  7,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 3: Mostrador sólido superior
    [ 1,  1,  1,  7,  7,  7,  7,  7,  7,  7,  7,  1,  0,  0,  0,  0,  1,  1,  1,  1], # 4: Cajones del mostrador
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1], # 5: Suelo frente al mostrador (hablar aquí)
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1], # 6: Alfombra central
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1], # 7: Alfombra central
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  1], # 8: Alfombra central
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  1,  1,  1,  1], # 9: Alrededor de la cama inferior
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  0,  1,  1,  1,  1], # 10: Cama inferior central
    [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1], # 11: Pasillo inferior
    [ 1,  1,  1,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,  1], # 12: Frente al tapete rojo
    [ 1,  1,  1,  1,  1,  1,  1,  1,  9,  9,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1], # 13: Tapete de salida
    [ 1,  1,  1,  1,  1,  1,  1,  1,  9,  9,  1,  1,  1,  1,  1,  1,  1,  1,  1,  1]  # 14: Muro inferior
]
