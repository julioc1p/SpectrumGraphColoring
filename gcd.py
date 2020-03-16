""" Python code for finding the GCD of
    two  or a list of floating numbers .
"""

import math

def lgcd(numbers):
    """ Return the gcd of the list "numbers"
        using the functiom gcd .
    """
    numb1, numb2 = numbers[0], numbers[1]
    _gcd = gcd(numb1, numb2)
    for i in numbers[2:]:
        _gcd = gcd(_gcd, i)
    return _gcd

def gcd(x, y):
    """ Recursive function to return gcd 
        of x and y .
    """
    if x < y:
        return gcd(y, x)
    # base case
    if abs(y) < 0.0001 :
        return x
    else:
        return (gcd(y, x - math.floor(x/y)*y))


if __name__ == "__main__":
    
    x = .5
    y = .25
    print(f'GCD of {x} and {y} :')
    print(f'{gcd(x, y)}')

    l = [.05, .25, .75, .5]
    print(f'GCD of the list {l} :')
    print(lgcd(l))