""" Codigo de Python para encontrar el maximo comun
    divisor de dos o de una lista de numeros flotantes.
"""

import math

def lgcd(numbers):
    """Determina el maximo comun divisor de una lista de numeros flotantes.
    Se asume que la lista tiene al menos dos elementos.

    Args:
        numbers (list): Lista de numeros.

    Returns:
        float: Maximo comun divisor.
    """    
    # calculamos el maximo comun divisor entre los dos primeros
    # elementos de la lista
    numb1, numb2 = numbers[0], numbers[1]
    _gcd = gcd(numb1, numb2)
    # calculamos el maximo comun divisor entre el que tenemos y cada
    # elemento de la lista
    for i in numbers[2:]:
        _gcd = gcd(_gcd, i)
    return _gcd

def gcd(x, y):
    """Determina el maximo comun divisor de dos numeros que pueden ser flotantes.

    Args:
        x (float): Primer numero.
        y (float): Segundo numero.

    Returns:
        float: Maximo comun divisor de 'x' y 'y'.
    """    
    # si 'x' es menor que 'y' invertimos para garantizar que
    # el primero argumento es el mayor (o son iguales)
    if x < y:
        return gcd(y, x)
    # caso base
    if abs(y) < 0.0001 :
        return x
    else:
        # calculamos el mcd recursivo por el metodo de Euclides
        return (gcd(y, x - math.floor(x/y)*y))


if __name__ == "__main__":
    
    x = .5
    y = .25
    print(f'GCD of {x} and {y} :')
    print(f'{gcd(x, y)}')

    l = [.05, .25, .75, .5]
    print(f'GCD of the list {l} :')
    print(lgcd(l))