import matplotlib.pyplot as plt
import matplotlib as mpl
import netCDF4 as nc
from list_files_in_directory import listfilepaths_nc
import numpy as np

inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/cru_ts4.04.2011.2019.pre.dat.nc"

ds = nc.Dataset(inpath)
threed_array = np.flip(ds['pre'][:,160:200, 360:440], axis=1)

map_t = plt.imshow(threed_array[0,:,:])
plt.colorbar(map_t)
plt.title('CRU_HR_pre')
plt.show()

map_std = plt.imshow(threed_array.data.std(axis=0))
plt.colorbar(map_std)
plt.title('CRU_HR_pre std')
plt.show()

(unique, counts) = np.unique(threed_array, return_counts=True, axis=0)
print(unique.shape)
exit()
map_unique = plt.imshow(counts)
plt.colorbar(map_unique)
plt.title('CRU_HR_pre mean')
plt.show()

filtered = np.where(np.isinf(threed_array.data.std(axis = 0)), 0, threed_array.data.std(axis = 0))

minimum_std = np.min(threed_array.data.std(axis = 0)[np.nonzero(threed_array.data.std(axis = 0))])

plt.hist(filtered.reshape(40*80), bins = 50)
plt.title('CRU_HR_pre std histogram')
plt.show()

print(np.where(threed_array.data.std(axis=0) == minimum_std))

plt.plot(threed_array[:, 20,55])
plt.title('CRU precipitation time series (20,55) std minimum')
plt.show()