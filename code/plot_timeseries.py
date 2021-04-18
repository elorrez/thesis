import numpy as np
from list_files_in_directory import listfilenames_csv
import pandas as pd
import matplotlib.pyplot as plt

inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_anomalies/"
path_zero = "C:/EVA/THESIS/data/empty_output_water_pixels/"

output_array = np.empty([20, 40])
zero_pixels = []
for x in range(40):
    for idx, y in enumerate(range(10, -10, -1)):

        file_names = listfilenames_csv(inpath)
        zero_file_names = listfilenames_csv(path_zero)
        var = inpath.split('/')[-3]

        if f'{var}_anom_{y - 0.5},{x + 0.5}.csv' in file_names:
            path = f'{inpath}{var}_anom_{y - 0.5},{x + 0.5}.csv'
        else:
            path = f'{path_zero}{y - 0.5},{x + 0.5}.csv'

        df = pd.read_csv(path, names = ['timestamp', 'month', var, 'trend', 'detrended', 'detrended_avg', 'anomaly'])
        value = df['anomaly'].std()
        if value == 0:
            zero_pixels.append([y - 0.5, x + 0.5])
                #print(idx, y, x)
        output_array[idx, x] = value

for zero_pixel in zero_pixels:
    print(zero_pixel)