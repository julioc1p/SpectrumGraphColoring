import numpy as np
import pyswarms as ps
from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from mypso import MyPSO
import psopy


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using an optimizer based in
    Particle Swarm Optimization (PSO).
"""

class PSOGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)

    def _index2dict(self, c):
        """ takes a coloring with a index representation ( it is a representation
            where the positions represents the index of the vertices and the values 
            there represents the index of the colors of that vertices ) and transform
            in the usual dict representation.
        """
        vertices = self.vertices()
        return {vertices[i]:self._spectrum[int(c[i]-1e-10)] for i in range(len(c))}

    def _opt_fun(self, x, k):
        """ function of optimization used for the PSO algorithm,
            where "x" is a vector and "k" is the k from the
            self.ThresholdSpectrumColoring method, .i.e the color number.    
        """
        coloring = self._index2dict(x) # corverting the coloring to the dict representation
        # Case when the coloring has more than k colors, so it is not valid
        if len(set(coloring.values())) > k:
            return 1e10
        return np.array(sum([self.vertex_interference(v, coloring) for v in self.vertices()]))

    def ThresholdSpectrumColoring(self, k, swarm_size=15, c1=1.0, c2=3.0, w=0.5, iterations=500):
        """ Solution for the TSC problem using a PSO algorithm
            It takes some aditional parameters for the algorithm
        """
        dim = len(self.vertices()) # Dimension of vector X
        pso = MyPSO(swarm_size, dim, (0, k)) # PSO object which sets up the dimensions and vector limits
        _, best_c = pso.minimize(self._opt_fun, iterations , w, c1, c2, k=k) 
        best_c = self._index2dict(best_c) # corverting the coloring to the dict representation
        return self.threshold(best_c), best_c

    def ChromaticSpectrumColoring(self, t, swarm_size=15, c1=1.0, c2=3.0, w=0.5, iterations=500):
        """ Solution for the CSC problem using a PSO algorithm
            It takes some aditional parameters for the algorithm
        """
        n_vertices = len(self.vertices())
        # we will just check for every 1 <= K <= n_vertices if the
        # previuos TSC algorithm result is lower than the threshold "t",
        # and the least of these Ks will be our result.
        for k in range(2, n_vertices):
            threshold, best_c = self.ThresholdSpectrumColoring(k, swarm_size, c1, c2, w, iterations)
            if threshold <= t:
                return k, best_c
        return n_vertices, {v:None for v in self.vertices()}
    

if __name__ == "__main__":
    

    g = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b", "d"],
        "d": ["c"]
    }
    graph = Graph(g)
    S = ["red", "green", "blue", "violet"]
    W = {
        "red": {"red": 1, "green": .5, "blue": .25, "violet":.125},
        "green": {"red": .5, "green": 1, "blue": .5, "violet": .25},
        "blue": {"red": .25, "green": .5, "blue": 1, "violet": .5},
        "violet": {"red": .125, "green": .25, "blue": .5, "violet": 1}        
    }
    sgraph = PSOGraphColoring(graph, S, W)

    k0 = 3
    # t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    # k = sgraph.ChromaticSpectrumColoring(t0)
    # print('Graph:')
    # print(sgraph)
    print(f'PSO best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    # print(f'PSO best value and coloring for the TSC problem and t = {t0}:')
    # print(k)
