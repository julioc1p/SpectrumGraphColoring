import numpy as np
import sys
import random
from vertex_merge import VertexMergeGraphColoring
from simple_search import SimpleSImprove
from graph2 import Graph


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a DSATUR-based heuristic.
"""

class MyImprove:

    def _sort(self, vertices):
        if not vertices:
            return []
        m = vertices[0]
        g = []
        le = []
        for v in vertices[1:]:
            if v[1] > m[1]:
                g.append(v)
            else:
                le.append(v)
        return self._sort(g) + [m] + self._sort(le)

    def _color(self, vertex_order, spectrum, base_solution):
        semi_coloring = base_solution._new_coloring()
        for v in vertex_order:
            color = base_solution._min_semi_interference(v[0], semi_coloring, spectrum)
            semi_coloring[v[0]] = color
            base_solution._update_values(v[0], color, semi_coloring)
        return semi_coloring
    
    def myh(self, vertex_order, coloring, spectrum, base_solution):
        vertex_order = [[v, base_solution.vertex_interference(v, coloring)/base_solution._graph.vertex_degree(v)] for v in vertex_order]
        vertex_order = self._sort(vertex_order)
        coloring = self._color(vertex_order, spectrum, base_solution)
        return base_solution.threshold(coloring), coloring
        

class MyGraphColoring(VertexMergeGraphColoring):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        """ Solution for the TSC problem using TSC-DSATUR heuristic 
        """
        t, c = super().ThresholdSpectrumColoring(k)
        my = MyImprove()
        nt, c = my.myh(self._vertex_order, c, self._spectrum[:k], self)
        if nt < t:
            print('+++++')
        else:
            print('-----')
        return nt, c
        


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
    sgraph = CombinedSGraphColoring(graph, S, W)

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