from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from pso import PSOGraphColoring
from heuristic import DSATURGraphColoring
from randomc import RandomGraphColoring
from stopwatch import Stopwatch
import numpy as np
import random
import json
from json import JSONEncoder

class RandomGraphTester(object):
    def __init__(self, n_vertices, conn_prob, s_size, extra_stats=False):
        self._n = n_vertices
        self._p = conn_prob
        self._s = s_size
        self._extra_stats = extra_stats
        self._w = self._make_w()
        self._spectrum = [str(i) for i in range(1, s_size+1)]

    def _make_graph(self):
        """ returns a random graph with self._n vertices and average 
            degree self._n*self._p
        """
        graph = np.zeros((self._n+1, self._n+1))
        for i in range(1, self._n+1):
            for j in range(i+1, self._n+1):
                if random.random() <= self._p:
                    graph[i,j] = graph[j, i] = 1
        graph_dict = {}
        for i in range(1, self._n+1):
            neighbours_i = []
            for j in range(1, self._n+1):
                if graph[i,j]:
                    neighbours_i.append(str(j))
            graph_dict[str(i)] = neighbours_i
        return Graph(graph_dict)

    def _make_w(self):
        """ make the W matrix of interferences using a potential decay 2 function
        """
        w = {}
        for i in range(1, self._s+1):
            w[str(i)] = { str(j):1/(2**(abs(i-j))) for j in range(1, self._s+1)}
        return w

    def _statistics(self, cost_list, time_list, solution_list):
        """ returns a dict of multiples statistics for a solotion list
        """
        mean = cost_list.mean()
        std = cost_list.std()
        min_by_iteration = []
        for i in range(cost_list.shape[0]):
            argmin = cost_list[i].argmin()
            min_by_iteration.append((i, cost_list[i,argmin], solution_list[i][argmin]))
        best_cost, best_s = (1e10, None)
        for _, cost, solution in min_by_iteration:
            if cost < best_cost:
                best_cost, best_s = cost, solution
        if self._extra_stats:
             return {
                'best_cost': best_cost,
                'mean': mean,
                'std': std,
                'time': time_list.mean(),
                'graph': best_s[0],
                'coloring': best_s[1],
                'best_sost_by_iteration': min_by_iteration
            }
        else:
            return {
                'best_cost': best_cost,
                'mean': mean,
                'std': std,
                'time': time_list.mean()
            }

    def run_test(self, parameter, algorithm_class_dict, n_graph, graph_iters, log=True, TSC_OR_CSC='TSC', *args, **kargs):
        """ run a test to solve the TSC or CSC problem specified in 'TSC_OR_CSC',
            making 'n_graph' different graphs itering 'graph_iters' times in every one,
            while to apply the algorithms in 'algorithm_class_dict' with the parameter
            'parameter'.
        """
        costs = { item:np.zeros((n_graph, graph_iters)) for item in algorithm_class_dict}
        times = { item:np.zeros((n_graph, graph_iters)) for item in algorithm_class_dict}
        degree = []
        solutions = {
                        item:[[0 for i in range(graph_iters)] for j in range(n_graph)] 
                        for item in algorithm_class_dict 
                    }
        timer = Stopwatch()
        for i in range(n_graph):
            graph = self._make_graph()
            for d in graph.degree_sequence():
                degree.append(d)
            for item in algorithm_class_dict:
                algorithm_class = algorithm_class_dict[item](graph, self._spectrum, self._w)
                for j in range(graph_iters):
                    timer.restart()
                    if TSC_OR_CSC == 'TSC':
                        cost, coloring = algorithm_class.ThresholdSpectrumColoring(parameter, *args, **kargs)
                    elif TSC_OR_CSC == 'CSC':
                        cost, coloring = algorithm_class.ChromaticSpectrumColoring(parameter, *args, **kargs)
                    else:
                        return None
                    timer.stop()
                    times[item][i,j] = timer.duration
                    costs[item][i,j] = cost
                    solutions[item][i][j] = algorithm_class, coloring
        statistics = {}
        degree = np.array(degree)
        for item in algorithm_class_dict:
            statistics[item] = self._statistics(costs[item], times[item], solutions[item])
            if log:
                print("---------------------------------")
                print(item)
                print("Best solution: {0:.2f}".format(statistics[item]['best_cost']))
                print("Mean: {0:.2f}".format(statistics[item]['mean']))
                print("Std: {0:.2f}".format(statistics[item]['std']))
                print("Time mean: {0:.3f}".format(statistics[item]['time']))
                print("Delta: {0}".format(degree.max()))
                print("Natural norm: {0}".format(algorithm_class._natural_norm()))
                print("Degree mean: {0}".format(int(degree.mean())))
                print("Bound: {0}".format(int(degree.max())*algorithm_class._natural_norm()/parameter))
                print("---------------------------------")
        return {'settings': {
                                'problem': TSC_OR_CSC,
                                'n_vertices': self._n,
                                'conn_prob': self._p,
                                's_size': self._s,
                                'parameter': parameter,
                                'n_graphs': n_graph,
                                'graph_iters': graph_iters,
                                'algorithms': list(algorithm_class_dict.keys())
                            }, 
                'statistics':statistics
            }


class MyEncoder(JSONEncoder):
    def default(self, o):
        try:
            return o.__dict__
        except:
            print(o)


if __name__ == "__main__":


    algorithms = {'RANDOM': RandomGraphColoring, 'DSATUR': DSATURGraphColoring, 'PSO': PSOGraphColoring}
    print("_________________________________")
    print("---------------------------------")
    print("TSC")
    tester = RandomGraphTester(60, .5, 11)
    tester.run_test(11, algorithms, 10, 5, log=True)
    print("_________________________________")
    print("---------------------------------")
    print("CSC")
    tester = RandomGraphTester(60, .5, 60)
    tester.run_test(15, algorithms, 10, 5, log=True, TSC_OR_CSC='CSC')