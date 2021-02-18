# ofen tiff mosaic and find the values of the pixels --> how many pixels are NAN

import gdal
from osgeo import gdal_array
import numpy as np
import numpy.ma as ma
import earthpy.plot as ep
import matplotlib.pyplot as plt

path = "C:/EVA/THESIS/code/testdata/tiff/2000032.tiff"

ds = gdal.Open(path)

#info
print("type: ",type(ds))
print("Projection:", ds.GetProjection())
print("XSize: ",ds.RasterXSize)
print("YSize: ",ds.RasterYSize)
print("Number of bands: ",ds.RasterCount)
print("Metadata: ",ds.GetMetadata())

# get band
band = ds.GetRasterBand(1)
print("band type: ",type(band))
print("type of value: ",gdal.GetDataTypeName(band.DataType))

# band statistics
if band.GetMinimum() is None or band.GetMaximum()is None:
    band.ComputeStatistics(0)
    print("Statistics computed.")

# Fetch metadata for the band
band.GetMetadata()
# Print only selected metadata:
print ("[ NO DATA VALUE ] = ", band.GetNoDataValue()) # none
print ("[ MIN ] = ", band.GetMinimum())
print ("[ MAX ] = ", band.GetMaximum())

# raster as array

rasterArray = ds.ReadAsArray()
print("type array: ", type(rasterArray))

#loading array directly from file with gdal_array
rasterArray = gdal_array.LoadFile(path)
print("minimum: ",rasterArray.min())

# get the nodata value
nodata = band.GetNoDataValue()

#Create a masked array for making calculations with nodata values
rasterArray = ma.masked_equal(rasterArray,nodata)
print(type(rasterArray))

#check again
print("minimum: ",rasterArray.min())

#ep.plot_bands(rasterArray)
#plt.show()

#print(rasterArray)

print(ds.GetGeoTransform())

ds = None
band = None