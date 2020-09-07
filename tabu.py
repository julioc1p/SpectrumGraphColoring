import numpy as np
import sys
import random
from vertex_merge import VertexMergeGraphColoring
from graph2 import Graph


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a DSATUR-based heuristic.
"""

                
class TabuGraphColoring(VertexMergeGraphColoring):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])

    def simple_search(self, coloring, spectrum, max_iters=30, n_vertices=0):
        if n_vertices is 0:
            n_vertices = int(len(self.vertices()))
        iters = 0
        best_coloring = coloring.copy()
        best = self.threshold(coloring)
        tabu_memory = {v:{c:0 for c in spectrum} for v in self.vertices()}
        while iters < max_iters:
            for v in self.vertices():
                c = self._min_semi_interference(v, coloring, spectrum)
                if self._color_interference[v][c] < self._color_interference[v][coloring[v]] \
                    and tabu_memory[v][c] < iters:
                    coloring[v] = c
                    self._update_values(v,c, coloring, True, True)
                    tabu_memory[v][c] = iters + 7
                    t = self.threshold(coloring)
                    if t < best:
                        # print(iters)
                        best = t
                        best_coloring = coloring.copy()
                    # break
            iters+=1
        return self.threshold(best_coloring), best_coloring


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