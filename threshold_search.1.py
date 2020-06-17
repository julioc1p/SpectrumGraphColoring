import numpy as np
import sys
import random
from vertex_merge import VertexMergeGraphColoring
from graph2 import Graph


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a DSATUR-based heuristic.
"""

class ThresholdSGraphColoring(VertexMergeGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)
        vertices = graph.vertices()
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in vertices}
        self._saturation_degree = {}
        self._color_interference = {}


    def _min_semi_interference(self, vertex, semi_coloring, spectrum):
        """ calculates the color with the lowest potential interference in the 
            coloring 'semi_coloring' for 'vertex' using self._color_interference.
        """
        best_c = None
        best = 1e10
        for c in spectrum:
            if self._color_interference[vertex][c] < best:
                best = self._color_interference[vertex][c]
                best_c = c
        return best_c

    def _update_values(self, vertex,color, semi_coloring, is_CSC=False, update_color=False):
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

    def ThresholdSpectrumColoring(self, k):
        """ Solution for the TSC problem using TSC-DSATUR heuristic 
        """
        _, semi_coloring = super().ThresholdSpectrumColoring(k)
        self._tabu_search(semi_coloring, self._spectrum[:k])
        return self.threshold(semi_coloring), semi_coloring

    def _new_coloring(self):
        """ cleans the self.saturation_degree and self._color_interference values
            and returns a new empty coloring
        """
        self._saturation_degree = {v:0 for v in self.vertices()}
        self._color_interference = {v:{c:0 for c in self._spectrum} for v in self.vertices()}
        return {v:None for v in self.vertices()}

    def _coloring2str(self, coloring):
        s = ''
        for item in coloring:
            s += str(item) + ':' + str(coloring[item]) + '-'
        return s

    def _tabu_search(self, coloring, spectrum):
        max_iters = 20
        iters = 0
        # tabus = []
        rep = int(len(self._graph.vertices())/3)
        best = self.threshold(coloring)
        while iters < max_iters:
            # c_mark = self._coloring2str(coloring)
            for v in random.sample(self.vertices(), rep):
                c = None#self._min_semi_interference(v, coloring, spectrum)
                v_color = coloring[v]
                # coloring[v] = c
                # v_mark = self._coloring2str(coloring)
                t = self.threshold(coloring)
                for color in spectrum:
                    # v_color = coloring[v]
                    coloring[v] = color
                    t0 = self.threshold(coloring)
                    if t0 < t:
                        c = color
                        t = t0
                # t = threshold - self._potential_interference(v, v_color, coloring) + self._potential_interference(v, c, coloring)
                coloring[v] = v_color
                if t < best:
                    best = t
                    self._update_values(v,c, coloring, True, True)
                    coloring[v] = c
                    # tabus.append((c_mark, v_mark))
                    # tabus.append((v_mark, c_mark))
                    # if len(tabus) == 14:
                    #     tabus.pop()
                    #     tabus.pop()
                    break
            # if changed:
            #     print(iters)
            iters+=1
                



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