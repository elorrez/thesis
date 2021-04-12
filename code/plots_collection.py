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

# 3 DIAGNOSTIC PLOTS

# easy ay to plot data (quick but ugly): pandas has a function : dataframe.plot(kind, figsize, title, bins, xlim, ylim)
# - kind: hist, bar, barh, scatter, area, kde, line, box, hexbin, pie
# - figsize expects a tuple (e.g., figsize=(12,8)
# - title: Title of the plot (string)
# -  x/ y : name of the axis (string)
# - bins: Allows overriding the bin width for histograms. bins expects a list or listlike sequence of values
#   (e.g., bins=np.arange(2,8,0.25))
#   - xlim and ylim expect a tuple (e.g., xlim=(0,5))

# SEABORN: pretty plots
#
# sns.reset_defaults()
# sns.set(
#     rc={'figure.figsize':(7,5)},
#     style="white" # nicer layout
# )
# sns.scatterplot(data= ..., x="", y= "")
# options: scatterplot, lineplot, barplot,
#
# Can be used in combinastion ith subplots from mpl:
# plt.subplot(1, 2, 1)
# sns.countplot(x='carat', data=diamonds_data)

# layout:
# sns.set_style("darkgrid"), Options: darkgrid, whitegrid, dark, white, and ticks

# to plot, use: sns. despine()

# Plotly: cool plots
# change over time:
# fig = px.choropleth(
#     data,
#     locations="ISO3",
#     color="",
#     hover_name="",
#     animation_frame="")
# fig.show()