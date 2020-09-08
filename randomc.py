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

if __name__ == "__main__":
    

    g = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b", "d"],
        "d": ["c"]
    }
    graph = Graph(g)
    S = ["1", "2", "3", "4"]
    W = {
        "1": {"1": 1, "2": .5, "3": .25, "4":.125},
        "2": {"1": .5, "2": 1, "3": .5, "4": .25},
        "3": {"1": .25, "2": .5, "3": 1, "4": .5},
        "4": {"1": .125, "2": .25, "3": .5, "4": 1}        
    }
    sgraph = RandomGraphColoring(graph, S, W)

    k0 = 3
    t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    k = sgraph.ChromaticSpectrumColoring(t0)
    print('Graph:')
    print(sgraph)
    print(f'Random best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    print(f'Random best value and coloring for the CSC problem and t = {t0}:')
    print(k)