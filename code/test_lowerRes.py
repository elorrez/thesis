import gdal
from osgeo import gdal_array
import numpy as np
import numpy.ma as ma
import earthpy.plot as ep
import matplotlib.pyplot as plt

path1km = "C:/EVA/THESIS/code/testdata/tiff/2000032.tiff"
path1deg = "C:/EVA/THESIS/code/testdata/test_1deg.tiff"

# inDs = gdal.Open(path1km)
# outDs = gdal.Warp(path1deg, inDs,
#                   format = 'GTiff',
#                   xRes = 111320, yRes = 111320,
#                   resampleAlg = gdal.GRA_Average)
# inDs = None
# outDs = None

ds1km = gdal.Open(path1km)
print("1km: ")
print("XSize: ",ds1km.RasterXSize)
print("YSize: ",ds1km.RasterYSize)
EVI = ds1km.GetRasterBand(1)
nodata = EVI.GetNoDataValue()
ds1km = None

ds1deg = gdal.Open(path1deg)
print("1deg: ")
print("XSize: ",ds1deg.RasterXSize)
print("YSize: ",ds1deg.RasterYSize)
ds1deg = None

print('Nodata: ', nodata)

ar1km = gdal_array.LoadFile(path1km)
print('shape 1km: ', np.shape(ar1km))
ar1km = ma.masked_equal(ar1km,nodata)
print("minimum km: ",ar1km.min())
print('not nodata pxls: ',np.count_nonzero(~np.isnan(ar1km)))
print('nodata pxls: ',np.count_nonzero(np.isnan(ar1km)))

ar1deg = gdal_array.LoadFile(path1deg)
print('shape 1deg: ', np.shape(ar1deg))
ar1deg = ma.masked_equal(ar1deg,nodata)
print("minimum deg: ",ar1deg.min())
print('not nodata pxls: ',np.count_nonzero(~np.isnan(ar1deg)))
print('nodata pxls: ',np.count_nonzero(np.isnan(ar1deg)))