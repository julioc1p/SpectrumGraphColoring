from graph2 import Graph

class GraphColoring(object):

    def __init__(self, graph, spectrum, w):
        self.__graph = graph
        self.__spectrum = spectrum
        self.__w = w

    def ThresholdSpectrumColoring(self, k):
        """ the TSC problem determinates the minimum threshold t, 
            such that (G, w) admits a k-coloring in which the interference
            at every vertex is at most t.
        """
        pass

    def ChromaticSpectrumColoring(self, t):
        """ the CSC problem fixes the parameter k
            and the spectrum is let to have as size the |V(G)|
            of vertices, the goal is determinate the minimum k,
            such that (G, w) admits a k-coloring in which the interference
            at every vertex is at most that threshold t.
        """
        pass