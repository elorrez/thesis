# Make a mosaic of all tiles from the same timestamp

from EVI_listfiles import listfilepaths
import re
import numpy as np
from pymodis.convertmodis_gdal import createMosaicGDAL

def EVI_timestamps(inpath): #or directory
    # This function makes a list with all the unique timestamps in the names of the hdf files.
    # for the path "folder/MOD13A3.A2020306.h10v08.006.2020338061338.hdf" it will select "2020306"

    paths = listfilepaths(inpath) # make list with pathnames of all files in directory
    times = [] # list with for every filename the timestamp
    # loop over files
    for path in paths:
        time = re.split(".h",re.split("MOD13A3.A", path)[1])[0] # for example: MOD13A3.A2020306.h10v08.006.2020338061338.hdf
        times.append(time)
    unique_times = list(set(times)) # make a list with the unique timestamps
    return paths, unique_times

def EVI_mosaic(inpath, outpath):
    # This function makes a mosaic of all hdf tiles for each timestamp
    paths, unique_times = EVI_timestamps(inpath)
    subset = "0 1 1 0 0 0 0 0 0 0 0"
    error =[]
    for time in unique_times:
        timestamp = [i for i in paths if time in i] # select all filenames with the time in the name
        try:
            ms = createMosaicGDAL(timestamp, subset, outformat='GTiff')   # subset : MOD_Grid_monthly_1km_VI:1 km monthly EVI
            ms.run(outpath + time +'.tiff')
            ms.write_mosaic_xml()
        except:
            error.append(timestamp)
    return error

# path="C:/EVA/THESIS/code/testdata/testimes"
# p, t =EVI_timestamps(path)
# print(p)
# print(t)