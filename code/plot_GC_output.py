# going from 1 file per pixel with results to a dataframe / tiff fil (?) to plot the output

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from EVI_listfiles import listfilenames_csv

inpath = "C:/EVA/THESIS/data/analyse_test1/"

def create_array_from_pixels(inpath, colname):
    output_array = np.empty([20,40])
    for x in range(40):
        for idx, y in enumerate(range(-10, 10)):
            file_names = listfilenames_csv(inpath)
            value = pd.read_csv(f'{y+0.5},{x+0.5}.csv', names = ['latitude', 'longitude', 'lin_R2_bl', 'lin_R2_full', 'lin_GC_dif', 'nonlin_R2_bl', 'nonlin_R2_full', 'nonlin_GC_dif']).loc[0,colname]
            output_array[idx, x] = value
            return output_array


GC_dif_matrix = create_array_from_pixels(inpath, 'nonlin_GC_dif')
print(GC_dif_matrix.shape)

nonlin_R2_matrix = create_array_from_pixels(inpath, 'nonlin_R2_full')
# plot histogram
# plt.hist(nonlin_R2_matrix)
# plt.gca().set(title='Frequency Histogram', ylabel='Frequency')
# plt.show()
cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['black','white'], 256)
bounds=[-6,-2,2,6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
img = plt.imshow(nonlin_R2_matrix,interpolation='nearest',
                    cmap = cmap,origin='Lower')
plt.colorbar(img,cmap=cmap)
plt.show()
