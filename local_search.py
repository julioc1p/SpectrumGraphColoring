import numpy as np
import sys
import random
from vertex_merge import VertexMergeGraphColoring
from graph2 import Graph


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a DSATUR-based heuristic.
"""

class LocalSGraphColoring(VertexMergeGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)
        vertices = graph.vertices()
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in vertices}
        self._saturation_degree = {}
        self._color_interference = {}

    def _update_values(self, vertex,color, semi_coloring, is_CSC=True, update_color=False):
        """ updates the internal values to compute the saturation degree and
            the color interference.
        """
        # add 1 to saturation degree of every v's neighbours
        for w in self._graph.neighbours(vertex):
            self._saturation_degree[w]+=1
            # if is_CSC is True it should update for every neighbours
            # no matter it is not None
            if semi_coloring[w] is None or is_CSC is True:
                # update the potential interference in w for every color
                for c in self._spectrum:
                    self._color_interference[w][c]+= self._w[color][c]
                    if update_color is True:
                        self._color_interference[w][c] -= self._w[semi_coloring[vertex]][c]

    def _decrease_value(self, vertex, color):
        for w in self._graph.neighbours(vertex):
            for c in self._spectrum:
                self._color_interference[w][c] -= self._w[color][c]

    def ThresholdSpectrumColoring(self, k):
        """ Solution for the TSC problem using TSC-DSATUR heuristic 
        """
        _, coloring = super().ThresholdSpectrumColoring(k)
        new_coloring = coloring.copy()
        self._local_search(new_coloring, self._spectrum[:k])
        while self.threshold(new_coloring) < self.threshold(coloring):
            print(self.threshold(new_coloring))
            coloring = new_coloring
            new_coloring = coloring.copy()
            self._local_search(new_coloring, self._spectrum[:k])
        return self.threshold(coloring), coloring

    def _local_search(self, coloring, spectrum):
        tmax = self.threshold(coloring)
        tabu = {v:False for v in self.vertices()}
        depth = 0
        cl = [v for v in self.vertices() if self.vertex_interference(v, coloring) == tmax]
        while cl and depth < 10:
            pool = cl
            cl = []
            while pool:
                v = pool.pop()
                tabu[v] = True
                vmax_interf = self._max_interf_vertice(v, coloring, tabu)
                if not vmax_interf:
                    continue
                color, new_interf = self._min_color(v, spectrum, [coloring[w] for w in vmax_interf])
                if new_interf >= tmax:
                    return False
                self._update_values(v, color, coloring, True, True)
                coloring[v] = color
                # print(self.threshold(coloring))
                cl += vmax_interf
            depth+=1
        return True
                    

    def _min_color(self, vertex, spectrum, icolor):
        """ calculates the color with the lowest potential interference in the 
            coloring 'semi_coloring' for 'vertex' using self._color_interference.
        """
        best_c = None
        best = 1e10
        for c in spectrum:
            interference = self._color_interference[vertex][c]
            for ic in icolor:
                interference-=self._w[c][ic]
            if interference < best:
                best = interference
                best_c = c
        return best_c, best

    def _max_interf_vertice(self, vertex, coloring, tabu):
        max_interf = 0
        vertices = []
        c = coloring[vertex]
        for v in self._graph.neighbours(vertex):
            if tabu[v]:
                continue
            interference = self._w[c][coloring[v]]
            if interference > max_interf:
                max_interf = interference
                vertices = [v]
            elif interference == max_interf:
                vertices.append(v)
        for v in vertices:
            tabu[v]=True
        return vertices
        
                



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
    sgraph = SWOGraphColoring(graph, S, W)

    k0 = 3
    t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    # k = sgraph.ChromaticSpectrumColoring(t0)
    print('Graph:')
    print(sgraph)
    print(f'PSO best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    # print(f'PSO best value and coloring for the TSC problem and t = {t0}:')
    # print(k)