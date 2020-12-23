# modis data --> hdf4 (open w rasterio)

# Import packages
import os
import re  # regular expressions
import warnings
import matplotlib.pyplot as plt
import numpy as np
import numpy.ma as ma
import rasterio as rio
from rasterio.plot import plotting_extent
import geopandas as gpd
import earthpy as et
import earthpy.plot as ep
import earthpy.spatial as es
import earthpy.mask as em
import pandas as pd
import pyhdf
from pyhdf.SD import SD, SDC
import gdal
# file path
path= 'C:/EVA/THESIS/code/testdata/xml/2000032.tiff'

# # view metadata
# with rio.open(path) as ds:
#  #   print(ds)
#     ds_meta = ds.meta
#print(ds_meta)
#
# with rio.open(path) as ds:
#     crs = ds.read_crs()
#     for name in ds.subdatasets:
#         print(name)
#
#
# EVI = []
# with rio.open(path) as ds:
#     for name in ds.subdatasets:
#         if re.search("EVI", name):
#             with rio.open(name) as subds:
#                 modis_meta = subds.profile
#                 EVI.append(subds.read(1))
#
# EVI_a = np.array(EVI)
# print(EVI_a.shape)

#print(EVI_a[0,1,1])

#print(EVI_a)



# file = SD(path, SDC.READ)
# print(file.info)
# datasets_dic = file.datasets()
#
# for sds in enumerate(datasets_dic.keys()):
#     print(sds)
# EVI = file.get()
#sds_obj = file.select('1 km monthly EVI') # select sds

#EVI = sds_obj.get() # get sds data
#print(EVI)
#print(EVI.shape)

# ds = pd.DataFrame(EVI)
# print(ds)
#
# print(np.where(np.isnan(EVI)))
# ep.plot_bands(np.array(EVI))
# plt.show()

tif = gdal.Open(path)
tifArray = tif.ReadAsArray()

print(tifArray.shape)

ep.plot_bands((tifArray))
plt.show()