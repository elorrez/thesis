import pandas as pd
import csv
# Find the pixels with only missing values for the climate variables
# find the NA value for each climate variable
from list_files_in_directory import listfilenames_csv
from list_files_in_directory import listcoords_csv


in_CRU_tmp = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_raw/"
in_CRU_pre = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_raw/"
in_ERA = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_raw/"
in_GPCC = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_raw/"
in_paths = [in_CRU_tmp, in_CRU_pre, in_ERA, in_GPCC]

def find_missing_value(inpath):
    all_na_list = []
    for (coordinate, file) in zip(listcoords_csv(inpath) ,listfilenames_csv(inpath)):
        #var = inpath.split('/')[-3]
        df = pd.read_csv(inpath + file, names = ['timestamp', 'anomaly'])

        if len(df['anomaly'].value_counts()) == 1:

            all_na_list.append(coordinate)
            #print(df[var].value_counts())
    return all_na_list
#
# for path in in_paths:
#     var = path.split('/')[-3]
#     all_na_list = find_missing_value(path)
#     print(f" {var}:{len(all_na_list)}")
#     with open(f"C:/EVA/THESIS/code/files/{var}_na_values_pixels_list.csv", 'w+') as na_values_pixels_list:
#         writer = csv.writer(na_values_pixels_list, delimiter=';')
#         writer.writerow(all_na_list)





