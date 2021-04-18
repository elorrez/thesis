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

inpath = "C:/EVA/THESIS/data/Climate_data/ERA5/adaptor.mars.internal-1618563855.2239437-9920-6-672d4cde-e751-451e-83ff-52fe5a944e16.nc"

ds = nc.Dataset(inpath)
print(ds)

temp = (ds['t2m'][:, :-1, :-1] - 273.15)
prec = (ds['tp'][:, :-1, :-1])
ssr = (ds['ssr'][:, :-1, :-1])
print(ssr)
print(temp.shape)
img = plt.imshow(ssr[0, :, :])
plt.colorbar(img)
plt.title('ERA5 radiatation')
plt.show()
map_std = plt.imshow(ssr.data.std(axis=0))
plt.colorbar(map_std)
plt.title('ERA5 radiatation std')
plt.show()
filtered = np.where(np.isinf(ssr.data.std(axis = 0)), 0, ssr.data.std(axis = 0))
plt.hist(filtered.reshape(200*400), bins = 50)
plt.title('ERA5 radiatation std histogram')
plt.show()

twenty_years = []
for path in listfilepaths_nc(inpath):
    ds = nc.Dataset(path)
    #print(layer)
    layer = path.split('.')[-3]
    #layer = 'ssr'
    if layer == 'precip':
        twenty_years.append(ds[layer][:, 80:100, 180:220])
    elif layer == 'ssr':
        twenty_years.append(ds[layer][:,:-1,: -1])
    else:
        twenty_years.append(np.flip(ds[layer][:,160:200, 360:440], axis=1))

    #print(np.flip(ds[layer][0,160:200, 360:440], axis=0))
    #img = plt.imshow(np.flip(ds[layer][0,160:200, 360:440], axis=0))
    #plt.colorbar(img)
    #plt.show()
    #print(np.flip(ds[layer][0,160:200, 360:440], axis=0).shape)
threed_array = np.ma.concatenate(twenty_years,  axis=0)
print(threed_array.shape)

#our_area = threed_array[0, 160:200, 360:440]


map_t = plt.imshow(threed_array[130,:,:])
plt.colorbar(map_t)
plt.title('ERA radiation')
plt.show()

map_std = plt.imshow(threed_array.data.std(axis=0))
plt.colorbar(map_std)
plt.title('ERA radiation std')
plt.show()

filtered = np.where(np.isinf(threed_array.data.std(axis = 0)), 0, threed_array.data.std(axis = 0))

minimum_std = np.min(threed_array.data.std(axis = 0)[np.nonzero(threed_array.data.std(axis = 0))])

plt.hist(filtered.reshape(40*80), bins = 50)
plt.title('ERA radiation std histogram')
plt.show()

print(np.where(threed_array.data.std(axis=0) == minimum_std))

low_std = threed_array.data.std(axis = 0)[np.nonzero(threed_array.data.std(axis = 0) < 30)]
print(np.where(threed_array.data.std(axis=0) == low_std[0]))

plt.plot(threed_array[:, 10, 71])
plt.title('CRU precipitation time series (10, 71) std minimum')
plt.show()




# for month in threed_array:
#     print(month.shape)
#     # #
#     month = np.where(month==9.96921e+36, 0, month)
#     fig = plt.figure()
#     cmap = mpl.colors.LinearSegmentedColormap.from_list('my_colormap', ['black', 'white'], 256)
#     img = plt.imshow(month, interpolation='nearest', cmap=cmap, origin='upper')
#     plt.colorbar(img, cmap=cmap)
#     #fig.suptitle(make_fig)
#     plt.xlabel('longitude')
#     plt.ylabel('latitude')
#     #fig.savefig(f'{inpath}{make_fig}.jpg')
#     plt.show()
    ##
    #month_df = pd.DataFrame(threed_array[0,:,:])
    # month_df = month_df.replace(9.96921e+36, 0)
    # #print(month_df)
    # month_df.plot.hist()





