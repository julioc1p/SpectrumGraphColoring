""" Funciones de peso usadas para generar 
    la matriz de interfencia entre los colores.
"""

def inv_pow2(x, y):
    """ Funcion de decrecimiento exponencial de base 2 para
    la interferencia entre dos colores del espectro.

    Args:
        x : Color 1.
        y : Color 2.

    Returns:
        float: Interferencia entre ambos colores.
    """    
    return 1/2**abs(x-y)

def empiric_dist(x, y):
    """ Funcion de valores empiricos para la interferencia
    entre dos colores del espectro.

    Args:
        x : Color 1.
        y : Color 2.

    Returns:
        float: Interferencia entre ambos colores.
    """   
    dif = abs(x-y)
    if dif is 0:
        return 1
    elif dif is 1:
        return 0.8
    elif dif is 2:
        return 0.5
    elif dif is 3:
        return 0.2
    elif dif is 4:
        return 0.1
    elif dif is 5:
        return 0.001
    elif dif >= 6:
        return 0