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

    def _opt_fun(self, x, k=4):
        """ function of optimization used for the PSO algorithm,
            where "x" is the swarm vector and "k" is the k from the
            self.ThresholdSpectrumColoring method, .i.e the color number.    
        """
        n_vertices = x.shape[0] # Dimension of the vectors
        vertices = self.vertices()

        coloring = self._index2dict(x)
        if len(set(coloring.values())) > k:
            return 1e10
        return np.array(sum([self.vertex_interference(v, coloring) for v in self.vertices()]))

        weights = [] # weights array which will be returned
        # It is important to explain that we use a index representation of
        # the colorings, because it is more efficient for the PSO's computations
        for c in x:
            coloring = self._index2dict(c) # corverting the coloring to the dict representation
            # case when the coloring has more than k colors
            if len(set(coloring.values())) > k:
                weights.append(1000000)
            else:
                weights.append(sum([self.vertex_interference(vertices[i], coloring) for i in range(n_vertices)]))
        return np.array(weights)

    # def best_hyperparameter_search(self, swarm_size=10, iterations=1000):
    #     from pyswarms.utils.search import RandomSearch
    #     dim = len(self.vertices()) # Dimension of vector X
    #     constraints = (0*np.ones(dim), len(self._spectrum)*np.ones(dim)) # limits for the vector values
    #     options = {
    #         'c1': [1, 5],
    #         'c2': [6, 10],
    #         'w': [2, 5],
    #         'k': [11, 15],
    #         'p': 1
    #     }
    #     g = RandomSearch(ps.single.GlobalBestPSO, 
    #                                         n_particles=swarm_size,
    #                                         dimensions=dim,
    #                                         options=options,
    #                                         iters=iterations,
    #                                         n_selection_iters=100,
    #                                         objective_func=self._opt_fun)
    #     # _, best_c = optimazer.optimize(objective_func=self._opt_fun, iters=iterations, k=k)
    #     return g.search()[1]
    
    def ThresholdSpectrumColoring(self, k, swarm_size=15, c1=1.0, c2=3.0, w=0.5, iterations=500):
        """ Solution for the TSC problem using a PSO algorithm
            It takes some aditional parameters for the algorithm
        """
        # Setting up the parameters for the algorithm
        dim = len(self.vertices()) # Dimension of vector X
        # constraints = (0*np.ones(dim), k*np.ones(dim)) # limits for the vector values
        # options = {'c1': c1, 'c2':c2, 'w':w}
        # optimazer = ps.single.GlobalBestPSO(n_particles=swarm_size,
        #                                     dimensions=dim,
        #                                     options=options,
        #                                     bounds=constraints)
        # _, best_c = optimazer.optimize(objective_func=self._opt_fun, iters=iterations, k=k)
        pso = MyPSO(swarm_size, dim, (0, k))
        _, best_c = pso.minimize(self._opt_fun, iterations , w, c1, c2, k=k)
        best_c = self._index2dict(best_c)
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
