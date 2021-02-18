import os
import glob
import re
import numpy as np

dir = "E:/Thesis/data/data_ts_raw"

def get_filenamescoords(directory, latmin, latmax, lonmin, lonmax):
    """
    This function creates a list with all the .csv files in the directory
    that
    """
    os.chdir(directory)
    file_names = []  # List which will store all of the full filepaths.

    # Walk the tree.
    for file in glob.glob("*.csv"):
        lat = float(re.split(',', file)[0])
        lon = float(re.split(',', re.split('.csv', file)[0])[1])
        if latmin<=lat and latmax>=lat and lonmin<=lon and lonmax>=lon:
            file_names.append(str(lat) +", "+ str(lon))  # Add it to the list.
    return file_names

names_coords = get_filenamescoords(dir, -10, 10, 10, 30.4713)

print(np.shape(names_coords))
print(names_coords)

coordinates = []
for name in names_coords:
    lat = float(name.split(',')[0])
    lon = float(name.split(',')[1])
    coordinates.append(f"{lat},{lon} \n")

with open("C:/EVA/THESIS/code/files/low_resolution_grid_coords_center.csv", 'w+') as lowres_coords:
    lowres_coords.writelines(coordinates)
