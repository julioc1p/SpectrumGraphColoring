from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from pso import PSOGraphColoring
from dsatur import DSATURGraphColoring
from randomc import RandomGraphColoring
from vertex_merge import VertexMergeGraphColoring
from random_graph_tester import RandomGraphTester
from real_graph_tester import RealGraphTester
import json

""" Experiments for random and real case graphs for the
    TSC and CSC problems, using different techniques
"""

algorithms = {
    'RANDOM': RandomGraphColoring, 
    'DSATUR': DSATURGraphColoring, 
    'VM': VertexMergeGraphColoring}
    # 'PSO': PSOGraphColoring}


simple_graph = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b", "d"],
        "d": ["c"]
    }
simple_graph = Graph(simple_graph)

# general random tests
def tsc_test_for_random_graph(algorithms ,n_vertices, p, s_size, n_graph, graph_iters, k):
    rtest = RandomGraphTester(n_vertices, p, s_size)
    return rtest.run_test(k, algorithms, n_graph, graph_iters)

def csc_test_for_random_graph(algorithms ,n_vertices, p, s_size, n_graph, graph_iters, t):
    rtest = RandomGraphTester(n_vertices, p, s_size)
    return rtest.run_test(t, algorithms, n_graph, graph_iters, TSC_OR_CSC='CSC')

# TSC different random tests
def tsc_simple_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC simple test for random graphs')
    global algorithms
    statistics = tsc_test_for_random_graph(algorithms, 60, 0.5, 4, 5, 3, 4)
    if save_file is True:
        with open('tsc_simple_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_medium_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC medium test for random graphs')
    global algorithms    
    statistics = tsc_test_for_random_graph(algorithms, 60, 0.5, 11, 10, 5, 11)
    if save_file is True:
        with open('tsc_medium_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_complex_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('TSC complex test for random graphs')
    global algorithms    
    statistics = tsc_test_for_random_graph(algorithms, 80, 0.9, 11, 20, 10, 11)
    if save_file is True:
        with open('tsc_complex_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def tsc_full_test_for_random_graph(save_file=True):
    global algorithms    
    statistics = {}
    for k in [4, 6, 11]:
        for n in [60, 70, 80]:
            for p in [0.1, 0.5, 0.9]:
                statistics[f'k={k}_n={n}_p={p}'] = tsc_test_for_random_graph(algorithms, n, p, k, 20, 10, k)
    if save_file is True:
        with open('tsc_full_test_for_random_graph.json', 'w') as handle:
                handle.write(json.dumps(statistics))


# CSC different random tests
def csc_simple_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('CSC simple test for random graphs')
    global algorithms
    statistics = csc_test_for_random_graph(algorithms, 60, 0.5, 60, 5, 3, 22.5)
    if save_file is True:
        with open('csc_simple_test_for_random_graph.json', 'w') as handle:
            handle.write(json.dumps(statistics))

def csc_medium_test_for_random_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('CSC medium test for random graphs')
    global algorithms    
    statistics = csc_test_for_random_graph(algorithms, 60, 0.5, 60, 10, 5, 15)
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
    for t in ['np/4', 'np/2', '3np/4']:
        for n in [60, 70, 80]:
            for p in [0.1, 0.5, 0.9]:
                if t is 'np/4':
                    statistics[f't={t}_n={n}_p={p}'] = csc_test_for_random_graph(algorithms, n, p, n, 20, 10, n*p/4)
                elif t is 'np/2':
                    statistics[f't={t}_n={n}_p={p}'] = csc_test_for_random_graph(algorithms, n, p, n, 20, 10, n*p/2)
                elif t is '3np/4':
                    statistics[f't={t}_n={n}_p={p}'] = csc_test_for_random_graph(algorithms, n, p, n, 20, 10, 3*n*p/4)
    if save_file is True:
        with open('csc_full_test_for_random_graph.json', 'w') as handle:
                handle.write(json.dumps(statistics))

# general simple test
def tsc_test(algorithms, graph, s_size, iters, k, pow2=False):
    stest = RealGraphTester(graph, s_size, pow2_mode=pow2)
    return stest.run_test(k, algorithms, iters)

def csc_test(algorithms, graph, s_size, iters, t, pow2=False):
    stest = RealGraphTester(graph, s_size, pow2_mode=pow2)
    return stest.run_test(t, algorithms, iters, TSC_OR_CSC='CSC')

# TSC simple tests
def simple_tsc_test():
    print("_________________________________")
    print("---------------------------------")
    print('Simple TSC test')
    global algorithms    
    tsc_test(algorithms, simple_graph, 4, 10, 4, pow2=True)

# CSC simple tests
def simple_csc_test():
    print("_________________________________")
    print("---------------------------------")
    print('Simple CSC test')
    global algorithms    
    csc_test(algorithms, simple_graph, 4, 10, 1, pow2=True)

# Real case of LD graph
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
def test_for_ld_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('Test for LD graph with TSC')
    graph = Graph(LD)
    global algorithms
    statistics = tsc_test(algorithms, graph, 11, 100, 11)
    if save_file is True:
        with open('test_for_real_case_ld.json', 'w') as handle:
            handle.write(json.dumps(statistics))

# Real case of HD graph
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
def test_for_hd_graph(save_file=False):
    print("_________________________________")
    print("---------------------------------")
    print('Test for HD graph with TSC')
    graph = Graph(HD)
    global algorithms
    statistics = tsc_test(algorithms, graph, 11, 100, 11)
    if save_file is True:
        with open('test_for_real_case_hd.json', 'w') as handle:
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
    # tsc_full_test_for_random_graph() # full test

    # CSC tests
    # csc_simple_test_for_random_graph() # simple test
    # csc_medium_test_for_random_graph()  # medium test
    # csc_complex_test_for_random_graph() # complex test
    # csc_full_test_for_random_graph() # full test

    ##############################################
    ## Tests for real graphs
    ##############################################

    test_for_ld_graph() # test for a real low-density graph
    test_for_hd_graph() # test for a real high-density graph

    import os
    freq = 440
    time = 3
    os.system('play -nq -t alsa synth {}'.format(time, freq))