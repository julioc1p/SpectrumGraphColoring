import random
from graph_coloring import SpectrumGraphColoring
from graph2 import Graph


class GRASPGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)
        vertices = graph.vertices()
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in vertices}
        self._saturation_degree = {}
        self._color_interference = {}

    def _min_semi_interference(self, vertex, spectrum):
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

    def _update_values(self, vertex,color, semi_coloring, is_CSC=False):
        """ updates the internal values to compute the saturation degree and
            the color interference.
        """
        # add 1 to saturation degree of every v's neighbours
        for w in self._graph.neighbours(vertex):
            self._saturation_degree[w]+=1
            # if is_CSC is True it should update for every neighbours
            # no matter it is not None
            if semi_coloring[w] is None or is_CSC:
                # update the potential interference in w for every color
                for c in self._spectrum:
                    self._color_interference[w][c]+= self._w[color][c]


    def ThresholdSpectrumColoring(self, k):
        semi_coloring = self._new_coloring()
        spectrum = self._spectrum[:k]
        r = random.choice(self.vertices())
        semi_coloring[r] = spectrum[0]
        self._update_values(r, spectrum[0], semi_coloring)
        n_colored = 1
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            cl = [v for v in semi_coloring if semi_coloring[v] is None]
            rcl = self._make_rcl(cl)
            vertex = random.choice(rcl)
            color = self._min_semi_interference(vertex, spectrum)
            semi_coloring[vertex] = color
            n_colored += 1
            self._update_values(vertex, color, semi_coloring)
        return self.threshold(semi_coloring), semi_coloring


    def _make_rcl(self, cl):
        a = 0.9
        evals = [self._eval(v) for v in cl]
        eth = min(evals) + a*(max(evals) - min(evals))
        rcl = [v for i, v in enumerate(cl) if evals[i] >= eth]
        return rcl

    def _eval(self, v):
        best_c = None
        best = 1e10
        for c in self._spectrum:
            if self._color_interference[v][c] < best:
                best = self._color_interference[v][c]
                best_c = c
        return best

    def _new_coloring(self):
        """ cleans the self.saturation_degree and self._color_interference values
            and returns a new empty coloring
        """
        self._saturation_degree = {v:0 for v in self.vertices()}
        self._color_interference = {v:{c:0 for c in self._spectrum} for v in self.vertices()}
        return {v:None for v in self.vertices()}