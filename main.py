from model_src import *

# Random seed
seed = 123457
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

n = 100
delta_up = 0.1
threshold = 0.25
delta_down = 0.00

fragment_tau = 0.5

degree = n

mysys = Mysys(n = n)

mysys.set_delta_up(delta_up)
mysys.set_delta_down(delta_down)

mysys.set_topology('random_regular', degree = degree)

mysys.set_threshold(threshold)

mysys.set_non_uniform_initial_state(p = 0.30)

print mysys.mean_hom()

#print mysys.fragments_size(fragment_tau)


mysys.evol2convergence()

print mysys.mean_hom()
print mysys.fragments_size(fragment_tau)

#            mysys.save_data('N{}_delta{:.2f}_degree{}.dat'.format(n,delta,degree))

