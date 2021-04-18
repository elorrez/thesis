# This pipeline does the pre-processing of the EVI data to the data format we need

# 1. Get the data
#
# ESA website -> C:/EVA/THESIS/data/EVI/
# A Bash script downloads all the raw hdf files from the ESA website to our local computer.
# Each hdf file contains data from a big tile of 1200x1200 km. The resolution is 1 pixel / km. So 1200x1200 px.
# The name of each hdf file consists of following elements (seperated by a dot):
# - Product name: always "MOD13A3"
# - Date (e.g. "2000032"): year + day of the year (3 numbers)
# - Tile (e.g. h18v09): coordinates of the tile
# - Unknown number, always 006
# - Unknown date
# We are only interested in the data from central Africa so we download the data for 8 tiles: h18 - h21, v08 & v09
# There is 1 datafile per month. We are interested in data from 2000 untill 2021. So 21 years x 12 months = 252 timestamps,
# januari 2000 is missing. So in total 251 timestamps.
# In total we have 8 tiles x 251 timestamps = 2008 snapshots (=hdf files).
#
# FILE: evi_read_hdf_metadata.py
#
# Every hdf file is also accompanied by an xml file with metadata.
# Every hdf file consists of several layers:
# - NDVI
# - relative azimuth angle
# - pixel reliability
# - EVI
# - VI Quality
# - red reflectance
# - NIR reflectance
# - blue reflectance
# - MIR reflectance
# - view zenith angle
# - sun zenith angle

# the EVI values have been multiplied with 10000 so we don't have to work with float values.

# 2. Create mosaic for every month
# FILES: evi_mosaic.py, list_files_in_directory.py
#
# We make a mosaic of the 8 tiles at every timestamp, making a map of the complete extent of our study area:
# latitude -10,10 and longitude 0,40 with 3 layers:
# - pixel reliability
# - EVI
# - VI Quality
# The output files are .tiff files
# The name of the new files is the same timestamp as the raw hdf files e.g. 2000032.tiff
# So we create 251 .tiff files and 251 .xml files with metadata

from evi_mosaic import EVI_mosaic

inpath = "C:/EVA/THESIS/data/EVI/raw"
outpath = "C:/EVA/THESIS/data/EVI/mosaic/"

error = EVI_mosaic(inpath, outpath)

# 3. Quality control
# FILES: evi_quality_control.py, list_files_in_directory.py
#
# We control the EVI value for the pixel quality by applying following process
# (see: C:/EVA/THESIS/code/files/AppEEARS_NC_QualityFiltering_Python_xjLPKVr.html):
# Import the lookup table (a csv file  from an AppEEARS request, value refers to the pixel values of the VI quality
# layer, followed by the specific bit)( AppEEARS decodes each binary quality bit-field into more meaningful
# information for the user.)
# Select the parameters and conditions you want the quality of the data to meet. In this case we use the ones suggested
# in the linked document:
# 1. MODLAND_QA flag = 0 or 1
#     0 = good quality
#     1 = check other QA
# 2. VI usefulness <= 11
#     0000    Highest quality = 0
#     0001    Lower quality = 1
#     0010    Decreasing quality = 2
#     ...
#     1011   Decreasing quality = 11
# 3. Adjacent cloud detected, Mixed Clouds, and Possible shadow = 0
#     0 = No
# 4. Aerosol Quantity = 1 or 2
#     1 = low aerosol
#     2 = average aerosol
# Then, the remaining quality values are made into a mask. The EVI data is filtered with the mask, only the pixels with
# the right values in the quality layer will remain in the EVI layer.
# For every initial .tiff we also made a tiff from the mask layer. This helps us to visualize the low quality pixels.
# These files are stored in the folder "outpath_masks" with names like eg: 2000032_mask.tiff
# We also write a csv file with 4 cols "mosaics_quality.csv":
# - timestamp
# - amount of good pixels (pixels that get false label in masked EVI)
# - amount of bad pixels (pixels that get true label in masked EVI)
# - amount of NoData pixels in the EVI layer

from evi_quality_control import mask_EVI

inpath = "C:/EVA/THESIS/data/EVI/mosaic/"
outpath = "C:/EVA/THESIS/data/EVI/quality_controlled/"
outpath_masks = "C:/EVA/THESIS/data/EVI/quality_masks/"
lookup_csv = 'C:/EVA/THESIS/Code/files/MOD13A3-006-1-km-monthly-VI-Quality-lookup.csv'

mask_EVI(lookup_csv, inpath, outpath, outpath_masks)

# 4. Lower resolution
# FILES: evi_lower_resolution.py, list_files_in_directory.py
#
# The evi data has a spatial resolution of 1 km. To combine it with the climate data in one dataset, we need to lower
# the resolution to 1°. To do this we made an empty grid with the right dimensions (20, 40), (1° resolution).
# Then, we divided the image in submatrices of the right size (kernel: 120 x 120). For each submatrix we calculated the
# mean of the values > 0 (important!) and filled this value in the empty 20x40 grid.
# The output files have names e.g. 2000032_lr.tiff and are in the folder 'EVI/low_resolution'

from evi_lower_resolution import lower_resolution

inpath = "C:/EVA/THESIS/data/EVI/quality_controlled/"
outpath = "C:/EVA/THESIS/data/EVI/low_resolution/"

lower_resolution(inpath, outpath)

# 5. Create time series per pixel
# FILES: evi_create_time_series.py, list_files_in_directory.py
#
# The final dataset consists out of one time series per pixel (csv file). To merge the EVI into this dataset, we
# create a time series for each pixel. We make an artificial coordinate system of lat: -10 to 10 and
# lon: 0 to 40 (isn't completely right, but okay). We end up with 800 csv files (800 pixels = 40*20) with each 251 rows
# (= # of months) and two columns: timestamp and EVI.
# The output has name e.g. evi_0.5,0.5.csv in folder: EVI/time_series

from evi_create_time_series import create_time_series

inpath = "C:/EVA/THESIS/data/EVI/low_resolution/"
outpath = "C:/EVA/THESIS/data/EVI/time_series/"
create_time_series(inpath, outpath)

# INBETWEEN: MISSING VALUES
# FILE: evi_missing_values.py

# find out which pixels have only nan values, these are the pixels where there is water and there is no EVI value:
from evi_missing_values import find_na_pixels
inpath = "C:/EVA/THESIS/data/EVI/time_series/"
all_na_values = find_na_pixels(inpath)

# In other pixels there are no time stamps with NAN values

# move the files of pixels with only na values to the folder "C:/EVA/THESIS/data/EVI/na_pixels"
# (I could also actually just delete them, but just to be sure)
from evi_missing_values import move_to_na_folder
inpath = "C:/EVA/THESIS/data/EVI/time_series/"
outpath = "C:/EVA/THESIS/data/EVI/na_pixels/"
move_to_na_folder(inpath,outpath, "C:/EVA/THESIS/code/files/evi_na_values_pixels_list.csv")

# now, there are only 657 files ( = pixels left)

# evi_missing_values. py : make list with the missing values + make files with the right names to plot the output.
# In the rest of the analysis we will exclude the files of which all values are NA, the coordinates of these pixels can
# be found in the file: "C:/EVA/THESIS/code/files/evi_na_values_pixels_list.csv"
# to plot the output of the analysis, we still need to fill in the gaps that have been made by excluding these pixels
# tot do so, we make 143 csv files with the right names (coordinates of the file) with 8 cols (all = 0)
from evi_missing_values import make_empty_output
make_empty_output(all_na_values)

# 6. Anomaly decomposition
# FILES: evi_anomaly_decomposition.py
#
# We want to do the analysis on anomalies of evi, not on the raw data. The anomalies are calculated in the following way:
# 1: Subtract long term trend from the raw data: detrended = raw - trend
# 2: Subtract the seasonal cycle from the detrended data: anomaly = detrended - seasonal
# The long term trend is a linear function with time as x
# The seasonal cycle is the average per month over the years.
# The output is a csv file with the following columns:
# - 'timestamp'
# - 'year'
# - 'month'
# - 'evi'
# - 'trend'
# - 'detrended'
# - 'detrended_avg'
# - 'anomaly'

from evi_anomaly_decomposition import anomaly_decomposition

inpath = 'C:/EVA/THESIS/data/EVI/time_series/'
outpath = 'C:/EVA/THESIS/data/EVI/anomaly_time_series/'

anomaly_decomposition(inpath, outpath)
