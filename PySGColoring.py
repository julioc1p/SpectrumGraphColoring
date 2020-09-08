""" Modulo que brinda varias herramientas para resolver los problemos de coloracion de grafos con espectros de colores TSC y CSC.
"""

from code.graph2 import Graph
from code.graph_coloring import SpectrumGraphColoring
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
from code.weight_functions import inv_pow2, empiric_dist


def random_graph(n, p):
    """Crea un grafo aleatorio de 'n' vertices con una probabilidad
    de conexion 'p'.

    Args:
        n (int): Cantidad de vertices del grafo.
        p (float): Probabilidad de que dos vertices del grafo esten conectados.

    Returns:
        Graph: Nuevo grafo.
    """        
    import random
    import numpy as np
    graph = np.zeros((n+1, n+1))
    for i in range(1, n+1):
        for j in range(i+1, n+1):
            if random.random() <= p:
                graph[i,j] = graph[j, i] = 1
    graph_dict = {}
    for i in range(1, n+1):
        neighbours_i = []
        for j in range(1, n+1):
            if graph[i,j]:
                neighbours_i.append(str(j))
        graph_dict[str(i)] = neighbours_i
    return Graph(graph_dict)

def make_spectrum(s_size):
        """Crear un espectro de colores desde 1 hasta 's_size'.

        Args:
            s_size (int): Dimension del espectro de colores.

        Returns:
            List: Espectro de colores.
        """        
        new_spectrum = [str(i) for i in range(1, s_size+1)]
        return new_spectrum

def make_w(spectrum, w_function):
        """Crea una matriz de interferencias para el espectro usando la funcion 'w_function'.
        Args:
            spectrum (list): Espectro de colores.
            w_function : Funcion de interferencia entre los colores.

        Returns:
            Matriz de interferencias.
        """        
        new_w = {item:{} for item in spectrum}
        for i, c1 in enumerate(spectrum):
            for j, c2 in enumerate(spectrum):
                new_w[c1][c2] = new_w[c2][c1] = w_function(i, j)
        return new_w