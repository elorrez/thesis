# Functions to extract netcdf to array and merge 2 time series (2000-2010 and 2011-2019)

import netCDF4 as nc
from EVI_listfiles import listfilepaths_nc
import numpy as np
import matplotlib.pyplot as plt

def lower_resolution_netcdf(path):
    ds = nc.Dataset(path)
    layer = path.split('.')[-3]
    if layer == 'precip':
        ds_resampled = ds[layer][:, 80:100, 180:220]
    else:
        our_area = ds[layer][:, 160:200, 360:440]
        ds_resampled = our_area.reshape(our_area.shape[0], 20, 40, 2, 2).mean(axis=4).mean(axis=3)
    return ds_resampled

def netcdf_to_arraylowres(inpath):
    paths = listfilepaths_nc(inpath)
    lower_res_arrays = []
    for path in paths:
        lower_res_arrays.append(lower_resolution_netcdf(path))
    return np.concatenate(lower_res_arrays, axis=0)

def netcdf_to_array(inpath):
    paths = listfilepaths_nc(inpath)
    print(paths)
    arrays = []
    for path in paths:
        ds = nc.Dataset(path)
        array = ds['ssr'][:,:-1,:-1]
        arrays.append(array)
    return np.concatenate(arrays, axis = 0)

# inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/"
# rad_full_array = netcdf_to_array(inpath)
# print(f"jan 2018: {rad_full_array[205,:,:].mean()}")
# print(f"    2019: {rad_full_array[217,:,:].mean()}")
# print(f"feb 2018: {rad_full_array[206,:,:].mean()}")
# print(f"    2019: {rad_full_array[218,:,:].mean()}")
# print(f"mar 2018: {rad_full_array[207,:,:].mean()}")
# print(f"    2019: {rad_full_array[219,:,:].mean()}")
# print(f"apr 2018: {rad_full_array[208,:,:].mean()}")
# print(f"    2019: {rad_full_array[220,:,:].mean()}")
# print(f"may 2018: {rad_full_array[209,:,:].mean()}")
# print(f"    2019: {rad_full_array[221,:,:].mean()}")
# print(f"jun 2018: {rad_full_array[210,:,:].mean()}")
# print(f"    2019: {rad_full_array[222,:,:].mean()}")
# print(f"aug 2018: {rad_full_array[211,:,:].mean()}")
# print(f"    2019: {rad_full_array[223,:,:].mean()}")
