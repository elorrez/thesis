# going from 1 file per pixel with results to a dataframe / tiff fil (?) to plot the output

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
plt.style.use('seaborn-white')

from list_files_in_directory import listfilenames_csv

inpath = "C:/EVA/THESIS/data/analyse_test_7/"
zero_pixels = "C:/EVA/THESIS/data/empty_output_water_pixels/"

def create_array_from_pixels(inpath, path_zero, colname):
    output_array = np.empty([20,40])
    for x in range(40):
        for idx, y in enumerate(range(10, -10,-1)):
            file_names = listfilenames_csv(inpath)
            zero_file_names = listfilenames_csv(path_zero)

            if  f'{y-0.5},{x+0.5}.csv' in file_names:
                path = f'{inpath}{y-0.5},{x+0.5}.csv'
            elif f'{y-0.5},{x+0.5}.csv' in zero_file_names:
                path = f'{path_zero}{y - 0.5},{x + 0.5}.csv'

            value = pd.read_csv(path,
                                names=['latitude', 'longitude', 'lin_R2_bl', 'lin_R2_full', 'lin_GC_dif',
                                       'nonlin_R2_bl', 'nonlin_R2_full', 'nonlin_GC_dif']).loc[0, colname]
            #print(value)
            print(idx, y, x)
            output_array[idx, x] = value

    return output_array



make_figs = ['lin_R2_full', 'nonlin_R2_full']
for idx, make_fig in enumerate(make_figs):
    matrix = create_array_from_pixels(inpath,zero_pixels, make_fig)
    fig = plt.figure()
    #cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['black', 'white'], 256)
    #img = plt.imshow(matrix, interpolation='nearest', cmap=cmap, origin='upper')
    img = plt.imshow(matrix)
    plt.colorbar(img)
    fig.suptitle(make_fig)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    fig.savefig(f'{inpath}{make_fig}.jpg')
    plt.show()



