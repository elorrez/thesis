# Change the resolution of the images from 1kmx1km to 1°x1°

from EVI_open import EVI_hdf2array
from EVI_listfiles import listfilepaths

def lowerRes(directory):
    paths = listfilepaths(directory)
    for path in paths:
        EVI = EVI_hdf2array(path)
