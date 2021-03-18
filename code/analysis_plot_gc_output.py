# going from 1 file per pixel with results to a dataframe / tiff fil (?) to plot the output

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-white')

from list_files_in_directory import listfilenames_csv

inpath = "C:/EVA/THESIS/data/analyse_test2/"

def create_array_from_pixels(inpath, colname):
    output_array = np.empty([20,40])
    for x in range(40):
        for idx, y in enumerate(range(10, -10,-1)):
            file_names = listfilenames_csv(inpath)
            value = pd.read_csv(f'{y-0.5},{x+0.5}.csv', names = ['latitude', 'longitude', 'lin_R2_bl', 'lin_R2_full', 'lin_GC_dif', 'nonlin_R2_bl', 'nonlin_R2_full', 'nonlin_GC_dif']).loc[0,colname]
            #print(value)
            print(idx, y, x)
            output_array[idx, x] = value

    return output_array



make_figs = ['lin_R2_full', 'lin_GC_dif', 'nonlin_R2_full', 'nonlin_GC_dif']
for idx, make_fig in enumerate(make_figs):
    matrix = create_array_from_pixels(inpath, make_fig)
    fig = plt.figure()
    cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['black', 'white'], 256)
    img = plt.imshow(matrix, interpolation='nearest', cmap=cmap, origin='Lower')
    plt.colorbar(img, cmap=cmap)
    fig.suptitle(make_fig)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    fig.savefig(f'{make_fig}.jpg')
    plt.show()



