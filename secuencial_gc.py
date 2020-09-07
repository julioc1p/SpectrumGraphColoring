""" Python Class
    Clase de Python que brinda algunos metodos auxiliares
    para la aplicacion de un algoritmo de coloracion secuencial 
    en SpectrumGraphColoring.
    Un algoritmo de coloracion secuencial no es mas que una
    ordenacion de los vertices del grafo mediante algun
    criterio, para luego colorearlos en dicho orden de forma
    greedy.
"""

import random
from graph_coloring import SpectrumGraphColoring


class SecuencialGraphColoring(SpectrumGraphColoring):

    def __init__(self, graph, spectrum, w):
        """Inicializa un objeto SecuecialGraphColoring usando
        un grafo, un espectro de colores y una matriz de interferencias.

        Args:
            graph (Graph): Grafo en forma de lista de adyacencia.
            spectrum (list): Espectro de colores.
            w (dict): Matriz de interferencias entre los colores.
        """        
        # inicializamos la clase padre
        super().__init__(graph, spectrum, w)
        # guardamos los grados de los vertices para optimizar en su consulta
        self._vertex_degree = {v:len(graph.neighbours(v)) for v in self.vertices()}
        # diccionario que almacenara la interferencia de cada color para
        # cada vertice en tiempo real de forma dinamica
        self._color_interference = {}
        # orden en que los vertices son visitados para su
        # posterior coloracion mediante un algoritmo greedy
        self._vertex_order = []

    def _max_vdegree(self, vertices):
        """Determina el vertice de mayor grado. En caso de haber mas de uno,
        se selecciona aleatoriamente uno de ellos.

        Args:
            vertices (list): Lista de vertices del grafo.

        Returns:
            Vertice con mayor grado.
        """        
        # lista de los vertices con mayor grado
        best_v = []
        for v in vertices:
            if not best_v:
                best_v = [v]
            if self._vertex_degree[v] > self._vertex_degree[best_v[0]]:
                best_v = [v]
            elif self._vertex_degree[v] == self._vertex_degree[best_v[0]]:
                best_v.append(v)
        return random.choice(best_v)

    def _min_semi_interference(self, vertex, semi_coloring, spectrum):
        """Determina el color con la menor potencial interferencia para
        el vertice en una coloracion parcial del grafo.

        Args:
            vertex : Vertice del grafo.
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.
            spectrum (list): Espectro de colores.

        Returns:
            Color con la menor potencial interferencia.
        """        
        # mejor color
        best_c = None
        # mejor valor
        best = 1e10
        for c in spectrum:
            if self._color_interference[vertex][c] < best:
                best = self._color_interference[vertex][c]
                best_c = c
        return best_c

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        """Actualiza la potencial interferencia para los vecinos de 'vertex'
        como resultado de asignarle el color 'color'. Este metodo no asigna
        directamente el color al vertice, y debe de ser llamado antes de dicha
        asignacion.

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
        # actualizamos la potencial interferencia para cada vertice del grafo
        for u in self._graph.neighbours(vertex):
            if semi_coloring[u] is None or aupdate:
                # actualizamos la potencial interferencia para cada color
                for c in self._spectrum:
                    self._color_interference[u][c] += self._w[color][c]
                    # en caso que 'vertex' tuviera un color previo, tenemos
                    # que restar su valor tambien
                    if update_color is True:
                        self._color_interference[u][c] -= self._w[semi_coloring[vertex]][c]

    def _semi_interference(self, vertex, semi_coloring):
        """Determina manualmente la potencial interferencia del vertice
        sin hacer uso de la memoria 'self._color_interference'.

        Args:
            vertex : Vertice del grafo.
            semi_coloring (dict): Coloracion parcial de los vertices del grafo.

        Returns:
            float: Potencial interferencia del vertice.
        """        
        interference = 0
        for v in self._graph.neighbours(vertex):
            # ignoramos los vertices que aun no han sido coloreados
            if semi_coloring[v]:
                interference += self._w[semi_coloring[vertex]][semi_coloring[v]]
        return interference

    def _new_coloring(self):
        """Devuelve una nueva coloracion vacia de los vertices del grafo y
        resetea las memorias.

        Returns:
            dict: Nueva coloracion vacia de los vertices del grafo.
        """        
        # ponemos en cero las potenciales interferencias
        self._color_interference = {v:{c:0 for c in self._spectrum} for v in self.vertices()}
        self._vertex_order = []
        return {v:None for v in self.vertices()}