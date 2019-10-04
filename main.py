from model_src import *

# Random seed
seed = 123458
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

F = 100
Q = 100

n = 100
degree = n

delta = 1.00/F
threshold = 0.5 * delta

mysys = Mysys(n = n)

mysys.set_delta(delta)
mysys.set_topology('random_regular', degree = degree)
mysys.set_threshold(threshold)

for Q in range(100, 10001, 15):

  mysys.set_axelrod_initial_state(F,Q)

  mysys.evol2convergence()

  print Q,(n-1)*(1.00-mysys.fraction_of_zeros), np.max(mysys.fragments_size(threshold))
