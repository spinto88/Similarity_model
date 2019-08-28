def read_data(fName):

    fp = open(fName,'r').read().split('\n')
    fp = [f.split(',') for f in fp[:len(fp)-1]]

    fz = [float(f[0]) for f in fp]
    fragments = [[int(g) for g in f[3:]] for f in fp]

    return fz, fragments

def biggest_fragment(fName):

    import numpy as np

    fz, fragments = read_data(fName)

    fzrange = sorted(list(set(fz)))

    bigfrag_fz = []

    for fz_aux in fzrange:
        frag_fz = []
        for d in range(len(fragments)):
            if fz[d] == fz_aux:
                frag_fz += [np.max(fragments[d])]

        bigfrag_fz.append([fz_aux, np.mean(frag_fz), frag_fz])

    return bigfrag_fz

import matplotlib.pyplot as plt
import numpy as np

data = biggest_fragment('Data_F10.dat')

plt.axes([0.15, 0.15, 0.75, 0.75])

plt.plot([b[0] for b in data], [b[1] for b in data], '-', linewidth = 3, alpha = 0.75)

for i in range(len(data)):
    plt.scatter([data[i][0]] * len(data[i][2]), data[i][2], alpha = 0.15, color = 'k')

plt.xlabel('Fraction of zeros', size = 15)
plt.ylabel('Biggest fragment', size = 15)
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.grid(True, alpha = 0.25)

#plt.savefig('Colapso_con_el_grado_N{}.png'.format(N), dpi = 300)
plt.show()
