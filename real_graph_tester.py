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

class RealGraphTester(object):
    def __init__(self, graph, s_size, pow2_mode=False, extra_stats=False):
        self.graph = graph
        self._n = len(graph.vertices())
        self._s = s_size
        self._extra_stats = extra_stats
        if pow2_mode is True:
            self._w = self._make_w_pow2()
        else:
            self._w = self._make_w()
        self._spectrum = [str(i) for i in range(1, s_size+1)]


    def _make_w(self):
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
        w = {}
        for i in range(1, self._s+1):
            w[str(i)] = { str(j):1/(2**(abs(i-j))) for j in range(1, self._s+1)}
        return w

    def _statistics(self, cost_list, time_list, solution_list):
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
        costs = { item:np.zeros(iters) for item in algorithm_class_dict}
        times = { item:np.zeros(iters) for item in algorithm_class_dict}
        degree = []
        solutions = { item:[0 for i in range(iters)] for item in algorithm_class_dict }
        timer = Stopwatch()
        for d in self.graph.degree_sequence():
            degree.append(d)
        for item in algorithm_class_dict:
            algorithm_class = algorithm_class_dict[item](self.graph, self._spectrum, self._w)
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

# def full_test():
#     algorithms = {'DSATUR': DSATURGraphColoring, 'PSO': PSOGraphColoring, 'Random': RandomGraphColoring}    
#     for t in [3]:
#         for n in [60, 70, 80]:
#             for p in [.1, .5,.9]:
#                 str_t = ''
#                 test = RandomGraphTester(n, p, n)
#                 if t == 1:
#                     str_t = 'np4'
#                     statistics = test.run_test(n*p/4, algorithms, 20, 5, TSC_OR_CSC='CSC',log=True)
#                 elif t == 2:
#                     str_t = 'np2'
#                     statistics = test.run_test(n*p/2, algorithms, 20, 5, TSC_OR_CSC='CSC', log=False)
#                 else:
#                     str_t = '3np4'
#                     statistics = test.run_test(3*n*p/4, algorithms, 20, 5, TSC_OR_CSC='CSC', log=False)
#                 # statistics = test.run_test(k, algorithms, 10, 20, log=False)
#                 case = 1
#                 if p == .5:
#                     case = 5
#                 if p == .9:
#                     case = 9
#                 with open(f'test_{str_t}_n{n}_p{case}.json', 'w') as handle:
#                     handle.write(json.dumps(statistics, cls=MyEncoder))

# def test2file(algorithms, color_sizes, vertice_sizes, probabilities, file_name):
#     d = {}
#     for k in color_sizes:
#         for n in vertice_sizes:
#             for p in probabilities:
#                 test = RandomGraphTester(n, p, k)
#                 statistics = test.run_test(k, algorithms, 20, 10, log=False)
#                 d[f'k={k}_n={n}_p={p}'] = statistics
#     with open(f'{file_name}.json', 'w') as handle:
#         handle.write(json.dumps(d, cls=MyEncoder))


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

    BD = {
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

    
    AD = {
            '1': ['2', '3', '4', '5', '6', '7'], #6
            '2': ['1', '3', '4', '5', '6', '7', '24', '26'], #8
            '3': ['1', '2', '4', '5', '6', '7', '9', '13', '15', '22', '24'], #11
            '4': ['1', '2', '3', '5', '7', '9', '13', '15', '22', '24', '25', '26'],#13
            '5': ['1', '2', '3', '4', '6', '7', '8', '9'], #8
            '6': ['1', '2', '3', '5', '7', '8', '9', '10', '11', '13'], #10            
            '7': ['1', '2', '3', '4', '5', '6', '8', '9', '11', '13', '15', '22', '24'], #13
            '8': ['5', '6', '7', '9', '10', '11', '13', '14'], #8
            '9': ['3', '4', '5', '6','7', '8', '10', '11', '13', '14', '15', '16', '22'],#13
            '10': ['6', '8', '9', '11', '13', '14'], #6
            '11': ['6', '8', '9', '10', '13', '14', '15'],#7
            # '12': ['8', '9', '10', '11', '13', '14', '16'], #7
            '13': ['3', '4', '6', '7', '8', '9', '10', '11', '14', '15', '16', '17', '22'],#13
            '14': ['8', '9', '10', '11', '13', '15', '16', '17', '18', '22'], #10
            '15': ['3', '4', '7', '9', '11', '13', '14', '16', '17', '18', '21', '22', '23', '24', '25'],#14
            '16': ['9', '13', '14', '15', '17', '18', '19', '20', '21', '22', '23'],#11
            '17': ['13', '14', '15', '16', '18', '19', '20', '21', '22', '23', '24'],#11
            '18': ['14', '15', '16', '17', '19', '20', '21', '22', '23'],#9
            '19': ['16', '17', '18', '20', '21', '22', '23'],#7
            '20': ['16', '17', '18', '19', '21', '22'],#6
            '21': ['15', '16', '17', '18', '19', '20', '22', '23', '24', '25'],#10
            '22': ['3', '4', '7', '9', '13', '14', '15', '16', '17', '18', '19', '20', '21', '23', '24', '25', '26'],#17
            '23': ['15', '16', '17', '18', '19' ,'21', '22', '24', '25', '26'],#10
            '24': ['2', '3', '4', '7', '15', '17', '21', '22', '23', '25', '26'],#11
            '25': ['4', '15', '21', '22', '23', '24', '26'],#7
            '26': ['2', '4' , '22', '23', '24', '25']#6
    }

    # graph = Graph(AD)
    algorithms = {'RANDOM': RandomGraphColoring, 'DSATUR': DSATURGraphColoring, 'PSO': PSOGraphColoring}
    tester = RealGraphTester(graph, 4)
    tester.run_test(4, algorithms, 10)
    import os
    freq = 440
    time = 3
    os.system('play -nq -t alsa synth {}'.format(time, freq))

    # encoder = MyEncoder().encode(graph)
    # print(encoder)