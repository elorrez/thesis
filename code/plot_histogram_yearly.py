# plot the climate data: one histogram per year

import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4 as nc
from list_files_in_directory import listfilepaths_nc
import numpy as np
import pandas as pd


import json
#import plotly_express as px
# CRU_T

inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/"

twenty_years = []
for path in listfilepaths_nc(inpath):
    ds = nc.Dataset(path)
    print(ds['lat'])
    print(ds['tmp'])
    layer = path.split('.')[-3]
    #print(layer)
    our_area = ds[layer][:, 160:200, 360:440]

    print(our_area.shape)
    twenty_years.append(our_area)

threed_array = np.concatenate(twenty_years,  axis=0)

for month in threed_array:
    print(month.shape)
    # #
    month = np.where(month==9.96921e+36, 0, month)
    fig = plt.figure()
    cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['black', 'white'], 256)
    img = plt.imshow(month, interpolation='nearest', cmap=cmap, origin='upper')
    plt.colorbar(img, cmap=cmap)
    #fig.suptitle(make_fig)
    plt.xlabel('longitude')
    plt.ylabel('latitude')
    #fig.savefig(f'{inpath}{make_fig}.jpg')
    plt.show()
    ##
    #month_df = pd.DataFrame(threed_array[0,:,:])
    # month_df = month_df.replace(9.96921e+36, 0)
    # #print(month_df)
    # month_df.plot.hist()





