from model_src import *

# Random seed
seed = 123457
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

n = 100
f = 1000

delta = 0.10
threshold = 0.5 * delta 

type_of_interaction = 'simetric'
  
mysys = Mysys(n = n)

mysys.set_delta(delta)
mysys.set_threshold(threshold)

mysys.set_topology('random_regular', degree = 4)


for fz in np.arange(0.25, 0.96, 0.05):

  for i in range(10):

    mysys.set_initial_state(f, fz)

    mysys.evol2convergence(type_of_interaction)

    print fz, np.max(mysys.fragments())

    mysys.save_data('Data_F{}.dat'.format(f))

