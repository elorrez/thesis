import pandas as pd
import csv
import numpy as np

from list_files_in_directory import listfilenames_csv
from analysis_GC_script import run_GC_script

inpath = "C:/EVA/THESIS/data/full_datasets/"
# #outpath = "C:/EVA/THESIS/data/analyse_test1/"
#
df = pd.read_csv(inpath + listfilenames_csv(inpath)[10], header=0)
# print(df.columns)
data = df.values

X = data[:, 2:data.shape[1] - 1]  # exclude the first column because it is the timestamp column
y = data[:, data.shape[1] - 1]  # the target variable is the last column
print(X)
print(y)

def write_ouput_analysis(inpath, outpath):
    for file in listfilenames_csv(inpath):
        linear_result = run_GC_script(file, 'linear')
        nonlinear_result = run_GC_script(file, 'non-linear')
        latitude = file.split(',')[0]
        longitude = file.split(',')[1].split('.csv')[0]

        print(latitude, longitude)
        print(linear_result)
        print(nonlinear_result)

        with open(outpath+latitude+','+longitude + '.csv' , 'w', newline='') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow([float(latitude), float(longitude), linear_result[0],linear_result[1],linear_result[2], nonlinear_result[0], nonlinear_result[1], nonlinear_result[2]])

#write_ouput_analysis(inpath,outpath)