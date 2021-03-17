# In this script I collect all plots and visualizations of the data (not the analysis) to be used in the paper afterwards.

# 1. Plot of the climate in Africa compared to the Amazon rainforest
from plot_climate import extent_climatevar_df

inpath_Africa = "C:/EVA/THESIS/data/AFR_SAM_climate_for_plot/AFR/"
inpath_SouthAmerica = "C:/EVA/THESIS/data/AFR_SAM_climate_for_plot/SAM/"

extent_climatevar_df(inpath_Africa, "lat_low", "air_temperature")

# 2. Visualize the EVI time in tim for a couple of pixels. In the first analysis the results didn't make a
# lot of sense and maybe pointed to the fact that the EVI didn't fluctuate enough in time.
# make plots for a couple of pixels with: EVI raw, linear trend, seasonal cylce, anomaly

inpath = "C:/EVA/THESIS/data/EVI/anomaly_time_series/"
coordinates = ["-9.5,25.5", "0.5,20.5", "0.5,26.5", "5.5, 30.5"]