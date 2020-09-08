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
        if line == '\n':
            continue
        line = line.split()
        if line[0] == 'c' or (len(line[0])> 1 and line[0][0] == '%'):
            continue
        if line[0] == 'p':
            graph_dict = {str(i):[] for i in range(1, int(line[2]) + 1)}
        elif line[0] == 'e':
            graph_dict[line[1]].append(line[2])
            graph_dict[line[2]].append(line[1])
        else:
            if not graph_dict :
                graph_dict = {str(i):[] for i in range(1, int(line[1]) + 1)}
            else:
                graph_dict[line[0]].append(line[1])
                graph_dict[line[1]].append(line[0])
    return Graph(graph_dict)
