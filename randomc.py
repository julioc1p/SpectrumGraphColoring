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
    S = ["red", "green", "blue", "violet"]
    W = {
        "red": {"red": 1, "green": .5, "blue": .25, "violet":.125},
        "green": {"red": .5, "green": 1, "blue": .5, "violet": .25},
        "blue": {"red": .25, "green": .5, "blue": 1, "violet": .5},
        "violet": {"red": .125, "green": .25, "blue": .5, "violet": 1}        
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