# SPATIAL interpolation of missing values
import numpy as np
import numpy.ma as ma
from skimage.util.shape import view_as_windows

# input = 3D array
# The result from unpacking the netcdf files is an array for each variable with following dimensions:
# -CRU_tmp: (228, 20, 40)
# -CRU_pre: (228, 20, 40)
# -GPCC_pre: (228, 20, 40)
# -ERA_rad: (224, 20, 40)

from climate_extract_from_netcdf import netcdf_to_arraylowres
#
# inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/"
# full_array = netcdf_to_arraylowres(inpath)
# #print(type(tmp_full_array))
# print(full_array.shape)

def interpolate_missing_values(in_array, missing_val):
    padded_array = np.pad(in_array, pad_width=1,mode='edge')
    for t in range(0, in_array.shape[0]):
        kernel = np.ones((3,3))
        windows = view_as_windows(padded_array[t,:,:], kernel.shape, step = 1)
        print(windows.shape)
        print(in_array[t, :, :].shape)
        for x in range (0,40):
            for y in range(0,20):
                if in_array[t,y,x]==missing_val:
                    #print(layer[y,x])
                    in_array[t,y,x] = np.mean(windows[y,x])
                    #print(layer[y,x])
    return in_array

#out_array = interpolate_missing_values(full_array, 0)

