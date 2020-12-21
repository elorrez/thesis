import csv
import numpy as np

with open('C:/EVA/THESIS/code/testdata/varnames.csv', 'r') as v:
    varns = list(csv.reader(v))

with open('C:/EVA/THESIS/code/testdata/infs.csv', 'r') as v:
    ind = list(csv.reader(v))

#print(varns)
#print(ind)

iind = [int(i) for i in ind[0]]
#print(iind)
inf = [varns[i] for i in iind]
np.shape(inf)
print(inf)
#iinf = [inf[i][0] for i in inf]
#print(iinf)

with open("C:/EVA/THESIS/code/testdata/infcolumns.csv", 'w',newline='') as outfile:
    writer = csv.writer(outfile, delimiter=',')
    writer.writerows(inf)