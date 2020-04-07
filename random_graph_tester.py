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

    def make_graph(self):
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
        w = {}
        for i in range(1, self._s+1):
            w[str(i)] = { str(j):1/(2**(abs(i-j))) for j in range(1, self._s+1)}
        return w

    def _statistics(self, cost_list, time_list, solution_list):
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
        costs = { item:np.zeros((n_graph, graph_iters)) for item in algorithm_class_dict}
        times = { item:np.zeros((n_graph, graph_iters)) for item in algorithm_class_dict}
        degree = []
        solutions = {
                        item:[[0 for i in range(graph_iters)] for j in range(n_graph)] 
                        for item in algorithm_class_dict 
                    }
        timer = Stopwatch()
        for i in range(n_graph):
            graph = self.make_graph()
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

def full_test():
    algorithms = {'DSATUR': DSATURGraphColoring, 'Random': RandomGraphColoring}    
    for t in [3]:
        for n in [80]:
            for p in [.1]:
                str_t = ''
                test = RandomGraphTester(n, p, n)
                if t == 1:
                    str_t = 'np4'
                    statistics = test.run_test(n*p/4, algorithms, 20, 10, TSC_OR_CSC='CSC',log=False)
                elif t == 2:
                    str_t = 'np2'
                    statistics = test.run_test(n*p/2, algorithms, 20, 10, TSC_OR_CSC='CSC', log=False)
                else:
                    str_t = '3np4'
                    statistics = test.run_test(3*n*p/4, algorithms, 20, 10, TSC_OR_CSC='CSC', log=False)
                # statistics = test.run_test(k, algorithms, 10, 20, log=False)
                case = 1
                if p == .5:
                    case = 5
                if p == .9:
                    case = 9
                with open(f'test_{str_t}_n{n}_p{case}.json', 'w') as handle:
                    handle.write(json.dumps(statistics, cls=MyEncoder))

def test2file(algorithms, color_sizes, vertice_sizes, probabilities, file_name):
    d = {}
    for k in color_sizes:
        for n in vertice_sizes:
            for p in probabilities:
                test = RandomGraphTester(n, p, k)
                statistics = test.run_test(k, algorithms, 20, 10, log=False)
                d[f'k={k}_n={n}_p={p}'] = statistics
    with open(f'{file_name}.json', 'w') as handle:
        handle.write(json.dumps(d, cls=MyEncoder))


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
    full_test()
    # algorithms = {'DSATUR': DSATURGraphColoring}
    # solution = {}
    # for iters in [300, 500]:
    #     for c1 in [0.5, 1.0, 1.5, 2.0, 3.0]:
    #         for c2 in [0.5, 1.0, 1.5, 2.0, 3.0]:
    #             for w in [0.5]:
    #                 print("---------------------------------")
    #                 print("---------------------------------")
    #                 tester = RandomGraphTester(60, .5, 4)
    #                 print(f'Config i={iters}_c1={c1}_c2={c2}_w={w}')
    #                 best = tester.run_test(4, algorithms, 10, 5, log=True, TSC_OR_CSC='TSC', swarm_size=15, c1=c1 ,c2=c2, w=w, iterations=iters)
    #                 solution[f'i={iters}_c1={c1}_c2={c2}_w={w}'] = best
    # with open('pso_parameters.json', 'w') as handle:
    #     handle.write(json.dumps(solution, cls=MyEncoder))
    # for w in [.1, .2,.3,.4, .5,.6, .7,.8, .9,1.0, 1.1, 1.5, 2.0]:
    # iters = 300
    # n_particles = 15
    # c1, c2 = 1.0, 3.0
    # w = 0.5
    # print(f'iters = {iters} n = {n_particles} c1={c1} c2={c2} w={w}')
    # tester = RandomGraphTester(80, .9, 80)
    # r = []
    # for _ in range(20):
    # tester.run_test(18, algorithms, 10, 5, log=True, TSC_OR_CSC='CSC')#, swarm_size=n_particles, c1=c1 ,c2=c2, w=w, iterations=iters)
    # print(r)
    import os
    freq = 440
    time = 3
    os.system('play -nq -t alsa synth {}'.format(time, freq))

    # encoder = MyEncoder().encode(graph)
    # print(encoder)