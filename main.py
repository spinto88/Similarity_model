from model_src import *

# Random seed
seed = 123457
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

n = 100
type_of_interaction = 'simetric'
 
mysys = Mysys(n = n)

for delta in [0.5, 0.25, 0.1, 0.05, 0.01]:

  mysys.set_delta(delta)

  for degree in [4, n]:

    mysys.set_topology('random_regular', degree = degree)

    for i in range(100):

        for threshold in np.arange(0.10, 0.51, 0.015):

            mysys.set_threshold(threshold)

            mysys.set_uniform_initial_state()

            mysys.evol2convergence(type_of_interaction)

            mysys.save_data('N{}_delta{:.2f}_degree{}.dat'.format(n,delta,degree))

