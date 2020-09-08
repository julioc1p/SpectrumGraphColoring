""" Python class
    Clase de Python que resuelve TSC y CSC mediante un metodo
    de coloracion secuencial inspirado en DSATUR.
    DSATUR usa el grado de saturacion de los vertices para
    establecer su prioridad. El grado de saturacion de un vertice
    no es mas que el numero de vecinos que tiene coloreado el
    vertice hasta ese momento.
"""

import random
from graph2 import Graph
from secuencial_gc import SecuencialGraphColoring


class DSATURGraphColoring(SecuencialGraphColoring):

    def __init__(self, graph, spectrum, w):
        """Inicializa un objeto DSATURGraphColoring usando
        un grafo, un espectro de colores y una matriz de interferencias.

        Args:
            graph (Graph): Grafo en forma de lista de adyacencia.
            spectrum (list): Espectro de colores.
            w (dict): Matriz de interferencias entre los colores.
        """        
        # inicializamos la clase padre
        super().__init__(graph, spectrum, w)
        # diccionario que almacenara el grado de saturacio de cada vertice
        self._saturation_degree = {}

    def _new_coloring(self):
        """Devuelve una nueva coloracion vacia de los vertices del grafo y
        resetea las memorias.

        Returns:
            dict: Nueva coloracion vacia de los vertices del grafo.
        """        
        self._saturation_degree = {v:0 for v in self.vertices()}
        return super()._new_coloring()
        
    def _max_saturation_degree(self, vertices, semi_coloring):
        """Determina el vertice no coloreado con mayor grado de saturacion
        en la coloracion parcial. En caso de un empate, se toma el de mayor
        grado dentro de ellos, y en caso de doble empate, se seleccionara de
        forma aleatoria.

        Args:
            vertices (list): Lista de vertices del grafo.
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.

        Returns:
            Vertice con mayor grado de saturacion.
        """        
        best_v = []
        for v in vertices:
            # ignoramos los vertices ya coloreamos
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

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        """Actualiza la potencial interferencia y el grado de saturacion de los 
        vecinos de 'vertex' como resultado de asignarle el color 'color'. Este 
        metodo no asigna directamente el color al vertice, y debe de ser llamado
        antes de dicha asignacion.

        Args:
            vertex : Vertice del grafo.
            color : Color que se asigno a 'vertex'.
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.
            aupdate (bool): Si es True si se actualizaran los valores de todos
                los vecinos de 'vertex', en otro caso solo los que aun no se 
                colorean. Por defecto es False.
            update_color (bool): Si es True representa que 'vertex' tenia un color
                previo en la coloracion y se actualizara con uno nuevo. Por defecto 
                es False.
        """        
        # sumamos 1 al grado de saturacion de cada vecino del vertice
        for w in self._graph.neighbours(vertex):
            self._saturation_degree[w]+=1
        super()._update_values(vertex, color, semi_coloring, aupdate, update_color)

    def ThresholdSpectrumColoring(self, k):
        """Determina el minimo umbral k-cromatico de TSC 
        usando una heuristica basada en DSATUR.

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
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            # tomamos el vertice de mayor grado de saturacion
            vertex = self._max_saturation_degree(self.vertices(), semi_coloring)
            self._vertex_order.append(vertex)
            # tomamos el color con la menor potencial interferencia para el vertice
            color = self._min_semi_interference(vertex, semi_coloring, spectrum)
            # asignamos el color al vertice
            semi_coloring[vertex] = color
            n_colored+=1
            # actualizamos los valores de las memorias
            self._update_values(vertex, color, semi_coloring)
        return self.threshold(semi_coloring), semi_coloring

    def ChromaticSpectrumColoring(self, t):
        """Determina el numero cromatico de t-interferencia de CSC
        usando una heuristica basada en DSATUR.

        Args:
            t (float): Umbral de interferencia permitido.

        Returns:
            int, dict: Numero cromatico de t-interferencia, coloracion
                del grafo que cumple las restricciones.
        """        
        # inicializamos una coloracion y limpiamos la memoria
        semi_coloring = self._new_coloring()
        n_colored = 0
        n_vertices = len(self.vertices())
        while n_colored < n_vertices:
            # tomamos el vertice de mayor grado de saturacion
            vertex = self._max_saturation_degree(self.vertices(), semi_coloring)
            # intentamos colorear el vertice con cada color garantizando
            # que no superaremos el umbral t
            self._try_color(vertex, semi_coloring, t)
            # si el vertice no pudo ser coloreado se devuelve una coloracion vacia
            # con |V| colores
            if not semi_coloring[vertex]:
                return n_vertices, {v:None for v in self.vertices()}
            else:
                n_colored+=1
        return int(max(semi_coloring.values())), semi_coloring

    def _try_color(self, vertex, semi_coloring, t):
        """Intenta colorear el vertice con cada color
        garantizando que no se superara el umbral 't'.

        Args:
            vertex : Vertice del grafo.
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.
            t (float): Umbral de interferencia permitido.
        """        
        I = 1e10        
        for c in self._spectrum:
            # interferencia del vertice con el color c
            I = self._color_interference[vertex][c]
            # si el vertice no tiene vecinos le asignamos el primer color
            if len(self._graph.neighbours(vertex)) == 0:
                semi_coloring[vertex] = c
                self._update_values(vertex, c, semi_coloring, aupdate=True)
                break
            # comprobamos que la interferencia del vertice no exceda la razon
            # entre el numero de vecinos coloreados (= grado de saturacion) y 
            # el total de vecinos del umbral t
            if I > self._saturation_degree[vertex]/len(self._graph.neighbours(vertex))*t:
                continue
            semi_coloring[vertex] = c
            # comprobamos que la relacion anterior sea cumplida ademas por cada vecino del vertice
            if all([1 if not semi_coloring[w] else self._semi_interference(w, semi_coloring) <= \
                (self._saturation_degree[w]+1)/len(self._graph.neighbours(w))*t for w in self._graph.neighbours(vertex)]):
                # en caso que se cumpla la razon para el vertice y para sus vecinos, aseguramos
                # que el umbral t no se superara al asignar el color c al vertice
                self._update_values(vertex, c, semi_coloring, aupdate=True)
                break
            semi_coloring[vertex] = None
        


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

    k0 = 3
    t0 = 1.0
    t = sgraph.ThresholdSpectrumColoring(k0)
    k = sgraph.ChromaticSpectrumColoring(t0)
    print('Graph:')
    print(sgraph)
    print(f'DSATUR best value and coloring for the TSC problem and k = {k0}:')
    print(t)
    print(f'DSATUR best value and coloring for the CSC problem and t = {t0}:')
    print(k)