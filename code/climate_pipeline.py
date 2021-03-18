# The predictor variables of our dataset consist of a number of climate variables:
# - temperature (tmp)
# - precipitation (pre)
# - radiation

# 1. Download data
# https://crudata.uea.ac.uk/cru/data/hrg/
# ERA: 1°, monthly, (-10,10 0,40), 2001- aug 2019
# https://apps.ecmwf.int/datasets/data/interim-full-mnth/levtype=sfc/?month_years=2001&time=12:00:00&step=12&param=176.128
# GPCC precipitation: 1°, monthly, global, 2001-2019
# https://opendata.dwd.de/climate_environment/GPCC/html/fulldata-monthly_v2020_doi_download.html

# 1. From netcdf to arrays
# FILES: extract_from_netcdf.py
#
# The downloaded data is in netcdf format, to work with it we need to change it to arrays. The netcdf files have 3
# dimensions: time, latitude, longitude (2000-2010: 120, 360, 720 and 2011-2019: 108, 360, 720) The data has global
# coverage, we need a rectangle with coordinates (-10, 10) and (0, 40). In the array we can extract the desired spatial extent.
# After that, we need to lower the resolution (0.5° to 1°). (120, 20, 40 and 108, 20, 40) To complete the time series,
# we concatenate the two series: 228, 20, 40.

from extract_from_netcdf import netcdf_to_arraylowres

# CRU_HR_tmp
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/"
tmp_full_array = netcdf_to_arraylowres(inpath)

# CRU_HR_pre
inpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/"
pre_full_array = netcdf_to_arraylowres(inpath)

# ERA_rad
from extract_from_netcdf import netcdf_to_array
inpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/"
rad_full_array = netcdf_to_array(inpath)

# GPCC_pre
inpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/"
GPCC_pre_full_array = netcdf_to_arraylowres(inpath)

# 2. Make a time series for each pxl
#
# Now we have 1 array with dimensions 228, 20, 40. We want to make one array for each pixel (20*40=800 pixels). With
# rows for each timestamp (=228 rows)

from climate_timeseries import time_series_to_csv
# CRU_HR_tmp
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_raw/"
time_series_to_csv(tmp_full_array, outpath)

# CRU_HR_pre
outpath = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_raw/"
time_series_to_csv(pre_full_array, outpath)

# ERA_rad
outpath = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_raw/"
time_series_to_csv(rad_full_array, outpath)

# GPCC_pre
outpath = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_raw/"
time_series_to_csv(GPCC_pre_full_array, outpath)

# 3. Anomaly decomposition
# FILES: climatevar_anomaly_decomposition.py, EVI_listfiles.py
# detrended = raw - trend and anomaly = detrended - seasonal cycle
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

# 4. Calculate lagged and cumulative variables
# FILES: add_lagged_and_cumulative_vars.py, EVI_listfiles.py
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

# 5. Merge the datasets into 1 dataset per pixel
# FILES:
#
# For each pixel, add the different climate variables and EVI to 1 dataset.
# A problem: not all datasets have the same length
# CRU_HR tmp: 01/2001 - 12/2019 = 12 * 19 = 228
# CRU_HR pre: 01/2001 - 12/2019 = 12 * 19 = 228
# ERA: 01/2001 - 08/2019 = 12 * 9 -4 = 224
# GPCC: 01/2001 - 12/2019 = 12 * 19 = 228
# EVI: 02/2000 - 12/2020 = 12 * 21 -1 = 251
# Totaal: 01/2001 - 08/2019
# De eerste 12 maanden worden weggelaten door de lagged en cumulatieve variabelen
#

from climate_create_full_dataset import create_full_datset
outpath = "C:/EVA/THESIS/data/full_datasets/"
create_full_datset(outpath)



