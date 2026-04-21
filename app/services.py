def calcular_valor_total(producto):
    return producto.valoru * producto.existencias


def calcular_estado(producto):
    if producto.existencias < 50:
        return "Bajo"
    elif producto.existencias <= 100:
        return "Medio"
    else:
        return "Alto"