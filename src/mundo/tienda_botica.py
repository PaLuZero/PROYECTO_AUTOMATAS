CATALOGO_TIENDA = [
    {"id": "pocion", "nombre": "Poción Curativa", "precio": 15, "desc": "Restaura 45 HP a un héroe."},
    {"id": "eter", "nombre": "Éter Místico", "precio": 20, "desc": "Restaura 10 MP para habilidades de Vínculo."},
    {"id": "revivir", "nombre": "Fragmento del Despertar", "precio": 35, "desc": "Revive a un héroe noqueado con 50 HP."}
]

def intentar_comprar(indice_item, monedas_actuales, inventario_actual):
    """
    Retorna: (exito, monedas_restantes, mensaje)
    """
    if 0 <= indice_item < len(CATALOGO_TIENDA):
        item = CATALOGO_TIENDA[indice_item]
        if monedas_actuales >= item["precio"]:
            monedas_actuales -= item["precio"]
            inventario_actual.append(item["nombre"])
            return True, monedas_actuales, f"¡Compraste [{item['nombre']}] por {item['precio']} oro!"
        else:
            return False, monedas_actuales, f"Oro insuficiente. Requiere {item['precio']} oro."
    return False, monedas_actuales, "Objeto no válido."