import os
import glob
import re
import numpy as np
import shutil

#dir = "E:/Thesis/data/large_dataset/var/www/html/satex/data_per_pix"
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
            file_names.append(file)  # Add it to the list.
    return file_names

# Run the above function and store its results in a variable.
names_coords = get_filenamescoords(dir, -10, 10, -10, 10)

print(np.shape(names_coords))

#os.chdir(dir)

#for file in names_coords:
#    shutil.copy(file, "E:\Thesis\var\www\html\satex\data_per_pix\Africa_1010_1010")
