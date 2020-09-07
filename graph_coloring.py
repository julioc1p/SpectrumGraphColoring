""" Python Class
    Clase en Python para dos problemas de coloracion de grafos con espectros,
    el problema Threshold Spectrum Coloring y el problema Chromatic Spectrum
    Coloring. Esta clase implementa algunos metodos y brinda cotas para estos
    problemas.

    "Threshold Spectrum Coloring (TSC)":
        Dado un grafo G y un espectro de k colores dotado con
        una matriz W de k x k de interferencias entre los colores, el objetivo
        de TSC es determinar el minimo umbral t ∈ R ≥ 0 tal que  el grafo 
        (G, W) admita una k-coloracion c en donde la interferencia en cada 
        vertice es a lo sumo t, a este umbral lo denotaremos como el minimo
        umbral k-cromatico de (G, W).

    "Chromatic Spectrum Coloring (CSC)":
        Dado un grafo G y un espectro de colores S, dotado con
        una matriz W de |S| x |S| de interferencia entre los colores, fijado
        un umbral t ∈ R ≥ 0 y donde el espectro tiene un numero de colores
        hasta la cantidad de vertices |V|, el objetivo de CSC es determinar
        el minimo numero de colores k ∈ N tal que el grafo (G, W) admita una
        k-coloracion c en donde la interferencia en cada vertice es lo sumo
        el umbral t fijado, a este k lo denotaremos como el minimo numero
        cromatico de t-interferencia de (G, W).
"""

from graph2 import Graph
from gcd import lgcd


class SpectrumGraphColoring(object):

    def __init__(self, graph, spectrum, w, c=None):
        """Inicializa un objeto SpectrumGraphColoring usando
        un grafo, un espectro de colores y una matriz de interferencias.

        Args:
            graph (Graph): Grafo en forma de lista de adyacencia.
            spectrum (list): Espectro de colores.
            w (dict): Matriz de interferencias entre los colores.
            c (dict, opcional): Coloracion del grado. Por defecto es None.
        """        
        self._graph = graph
        self._spectrum = spectrum
        self._w = w
        self._c = c

    def set_coloring(self, c):
        """Colorea el grafo.

        Args:
            c (dict): Nueva coloracion del grafo.
        """        
        self._c = c
    
    def vertices(self):
        """Vertices del grafo.

        Returns:
            list: Lista de vertices.
        """   
        return self._graph.vertices()

    def vertex_interference(self, vertex, c=None):
        """Interferencia de un vertice en una coloracion.
        La interferencia de un vertice es la suma entre las
        interferencias del color del 'vertex' y el de cada uno de
        sus vecinos en la matriz W. Se usara la coloracion de la
        clase en caso que c sea None.

        Args:
            vertex : Vertice del grafo.
            c (dict): Coloracion del grafo. Por defecto es None.

        Returns:
            float: Interferencia del vertice 'vertex'.
        """   
        # calculamos la potencial interferencia para el color de 'vertex' en la coloracion
        return self._potential_interference(vertex, c[vertex], c)

    def _potential_interference(self, vertex, color, c=None):
        """Potencial interferencia de un vertice en una coloracion.
        La potencial interferencia del vertice 'vertex' con un
        con color 'color' es la suma entre las interferencias de
        'color' y cada uno de los colores de los adyacentes de 'vertex'.
        Se usara la coloracion de la clase en caso que c sea None.

        Args:
            vertex : Vertice del grafo.
            color : Color del espectro
            c (dict): Coloracion del grafo. Por defecto es None.

        Returns:
            float Potencial interferencia de 'vertex' con el color 'color'.
        """        
        # usamos la coloracion de la clase en caso que 'c' sea None     
        if not c:
            c = self._c
        interference = 0
        # sumamos las interferencias entre 'color' y cada uno
        # de los colores de los adyacentes a 'vertex'
        for neighbour in self._graph.neighbours(vertex):
            neighbour_color = c[neighbour]
            interference += self._w[color][neighbour_color]
        return interference
        
    def is_wstable(self, c=None):
        """Coloracion w-estable. Una coloracion es w-estable
        si para cada uno de los vertices su interferencia actual
        no es mayor que ninguna de las potenciales interferencias
        en la coloracion.

        Args:
            c (dict): Coloracion del grafo. Por defecto es None.

        Returns:
            bool: True si la coloracion es w-estable, False en otro caso.
        """        
        for vertex in self._graph.vertices():
            vertex_interference = self.vertex_interference(vertex, c)
            for color in self._spectrum:
                if self._potential_interference(vertex, color, c) < vertex_interference:
                    return False
        return True

    def threshold(self, c=None):
        """Determina el umbral de interferencia para una coloracion.
        Este umbral es el maximo valor de las interferencias de los
        vertices del grafo.

        Args:
            c (dict): Coloracion del grafo. Por defecto es None.

        Returns:
            float: Umbral de interferencia.
        """        
        return max([self.vertex_interference(v, c) for v in self.vertices()])

    def tsc_upper_bound(self, k):
        """Determina la cota superior para el problema TSC.

        Args:
            k (int): Numero de colores permitidos.

        Returns:
            float: Cota superior para el umbral de TSC.
        """        
        nnorm = self._natural_norm()
        Delta = self._graph.Delta()
        return (Delta*nnorm)/k
    
    def csc_upper_bound(self, t):
        """Determina la cota superior para el problema CSC.

        Args:
            t (float): Umbral de interferencia permitido.

        Returns:
            int: Cota superior para el numero de colores de CSC.
        """        
        nnorm = self._natural_norm()
        Delta = self._graph.Delta()
        # convertimos el diccionario 'self._w' en una lista con todos sus elementos
        w = [self._w[i].values() for i in self._w]
        w = [item for sublist in w for item in sublist]
        # calculamos el maximo comun divisor de la lista (numeros no enteros)
        gcd_w = lgcd(w)
        # caso donde 't' es divisor del mcd
        # usar -(-a//b) calcula la division parte entera por encima
        if gcd_w % t == 0 or t == 1:
            return -( -(Delta*nnorm + gcd_w) // (t + gcd_w) )
        # caso donde 't' no es divisor del mcd
        else :
            return -( -(Delta*nnorm + gcd_w) // (gcd_w * (t//gcd_w) + gcd_w) )

    def _natural_norm(self):
        """Calcula la norma natural de la matriz 'self._w'.
        Esta es la maxima de las sumas de sus filas.

        Returns:
            float: Norma natural de la matriz.
        """        
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
        """Metodo abstracto del problema TSC.

        Args:
            k (int): Numero de colores permitidos.

        Returns:
            float, dict: Minimo umbral k-cromatico, coloracion
                del grafo que cumple las restricciones.
        """        
        return None

    def ChromaticSpectrumColoring(self, t):
        """Metodo abstracto del problema CSC.

        Args:
            t (float): Umbral de interferencia permitido.

        Returns:
            int, dict: Numero cromatico de t-interferencia, coloracion
                del grafo que cumple las restricciones.
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

    print('The threshold is:')
    print(sgraph.threshold())

    print('Upper bound for the TSC problem:')
    print(sgraph.tsc_upper_bound(3))

    print('Upper bound for the CSC problem:')
    print(sgraph.csc_upper_bound(1))