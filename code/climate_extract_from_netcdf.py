# Functions to extract netcdf to array and merge 2 time series (2000-2010 and 2011-2019)

import netCDF4 as nc
from list_files_in_directory import listfilepaths_nc
import numpy as np
import matplotlib.pyplot as plt

# CRU_HR and GPCC: need resampling / cropping
def lower_resolution_netcdf(path):
    ds = nc.Dataset(path)
    layer = path.split('.')[-3]
    # GPCC: layer = 'precip'
    # GPCC: global
    if layer == 'precip':
        ds_resampled = ds[layer][:, 80:100, 180:220]
    else:
        # CRU: global, 0.5° resolution
        our_area = np.flip(ds[layer][:, 160:200, 360:440], axis =1)
        ds_resampled = our_area.reshape(our_area.shape[0], 20, 2, 40, 2).mean(axis=4).mean(axis=2)
    return ds_resampled

# CRU and GPCC : concatenate 2 arrays (2000-2010 and 2011-2020) into 1 array
def netcdf_to_arraylowres(inpath):
    paths = listfilepaths_nc(inpath)
    lower_res_arrays = []
    for path in paths:
        lower_res_arrays.append(lower_resolution_netcdf(path))
    return np.concatenate(lower_res_arrays, axis=0)

# ERA5 : need resampling + Temperature is in K --> °C
def lower_resolution_netcdf_ERA5(path, layer):
    ds = nc.Dataset(path)
    if layer == 't2m':
        var = ds[layer][:, :-1, :-1] - 273.15
    else:
        var = ds[layer][:, :-1, :-1]
    ds_resampled = var.reshape(var.shape[0], 20, 10, 40, 10).mean(axis=4).mean(axis=2)
    img =plt.imshow(ds_resampled[0, :, :])
    plt.colorbar(img)
    plt.title(f'ERA5 {layer} low resolution')
    plt.show()
    return ds_resampled

# ERA interim : concatenate arrays into 1 array
def netcdf_to_array(inpath):
    paths = listfilepaths_nc(inpath)
    #print(paths)
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

# inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/"
# paths = listfilepaths_nc(inpath)
#
# ds = nc.Dataset(paths[0])
# print(ds.dimensions)
