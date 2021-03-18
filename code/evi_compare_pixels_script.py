#Script to compare the coordinates of the dataset with the coordinates of the low resolution EVI to find out which
# coordinates are in both

from shutil import copyfile
import pandas as pd
from list_files_in_directory import listcoords_csv

evi_pixels = listcoords_csv("C:/EVA/THESIS/data/EVI_time_series/")
df = pd.read_csv("C:/EVA/THESIS/code/files/low_resolution_grid_coords.csv", header=None)

dataset_pixels = (df[0].astype(str) + ',' + df[1].astype(str)).tolist()
dataset_pixels.sort()
evi_pixels.sort()
print(len(dataset_pixels))
print(len(evi_pixels))
intersection = set(dataset_pixels) & set(evi_pixels)
for coords in intersection:
    print(coords)
    copyfile(f"C:/EVA/THESIS/data/EVI_time_series/evi_{coords}.csv", f"C:/EVA/THESIS/data/EVI_time_series_intersection/evi_{coords}.csv")
