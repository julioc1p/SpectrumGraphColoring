from graph2 import Graph

class GraphColoring(object):

    def __init__(self, graph, spectrum, w, c=None):
        self.__graph = graph
        self.__spectrum = spectrum
        self.__w = w
        self.__c = c

    def set_coloring(self, c):
        """ set a coloring "c" to the vertices of self.__graph, 
            "c" is expected to be a dict .  
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
        nnorm = self.__natural_norm()
        Delta = self.__graph.Delta()
        return (Delta*nnorm)/k
    
    def __natural_norm(self):
        """ a static method to calculate the natural norm of self.__w """
        max_row_sum = 0
        for i in self.__w:
            row_sum = sum(self.__w[i])
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