from graph_coloring import SpectrumGraphColoring
from graph2 import Graph
from pso import PSOGraphColoring
from dsatur import DSATURGraphColoring
from randomc import RandomGraphColoring
from stopwatch import Stopwatch
import numpy as np
import random
import json
from json import JSONEncoder

class RealGraphTester(object):
    def __init__(self, graph, s_size, pow2_mode=False, extra_stats=False):
        self._graph = graph
        self._n = len(graph.vertices())
        self._s = s_size
        self._extra_stats = extra_stats
        if pow2_mode is True:
            self._w = self._make_w_pow2()
        else:
            self._w = self._make_w()
        self._spectrum = [str(i) for i in range(1, s_size+1)]


    def _make_w(self):
        """ make the W matrix of interferences using a decay function
        """
        w = {}
        for i in range(1, self._s+1):
            w[str(i)] = {}
            for j in range(1, self._s+1):
                dif_ij = abs(i-j)
                if dif_ij is 0:
                    w[str(i)][str(j)] = 1
                elif dif_ij is 1:
                    w[str(i)][str(j)] = 0.8
                elif dif_ij is 2:
                    w[str(i)][str(j)] = 0.5
                elif dif_ij is 3:
                    w[str(i)][str(j)] = 0.2
                elif dif_ij is 4:
                    w[str(i)][str(j)] = 0.1
                elif dif_ij is 5:
                    w[str(i)][str(j)] = 0.001
                elif dif_ij >= 6:
                    w[str(i)][str(j)] = 0
        return w

    def _make_w_pow2(self):
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
        best_cost, best_s = (1e10, None)
        for i, cost in enumerate(cost_list):
            if cost < best_cost:
                best_cost, best_s = cost, solution_list[i]
        if self._extra_stats:
             return {
                'best_cost': best_cost,
                'mean': mean,
                'std': std,
                'time': time_list.mean(),
                'graph': best_s[0],
                'coloring': best_s[1],
            }
        else:
            return {
                'best_cost': best_cost,
                'mean': mean,
                'std': std,
                'time': time_list.mean()
            }

    def run_test(self, parameter, algorithm_class_dict, iters, log=True, TSC_OR_CSC='TSC', *args, **kargs): 
        """ run a test to solve the TSC or CSC problem specified in 'TSC_OR_CSC',
            itering 'graph_iters' times in self._graph,
            while to apply the algorithms in 'algorithm_class_dict' with the parameter
            'parameter'.
        """
        costs = { item:np.zeros(iters) for item in algorithm_class_dict}
        times = { item:np.zeros(iters) for item in algorithm_class_dict}
        degree = []
        solutions = { item:[0 for i in range(iters)] for item in algorithm_class_dict }
        timer = Stopwatch()
        for d in self._graph.degree_sequence():
            degree.append(d)
        for item in algorithm_class_dict:
            algorithm_class = algorithm_class_dict[item](self._graph, self._spectrum, self._w)
            for i in range(iters):
                timer.restart()
                if TSC_OR_CSC == 'TSC':
                    cost, coloring = algorithm_class.ThresholdSpectrumColoring(parameter, *args, **kargs)
                elif TSC_OR_CSC == 'CSC':
                    cost, coloring = algorithm_class.ChromaticSpectrumColoring(parameter, *args, **kargs)
                else:
                    return None
                timer.stop()
                times[item][i] = timer.duration
                costs[item][i] = cost
                solutions[item][i] = algorithm_class, coloring
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
                                's_size': self._s,
                                'parameter': parameter,
                                'iters': iters,
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

    g = {
        "a": ["b", "c"],
        "b": ["a", "c"],
        "c": ["a", "b", "d"],
        "d": ["c"]
    }

    LD = {
            '1': ['2', '3', '4', '5'],
            '2': ['1', '3', '4', '5', '6'],
            '3': ['1', '2', '4', '5', '6'],
            '4': ['1', '2', '3', '5', '6', '7', '8'],
            '5': ['1', '2', '3', '4', '6', '7', '8', '9'],
            '6': ['2', '3', '4', '5', '7', '8', '9', '10'],
            '7': ['4', '5', '6', '8', '9', '10'],
            '8': ['4', '5', '6', '7', '9', '10', '11'],
            '9': ['5', '6', '7', '8', '10', '11', '12'],
            '10': ['6', '7', '8', '9', '11', '12', '13', '14'],
            '11': ['8', '9', '10', '12', '13', '14', '15'],
            '12': ['9', '10', '11', '13', '14', '15'],
            '13': ['10', '11', '12', '14', '15', '16'],
            '14': ['10', '11', '12', '13', '15', '16', '17'],
            '15': ['11', '12', '13', '14', '16', '17'],
            '16': ['13', '14', '15', '17', '18'],
            '17': ['14', '15', '16', '18'],
            '18': ['16', '17']
    }

    algorithms = {'RANDOM': RandomGraphColoring, 'DSATUR': DSATURGraphColoring, 'PSO': PSOGraphColoring}
    print("_________________________________")
    print("---------------------------------")
    print('Case 1:')
    graph = Graph(g)
    print(graph)
    tester = RealGraphTester(graph, 4)
    tester.run_test(4, algorithms, 100)
    print("_________________________________")
    print("---------------------------------")
    print('Case 2:')
    graph = Graph(LD)
    print(graph)
    tester = RealGraphTester(graph, 11)
    tester.run_test(11, algorithms, 100)