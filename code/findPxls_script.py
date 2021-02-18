import os
import glob
import re
import numpy as np
import shutil
import csv
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
            file_names.append(str(lat) +", "+ str(lon))  # Add it to the list.
    return file_names

#Run the above function and store its results in a variable.
# names_coords = get_filenamescoords(dir, -10, 10, 0, 40.6255)
# print(names_coords)
# To copy all the files with these names to another folder:

#os.chdir(dir)
#for file in names_coords:
#    shutil.copy(file, "E:\Thesis\var\www\html\satex\data_per_pix\modisgridEVI")

# write csv with the file names
# with open("C:/EVA/THESIS/code/filenamesGrid.csv", 'w',newline='') as outfile:
#     writer = csv.writer(outfile, delimiter=',')
#     writer.writerows(names_coords)