from model_src import *

# Random seed
seed = 123458
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

n = 400
delta_up = 0.216
threshold = 0.00
delta_down = 0.005

fragment_tau = 0.5

degree = n

mysys = Mysys(n = n)

mysys.set_delta_up(delta_up)
mysys.set_delta_down(delta_down)

mysys.set_topology('random_regular', degree = degree)

mysys.set_threshold(threshold)

data = []

p = 0.5
for delta_up in np.arange(0.5, 0.76, 0.025):#linspace(0.40, 0.95, 11):

  for i in range(1):

    #mysys.set_threshold(threshold)
    mysys.set_non_uniform_initial_state(p = p)
    mysys.set_delta_up(delta_up)

#    mysys.similarities_histogram()

#    print p, 
#    print mysys.mean_hom()

#    print np.max(mysys.fragments_size(fragment_tau)),

    mysys.evol2convergence()

#    mysys.similarities_histogram()

    print np.max(mysys.fragments_size(fragment_tau)), len(mysys.fragments_size(fragment_tau))
    data.append([delta_up, np.max(mysys.fragments_size(fragment_tau))])

import matplotlib.pyplot as plt

plt.scatter([d[0] for d in data], [d[1] for d in data])
plt.show()

#            mysys.save_data('N{}_delta{:.2f}_degree{}.dat'.format(n,delta,degree))

