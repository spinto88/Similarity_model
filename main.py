from model_src import *

# Random seed
seed = 123451
# Set the random generator seed
np.random.seed(seed)

# --------------------------------------------------- #

F = 5

n = 400
degree = 4

delta = 1.00/F
threshold = 0.00

mysys = Mysys(n = n)

mysys.set_delta(delta)
mysys.set_topology('random_regular', degree = degree)
mysys.set_threshold(threshold)

krange = np.logspace(-1, np.log10(n)-0.01, 21)
q_value = lambda k, delta, n: int((1.00 - (1.00 - float(k)/(n-1))**delta)**(-1))

qrange = [q_value(k, delta, n) for k in krange]
try:
    qrange.remove(1)
except:
    pass

for i in range(len(qrange)): 

  for iteration in range(2):

      mysys.set_axelrod_initial_state(F,qrange[i])

      mysys.evol2convergence(simetric = 1)

      print krange[i], np.max(mysys.fragments_size(threshold))

  #mysys.save_data_axelrod('Data.dat')
