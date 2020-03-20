""" A Python Class
A simple Python graph class, demonstrating the essential 
facts and functionalities of graphs.
"""

class Graph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self._graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self._generate_edges()

    def neighbours(self, vertex):
        """ returns the neighbours of "vertex" in
            the graph
        """
        return self._graph_dict[vertex]

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self._graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            the edges are undirected and
            between two vertices cannot be multiple edges! 
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
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with two vertices 
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
        """ The degree of a vertex is the number of edges connecting
            it, i.e. the number of adjacent vertices. 
        """ 
        adj_vertices =  self._graph_dict[vertex]
        degree = len(adj_vertices) + adj_vertices.count(vertex)
        return degree

    def degree_sequence(self):
        """ calculates the degree sequence """
        seq = []
        for vertex in self._graph_dict:
            seq.append(self.vertex_degree(vertex))
        seq.sort(reverse=True)
        return tuple(seq)

    def delta(self):
        """ the minimum degree of the vertices """
        min = 100000000
        for vertex in self._graph_dict:
            vertex_degree = self.vertex_degree(vertex)
            if vertex_degree < min:
                min = vertex_degree
        return min
        
    def Delta(self):
        """ the maximum degree of the vertices """
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

