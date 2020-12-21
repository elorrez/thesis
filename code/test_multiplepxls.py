# TODO: hoe werkt dit met de HPC
# TODO: nadenken wat er daarna met de output moet gebeuren
#Een script om meerdere pixels in 1 keer te berekenen
# input: de namen van de csv bestanden van de gekozen pixels
#        het script 'GC_script'
#        linear / non-linear
# output: voor elke pixel een bestand met 8 waarden
import os
import glob
from GC_script import run_GC_script
import csv
import re

#path = "E:/Thesis/data/data_ts_raw/Africa_1010_1010"
path = "C:/EVA/THESIS/code/testdata/1pxl/"

def get_filepaths(dir):
    file_paths = []
    for root, directories, files in os.walk(dir):
        for file in files:
            file_path =os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def write_outputcsv(og_file, row):
    # make a .csv file with 1 row and 8 columns: lat, lon, np.mean(R_squared_baseline)_nonlin, np.mean(R_squared_full)_lin, GC_dif_lin,
    # np.mean(R_squared_baseline)_nonlin, np.mean(R_squared_full)_nonlin, GC_dif_nonlin
    # the og file looks like this: ../path/lon,lat.csv
    # row is output of GC_script_lin and output of GC_script_nonlin in 1 list
    lat = re.split(',', re.split('/', og_file)[-1])[0]
    lon = re.split(',', re.split('.csv', og_file)[0])[1]
    out = lat + ',' + lon + '_out.csv'
    with open(out, 'w', newline='') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow([float(lat), float(lon)] + row)

def run_GC_script_allpxls(dir):
    # for all files in the directory --> execute GC_script for linear and non-linear
    # write_outputcsv makes a csv file with the output for 1 pixel
    file_names = get_filepaths(dir)
    for file in file_names:
        lin = run_GC_script(file, 'linear')
        nonlin = run_GC_script(file, 'non-linear')
        write_outputcsv(file, lin+nonlin)

run_GC_script_allpxls(path)