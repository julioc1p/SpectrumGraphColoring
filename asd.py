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

class SWOImprove:

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
    
    def swo(self, vertex_order, spectrum, base_solution):
        max_iters = 20
        iters = 0
        n_vertices = len(vertex_order)
        vertex_order = [[v, n_vertices - i] for i, v in enumerate(vertex_order)]
        k = len(spectrum)
        solution = None
        best = 1e10
        a = 0.9
        b = 4
        while iters < max_iters:
            coloring = self._color(vertex_order, spectrum,base_solution)
            t = base_solution.threshold(coloring)
            if t < best:
                best = t
                solution = coloring
            for i, v in enumerate(vertex_order):
                v[1] = n_vertices-i
                if base_solution.vertex_interference(v[0], coloring) >= a*t:
                    v[1] += b
            vertex_order = self._sort(vertex_order)            
            iters+=1
        return base_solution.threshold(solution), solution
  

class CombinedSGraphColoring(VertexMergeGraphColoring):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        """ Solution for the TSC problem using TSC-DSATUR heuristic 
        """
        super().ThresholdSpectrumColoring(k)
        swo = SWOImprove()
        _, coloring = swo.swo(self._vertex_order, self._spectrum[:k], self)
        ss = SimpleSImprove()
        return ss._simple_search(coloring, self._spectrum[:k], self)
