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
        self._graph = graph
        self._spectrum = spectrum
        self._w = w
        self._c = c

    def set_coloring(self, c):
        """ set a coloring "c" to the vertices of self._graph, 
            "c" is expected to be a dict.
        """
        self._c = c
    
    def vertices(self):
        return self._graph.vertices()

    def vertex_interference(self, vertex):
        """ The interference of a vertex is the sum of the interferences in self._w
            between the color of "vertex" and the color of its neighbours.
        """
        return self._potential_interference(vertex, self._c[vertex])

    def _potential_interference(self, vertex, color):
        """ potential interference of a vertex "vertex" with a color "color" is
            the sum of the interferences in self._w of "color" and the color of
            "vertex"'s neighbours.
        """
        if not self._c or not color in self._spectrum:
            return -1
        interference = 0
        for neighbour in self._graph.neighbours(vertex):
            neighbour_color = self._c[neighbour]
            interference += self._w[color][neighbour_color]
        return interference
        
    def is_wstable(self):
        """ we say that the k-coloring c is w-stable if, for every vertex,
            the actual interference is not greater than any of the potential interferences.
        """
        for vertex in self._graph.vertices():
            vertex_interference = self.vertex_interference(vertex)
            for color in self._spectrum:
                if self._potential_interference(vertex, color) < vertex_interference:
                    return False
        return True

    def tsc_upper_bound(self, k):
        """ it determites the upper bound for the tsc problem,
            using self._graph, self._spectrum and the matrix self._w,
            and a "k" between 2 and |self._w|.
        """
        nnorm = self._natural_norm()
        Delta = self._graph.Delta()
        return (Delta*nnorm)/k
    
    def csc_upper_bound(self, t):
        """ it determites the upper bound for the csc problem,
            using self._graph, self._spectrum, the matrix self._w
            and a "t" such that 
            |self._w|*t >= MaxDeg(self._graph)*NormalNorm(self._w).
        """
        nnorm = self._natural_norm()
        Delta = self._graph.Delta()
        # if len(self._spectrum)*t < Delta*nnorm:
        #     return -1
        w = [self._w[i].values() for i in self._w]
        w = [item for sublist in w for item in sublist]
        gcd_w = lgcd(w)
        if gcd_w % t == 0 or t == 1:
            return -( -(Delta*nnorm + gcd_w) // (t + gcd_w) )
        else :
            return -( -(Delta*nnorm + gcd_w) // (gcd_w * (t//gcd_w) + gcd_w) )

    def _natural_norm(self):
        """ a static method to calculate the natural norm of self._w """
        max_row_sum = 0
        for i in self._w:
            row_sum = sum(self._w[i].values())
            if row_sum > max_row_sum:
                max_row_sum = row_sum
        return max_row_sum

    def __str__(self):
        res = "vertices: "
        for v in self._graph.vertices():
            res += str(v) + " "
        res += "\nedges: "
        for edge in self._graph.edges():
            res += str(edge) + " "
        res += "\ncolors: "
        for color in self._spectrum:
            res += str(color) + " "
        res += "\ncoloring: "
        if self._c:
            for item in self._c:
                res += str(item) + "->" + str(self._c[item]) + " "
        else:
            res += "-"
        return res

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
    c = {"a": "red", "b": "green", "c": "blue", "d": "red"}
    sgraph = SpectrumGraphColoring(graph, S, W, c)

    print('Graph:')
    print(sgraph)

    print('Interference of every vertex:')
    for vertex in sgraph.vertices():
        print(f'the interference of {vertex} is: {sgraph.vertex_interference(vertex)}')
    
    print('The graph is w-stable: ')
    print(sgraph.is_wstable())

    print('Upper bound for the TSC problem:')
    print(sgraph.tsc_upper_bound(3))

    print('Upper bound for the CSC problem:')
    print(sgraph.csc_upper_bound(1))