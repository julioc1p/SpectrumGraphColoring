import numpy as np
import sys
import random
from graph_coloring import SpectrumGraphColoring
from graph2 import Graph


""" A Python class
    A Python graph class which inherites of SpectrumGraphColoring class
    and solves its TSC and CSC problems using a DSATUR-based heuristic.
"""

class VertexMergeGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)
        vertices = graph.vertices()
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in vertices}
        self._saturation_degree = {}
        self._color_interference = {}

        
    def _max_saturation_degree(self, vertices):
        """ takes a coloring and returns the vertex with lowest
            saturation degree (it is the vertice with more already colored
            neighbours), the one which the higher degree in a tie or
            a random one in a double tie.
        """
        if len(vertices) == 1:
            return vertices[0]
        v = vertices[0]
        index = 1
        while index < len(vertices) and self._vertex_degree[v] == self._vertex_degree[vertices[index]]:
            if self._saturation_degree[vertices[index]] > self._saturation_degree[v]:
                v = vertices[index]
            index+=1
        return v

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

    def _quick_sort(self, vertices):
        if not vertices:
            return []
        m = vertices[0]
        g = []
        le = []
        for v in vertices[1:]:
            if self._vertex_degree[v] > self._vertex_degree[m] or \
                (self._vertex_degree[v] == self._vertex_degree[m] and self._saturation_degree[v] > self._saturation_degree[m]):
                g.append(v)
            else:
                le.append(v)
        return self._quick_sort(g) + [m] + self._quick_sort(le)

    def first_no_neighbours(self, vertex, vertices):
        neighbours = self._graph.neighbours(vertex)
        for v in vertices:
            if not v in neighbours:
                return v
        return None

    def ThresholdSpectrumColoring(self, k):
        """ Solution for the TSC problem using TSC-DSATUR heuristic 
        """
        semi_coloring = self._new_coloring() # clean self values
        spectrum = self._spectrum[:k]
        vertices = self.vertices()
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            vertices = self._quick_sort(vertices)
            vertex = vertices[0]
            color = self._min_semi_interference(vertex, semi_coloring, spectrum)
            semi_coloring[vertex] = color
            n_colored+= 1 
            self._update_values(vertex, color, semi_coloring)
            vertices.remove(vertex)
            fneighbour = self.first_no_neighbours(vertex, vertices)
            if fneighbour is not None:
                color = self._min_semi_interference(fneighbour, semi_coloring, spectrum)
                semi_coloring[fneighbour] = color
                n_colored+= 1 
                self._update_values(fneighbour, color, semi_coloring)
                vertices.remove(fneighbour)
        return self.threshold(semi_coloring), semi_coloring

    def ChromaticSpectrumColoring(self, t):
        """ Solution for the CSC problem using CSC-DSATUR heuristic 
        """
        semi_coloring = self._new_coloring()
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            v = self._max_saturation_degree(semi_coloring)
            I = 1e10
            # try to put every color to v
            for c in self._spectrum:
                I = self._color_interference[v][c]
                # case v does not have neighbours
                if len(self._graph.neighbours(v)) == 0:
                    n_colored+=1
                    self._update_values(v, c, semi_coloring, is_CSC=True)
                    break
                # the proportion of the interference of v is right for the color c
                if I > self._saturation_degree[v]/len(self._graph.neighbours(v))*t:
                    continue
                semi_coloring[v] = c
                # the proportion of the interference of every v's neighbour is right for the color c
                if all([1 if not semi_coloring[w] else self._semi_interference(w, semi_coloring) <= \
                    (self._saturation_degree[w]+1)/len(self._graph.neighbours(w))*t for w in self._graph.neighbours(v)]):
                    n_colored+=1
                    self._update_values(v, c, semi_coloring, is_CSC=True)
                    break
                semi_coloring[v] = None
            if not semi_coloring[v]:
                return n_vertices, {v:None for v in self.vertices()}
        return len(set(semi_coloring.values())), semi_coloring

    def _new_coloring(self):
        """ cleans the self.saturation_degree and self._color_interference values
            and returns a new empty coloring
        """
        self._saturation_degree = {v:0 for v in self.vertices()}
        self._color_interference = {v:{c:0 for c in self._spectrum} for v in self.vertices()}
        return {v:None for v in self.vertices()}

    def _semi_interference(self, vertex, semi_coloring):
        """ calculates the color with the lowest potential interference in the 
            coloring 'semi_coloring' for 'vertex' without using self._color_interference.
        """
        interference = 0
        for v in self._graph.neighbours(vertex):
            if semi_coloring[v]:
                interference+=self._w[semi_coloring[vertex]][semi_coloring[v]]
        return interference



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
    sgraph = MyGraphColoring(graph, S, W)

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