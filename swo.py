""" Python Class
    Clase de Python que resuelve TSC usando un
    metodo de colacion secuencial basado en el
    algoritmo de optimizacion SWO. Este algoritmo
    sigue un proceso iterativo donde los vertices
    cuentan con una prioridad de acuerdo a su posicion
    en la ordenacion, luego a los vertices que tienen 
    valores de interferencia cercanos al umbral se les 
    asigna un valor de culpa que aumentara su prioridad,
    provocando que al reordenar los vertices para la 
    proxima iteracion, estos sean visitados mas tempranamente. 
    La ordenacion inicial es aleatoria.
"""

import random
from graph2 import Graph
from secuencial_gc import SecuencialGraphColoring
from csc_binarysearch import CSCBinarySearch
# implementacion Quick Sort iterativa
from iterative_quicksort import quickSortIterative


class SWOGraphColoring(SecuencialGraphColoring, CSCBinarySearch):

    def ThresholdSpectrumColoring(self, k):
        """Determina el minimo umbral k-cromatico de TSC
        usando un metodo de coloracion secuencial basado
        en el algoritmo de optimizacion SWO.

        Args:
            k (int): Numero de colores permitidos.

        Returns:
            float, dict: Minimo umbral k-cromatico, coloracion
                del grafo que cumple las restricciones.
        """        
        # reducimos el numero de colores del espectro a k
        spectrum = self._spectrum[:k]
        # creamos una copia de los vertices del grafo y
        # los ordenamos aleatoriamente
        vertex_order = self._graph.vertices().copy()
        random.shuffle(vertex_order)
        iters = 0
        max_iters = 20
        n_vertices = len(vertex_order)
        # orden de los vertices que sera utilizado para
        # colorearlos por el algoritmo greedy
        # contiene los vertices y sus prioridades
        vertex_order = [[v, n_vertices - i] for i, v in enumerate(vertex_order)]
        solution = None
        best = 1e10
        # parametro de SWO para representa el margen de culpabilidad
        a = 0.8
        # parametro de SWO que representa el valor de penalizacion en caso de culpa
        b = n_vertices/5
        while iters < max_iters:
            # coloreamos los vertices en el orden de 'vertex_order' de forma greedy
            coloring = self._coloring(vertex_order, spectrum)
            # calculamos el umbral de la coloracion
            t = self.threshold(coloring)
            # si el umbral mejora el mejor valor obtenido, se actualiza con los nuevos valores
            if t < best:
                best = t
                solution = coloring
            # recorremos cada vertice del grafo asignandoles una prioridad que corresponda con su orden
            # en 'vertex_order' (los primeros vertices tendran la mayor prioridad) y le sumamos un valor 
            # de culpa a aquellos vertices que tengan una interferencia mayor o igual al margen de culpa
            # 'a*t', para que asi sean visitados mas tempranamente al reordenar 'vertex_order'
            for i, v in enumerate(vertex_order):
                v[1] = n_vertices-i
                if self._color_interference[v[0]][coloring[v[0]]] >= a*t:
                    v[1] += b
            # reordenamos los vertices de 'vertex_order' de mayor a menor acorde a su prioridad
            quickSortIterative(vertex_order, 0, len(vertex_order)-1)            
            iters+=1
        return self.threshold(solution), solution
    
    def _coloring(self, vertex_order, spectrum):
        """Colorea a los vertices del grafo en el
        orden dado de forma greedy.

        Args:
            vertex_order (list): Ordenacion de los vertices.
            spectrum (list): Espectro de colores.

        Returns:
            dict: Coloracion de los vertices del grafo.
        """        
        # inicializamos una coloracion y limpiamos la memoria        
        semi_coloring = self._new_coloring()
        # coloreamos los vertices en el orden dado de forma greedy
        # minimizando la interferencia en cada paso y
        # actualizamos los valores de las memorias        
        for v in vertex_order:
            color = self._min_semi_interference(v[0], semi_coloring, spectrum)
            semi_coloring[v[0]] = color
            self._update_values(v[0], color, semi_coloring, True)
        return semi_coloring

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
    sgraph = CombinedSGraphColoring(graph, S, W)

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