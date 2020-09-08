""" Consola interactiva util y sencilla consola que permite experimentar con los problemas de coloracion de grafos con espectros TSC y CSC.
"""

import os
import json
import platform
clear = lambda: os.system('clear')
if platform.system() == 'Windows':
    clear = lambda: os.system('cls')
from code.weight_functions import inv_pow2, empiric_dist
from code.dsatur import DSATURGraphColoring
from code.randomc import RandomGraphColoring
from code.vertex_merge import VertexMergeGraphColoring
from code.bfs import BFSGraphColoring
from code.simple_search import SimpleSearch
from code.degree_bfs import DegreeBFSGraphColoring
from code.swo import SWOGraphColoring
from code.improved_methods import DSATURPlusSS, VMPlusSS, \
    BFSPlusSS, DBFSPlusSS, SWOPlusSS
from code.dimacs import dimacs_reader
from tests import tsc_test, csc_test, tsc_test_for_random_graph, csc_test_for_random_graph


while True:
    clear()
    print('Bienvenidos a la consola interactiva para realizar experimentos\nen los problemas de coloracion de grafos con espectros TSC y CSC.\n')
    print('Introduzca el numero correspondiente para realizar experimentos en:\n \n(1) TSC \n(2) CSC\n')

    text = input()
    if text != '1' and text != '2':
        print('\nERROR: "{}" no es una opcion valida'.format(text))
        break
    TSC_OR_CSC = 'TSC' if text == '1' else 'CSC'
    print('\nIntroduzca el numero correspondiente para realizar experimentos con grafos:\n \n(1) Aleatorios \n(2) DIMACS\n')
    text = input()
    if text != '1' and text != '2':
        print('\nERROR: "{}" no es una opcion valida'.format(text))
        break
    RANDOM_OR_DIMACS = 'RANDOM' if text == '1' else 'DIMACS'
    clear()
    n_vertices = 0
    p = 0
    n_graph = 0
    dimacs_path = ''
    iters = 0
    s_size = 0
    matrix = None
    k = 0
    t = 0
    algorithms = {}
    if text == '1':
        print('Introduzca el numero de vertices (n) y la probabilidad de conexion (p)\nentre ellos, separados por un espacio:')
        text = input()
        text = text.split()
        if len(text) != 2:
            print('\nERROR: la cantidad de valores introducidos no es valida.')
            break
        try:
            n_vertices = int(text[0])
            p = float(text[1])
            if n_vertices <= 0 or p < 0 or p > 1:
                print('\nERROR: los valores introducidos no son validos.')
                break
        except:
            print('\nERROR: el tipo de los valores introducidos no es valido.')
            break
        print('\nIntroduzca el numero de grafos que desea generar y el numero de\nexperimentos con cada grafo, separados por un espacio:')
        text = input()
        text = text.split()
        if len(text) != 2:
            print('\nERROR: la cantidad de valores introducidos no es valida.')
            break
        try:
            n_graph = int(text[0])
            iters = int(text[1])
            if n_graph <= 0 or iters <= 0:
                print('\nERROR: los valores introducidos no son validos.')
                break
        except:
            print('\nERROR: el tipo de los valores introducidos no es valido.')
            break
    elif text == '2':
        print('En esta carpeta podemos encontrar un fichero "DIMACS.txt" que explica\nesta representacion, en caso de querer agregar nuevos grafos.\n')
        print('Introduzca el nombre del fichero de prueba de la carpeta /DIMACS:')
        text = input()
        if not os.path.isfile('DIMACS/'+text):
            print('\nERROR: el fichero {} no existe.'.format(text))
            break
        dimacs_path = 'DIMACS/'+text

        print('\nIntroduzca el numero de experimentos deseados:')
        text = input()
        try:
            iters = int(text)
            if iters <= 0 :
                print('\nERROR: el valor introducido no es valido.')
                break
        except:
            print('\nERROR: el tipo del valor introducido no es valido.')
            break
    if TSC_OR_CSC == 'TSC':
        print('\nIntroduzca el numero de colores del espectro:')
        text = input()
        try:
            s_size = int(text)
            if s_size <= 0 :
                print('\nERROR: el valor introducido no es valido.')
                break
        except:
            print('\nERROR: el tipo del valor introducido no es valido.')
            break
    print('\nIntroduzca el numero correspondiente a la matriz de interferencia deseada:\n \n(1) Decremento exponencial de base 2 \n(2) Valores de medida empiricos\n')
    text = input()
    if text != '1' and text != '2':
        print('\nERROR: "{}" no es una opcion valida'.format(text))
        break
    if text == '1':
        matrix = inv_pow2
    else:
        matrix = empiric_dist
    if TSC_OR_CSC == 'TSC':
        print('\nIntroduzca el valor del parametro k para el problema TSC:')
        text = input()
        try:
            k = int(text)
            if k <= 0 or k > s_size:
                print('\nERROR: el valor introducido no es valido.')
                break
        except:
            print('\nERROR: el tipo del valor introducido no es valido.')
            break
    else:
        print('\nIntroduzca el valor del parametro t para el problema CSC:')
        text = input()
        try:
            t = float(text)
            if t < 0 :
                print('\nERROR: el valor introducido no es valido.')
                break
        except:
            print('\nERROR: el tipo del valor introducido no es valido.')
            break

    algorithm_list = ['Random', 'DSATUR', 'BFS', 'DegBFS', 'VM', 'SWO', 'DSATUR+SS', 'BFS+SS', 'DegBFS+SS', 'VM+SS', 'SWO+SS']
    algorithm_dict = {
        'Random': RandomGraphColoring,
        'DSATUR': DSATURGraphColoring,
        'BFS': BFSGraphColoring,
        'DegBFS': DegreeBFSGraphColoring,
        'VM': VertexMergeGraphColoring,
        'SWO': SWOGraphColoring,
        'DSATUR+SS': DSATURPlusSS,
        'BFS+SS': BFSPlusSS,
        'DegBFS+SS': DBFSPlusSS,
        'VM+SS': VMPlusSS,
        'SWO+SS': SWOPlusSS
        }
    clear()
    print('Introduzca el numero correspondiente al algoritmo deseado, use un\nespacio entre ellos en caso de seleccionar mas de uno:\n')
    print('(0) Todos')
    for i, algorithm in enumerate(algorithm_list):
        print("({}) {}".format(i+1, algorithm))
    print()
    text = input()
    if text == '':
        print('\nERROR: no se selecciono ningun algoritmo.')
        break
    if text == '0':
        algorithms = algorithm_dict
    else:
        text = text.split()
        error = False
        for item in text:
            try:
                i = int(item)-1
                if i < 0 or i >= len(algorithm_list):
                    print('\nERROR: valor fuera del rango valido.')
                    error = True
                    break
                algorithms[algorithm_list[i]] = algorithm_dict[algorithm_list[i]]
            except:
                print('\nERROR: el tipo de valor introducido no es valido.')
                error = True
                break
        if error is True:
            break
    clear()
    print('Desea guardar el resultado de los experimentos en un fichero ?\n \n(y) Si')
    text = input()
    save_file = False
    file_name = 'results'
    if text == 'y':
        save_file = True
        text = input('\nIntroduzca un nombre para el fichero: ')
        if text != '':
            file_name = text
    clear()
    print('Por favor espere mientras se realizan los experimentos.\n')
    if TSC_OR_CSC == 'TSC':
        if RANDOM_OR_DIMACS == 'RANDOM':
            result = tsc_test_for_random_graph(algorithms, n_vertices, p, s_size, n_graph, iters, k, w_function=matrix)
        elif RANDOM_OR_DIMACS == 'DIMACS':
            result = tsc_test(algorithms, dimacs_reader(dimacs_path), s_size, iters, k, w_function=matrix)
    elif TSC_OR_CSC == 'CSC':
        if RANDOM_OR_DIMACS == 'RANDOM':
            result = csc_test_for_random_graph(algorithms, n_vertices, p, n_graph, iters, t, w_function=matrix)
        elif RANDOM_OR_DIMACS == 'DIMACS':
            result = csc_test(algorithms, dimacs_reader(dimacs_path), iters, t, w_function=matrix)
    if save_file is True:
        with open('{}.json'.format(file_name), 'w') as handle:
            handle.write(json.dumps(result))
    print()
    input('Pulse enter para continuar ... ')
