""" Python Class
    Clase de Python que ofrece un ofrece una optimizacion
    a los resultados obtenidos en TSC. Realiza un proceso
    iterativo que analiza un subconjunto de los vertices
    del grafo y ve si minimizar su interferencia minimiza
    el umbral de la coloracion.
"""

import random
from graph2 import Graph
from secuencial_gc import SecuencialGraphColoring


class SimpleSearch(SecuencialGraphColoring):

    def simple_search(self, coloring, spectrum, max_iters=20, subset_size=0):
        """Optimiza el umbral de interferencia k-cromatico obtenido en la
        coloracion mediante la minimizacion de la interferencia en los
        vertices del grafo.

        Args:
            coloring (dict): Coloracion de los vertices del grafo.
            spectrum (list): Espectro de colores.
            max_iters (int): Numero de iteraciones que realizara el
                algoritmo. Por defecto es 20.
            subset_size (int): Dimension de los subconjuntos tomados
                en cada iteracion. Por defecto es un tercio de los
                vertices del grafo.

        Returns:
            float, dict: Minimo umbral k-cromatico, coloracion
                del grafo que cumple las restricciones optimizados.
        """        
        # usamos 1/3 de los vertices del grafo en caso que no 
        # se proporcione dimension
        if subset_size is 0:
            subset_size = int(len(self.vertices())/3)
        iters = 0
        # mejor valor del umbral
        best = self.threshold(coloring)
        while iters < max_iters:
            # creamos un subconjunto de dimension subset_size
            for v in random.sample(self.vertices(), subset_size):
                # tomamos el color con la menor potencial interferencia para el vertice
                c = self._min_semi_interference(v, coloring, spectrum)
                v_color = coloring[v]
                # si el color tomado es el mismo que tiene el vertice, continuamos
                if c == v_color:
                    continue
                # asignamos el color al vertice                
                coloring[v] = c
                # calculamos el umbral de la nueva coloracion
                t = self.threshold(coloring)
                coloring[v] = v_color
                # si obtenemos un menor umbral con la nueva coloracion,
                # actualizamos los valores de las memorias y del mejor umbral
                if t < best:
                    best = t
                    self._update_values(v,c, coloring, True, True)
                    coloring[v] = c
                    break
            iters+=1
        return self.threshold(coloring), coloring
        