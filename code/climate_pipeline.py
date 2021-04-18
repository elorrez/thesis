# The predictor variables of our dataset consist of a number of climate variables:
# - temperature (tmp)
# - precipitation (pre)
# - radiation
# Different datasets are used for each of these variables:
# CRU_HR temperature
# CRU_HR precipitation
# GPCC precipiation
# ERA_Interim radiation
# ERA5 temperature
# ERA5 precipitation
# ERA5 surface short wave radiation


# 1. Download data
# CRU: 1°, monthly, 2001-2019
# https://crudata.uea.ac.uk/cru/data/hrg/
# ERA: 1°, monthly, (-10,10 0,40), 2001- aug 2019
# https://apps.ecmwf.int/datasets/data/interim-full-mnth/levtype=sfc/?month_years=2001&time=12:00:00&step=12&param=176.128
# GPCC precipitation: 1°, monthly, global, 2001-2019
# https://opendata.dwd.de/climate_environment/GPCC/html/fulldata-monthly_v2020_doi_download.html
# ERA5: 0.1°, monthly, 2000-2020
# https://cds.climate.copernicus.eu/cdsapp#!/dataset/reanalysis-era5-land-monthly-means?tab=overview
# FILE: download_ERA5.py

# 1. From netcdf to arrays
# FILES: climate_extract_from_netcdf.py, list_files_in_directory.py
#
# The downloaded data is in netcdf format. It can be opened as a dataset with the netcdf4 package. From that dataset the
# right 'layer' can be selected:
# CRU_HR_tmp : 'tmp'
# CRU_HR_pre : 'pre'
# GPCC_pre : 'precip'
# ERA_rad : 'ssr'
# ERA5_tmp : 't2m' (temperature at 2m above surface (K))
# ERA5_pre : 'tp' (total precipitation (m))
# ERA5_ssr : 'ssr'

# These layers have 3 dimensions: time, latitude, longitude. Depending on the dataset, the arrays have to be cropped to
# the right dimensions: time: all --> concatenate different arrays with parts of the time series if needed
# latitude: 10, -10
# longitude: 0,40

# The result is a 3D array for each variable with dimensions:
# CRU tmp and pre: 228, 20, 40
# ERA rad: 224, 20, 40
# GPCC pre: 228
# ERA5 tmp, pre, ssr : 252, 20, 40

from climate_extract_from_netcdf import netcdf_to_arraylowres
# CRU_HR_tmp
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/"
CRU_HR_tmp = netcdf_to_arraylowres(inpath)

# CRU_HR_pre
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/"
CRU_HR_pre = netcdf_to_arraylowres(inpath)

# ERA_rad
from climate_extract_from_netcdf import netcdf_to_array
inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/"
ERA_rad = netcdf_to_array(inpath)

# GPCC_pre
inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/"
GPCC_pre = netcdf_to_arraylowres(inpath)

# ERA5
from climate_extract_from_netcdf import lower_resolution_netcdf_ERA5
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5/adaptor.mars.internal-1618563855.2239437-9920-6-672d4cde-e751-451e-83ff-52fe5a944e16.nc"
#tmp
ERA5_tmp = lower_resolution_netcdf_ERA5(inpath, 't2m')
# precipitation
ERA5_pre = lower_resolution_netcdf_ERA5(inpath, 'tp')
# surface net solar radiation
ERA5_ssr = lower_resolution_netcdf_ERA5(inpath, 'ssr')

# 2. Make a time series for each pxl
# FILES: climate_time_series.py

# From these 3D arrays we make a timeseries for each pixel. There are 20*40 = 800 pixels in total and 228, 224 or 252
# timestamps.

from climate_timeseries import time_series_to_csv
full_arrays = [CRU_HR_tmp, CRU_HR_pre, GPCC_pre, ERA_rad, ERA5_tmp, ERA5_pre, ERA5_ssr]

# CRU_HR_tmp
out_CRU_tmp = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_raw/"
# CRU_HR_pre
out_CRU_pre = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_raw/"
# ERA_rad
out_ERA_rad = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_raw/"
# GPCC_pre
out_GPCC_pre = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_raw/"
#ERA5 tmp
out_ERA5_tmp = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_raw/"
#ERA5 pre
out_ERA5_pre = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_raw/"
#ERA5 ssr
out_ERA5_ssr = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_raw/"

outpaths = [out_CRU_tmp, out_CRU_pre, out_GPCC_pre, out_ERA_rad, out_ERA5_tmp, out_ERA5_pre, out_ERA5_ssr]
for full_array, outpath in zip(full_arrays, outpaths):
    time_series_to_csv(full_array, outpath)

# IN BETWEEN: Check for missing values:
# FILE: climate_missing_values.py

# Which pixels have only missing values?
# EVI NA: 143 pixels with all NA values
# ERA5: ['-0.5,6.5', '-1.5,5.5', '-5.5,11.5', '-8.5,12.5', '-9.5,12.5', '5.5,1.5'] (add these to the NA_pxls file
# and move these pixels to the 'na_pixels' folder for both climate and Evi


# move the pixels that have all NA for evi to another folder (I could just delete them, but just to be sure)
from evi_missing_values import move_to_na_folder
csv_pixels = "C:/EVA/THESIS/code/files/evi_na_values_pixels_list.csv"
#CRU tmp
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/na_pixels/"
move_to_na_folder(inpath, outpath, csv_pixels)

# 3. Anomaly decomposition
# FILES: climate_anomaly_decomposition.py, list_files_in_directory.py
#
# Just like with the EVI we want the anomalies instead of the raw data to perform the analysis
# detrended = raw - trend and anomaly = detrended - seasonal cycle
# add all columns to one dataframe and write as csv

from climate_anomaly_decomposition import climatevar_anomaly_decomposition

# CRU_HR_tmp
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)
# CRU_HR_pre
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)
# ERA_rad
inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)
# GPCC_pre
inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)
# ERA5 tmp
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_anomalies/"
nan_coord = climatevar_anomaly_decomposition(inpath, outpath)
print(nan_coord)
# ERA5 pre
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)
# ERA5 ssr
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_raw/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_anomalies/"
climatevar_anomaly_decomposition(inpath, outpath)

# 4. Calculate lagged and cumulative variables
# FILES: climate_lagged_and_cumulative_vars.py, list_files_in_directory.py
#
# For every variable we have so far we need to add the 12 months lagged values as variables.
# Also, we need to calculate for each month the cumulative value of the previous months, up to 12 months.
# So we need to add 22 variables in total (11 lag and 11 cum)
# names of the variables:
# name_lag_2
# name_lag_3
# ... name_lag_12
# name_cum_2
# name_cum_3
# ... name_cum_12

from climate_lagged_and_cumulative_vars import add_lag_cum_vars

# CRU_HR_tmp
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
# CRU_HR_pre
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
# ERA_rad
inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
# GPCC_pre
inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
# ERA5 tmp
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_tmp/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
# ERA5 pre
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_pre/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)
#ERA5 ssr
inpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_anomalies/"
outpath = "C:/EVA/THESIS/data/Climate_data/ERA5_ssr/time_series_lagged/"
add_lag_cum_vars(inpath, outpath)

# 5. Merge the datasets into 1 dataset per pixel
# FILES: climate_create_full_datasets.py
#
# For each pixel, add the different climate variables and EVI to 1 dataset.
# A problem: not all datasets have the same length
# CRU_HR tmp: 01/2001 - 12/2019 = 12 * 19 = 228
# CRU_HR pre: 01/2001 - 12/2019 = 12 * 19 = 228
# ERA: 01/2001 - 08/2019 = 12 * 9 -4 = 224
# GPCC: 01/2001 - 12/2019 = 12 * 19 = 228
# EVI: 02/2000 - 12/2020 = 12 * 21 -1 = 251
# ERA5: 2000 - 12/2020 = 252
# Totaal: 01/2001 - 08/2019
# The first 12 months should be left out because of the lagged and cumulative variables


from climate_create_full_dataset import create_full_datset
outpath = "C:/EVA/THESIS/data/full_datasets_ERA5/"

from climate_create_full_dataset import create_full_datset
create_full_datset(outpath)
