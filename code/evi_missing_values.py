import pandas as pd
import csv
import shutil
# How to handle missing values in this dataset?
# EVI missing value fill in values = -3000
# on spatial resolution there are pixels for which every timestamp is NA e.g. water
# there are also some timestamps with NA values.

# We will handle these two differently:
# - the pixels with NA for each timestamp will be removed from the dataset (make list with the coordinate names for later)
# - random timestamps with NA will be interpolated with the mean of all the timestamps of the pixel.

from list_files_in_directory import listfilenames_csv
from list_files_in_directory import listcoords_csv

# Find out which pixels have NA value for each timestep:
# And write csv file with pixels that we won't use in the analysis.
#inpath = "C:/EVA/THESIS/data/EVI/time_series/"

def find_na_pixels(inpath):
    all_na_list = []
    some_na_list = []
    for (coordinate, file) in zip(listcoords_csv(inpath) ,listfilenames_csv(inpath)):
        df = pd.read_csv(inpath + file, names = ['timestamp', 'evi'])

        if all(df['evi']==-3000):
            all_na_list.append(coordinate)

    # print(len(all_na_list)) 143 pixels with all NA values
            with open("C:/EVA/THESIS/code/files/evi_na_values_pixels_list.csv", 'w+') as evi_na_values_pixels_list:
                    writer = csv.writer(evi_na_values_pixels_list, delimiter = ';')
                    writer.writerow(all_na_list)

        else:
            some_na_list.append(sum(df['evi']==-3000))
    return all_na_list

#print(len(all_na_list))
# In the other pixels there are no missing values

# Make the csv files with 0 values to plot the output:

def make_empty_output(coordinate_list):
    output_zeros = [i for i in range(0,1)]*8
    for coordinate in coordinate_list:
        with open(f"C:/EVA/THESIS/data/EVI/empty_output_water_pixels/{coordinate}.csv", 'w+') as pixel_zeros:
            writer = csv.writer(pixel_zeros)
            writer.writerow(output_zeros)

# Move the files of pixels with all NA values to a subfolder :

# from C:/EVA/THESIS/data/EVI/time_series to C:/EVA/THESIS/data/EVI/time_series/na_pixels
def move_to_na_folder(inpath, outpath, csv_coordinates):
    if 'EVI' in inpath:
        var = 'evi'
    else:
        var = inpath.split('/')[-3]
        #var = f"{name}_lag"

    with open(csv_coordinates) as r:
        coordinates=(list(csv.reader(r,delimiter = ';')))
    for coordinate in coordinates[0]:
        file = f"{var}_{coordinate}.csv"
        shutil.move(inpath+file, outpath+file)

