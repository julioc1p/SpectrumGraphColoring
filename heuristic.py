import numpy as np
import sys
import random
from graph_coloring import SpectrumGraphColoring
from graph2 import Graph


class DSATURGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w, c=None):
        super().__init__(graph, spectrum, w, c)
        vertices = graph.vertices()
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in vertices}
        self._saturation_degree = {}
        self._color_interference = {}

        
    def _max_saturation_degree(self, semi_coloring):
        best_v = []
        for v in self.vertices():
            if not semi_coloring[v]:
                if not best_v:
                    best_v = [v]
                if self._saturation_degree[v] > self._saturation_degree[best_v[0]]:
                    best_v = [v]
                elif self._saturation_degree[v] == self._saturation_degree[best_v[0]] and \
                        self._vertex_degree[v] > self._vertex_degree[best_v[0]]:
                    best_v = [v]
                elif self._saturation_degree[v] == self._saturation_degree[best_v[0]] and \
                        self._vertex_degree[v] == self._vertex_degree[best_v[0]]:
                    best_v.append(v)
        return random.choice(best_v)

    def _min_semi_interference(self, vertex, semi_coloring, spectrum):
        # if sum([1 if x else 0 for x in semi_coloring.values()])==0:
        #     return random.choice(spectrum)
        best_c = None
        best = 1e10
        for c in spectrum:
            if self._color_interference[vertex][c] < best:
                best = self._color_interference[vertex][c]
                best_c = c
        return best_c

    def _update_saturation_degree(self, vertex,color, semi_coloring, is_CSC=False):
        for w in self._graph.neighbours(vertex):
            self._saturation_degree[w]+=1
            if semi_coloring[w] is None or is_CSC:
                for c in self._spectrum:
                    self._color_interference[w][c]+= self._w[color][c]

    def ThresholdSpectrumColoring(self, k):
        semi_coloring = self._new_coloring()
        spectrum = self._spectrum[:k]
        # k_spectrum = set()
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            vertex = self._max_saturation_degree(semi_coloring)
            color = self._min_semi_interference(vertex, semi_coloring, spectrum)
            # if len(k_spectrum) == k-1:
            #     k_spectrum.add(color)
            #     spectrum = list(k_spectrum)
            # if len(k_spectrum) < k: 
            #     k_spectrum.add(color)
            semi_coloring[vertex] = color
            n_colored+=1
            self._update_saturation_degree(vertex, color, semi_coloring)
        return self.threshold(semi_coloring), semi_coloring

    def ChromaticSpectrumColoring(self, t):
        semi_coloring = self._new_coloring()
        n_colored = 0
        n_vertices = len(self.vertices())
        color = None
        while n_colored < n_vertices:
            v = self._max_saturation_degree(semi_coloring)
            i = 0
            I = 1e10

            for c in self._spectrum:
                I = self._color_interference[v][c]
                if len(self._graph.neighbours(v)) == 0:
                    n_colored+=1
                    self._update_saturation_degree(v, c, semi_coloring, is_CSC=True)
                    break
                if I > self._saturation_degree[v]/len(self._graph.neighbours(v))*t:
                    continue
                semi_coloring[v] = c
                if all([1 if not semi_coloring[w] else self._semi_interference(w, semi_coloring) <= \
                    (self._saturation_degree[w]+1)/len(self._graph.neighbours(w))*t for w in self._graph.neighbours(v)]):
                    n_colored+=1
                    self._update_saturation_degree(v, c, semi_coloring, is_CSC=True)
                    break
                semi_coloring[v] = None
            if not semi_coloring[v]:
                return n_vertices, {v:None for v in self.vertices()}
        return len(set(semi_coloring.values())), semi_coloring
        

        #     while I > self._saturation_degree[v]/len(self._graph.neighbours(v))*t and \
        #         i < len(self._spectrum):
        #         color = self._spectrum[i]
        #         I = self._color_interference[v][color]
        #         if I <= self._saturation_degree[v]/len(self._graph.neighbours(v))*t:
        #             semi_coloring[v] = color
        #             for w in self._graph.neighbours(v):
        #                 if not semi_coloring[w]:
        #                     continue
        #                 I = self._semi_interference(w, semi_coloring)
        #                 if I > (self._saturation_degree[w]+1)/len(self._graph.neighbours(w))*t:
        #                     break
        #             semi_coloring[v] = None
        #         i+=1
        #     if i >= len(self._spectrum):
        #         return n_vertices, {v:None for v in self.vertices()}
        #     else:
        #         semi_coloring[v] = color
        #         n_colored+=1
        #         self._update_saturation_degree(v, color, semi_coloring)
        # return len(set(semi_coloring.values())), semi_coloring


    def _new_coloring(self):
        self._saturation_degree = {v:0 for v in self.vertices()}
        self._color_interference = {v:{c:0 for c in self._spectrum} for v in self.vertices()}
        return {v:None for v in self.vertices()}

    def _semi_interference(self, vertex, semi_coloring):
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
    sgraph = DSATURGraphColoring(graph, S, W)

    print('Graph:')
    print(sgraph)

    k = 3
    t = sgraph.ChromaticSpectrumColoring(1)
    print(f'PSO best value and coloring for the TSC problem and k = {k}:')
    print(t)

    
    LD = {
            '1': ['2', '3', '4', '5'],
            '2': ['1', '3', '4', '5', '6'],
            '3': ['1', '2', '4', '5', '6'],
            '4': ['1', '2', '3', '5', '6', '7', '8'],
            '5': ['1', '2', '3', '4', '6', '7', '8', '9'],
            '6': ['2', '3', '4', '5', '7', '8', '9', '10'],
            '7': ['4', '5', '6', '8', '9', '10'],
            '8': ['4', '5', '6', '7', '9', '10', '11'],
            '9': ['5', '6', '7', '8', '10', '11', '12'],
            '10': ['6', '7', '8', '9', '11', '12', '13', '14'],
            '11': ['8', '9', '10', '12', '13', '14', '15'],
            '12': ['9', '10', '11', '13', '14', '15'],
            '13': ['10', '11', '12', '14', '15', '16'],
            '14': ['10', '11', '12', '13', '15', '16', '17'],
            '15': ['11', '12', '13', '14', '16', '17'],
            '16': ['13', '14', '15', '17', '18'],
            '17': ['14', '15', '16', '18'],
            '18': ['16', '17']
    }

    
    MD_ = {
            '1': ['2', '3', '4', '5', '6', '7'], #6
            '2': ['1', '3', '4', '5', '6', '7', '24', '26'], #8
            '3': ['1', '2', '4', '5', '6', '7', '9', '13', '15', '22', '24'], #11
            '4': ['1', '2', '3', '5', '7', '9', '13', '15', '22', '24', '25', '26'],#13
            '5': ['1', '2', '3', '4', '6', '7', '8', '9'], #8
            '6': ['1', '2', '3', '5', '7', '8', '9', '10', '11', '13'], #10            
            '7': ['1', '2', '3', '4', '5', '6', '8', '9', '11', '13', '15', '22', '24'], #13
            '8': ['5', '6', '7', '9', '10', '11', '13', '14'], #8
            '9': ['3', '4', '5', '6','7', '8', '10', '11', '13', '14', '15', '16', '22'],#13
            '10': ['6', '8', '9', '11', '13', '14'], #6
            '11': ['6', '8', '9', '10', '13', '14', '15'],#7
            # '12': ['8', '9', '10', '11', '13', '14', '16'], #7
            '13': ['3', '4', '6', '7', '8', '9', '10', '11', '14', '15', '16', '17', '22'],#13
            '14': ['8', '9', '10', '11', '13', '15', '16', '17', '18', '22'], #10
            '15': ['3', '4', '7', '9', '11', '13', '14', '16', '17', '18', '21', '22', '23', '24', '25'],#14
            '16': ['9', '13', '14', '15', '17', '18', '19', '20', '21', '22', '23'],#11
            '17': ['13', '14', '15', '16', '18', '19', '20', '21', '22', '23', '24'],#11
            '18': ['14', '15', '16', '17', '19', '20', '21', '22', '23'],#9
            '19': ['16', '17', '18', '20', '21', '22', '23'],#7
            '20': ['16', '17', '18', '19', '21', '22'],#6
            '21': ['15', '16', '17', '18', '19', '20', '22', '23', '24', '25'],#10
            '22': ['3', '4', '7', '9', '13', '14', '15', '16', '17', '18', '19', '20', '21', '23', '24', '25', '26'],#17
            '23': ['15', '16', '17', '18', '19' ,'21', '22', '24', '25', '26'],#10
            '24': ['2', '3', '4', '7', '15', '17', '21', '22', '23', '25', '26'],#11
            '25': ['4', '15', '21', '22', '23', '24', '26'],#7
            '26': ['2', '4' , '22', '23', '24', '25']#6
    }

    W = {}
    for i in range(1, 12):
        w_ = {}
        for j in range(1, 12):
            res = abs(i-j)
            if res == 0:
                w_[str(j)] = 1
            elif res == 1:
                w_[str(j)] = .8
            elif res == 2:
                w_[str(j)] = .5
            elif res == 3:
                w_[str(j)] = .2
            elif res == 4:
                w_[str(j)] = .1
            elif res == 5:
                w_[str(j)] = 0.001
            else:
                w_[str(j)] = 0
        W[str(i)] = w_
    S = [str(i) for i in range(1,12)]

    graph = Graph(LD)
    sgraph = DSATURGraphColoring(graph, S, W)
    print(sgraph.ChromaticSpectrumColoring(2))
    # # print('Graph:')
    # # print(sgraph)

    # k = 11
    # r = []
    # solution = None
    # for _ in range(1000):
    #     t = sgraph.ThresholdSpectrumColoring(k)
    #     # print(f'DSATUR best value and coloring for the TSC problem and k = {k}:')
    #     # print(t)
    #     r.append(t[0])
    #     # solution = t[1]
    # r = np.array(r)
    # print('{0:.1f}'.format(r.mean()))
    # print('{0:.2f}'.format(r.std()))    
