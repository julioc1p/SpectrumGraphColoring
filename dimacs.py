""" Metodo para leer grafos en formato DIMACS
"""

from graph2 import Graph


def dimacs_reader(path):
    """Crea un grafo a partir de un fichero en formato DIMACS.

    Args:
        path (str): Ruta del fichero.

    Returns:
        Graph: Nuevo grafo.
    """    
    fil = open(path)
    graph_dict = {}
    for line in fil:
        if line[0] == 'c' or line[0] == '%':
            continue
        if line[0] == 'p':
            s = line.split()
            graph_dict = {str(i):[] for i in range(1, int(s[2]) + 1)}
        elif line[0] == 'e':
            s = line.split()
            graph_dict[s[1]].append(s[2])
            graph_dict[s[2]].append(s[1])
        else:
            s = line.split()
            if not graph_dict :
                graph_dict = {str(i):[] for i in range(1, int(s[0]) + 1)}
            else:
                graph_dict[s[0]].append(s[1])
                graph_dict[s[1]].append(s[0])
    return Graph(graph_dict)
