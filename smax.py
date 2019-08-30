def read_data(fName):

    fp = open(fName,'r').read().split('\n')
    fp = [f.split(',') for f in fp[:len(fp)-1]]

    delta = [float(f[0]) for f in fp]
    threshold = [float(f[1]) for f in fp]
    fragments = [[int(g) for g in f[2:]] for f in fp]

    return delta, threshold, fragments

def biggest_fragment(fName):

    import numpy as np

    delta, threshold, fragments = read_data(fName)

    trange = sorted(list(set(threshold)))

    bigfrag_t = []

    for t in trange:
        frag_t = []
        for d in range(len(fragments)):
            if threshold[d] == t:
                frag_t += [np.max(fragments[d])]

        bigfrag_t.append([t, np.mean(frag_t), frag_t])

    return bigfrag_t

import matplotlib.pyplot as plt
import numpy as np

N = 100
delta = 0.1
degree = N

plt.axes([0.15, 0.15, 0.75, 0.75])

data = biggest_fragment('N{}_delta{:.2f}_degree{}.dat'.format(N,delta,degree))
plt.plot([b[0] for b in data], [b[1] for b in data], '-', linewidth = 3, alpha = 0.75, label = 'N')

degree = 4
data = biggest_fragment('N{}_delta{:.2f}_degree{}.dat'.format(N,delta,degree))
plt.plot([b[0] for b in data], [b[1] for b in data], '-', linewidth = 3, alpha = 0.75, label = '4')

#for i in range(len(data)):
#    plt.scatter([data[i][0]] * len(data[i][2]), data[i][2], alpha = 0.15, color = 'k')

plt.xlabel('Threshold', size = 15)
plt.ylabel('Biggest fragment', size = 15)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.grid(True, alpha = 0.25)
plt.legend(loc = 'best')

#plt.savefig('Colapso_con_el_grado_N{}.png'.format(N), dpi = 300)
plt.show()
