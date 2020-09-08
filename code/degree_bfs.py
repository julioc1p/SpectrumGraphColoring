""" Python Class
    Clase de Python que resuelve TSC mediante un metodo
    de coloracion secuencial inspirado en BFS, usando
    una cola con prioridad en funcion del grado de los
    vertices.

    Esta clase usa la implementacion de CSCBinarySearch
    para resolver CSC mediante su implementacion de TSC.
"""

from code.graph2 import Graph
from code.csc_binarysearch import CSCBinarySearch
from code.secuencial_gc import SecuencialGraphColoring


class DegreeBFSGraphColoring(SecuencialGraphColoring, CSCBinarySearch):

    def ThresholdSpectrumColoring(self, k):
        """Determina el minimo umbral k-cromatico de TSC 
        usando una heuristica basada en BFS con una cola
        con prioridad en funcion del grado de los vertices.

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
        # creamos una memoria para los vertices visitados
        visit = {v:0 for v in self.vertices()}
        n_colored = 0
        n_vertices = len(self.vertices())
        # la condicion asegura visitar cada componente conexa del grafo
        while n_colored < n_vertices:
            # tomamos el vertices con mayor grado entre los no visitados
            # y creamos una lista que representa a su componente conexa
            bfs_vertices = [self._max_vdegree([v for v in self.vertices() if not visit[v]])]
            # marcamos el vertice como visitado            
            visit[bfs_vertices[0]] = 1
            while len(bfs_vertices):
                # extraemos el vertice con mayor grado dentro de la lista
                # de la componente conexa
                vertex = self._max_vdegree(bfs_vertices)
                self._vertex_order.append(vertex)
                bfs_vertices.remove(vertex)
                # tomamos el color con la menor potencial interferencia para el vertice
                color = self._min_semi_interference(vertex, semi_coloring, spectrum)
                # asignamos el color al vertice                
                semi_coloring[vertex] = color
                n_colored+=1
                # actualizamos los valores de las memorias                
                self._update_values(vertex, color, semi_coloring)
                # agregamos cada vecino del vertice a la lista de
                # la componente conexa en caso de que no haya sido visitado
                for neighbour in self._graph.neighbours(vertex):
                    if visit[neighbour] is 0:
                        visit[neighbour] = 1
                        bfs_vertices.append(neighbour)
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
    sgraph = DegreeBFSGraphColoring(graph, S, W)

    k0 = 3
    t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    k = sgraph.ChromaticSpectrumColoring(t0)
    print('Graph:')
    print(sgraph)
    print(f'DegreeBFS best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    print(f'DegreeBFS best value and coloring for the CSC problem and t = {t0}:')
    print(k)