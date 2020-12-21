import netCDF4 as nc
import numpy as np

path = "C:/EVA/THESIS/code/testdata/NDVI_2006_GIMMS.nc"

ds = nc.Dataset(path)
print(ds)
#print(ds.__dict__)

for dim in ds.dimensions.values():
    print(dim)

print(ds['NDVI'])

print(np.sum(np.isnan(ds['NDVI'][:])))
print(12*360*180)

print(ds['NDVI'][1, 2,38])
