
import csv

from EVI_listfiles import listfilenames_csv
from GC_script import run_GC_script

# inpath = "C:/EVA/THESIS/data/full_datasets/"
# outpath = "C:/EVA/THESIS/data/analyse_test1/"


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