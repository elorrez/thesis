import netCDF4 as nc
import numpy as np

from EVI_listfiles import listfilepaths_nc

# Layers in netcdf : air_temperature , surface_downwelling_shortwave_flux_in_air, precipitation_flux
# dimensions: (366, 71, 161)
# longitude (161): -20 , 60 (step of 0.5)
# latitude (71): -20, 15 (step of 0.5)

# lat_mid<-extent(c(-20.25,60.25,-5,5))
# lat_high<-extent(c(-20.25,60.25,5,15))
# lat_low<-extent(c(-20.25,60.25,-15,-5))

def extent_climatevar_df(inpath, extent, variable):
    arrays = []
    for file in listfilepaths_nc(inpath):
        ds = nc.Dataset(file)
        if extent == "lat_mid":
            ds_resampled = ds[variable][:, 30:51, 0:161]
            arrays.append(ds_resampled)
        elif extent == "lat_high":
            ds_resampled = ds[variable][:,50:70, 0:161]
            arrays.append(ds_resampled)
        elif extent == "lat_low":
            ds_resampled = ds[variable][:, 0:29, 0:161]
            print(ds_resampled.shape)
            arrays.append(ds_resampled)
    array = np.concatenate(arrays, axis =0)
    # (longitude = , latitude = 21/20/29, time = 4018
    print(array.shape)





# Africa


# South-America