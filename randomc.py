from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from random import choice


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a random strategy
"""

class RandomGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)

    def ThresholdSpectrumColoring(self, k):
        coloring = {v:None for v in self.vertices()}
        spectrum = self._spectrum[:k]
        for v in self.vertices():
            coloring[v] = choice(spectrum)
        return self.threshold(coloring), coloring

    def ChromaticSpectrumColoring(self, t):
        for i in range(2, len(self._spectrum)):
            t0, coloring = self.ThresholdSpectrumColoring(i)
            if t0 <= t:
                return i, coloring
        return len(self._spectrum), {v:None for v in self.vertices()}