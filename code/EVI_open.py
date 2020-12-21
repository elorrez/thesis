# Open a hdf mosaic file and store the values in an array

from EVI_listfiles import listfilepaths
import re
import rasterio as rio
import numpy as np

def EVI_hdf2array(directory):
    paths = listfilepaths(directory)
    EVI = []
    for path in paths:
        with rio.open(path) as ds:
            for name in ds.subdatasets:
                if re.search("EVI", name):
                    with rio.open(name) as subds:
                        modis_meta = subds.profile
                        EVI.append(subds.read(1))
    return np.array(EVI)


