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

    def set_non_uniform_initial_state(self, p = 0.5, features = 100):

        state_matrix = np.random.choice([0.00, 1.00], p = [1-p, p], size = [self.n, features])

        def similarity(a,b):
            ans = np.float(a.dot(b)) / ((np.sum(a)*np.sum(b))**0.5)
            return ans

        corr_matrix = np.zeros([self.n, self.n], dtype = np.float)
        for i in range(self.n):
            for j in range(i+1, self.n):
                corr_matrix[i,j] = similarity(state_matrix[i], state_matrix[j])

        corr_matrix += corr_matrix.T

	self.corr = (self.n * C.POINTER(C.c_double))()
        for i in range(self.n):
            self.corr[i] = ((self.n) * C.c_double)(*corr_matrix[i])

    def set_uniform_initial_state(self):

        corr_matrix = np.zeros([self.n, self.n], dtype = np.float)
        for i in range(self.n):
            for j in range(i+1, self.n):
                corr_matrix[i,j] = np.random.random() * 0.5

        corr_matrix += corr_matrix.T

	self.corr = (self.n * C.POINTER(C.c_double))()
        for i in range(self.n):
            self.corr[i] = ((self.n) * C.c_double)(*corr_matrix[i])

    def set_axelrod_initial_state(self, f, fraction_of_zeros):

        # Calculate q from the fraction of zeros
        q = np.int(np.round((1 - fraction_of_zeros**(1.00 / f))**(-1)))

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
    def dynamics(self, type_of_interaction, steps = 1):

        libc = C.CDLL(os.getcwd() + '/model_src/libc.so')

        if type_of_interaction == 'asimetric':
       	
	    libc.dynamics_asimetric.argtypes = [C.POINTER(Mysys), C.c_double, C.c_double, C.c_int]
            libc.dynamics_asimetric.restype = C.c_int

            libc.dynamics_asimetric(C.byref(self), self.delta, self.threshold, steps)

        elif type_of_interaction == 'simetric':

	    libc.dynamics_simetric.argtypes = [C.POINTER(Mysys), C.c_double, C.c_double, C.c_int]
            libc.dynamics_simetric.restype = C.c_int

            libc.dynamics_simetric(C.byref(self), self.delta, self.threshold, steps)
        else:
            warnings.warn('Invalid type of interaction')

        return None

    def fragments_size(self):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > self.threshold and self.adjacency_matrix[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [len(x) for x in list(nx.connected_components(final_graph))]

        return fragments

    def fragments(self):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > self.threshold and self.adjacency_matrix[i,j] == 1:
                    final_ad_matrix[i,j] = 1

        final_ad_matrix += final_ad_matrix.T
        final_graph = nx.from_numpy_array(final_ad_matrix)
        fragments = [x for x in list(nx.connected_components(final_graph))]

        return fragments

    def corr_fragments_size(self):

        corr_matrix = self.get_corr_matrix()
        final_ad_matrix = np.zeros(corr_matrix.shape, dtype = np.int)
        for i in range(self.n):
            for j in range(i+1, self.n):
                if corr_matrix[i,j] > self.threshold:
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

        libc.number_of_active_links_simetric.argtypes = [C.POINTER(Mysys), C.c_double, C.c_double]
        libc.number_of_active_links_simetric.restype = C.c_int

        return libc.number_of_active_links_simetric(C.byref(self), self.delta, self.threshold)

    def evol2convergence(self, type_of_interaction):

        steps = 0
        while self.number_of_active_links() != 0:
            self.dynamics(type_of_interaction, 100)
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
        fp.write(','.join([str(s) for s in self.fragments_size()]))
        fp.write('\n')
        fp.close()

    def save_data(self, fname):

        fp = open(fname, 'a')
        fp.write("{},{},".format(self.delta, self.threshold))
        fp.write(','.join([str(s) for s in self.fragments_size()]))
        fp.write('\n')
        fp.close()

    def one_step_dynamics(self, type_of_interaction, i, j):

        libc = C.CDLL(os.getcwd() + '/model_src/libc.so')

        if type_of_interaction == 'asimetric':
       	
	    libc.one_step_asimetric.argtypes = [C.POINTER(Mysys), C.c_double, C.c_int, C.c_int]
            libc.one_step_asimetric.restype = C.c_int

            libc.one_step_asimetric(C.byref(self), self.delta, i, j)

        elif type_of_interaction == 'simetric':

	    libc.one_step_simetric.argtypes = [C.POINTER(Mysys), C.c_double, C.c_int, C.c_int]
            libc.one_step_simetric.restype = C.c_int

            libc.one_step_simetric(C.byref(self), self.delta, i, j)

        return None
