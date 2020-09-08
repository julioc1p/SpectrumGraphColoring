""" Python Class
    Clase de Python que resuelve TSC usando un metodo 
    de coloracion secuencial basado en el grado de los
    vertices, tomando dos vertices en cada paso, el de
    mayor grado y el siguiente no adyacente el primero.
    En caso de empate, se toma el vertice de mayor grado
    de saturacion, lo que hace que sea un metodo 
    determinista.

    Esta clase usa la implementacion de CSCBinarySearch
    para resolver CSC mediante su implementacion de TSC.
"""

from code.graph2 import Graph
from code.secuencial_gc import SecuencialGraphColoring
from code.csc_binarysearch import CSCBinarySearch


class VertexMergeGraphColoring(SecuencialGraphColoring, CSCBinarySearch):
        
    def _max_vdegree_with_sdegree(self, semi_coloring, tabu_list=[]):
        """Determina el vertice con mayor grado que no este coloreado ni
        pertenezca la lista de tabues.

        Args:
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.
            tabu_list (list): Lista de vertices a ignorar por el metodo. Por
                defecto es vacia ([]).

        Returns:
            Vertice con mayor grado.
        """        
        best_v = None
        for v in self.vertices():
            # comprobamos que el vertice no este coloreado y no pertenezca
            # a tabu_list
            if not semi_coloring[v] and not v in tabu_list:
                if not best_v:
                    best_v = v
                if self._vertex_degree[v] > self._vertex_degree[best_v]:
                    best_v = v
        return best_v

    def ThresholdSpectrumColoring(self, k):
        """Determina el minimo umbral k-cromatico de TSC
        usando un metodo de coloracion secuencial que toma
        dos vertices en cada paso.

        Args:
            k (int): Numero de colores permitidos.

        Returns:
            float, dict: Minimo umbral k-cromatico, coloracion
                del grafo que cumple las restricciones.
        """        
        # inicializamos una coloracion y limpiamos la memoria        
        semi_coloring = self._new_coloring()
        # reducimos el numero de colores del espectro a k
        spectrum = self._spectrum[:k]
        # vertices = self.vertices()
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            # tomamos el vertices con mayor grado entre los no visitados
            vertex = self._max_vdegree_with_sdegree(semi_coloring)
            self._vertex_order.append(vertex)
            # tomamos el color con la menor potencial interferencia para el vertice            
            color = self._min_semi_interference(vertex, semi_coloring, spectrum)
            # asignamos el color al vertice
            semi_coloring[vertex] = color
            n_colored+=1
            # actualizamos los valores de las memorias
            self._update_values(vertex, color, semi_coloring)
            # tomamos el vertice de mayor grado no adyacente al que seleccionamos
            # anteriormente, y en caso de que exista, repetimos el mismo proceso
            fneighbour = self._max_vdegree_with_sdegree(semi_coloring, self._graph.neighbours(vertex))
            if fneighbour is not None:
                self._vertex_order.append(fneighbour)
                color = self._min_semi_interference(fneighbour, semi_coloring, spectrum)
                semi_coloring[fneighbour] = color
                n_colored+=1 
                self._update_values(fneighbour, color, semi_coloring)
        return self.threshold(semi_coloring), semi_coloring

    
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
    sgraph = VertexMergeGraphColoring(graph, S, W)

    k0 = 3
    t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    k = sgraph.ChromaticSpectrumColoring(t0)
    print('Graph:')
    print(sgraph)
    print(f'VM best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    print(f'VM best value and coloring for the CSC problem and t = {t0}:')
    print(k)