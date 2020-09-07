""" Experimentos de los problemas TSC y CSC en grafos reales y aleatorios.
    Todos los experimentos usaran los algoritmos definidos en el diccionario 'algorithms'.
"""

import json
from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from dsatur import DSATURGraphColoring
from randomc import RandomGraphColoring
from vertex_merge import VertexMergeGraphColoring
from bfs import BFSGraphColoring
from simple_search import SimpleSearch
from degree_bfs import DegreeBFSGraphColoring
from swo import SWOGraphColoring
from improved_methods import DSATURPlusSS, VMPlusSS, \
    BFSPlusSS, DBFSPlusSS, SWOPlusSS
from tester import GraphTester
from weight_funtions import inv_pow2, mydist
from dimacs import dimacs_reader


# Algoritmos usados en los experimentos
algorithms = {
    # 'RANDOM': RandomGraphColoring,
    'DSATUR': DSATURGraphColoring,
    'BFS': BFSGraphColoring,
    'DegreeBFS': DegreeBFSGraphColoring,
    'VM': VertexMergeGraphColoring,
    'SWO': SWOGraphColoring,
    # algoritmos con Busqueda simple
    'DSATUR+SS': DSATURPlusSS,
    'BFS+SS': BFSPlusSS,
    'DBFS+SS': DBFSPlusSS,
    'VM+SS': VMPlusSS,
    'SWO+SS': SWOPlusSS}


##############################################
## Tests para grafos aleatorios
##############################################

# Test de TSC general para grafos aleatorios
def tsc_test_for_random_graph(algorithms, n_vertices, p, s_size, n_graph, graph_iters, k):
    rtest = GraphTester()
    rtest.make_spectrum(s_size)
    rtest.make_w(inv_pow2)
    return rtest.run_random_test(n_graph, n_vertices, p , k, algorithms, graph_iters)

# Test de CSC general para grafos aleatorios
def csc_test_for_random_graph(algorithms, n_vertices, p, s_size, n_graph, graph_iters, t):
    rtest = GraphTester()
    rtest.make_spectrum(s_size)
    rtest.make_w(inv_pow2)
    return rtest.run_random_test(n_graph , n_vertices, p, t, algorithms, graph_iters, TSC_OR_CSC='CSC')

def tsc_simple_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC simple test for random graphs')
    global algorithms
    statistics = tsc_test_for_random_graph(algorithms, 60, 0.1, 4, 5, 3, 4)
    if save_file is True:
        with open('tsc_simple_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_medium_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC medium test for random graphs')
    global algorithms    
    statistics = tsc_test_for_random_graph(algorithms, 80, 0.5, 11, 10, 5, 11)
    if save_file is True:
        with open('tsc_medium_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_complex_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC complex test for random graphs')
    global algorithms    
    statistics = tsc_test_for_random_graph(algorithms, 80, 0.9, 11, 15, 10, 11)
    if save_file is True:
        with open('tsc_complex_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_full_test_for_random_graph(save_file=True):
    global algorithms    
    statistics = {}
    for k in [4, 11, 20]:
        for n in [60, 80, 100]:
            for p in [0.1, 0.5, 0.9]:
                print("_________________________________")
                print("---------------------------------")
                print(f'k={k}_n={n}_p={p}')
                statistics[f'k={k}_n={n}_p={p}'] = tsc_test_for_random_graph(algorithms, n, p, k, 15, 10, k)
    if save_file is True:
        with open('tsc_full_test_for_random_graph_all.json', 'w') as handle:
                handle.write(json.dumps(statistics))

def csc_simple_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('CSC simple test for random graphs')
    global algorithms
    statistics = csc_test_for_random_graph(algorithms, 60, 0.5, 60, 5, 3, 15)
    if save_file is True:
        with open('csc_simple_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def csc_medium_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('CSC medium test for random graphs')
    global algorithms    
    statistics = csc_test_for_random_graph(algorithms, 60, 0.5, 60, 10, 5, 20)
    if save_file is True:
        with open('csc_medium_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def csc_complex_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('CSC complex test for random graphs')
    global algorithms    
    statistics = csc_test_for_random_graph(algorithms, 80, 0.9, 80, 20, 10, 18)
    if save_file is True:
        with open('csc_complex_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def csc_full_test_for_random_graph(save_file=True):
    global algorithms    
    statistics = {}
    for t in ['np/5', 'np/2']:
        for n in [60, 80, 100]:
            for p in [0.1, 0.5, 0.9]:
                print("_________________________________")
                print("---------------------------------")
                print(f't={t}_n={n}_p={p}')
                if t == 'np/5':
                    statistics[f't={t}_n={n}_p={p}'] = csc_test_for_random_graph(algorithms, n, p, n, 15, 10, n*p/5)
                elif t == 'np/2':
                    statistics[f't={t}_n={n}_p={p}'] = csc_test_for_random_graph(algorithms, n, p, n, 15, 10, n*p/2)
    if save_file is True:
        with open('csc_full_test_for_random_graph.json', 'w') as handle:
                handle.write(json.dumps(statistics))

##############################################
## Tests para grafos NO aleatorios
##############################################

# Test de TSC general para grafos
def tsc_test(algorithms, graph, s_size, iters, k):
    rtest = GraphTester()
    rtest.make_spectrum(s_size)
    rtest.make_w(mydist)
    return rtest.run_test2(graph, k, algorithms, iters)

# Test de CSC general para grafos
def csc_test(algorithms, graph, s_size, iters, t, pow2=False):
    rtest = GraphTester()
    rtest.make_spectrum(s_size)
    rtest.make_w(mydist)
    return rtest.run_test2(graph , t, algorithms, iters, TSC_OR_CSC='CSC')

simple_graph = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b", "d"],
        "d": ["c"]
    }
simple_graph = Graph(simple_graph)


def simple_tsc_test():
    print("_________________________________")
    print("---------------------------------")
    print('Simple TSC test')
    global algorithms    
    tsc_test(algorithms, simple_graph, 4, 10, 4)

def simple_csc_test():
    print("_________________________________")
    print("---------------------------------")
    print('Simple CSC test')
    global algorithms    
    csc_test(algorithms, simple_graph, 4, 10, 1, pow2=True)

# Caso real de baja densidad de una red
LD = {
        '1': ['2', '3', '4', '5'],
        '2': ['1', '3', '4', '5', '6'],
        '3': ['1', '2', '4', '5', '6'],
        '4': ['1', '2', '3', '5', '6', '7', '8'],
        '5': ['1', '2', '3', '4', '6', '7', '8', '9'],
        '6': ['2', '3', '4', '5', '7', '8', '9', '10'],
        '7': ['4', '5', '6', '8', '9', '10'],
        '8': ['4', '5', '6', '7', '9', '10', '11'],
        '9': ['5', '6', '7', '8', '10', '11', '12'],
        '10': ['6', '7', '8', '9', '11', '12', '13', '14'],
        '11': ['8', '9', '10', '12', '13', '14', '15'],
        '12': ['9', '10', '11', '13', '14', '15'],
        '13': ['10', '11', '12', '14', '15', '16'],
        '14': ['10', '11', '12', '13', '15', '16', '17'],
        '15': ['11', '12', '13', '14', '16', '17'],
        '16': ['13', '14', '15', '17', '18'],
        '17': ['14', '15', '16', '18'],
        '18': ['16', '17']
}


def test_for_ld_graph(save_file=True):
    print("_________________________________")
    print("---------------------------------")
    print('Test for LD graph with TSC')
    graph = Graph(LD)
    global algorithms
    statistics = tsc_test(algorithms, graph, 11, 100, 11)
    if save_file is True:
        with open('test_for_real_case_ld.json', 'w') as handle:
            handle.write(json.dumps(statistics))

# Caso real de alta densidad de una red
HD = {
            '1': ['2', '3', '4', '5', '6', '7'], #6
            '2': ['1', '3', '4', '5', '6', '7', '24', '26'], #8
            '3': ['1', '2', '4', '5', '6', '7', '9', '13', '15', '22', '24'], #11
            '4': ['1', '2', '3', '5', '7', '9', '13', '15', '22', '24', '25', '26'],#13
            '5': ['1', '2', '3', '4', '6', '7', '8', '9'], #8
            '6': ['1', '2', '3', '5', '7', '8', '9', '10', '11', '13'], #10            
            '7': ['1', '2', '3', '4', '5', '6', '8', '9', '11', '13', '15', '22', '24'], #13
            '8': ['5', '6', '7', '9', '10', '11', '13', '14'], #8
            '9': ['3', '4', '5', '6','7', '8', '10', '11', '13', '14', '15', '16', '22'],#13
            '10': ['6', '8', '9', '11', '13', '14'], #6
            '11': ['6', '8', '9', '10', '13', '14', '15'],#7
            # '12': ['8', '9', '10', '11', '13', '14', '16'], #7
            '13': ['3', '4', '6', '7', '8', '9', '10', '11', '14', '15', '16', '17', '22'],#13
            '14': ['8', '9', '10', '11', '13', '15', '16', '17', '18', '22'], #10
            '15': ['3', '4', '7', '9', '11', '13', '14', '16', '17', '18', '21', '22', '23', '24', '25'],#14
            '16': ['9', '13', '14', '15', '17', '18', '19', '20', '21', '22', '23'],#11
            '17': ['13', '14', '15', '16', '18', '19', '20', '21', '22', '23', '24'],#11
            '18': ['14', '15', '16', '17', '19', '20', '21', '22', '23'],#9
            '19': ['16', '17', '18', '20', '21', '22', '23'],#7
            '20': ['16', '17', '18', '19', '21', '22'],#6
            '21': ['15', '16', '17', '18', '19', '20', '22', '23', '24', '25'],#10
            '22': ['3', '4', '7', '9', '13', '14', '15', '16', '17', '18', '19', '20', '21', '23', '24', '25', '26'],#17
            '23': ['15', '16', '17', '18', '19' ,'21', '22', '24', '25', '26'],#10
            '24': ['2', '3', '4', '7', '15', '17', '21', '22', '23', '25', '26'],#11
            '25': ['4', '15', '21', '22', '23', '24', '26'],#7
            '26': ['2', '4' , '22', '23', '24', '25']#6
}


def test_for_hd_graph(save_file=True):
    print("_________________________________")
    print("---------------------------------")
    print('Test for HD graph with TSC')
    graph = Graph(HD)
    global algorithms
    statistics = tsc_test(algorithms, graph, 11, 100, 11)
    if save_file is True:
        with open('test_for_real_case_hd.json', 'w') as handle:
            handle.write(json.dumps(statistics))

# Test para grafo en representacio DIMACS
def test_for_dimacs_graph(graph_path, save_file=True):
    case_name = graph_path.split('/')[-1]
    print("_________________________________")
    print("---------------------------------")
    print('Test for {} graph with TSC'.format(case_name))
    graph = dimacs_reader(graph_path)
    global algorithms
    statistics = tsc_test(algorithms, graph, 11, 100, 11)
    if save_file is True:
        with open('test_for_{}.json'.format(case_name), 'w') as handle:
            handle.write(json.dumps(statistics))

if __name__ == "__main__":
    
    ##############################################
    ## Tests for simple graph "simple_graph"
    ##############################################

    # simple_tsc_test() # simple test for TSC
    # simple_csc_test() # simple test for CSC

    ##############################################
    ## Tests for random graphs
    ##############################################

    # TSC tests
    # tsc_simple_test_for_random_graph() # simple test
    # tsc_medium_test_for_random_graph() # medium test
    # tsc_complex_test_for_random_graph() # complex test
    # tsc_full_test_for_random_graph(True) # full test

    # CSC tests
    # csc_simple_test_for_random_graph() # simple test
    # csc_medium_test_for_random_graph()  # medium test
    # csc_complex_test_for_random_graph() # complex test
    # csc_full_test_for_random_graph(True) # full test

    ##############################################
    ## Tests for real graphs
    ##############################################

    # test_for_ld_graph() # test for a real low-density graph
    # test_for_hd_graph() # test for a real high-density graph

    ##############################################
    ## Tests for DIMACS graphs
    ##############################################

    # test_for_dimacs_graph('DIMACS/hamming6-2.mtx')


    ### Codigo para hacer un sonido 'Beep' al final de la ejecucion
    # import os
    # freq = 440
    # time = 3
    # os.system('play -nq -t alsa synth {}'.format(time, freq))