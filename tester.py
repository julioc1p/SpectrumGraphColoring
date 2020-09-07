""" Python Class
    Clase de Python para testear los resultados de TSC y CSC con diferentes algoritmos.
"""

import random
import numpy as np
from graph2 import Graph
from stopwatch import Stopwatch


class GraphTester(object):

    def __init__(self, spectrum=None, w=None, extra_stats=False):
        """Inicializa un objeto GaphTester.

        Args:
            spectrum (list): Espectro de colores. Por defecto es None.
            w (dict): Matriz de interferencias entre los colores. Por defecto es None.
            extra_stats (bool): Se usan mas estadisticas en caso de ser True. Por defecto es False.
        """        
        self._w = w
        self._spectrum = spectrum
        self._extra_stats = extra_stats

    @property
    def w(self):
        return self._w
    
    @w.setter
    def w(self, new_w):
        self._w = new_w

    @property
    def spectrum(self):
        return self._spectrum

    @spectrum.setter
    def spectrum(self, new_spectrum):
        self._spectrum = new_spectrum

    def make_spectrum(self, s_size):
        """Crear un espectro de 's_size' colores.

        Args:
            s_size (int): Dimension del espectro de colores.
        """        
        new_spectrum = [str(i) for i in range(1, s_size+1)]
        self._spectrum = new_spectrum

    def make_w(self, w_function):
        """Crea una matriz de interferencias entre los colores usando la funcion 'w_function'.
        Args:
            w_function : Funcion de interferencia entre los colores.
        """        
        new_w = {item:{} for item in self._spectrum}
        for i, c1 in enumerate(self._spectrum):
            for j, c2 in enumerate(self._spectrum):
                new_w[c1][c2] = new_w[c2][c1] = w_function(i, j)
        self._w = new_w

    def _make_graph(self, n, p):
        """Crea un grafo aleatorio de 'n' vertices con una probabilidad
        de conexion 'p'.

        Args:
            n (int): Cantidad de vertices del grafo.
            p (float): Probabilidad de que dos vertices del grafo esten conectados.

        Returns:
            Graph: Nuevo grafo.
        """        
        graph = np.zeros((n+1, n+1))
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                if random.random() <= p:
                    graph[i,j] = graph[j, i] = 1
        graph_dict = {}
        for i in range(1, n+1):
            neighbours_i = []
            for j in range(1, n+1):
                if graph[i,j]:
                    neighbours_i.append(str(j))
            graph_dict[str(i)] = neighbours_i
        return Graph(graph_dict)

    def run_test2(self, graph, parameter, algorithm_class_dict, iters, log=True, all_solutions=False, TSC_OR_CSC='TSC', *args, **kargs):
        """Ejecuta los tests del problema 'TSC_OR_CSC' para el grafo dado usando los algoritmos de la lista.

        Args:
            graph (Graph): Grafo de prueba.
            parameter : Parametro del problema TSC o CSC.
            algorithm_class_dict (dict): Diccionario de algoritmos a usar.
            iters (int): Numero de veces que se ejecutaran las pruebas sobre el grafo.
            log (bool): Se imprimen los resultados mas relevantes en consola si es True. Por defecto es True.
            all_solutions (bool): Agrega todas las soluciones obtenidas al diccionario devuelto si es True. Por defecto es False.
            TSC_OR_CSC (str): Indica si se quiere resolver el problema TSC o CSC. Por defecto es 'TSC'.

        Returns:
            dict: Diccionario con los resultados de los experimentos.
        """        
        cost_list = { alg:np.zeros(iters) for alg in algorithm_class_dict}
        solution_list = { alg:[] for alg in algorithm_class_dict}
        time_list = { alg:np.zeros(iters) for alg in algorithm_class_dict}
        Rank = {alg:0 for alg in algorithm_class_dict}
        Nbest = {alg:0 for alg in algorithm_class_dict}
        for i in range(iters):
            slist, times = self._run(graph, parameter, algorithm_class_dict, TSC_OR_CSC, *args, **kargs)
            nbest, rank = self._nbest_rank([(alg, slist[alg][0]) for alg in slist])
            for alg in algorithm_class_dict:
                time_list[alg][i] = times[alg]
                cost_list[alg][i] = slist[alg][0]
                solution_list[alg].append(slist[alg][1])
                Rank[alg]+=rank[alg]
            for alg in nbest:
                Nbest[alg]+=1
        statistics = {}
        for alg in algorithm_class_dict:
            statistics[alg] = self._statistics2(cost_list[alg], time_list[alg], solution_list[alg], Rank[alg], Nbest[alg])
            if log:
                self._log(alg, statistics[alg])
        result = {'settings': {
                                'problem': TSC_OR_CSC,
                                's_size': len(self._spectrum),
                                'parameter': parameter,
                                'iters': iters,
                                'algorithms': list(algorithm_class_dict.keys())
                            }, 
                'statistics':statistics
            }
        if all_solutions:
            result['solutions'] = {
                                    'cost_list':cost_list,
                                    'solution_list':solution_list,
                                    'time_list':time_list
                }
        return result

    def run_random_test(self, n_graph, n_vertices, p, parameter, algorithm_class_dict, iters, log=True, all_solutions=False, TSC_OR_CSC='TSC', *args, **kargs):
        """Ejecuta los tests del problema 'TSC_OR_CSC' para grafos aleatorios usando los algoritmos de la lista.

        Args:
            n_graph (int): Numero de grafos aleatorios a generar.
            n_vertices (int): Numero de vertices del grafo.
            p (int): Probabilidad de conexion de los vertices del grafo. 
            parameter : Parametro del problema TSC o CSC.
            algorithm_class_dict (dict): Diccionario de algoritmos a usar.
            iters (int): Numero de veces que se ejecutaran las pruebas sobre el grafo.
            log (bool): Se imprimen los resultados mas relevantes en consola si es True. Por defecto es True.
            all_solutions (bool): Agrega todas las soluciones obtenidas al diccionario devuelto si es True. Por defecto es False.
            TSC_OR_CSC (str): Indica si se quiere resolver el problema TSC o CSC. Por defecto es 'TSC'.

        Returns:
            dict: Diccionario con los resultados de los experimentos.
        """        
        cost_list = { alg:np.array([]) for alg in algorithm_class_dict}
        solution_list = { alg:[] for alg in algorithm_class_dict}
        time_list = { alg:np.array([]) for alg in algorithm_class_dict}
        Rank = {alg:0 for alg in algorithm_class_dict}
        Nbest = {alg:0 for alg in algorithm_class_dict}
        for _ in range(n_graph):
            graph = self._make_graph(n_vertices, p)
            for _ in range(iters):
                r = self.run_test2(graph, parameter, algorithm_class_dict, iters, False, True, TSC_OR_CSC, *args, **kargs)
                solutions = r['solutions']
                statistics = r['statistics']
                for alg in algorithm_class_dict:
                    cost_list[alg] = np.concatenate([cost_list[alg], solutions['cost_list'][alg]])
                    solution_list[alg]+= solutions['solution_list'][alg]
                    time_list[alg] = np.concatenate([time_list[alg], solutions['time_list'][alg]])
                    Rank[alg]+= statistics[alg]['rank']
                    Nbest[alg]+= statistics[alg]['nbest']
        statistics = {}
        for alg in algorithm_class_dict:
            statistics[alg] = self._statistics2(cost_list[alg], time_list[alg], solution_list[alg], Rank[alg], Nbest[alg])
            if log:
                self._log(alg, statistics[alg])
        result = {'settings': {
                                'problem': TSC_OR_CSC,
                                's_size': len(self._spectrum),
                                'parameter': parameter,
                                'n_graph': n_graph,
                                'v_vertices': n_vertices,
                                'conn_prob': p,
                                'iters': iters,
                                'algorithms': list(algorithm_class_dict.keys())
                            }, 
                'statistics':statistics
            }
        if all_solutions:
            result['solutions'] = {
                                    'cost_list':cost_list,
                                    'solution_list':solution_list,
                                    'time_list':time_list
                }
        return result

    def _run(self, graph, parameter, algorithm_class_dict, TSC_OR_CSC='TSC', *args, **kargs):
        """Ejecuta el problema 'TSC_OR_CSC' para el grafo dado usando los algoritmos de la lista.

        Args:
            graph (Graph): Grafo de prueba.
            parameter : Parametro del problema TSC o CSC.
            algorithm_class_dict (dict): Diccionario de algoritmos a usar.
            TSC_OR_CSC (str): Indica si se quiere resolver el problema TSC o CSC. Por defecto es 'TSC'.

        Returns:
            dict: Diccionario con los resultados del experimento.
        """        
        solution = {}
        times = {}
        timer = Stopwatch()
        for algorithm in algorithm_class_dict:
            algorithm_graph = algorithm_class_dict[algorithm](graph, self._spectrum, self._w)
            timer.restart()
            if TSC_OR_CSC == 'TSC':
                cost, coloring = algorithm_graph.ThresholdSpectrumColoring(parameter, *args, **kargs)
            elif TSC_OR_CSC == 'CSC':
                cost, coloring = algorithm_graph.ChromaticSpectrumColoring(parameter, *args, **kargs)
            else:
                return None
            timer.stop()
            times[algorithm] = timer.duration
            solution[algorithm] = cost, coloring
        return solution, times

    def _log(self, algorithm, statistics):
        """Imprime en consola los principales resultados del algoritmo.

        Args:
            algorithm (str): Nombre del algoritmo.
            statistics (dict): Estadisticas del algoritmo.
        """        
        print("---------------------------------")
        print(algorithm)
        print("Best solution: {0:.2f}".format(statistics['best_cost']))
        print("Mean: {0:.2f}".format(statistics['mean']))
        print("Std: {0:.2f}".format(statistics['std']))
        print("Time mean: {0:.3f}".format(statistics['time']))
        print("#Best: {}".format(statistics['nbest']))
        print("Rank: {}".format(statistics['rank']))
        print("---------------------------------")    

    def _statistics2(self, cost_list, time_list, solution_list, rank, nbest):
        """Devuelve en un mismo diccionario las estadisticas de los resultados de los experimentos.

        Args:
            cost_list (list): Resultados de los problemas TSC o CSC para los experimentos.
            time_list (list): Tiempos de ejecucion de cada experimento.
            solution_list (list): Coloracion obtenida en cada experimento.
            rank (int): Rank obtenido en los experimentos.
            nbest (int): Numero de veces que se obtuvo la mejor solucion es los experimentos.

        Returns:
            dict: Estadisticas de los experimentos.
        """        
        mean = cost_list.mean()
        std = cost_list.std()
        time_mean = time_list.mean()
        bcost = cost_list.min()
        stats = {
                'best_cost': bcost,
                'mean': mean,
                'std': std,
                'nbest': nbest,
                'rank': rank,
                'time': time_mean
            }
        if self._extra_stats:
            cost = 1e10
            bcoloring = None
            for i in range(cost_list.shape[0]):
                if cost_list[i] < cost:
                    cost = cost_list[i]
                    bcoloring = solution_list[i]
            stats['coloring'] = bcoloring
        return stats

    def _nbest_rank(self, solution_list):
        """Determina el Rank y el nBest de cada algoritmo.

        Args:
            solution_list (list): Soluciones de los experimentos.

        Returns:
            tuple: Listas de Rank y nBest para cada algoritmo.
        """        
        sorted_alg = self._sort(solution_list)
        best = []
        idx = 0
        while idx < len(solution_list) and sorted_alg[idx][1] == sorted_alg[0][1]:
            best.append(sorted_alg[idx][0])
            idx+=1
        rank = {}
        same_value = 0
        last_value = -1
        for i in range(len(sorted_alg)):
            alg = sorted_alg[i][0]
            value = sorted_alg[i][1]
            if value == last_value:
                same_value+=1
            else:
                same_value = 0
            rank[alg] = i - same_value 
            last_value = value
        return best, rank

    def _sort(self, solutions):
        """Implementacion de Quick Sort para ordenar los resultados de los experimentos.

        Args:
            solutions (list): Soluciones de los experimentos.

        Returns:
            list: Lista ordenada.
        """        
        if not solutions:
            return []
        m = solutions[0]
        l = []
        ge = []
        for v in solutions[1:]:
            if v[1] < m[1]:
                l.append(v)
            else:
                ge.append(v)
        return self._sort(l) + [m] + self._sort(ge)





if __name__ == "__main__":

    from dsatur import DSATURGraphColoring
    from randomc import RandomGraphColoring
    algorithms = {'RANDOM': RandomGraphColoring, 'DSATUR': DSATURGraphColoring}
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
    # wfuntion = lambda x, y: 1/2**abs(x-y)
    tester = GraphTester()
    tester.spectrum = S
    # tester.make_w(wfuntion)
    tester.w = W
    tester.run_test2(graph, 4, algorithms, 10)
    # tester.run_random_test(10, 60, 0.5, 4, algorithms, 5)