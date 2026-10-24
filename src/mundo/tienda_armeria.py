CATALOGO_ARMERIA = [
    {
        "id": "espada_hierro",
        "nombre": "Filo Rúnico",
        "precio": 50,
        "ranura": "arma",
        "bono": 8,
        "desc": "+8 ATK. Incrementa el daño base de los ataques físicos."
    },
    {
        "id": "coraza_malla",
        "nombre": "Cota de Escamas",
        "precio": 45,
        "ranura": "armadura",
        "bono": 15,
        "desc": "+15 HP Max. Refuerza la resistencia general del portador."
    },
    {
        "id": "anillo_eter",
        "nombre": "Banda de Resonancia",
        "precio": 60,
        "ranura": "accesorio",
        "bono": 5,
        "desc": "+5 MP Max. Amplía la reserva de energía para habilidades."
    }
]

def intentar_comprar_armeria(indice_item, monedas_actuales, inventario_actual):
    """
    Gestiona la compra de equipamiento en la forja/armería de Doran.
    Retorna: (exito: bool, monedas_restantes: int, mensaje: str)
    """
    if 0 <= indice_item < len(CATALOGO_ARMERIA):
        item = CATALOGO_ARMERIA[indice_item]
        if monedas_actuales >= item["precio"]:
            monedas_actuales -= item["precio"]
            inventario_actual.append(item["nombre"])
            return True, monedas_actuales, f"¡Forjaste [{item['nombre']}] por {item['precio']} oro!"
        else:
            return False, monedas_actuales, f"Oro insuficiente. Doran pide {item['precio']} monedas."
    return False, monedas_actuales, "Objeto no válido."