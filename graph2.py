""" Python Class
    Una clase simple de grafos en Python, con los
    elementos y funcionalidades esenciales.
"""

class Graph(object):

    def __init__(self, graph_dict=None):
        """Inicializa un objeto Graph usando un diccionario.
        Si no es dado un diccionario o se usa None, se usara un diccionario vacio.

        Args:
            graph_dict (dict) : diccionario donde cada llave sera 
                un vertice y los elementos asociados una lista de adyacentes al vertice.
                Por defecto es None.
        """        
        if graph_dict == None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def vertices(self):
        """Vertices del grafo.

        Returns:
            list: Lista de vertices.
        """        
        return list(self._graph_dict.keys())

    def edges(self):
        """Aristas del grafo.

        Returns:
            list: Lista de aristas.
        """        
        return self._generate_edges()

    def neighbours(self, vertex):
        """Vecinos del vertice 'vertex'.
        Se asume que este vertice pertenece al grafo.

        Args:
            vertex : Vertice del grafo.

        Returns:
            list: Lista de adyacentes a 'vertex'.
        """        
        return self._graph_dict[vertex]

    def add_vertex(self, vertex):    
        """Agrega un nuevo vertice con una lista vacia.
        En caso que ya exista, no se hace nada.

        Args:
            vertex : Nuevo vertice.
        """        
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = []

    def add_edge(self, edge):
        """Se agrega una nueva arista al grafo.
        Se asume que la arista es de tipo set, tuple o list.
        Las aristas son unidireccionales y dos vertices no
        pueden tener multiples aristas. En caso de que alguno
        de los vertices no pertenezca al grafo, se agrega con el otro
        en su lista de adyacencia.

        Args:
            edge : Nueva arista.
        """        
        vertex1, vertex2 = edge
        if vertex1 in self._graph_dict :
            if not vertex2 in self._graph_dict[vertex1]:
                self._graph_dict[vertex1].append(vertex2)
        else:
            self._graph_dict[vertex1] = [vertex2]
        if vertex2 in self._graph_dict :
            if not vertex1 in self._graph_dict[vertex2]:
                self._graph_dict[vertex2].append(vertex1)
        else:
            self._graph_dict[vertex2] = [vertex1]

    def _generate_edges(self):
        """Metodo que genera las aritas del grafo como tuplas.

        Returns:
            list: Lista de aristas del grafo.
        """        
        edges = []
        for vertex in self._graph_dict:
            for neighbour in self._graph_dict[vertex]:
                edges.append((vertex, neighbour))
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self._generate_edges():
            res += str(edge) + " "
        return res

    def vertex_degree(self, vertex):
        """Grado de un vertice del grafo.

        Args:
            vertex : Vertice del grafo.

        Returns:
            int: Grado del vertice.
        """        
        adj_vertices =  self._graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree

    def degree_sequence(self):
        """Secuencia ordenada de los grados de los vertices
        del grafo.

        Returns:
            tuple: Grados de los vertices del grafo.
        """        
        seq = []
        # se agregan los grados de los vertices a 'seq'
        for vertex in self._graph_dict:
            seq.append(self.vertex_degree(vertex))
        # se ordenan los grafos de mayor a menor
        seq.sort(reverse=True)
        return tuple(seq)

    def delta(self):
        """Minimo grado del grafo.

        Returns:
            int: Minimo grado.
        """        
        min = 100000000
        for vertex in self._graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min
        
    def Delta(self):
        """Maximo grado del grafo.

        Returns:
            int: Maximo grado.
        """        
        max = 0
        for vertex in self._graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree > max:
                max = vertex_degree
        return max
   


if __name__ == "__main__":

    g = { "a" : ["d"],
          "b" : ["c"],
          "c" : ["b", "d", "e"],
          "d" : ["a", "c"],
          "e" : ["c"],
          "f" : []
        }

    graph = Graph(g)
    print(graph)

    for node in graph.vertices():
        print(graph.vertex_degree(node))

    print("The maximum degree of the graph is:")
    print(graph.Delta())

    print("The minimum degree of the graph is:")
    print(graph.delta())

    print("Edges:")
    print(graph.edges())

    print("Degree Sequence: ")
    ds = graph.degree_sequence()
    print(ds)

    print("Add vertex 'z':")
    graph.add_vertex("z")
    print(graph)

    print("Add edge ('x','y'): ")
    graph.add_edge(('x', 'y'))
    print(graph)

    print("Add edge ('a','d'): ")
    graph.add_edge(('a', 'd'))
    print(graph)
    