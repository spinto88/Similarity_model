import ctypes as C
import numpy as np
import os
import networkx as nx
from copy import deepcopy
import warnings

class Mysys(C.Structure):

    _fields_ = [('n', C.c_int),
                ('corr', C.POINTER(C.POINTER(C.c_double))),
	        ('a', C.POINTER(C.POINTER(C.c_int))),
                ('seed', C.c_int)]

    def __init__(self, n):

        self.n = n
        
	self.seed = np.random.randint(10**6)

    def set_topology(self, topology, **kwargs):

        from set_topology import set_topology

        self.adjacency_matrix = set_topology(topology, self.n, **kwargs).toarray()

	self.a = (self.n * C.POINTER(C.c_int))()
        for i in range(self.n):
            self.a[i] = (self.n * C.c_int)(*self.adjacency_matrix[i])

        return None

    def set_axelrod_initial_state(self, f, q):

        # Calculate q from the fraction of zeros

        states = [np.random.choice(q,f) for i in range(self.n)]

        self.axelrod_params = [f,q]
        self.fraction_of_zeros = (1.00 - 1.00 / q)**f

        def homophily(state1, state2):

           ef = lambda x, y: x == y

           return (np.float(np.sum(ef(state1, state2))) / f)


        corr_matrix = np.zeros([self.n, self.n], dtype = np.float)
        for i in range(self.n):
            for j in range(i+1, self.n):
                corr_matrix[i,j] = homophily(states[i], states[j])

        corr_matrix += corr_matrix.T

	self.corr = (self.n * C.POINTER(C.c_double))()
        for i in range(self.n):
            self.corr[i] = ((self.n) * C.c_double)(*corr_matrix[i])

        return None

    def set_delta(self, delta):

        self.delta = delta
        return None

    def set_threshold(self, threshold):

        self.threshold = threshold
        return None

    def actual_fraction_of_zeros(self):

        corr_matrix = self.get_corr_matrix()

        zero_links = 0
        total_links = int(self.n * (self.n-1) * 0.5)
        for i in range(corr_matrix.shape[0]):
            for j in range(i+1, corr_matrix.shape[1]):
                if corr_matrix[i,j] <= self.threshold:
                    zero_links += 1

        return float(zero_links)/total_links

    # model dynamics
    def dynamics(self, steps = 1, simetric = 0):

        libc = C.CDLL(os.getcwd() + '/model_src/libc.so')

        libc.dynamics.argtypes = [C.POINTER(Mysys), C.c_double, C.c_double, C.c_int, C.c_int]
        libc.dynamics.restype = C.c_int

        libc.dynamics(C.byref(self), self.delta, self.threshold, steps, simetric)

        return None

    def fragments_size(self, fragment_tau):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > fragment_tau and self.adjacency_matrix[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [len(x) for x in list(nx.connected_components(final_graph))]

        return fragments

    def fragments(self, fragment_tau):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > fragment_tau and self.adjacency_matrix[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [x for x in list(nx.connected_components(final_graph))]

        return fragments

    def corr_fragments_size(self, fragment_tau):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > fragment_tau:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [len(x) for x in list(nx.connected_components(final_graph))]

        return fragments

    def mean_hom(self):
        aux = []
        corr_matrix = self.get_corr_matrix()
        for i in range(self.n):
            for j in range(i+1, self.n):
                aux.append(corr_matrix[i,j])
        return np.mean(aux)
    
    def get_corr_matrix(self):
        corr_matrix = np.zeros([self.n, self.n], dtype = np.float)
        for i in range(self.n):
            for j in range(i+1, self.n):
                corr_matrix[i][j] = self.corr[i][j]
            
        corr_matrix += corr_matrix.T
        for i in range(self.n):
            corr_matrix[i][i] = 1.00
        
        return corr_matrix

    def number_of_active_links(self):

        libc = C.CDLL(os.getcwd() + '/model_src/libc.so')

        libc.number_of_active_links.argtypes = [C.POINTER(Mysys), C.c_double]
        libc.number_of_active_links.restype = C.c_int

        return libc.number_of_active_links(C.byref(self), self.threshold)

    def active_links(self):

	ans = []
        corr_matrix = self.get_corr_matrix()
        for i in range(corr_matrix.shape[0]):
            for j in range(i+1, corr_matrix.shape[0]):
                if (corr_matrix[i,j] > self.threshold) and (corr_matrix[i,j] < 1.00 - self.delta):
			ans.append((i,j))
	return ans

    def evol2convergence(self, simetric = 0):

        steps = 0
        while self.number_of_active_links() != 0:
            self.dynamics(100, simetric)
            steps += 100
        
        return steps

    def check_tri_inequality(self):
        corr_matrix = self.get_corr_matrix()

        for i in range(self.n):
            for j in range(self.n):
                for k in range(self.n):
                    if k != i and k != j and j != i:
                        if (corr_matrix[i][j] + 1 >= corr_matrix[j][k] + corr_matrix[i][k]) and (corr_matrix[i][j] + np.abs(corr_matrix[j][k] - corr_matrix[i][k]) <= 1):
                            pass
                        else:
			    return 0
	return 1

    def save_data_axelrod(self, fname):

        fp = open(fname, 'a')
        fp.write("{},{},{},".format(self.fraction_of_zeros, *self.axelrod_params))
        fp.write(','.join([str(s) for s in self.fragments_size(self.threshold)]))
        fp.write('\n')
        fp.close()

    
    def increase_similarity(self, i, j, delta):

        libc = C.CDLL(os.getcwd() + '/model_src/libc.so')

        libc.increase_similarity.argtypes = [C.POINTER(Mysys), C.c_int, C.c_int, C.c_double]
        libc.increase_similarity.restype = C.c_int

        return libc.increase_similarity(C.byref(self), i, j, delta)

    def similarities_histogram(self):

        import matplotlib.pyplot as plt

	corr_matrix = self.get_corr_matrix()

	similarities = [corr_matrix[i,j] for i in range(self.n) for j in range(i+1, self.n)]

        plt.hist(similarities, bins = np.arange(-0.05, 1.15, 0.1), density = True)

	plt.show()
