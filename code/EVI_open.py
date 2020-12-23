# Open a hdf mosaic file and store the values in an array

from EVI_listfiles import listfilepaths
import re
from pyhdf.SD import SD, SDC
import numpy as np

def EVI_hdf2array(path):
    file = SD(path, SDC.READ)
    sds_obj = file.select('1 km monthly EVI')  # select sds
    EVI = sds_obj.get()
    return EVI


