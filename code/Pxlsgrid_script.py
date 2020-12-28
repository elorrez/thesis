import os
import glob
import re
import numpy as np
from findPxls_script import get_filenamescoords
import csv

dir = "E:/Thesis/data/data_ts_raw"
names_coords = get_filenamescoords(dir, -10, 10, 0, 40.6255)

print(np.shape(names_coords))
print(names_coords[0])
with open("C:/EVA/THESIS/code/testdata/pxlsgrid.csv", 'w',newline='') as outfile:
     writer = csv.writer(outfile, delimiter = ",")
     for name in names_coords:
         writer.writerow([name])
