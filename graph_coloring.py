from graph2 import Graph
from gcd import lgcd

""" A Python Class
    A Python graph class for two Spectrum Graph Coloring problems,
    the Threshold Spectrum Coloring problem and the Chromatic Spectrum
    Coloring problem. This class implements some methods and 
    bounds for these problems.

    "Threshold Spectrum Coloring (TSC) problem":
        Given a graph G and a spectrum of k colors, endowed with
        a k × k matrix W of interferences between them, the goal is to determine
        the minimum threshold t ∈ R ≥0 such that (G, W ) admits a k-coloring c 
        in which the interference at every vertex is at most t.

    "Chromatic Spectrum Coloring (CSC) problem":
        Given a graph G and a spectrum of colors S, endowed with a |S| × |S|
        matrix W of interferences between them, a threshold t ∈ R ≥0 is fixed and 
        the spectrum is let to have as size the number |V (G)| of vertices, the goal
        being to determine the minimum number of colors k ∈ N such that (G, W ) admits
        a k-coloring c in which the interference at every vertex is at most that 
        threshold t.
"""

class SpectrumGraphColoring(object):

    def __init__(self, graph, spectrum, w, c=None):
        """ initializes a GraphColoring object
            "graph" is a Graph object, "spectrum" is a list
            of colors and "w" is a dictionary of weights.
        """
        self.__graph = graph
        self.__spectrum = spectrum
        self.__w = w
        self.__c = c

    def set_coloring(self, c):
        """ set a coloring "c" to the vertices of self.__graph, 
            "c" is expected to be a dict.
        """
        self.__c = c
    
    def vertex_interference(self, vertex):
        """ The interference of a vertex is the sum of the interferences in self.__w
            between the color of "vertex" and the color of its neighbors.
        """
        return self.__potential_interference(vertex, self.__c[vertex])

    def __potential_interference(self, vertex, color):
        """ potential interference of a vertex "vertex" with a color "color" is
            the sum of the interferences in self.__w of "color" and the color of
            "vertex"'s neighbors.
        """
        if not self.__c or not color in self.__spectrum:
            return -1
        interference = 0
        for neighbor in self.__graph.vertices:
            neighbor_color = self.__c[neighbor]
            interference += self.__w[color][neighbor_color]
        return interference
        
    def is_wstable(self):
        """ we say that the k-coloring c is w-stable if, for every vertex,
            the actual interference is not greater than any of the potential interferences.
        """
        for vertex in self.__graph.vertices:
            vertex_interference = self.vertex_interference(vertex)
            for color in self.__spectrum:
                if self.__potential_interference(vertex, color) < vertex_interference:
                    return False
        return True

    def tsc_upper_bound(self, k):
        """ it determites the upper bound for the tsc problem,
            using self.__graph, self.__spectrum and the matrix self.__w,
            and a "k" between 2 and |self.__w|.
        """
        nnorm = self.__natural_norm()
        Delta = self.__graph.Delta()
        return (Delta*nnorm)/k
    
    def csc_upper_bound(self, t):
        """ it determites the upper bound for the csc problem,
            using self.__graph, self.__spectrum, the matrix self.__w
            and a "t" such that 
            |self.__w|*t >= MaxDeg(self.__graph)*NormalNorm(self.__w).
        """
        nnorm = self.__natural_norm()
        Delta = self.__graph.Delta()
        if len(self.__spectrum)*t < Delta*nnorm:
            return -1
        w = [self.__w[i] for i in self.__w]
        w = [item for sublist in w for item in sublist]
        gcd_w = lgcd(w)
        if gcd_w % t == 0:
            return -( -(Delta*nnorm + gcd_w) // (t + gcd_w) )
        else :
            return -( -(Delta*nnorm + gcd_w) // (gcd_w * (t//gcd_w) + gcd_w) )

    def __natural_norm(self):
        """ a static method to calculate the natural norm of self.__w """
        max_row_sum = 0
        for i in self.__w:
            row_sum = sum(self.__w[i].values())
            if row_sum > max_row_sum:
                max_row_sum = row_sum
        return max_row_sum  

    def ThresholdSpectrumColoring(self, k):
        """ The TSC problem determinates the minimum threshold t, 
            such that (G, w) admits a k-coloring in which the interference
            at every vertex is at most t.
        """
        pass

    def ChromaticSpectrumColoring(self, t):
        """ The CSC problem fixes the parameter k
            and the spectrum is let to have as size the |V(G)|
            of vertices, the goal is determinate the minimum k,
            such that (G, w) admits a k-coloring in which the interference
            at every vertex is at most that threshold t.
        """
        pass