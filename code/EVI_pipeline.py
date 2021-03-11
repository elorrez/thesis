# This pipeline does the pre-processing of the EO data to the data format we need

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
# There is 1 datafile per month. We are interested in data from 2000 till 2021. So 21 years x 12 months = 252 timestamps
# In total we have 8 tiles x 251 timestamps = 2008 snapshots (=hdf files).
#
# FILE: Read_HDFMetadata.py
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

# 2. Create mosaic for every month
# FILES: EVI_mosaic.py, EVI_listfiles.py
#
# We make a mosaic of the 8 tiles at every timestamp with 3 layers:
# - pixel reliability
# - EVI
# - VI Quality
# The output files are .tiff files
# The name of the new files is the same timestamp as the raw hdf files e.g. 2000032.tiff
# So we create 251 .tiff files and 251 .xml files with metadata

from EVI_mosaic import EVI_mosaic

inpath = "C:/EVA/THESIS/data/EVI/"
outpath = "C:/EVA/THESIS/data/EVI_mosaic/"

error = EVI_mosaic(inpath, outpath)

# 3. Quality control
# FILES: quality_control.py, EVI_listfiles.py
#
# We control the EVI value for the pixel quality by applying following process (see: C:/EVA/THESIS/AppEEARS_NC_QualityFiltering_Python_xjLPKVr.html):
# Import the lookup table (a csv file  from an AppEEARS request, value refers to the pixel values of the VI quality
# layer, followed by the specific bit)( AppEEARS decodes each binary quality bit-field into more meaningful
# information for the user.)
# Select the parameters and conditions you want the quality of the data to meet. In this case:
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

from quality_control import mask_EVI

inpath = "C:/EVA/THESIS/data/EVI_mosaic/"
outpath = "C:/EVA/THESIS/data/EVI_quality_controlled/"
outpath_masks = "C:/EVA/THESIS/data/quality_masks/"
lookup_csv = 'C:/EVA/THESIS/Code/files/MOD13A3-006-1-km-monthly-VI-Quality-lookup.csv'

mask_EVI(lookup_csv, inpath, outpath, outpath_masks)

# 4. Lower resolution
# FILES: Lower_Resolution.py, EVI_listfiles.py
#
# The original dataset from the phd with all the climate variables has a spatial resolution of 1°. The EVI data has a
# spatial resolution of 1 km. To fit the EVI data into the original dataset we have to lower the resolution. To do this,
# we made an empty grid with the right dimensions (20, 40), which is degrees. Then, we divided the image in submatrices of the right size
# (kernel: 120 x 120). For each submatrix we calculated the mean of the values > 0 (important!) and filled this value in
# the empty 20x40 grid. The output files have names e.g. 2000032_lr.tiff and are in the folder 'EVI_low_resolution'

from Lower_Resolution import lower_resolution

inpath = "C:/EVA/THESIS/data/EVI_quality_controlled/"
outpath = "C:/EVA/THESIS/data/EVI_low_resolution/"

lower_resolution(inpath, outpath)

# 5. Create time series per pixel
# FILES: create_time_series.py, EVI_listfiles.py, compare_pixels_script.py
#
# The final dataset consists out of one time series per pixel (csv file). To merge the EVI into this dataset, we
# create a time series for the EVI for each pixel. We make an artificial coordinate system of lat: -10 to 10 and
# lon: 0 to 40 (isn't completely right, but okay). We end up with 800 csv files (800 pixels = 40*20) with each 251 rows
# (= # of months) and two collumns: timestamp and EVI. The output has name e.g. evi_0.5,0.5.csv in
# folder: EVI_time_series
#
# WRONG: we are not working with the original dataset anymore (The original dataset only has 562 pixels in this area
# (lat: -10, 10, lon: 0, 40.6). To end up with the same pixels,
# we take the intersection of both lists with coordinates. In the end 551 pixels are in both datasets. We copy the
# csv files with the right coordinates to another folder: EVI_time_series_intersection)

# inpath = "C:/EVA/THESIS/data/EVI_low_resolution/"
# outpath = "C:/EVA/THESIS/data/EVI_time_series/"

# 6. Anomaly decomposition
# FILES: anomaly_decomposition.py
#
# We want to work with the anomalies, to do this we need to subtract the linear trend and seasonal cycle from the
# raw data. These will be stored in the csv files as collumns

from anomaly_decomposition import anomaly_decomposition

inpath = 'C:/EVA/THESIS/data/EVI_time_series/'
outpath = 'C:/EVA/THESIS/data/EVI_anomaly_time_series/'

anomaly_decomposition(inpath, outpath)
