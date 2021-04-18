import pandas as pd
import numpy as np
import rasterio as rio
from list_files_in_directory import listfilepaths_tiff

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

def make_qualityMask(lookup_csv):
    # Read in the look up table
    quality_lookup = pd.read_csv(lookup_csv)

    # Include good quality based on MODLAND
    modland = ['VI produced, good quality', 'VI produced, but check other QA']
    quality_lookup = quality_lookup[quality_lookup['MODLAND'].isin(modland)]

    # Exclude lower quality VI usefulness
    VIU =["Lowest quality","Quality so low that it is not useful","L1B data faulty","Not useful for any other reason\/not processed"]
    quality_lookup = quality_lookup[~quality_lookup['VI Usefulness'].isin(VIU)]

    # Include low or average aerosol
    AQ = ['Low','Average']
    quality_lookup = quality_lookup[quality_lookup['Aerosol Quantity'].isin(AQ)]

    # Include where adjacent cloud, mixed clouds, or possible shadow were not detected
    quality_lookup = quality_lookup[quality_lookup['Adjacent cloud detected'] == 'No' ]
    quality_lookup = quality_lookup[quality_lookup['Mixed Clouds'] == 'No' ]
    quality_lookup = quality_lookup[quality_lookup['Possible shadow'] == 'No' ]

    # Print list of possible QA values based on parameters above
    quality_mask = list(quality_lookup['Value'])
    return quality_mask

def mask_EVI(lookup_csv, inpath, outpath, outpath_masks):
    paths = listfilepaths_tiff(inpath)
    # print(paths)
    quality_mask = make_qualityMask(lookup_csv)

    quality_log = []

    for path in paths:
        with rio.open(path) as ds:
            evi = ds.read(1)
            quality = ds.read(2)

            # Apply QA mask to the EVI data
            mask = np.isin(quality, quality_mask, invert=True)
            evi_masked = np.ma.masked_where(mask, evi)

            # Write new .tiff file from masked output
            name_oldtiff = path.split('/')[-1].split('.')[0]
            path_newtiff = outpath + name_oldtiff + '_qc.tiff'

            # Register GDAL format drivers and configuration options with a
            # context manager.
            with rio.Env():
                # Write an array as a raster band.
                # For the new file's profile, we start with the profile of the source
                profile = ds.profile

                # And then change the band count to 1, set the
                profile.update(count=1)

                with rio.open(path_newtiff, 'w', **profile) as dst:
                    dst.write(evi_masked, 1)

            # Write mask as .tiff
            mask_name =  outpath_masks + name_oldtiff + '_mask.tiff'
            with rio.Env():
                # Write an array as a raster band.
                # For the new file's profile, we start with the profile of the source
                profile = ds.profile

                # And then change the band count to 1, set the
                profile.update(count=1)

                with rio.open(mask_name, 'w', **profile) as dst:
                    dst.write(mask.astype(rio.int16) * 10000, 1)

            # Write quality to csv (timestamp, # of good pixels, # of bad pixels, #of nodatapixels before qc)
            good_pixels = np.sum(~mask)
            bad_pixels = np.sum(mask)
            print(path.split('/')[-1].split('.')[0])
            print(f"Quality control:")
            print(f"Good pixels: {good_pixels} ({good_pixels / (good_pixels + bad_pixels)} %)")
            print(f"Bad pixels:  {bad_pixels} ({bad_pixels / (good_pixels + bad_pixels)} %)")

            nodata_pixels = (evi < 0).sum()
            total_pixels = 2400*4800
            print(f"NoData pixels (< 0): {nodata_pixels} ({nodata_pixels / total_pixels} %) ")
            quality_log.append(f"{name_oldtiff}, {good_pixels}, {bad_pixels}, {nodata_pixels} \n")


    # Write quality to csv
    with open("C:/EVA/THESIS/code/files/mosaics_quality.csv", 'w+') as quality_log_file:
        quality_log_file.writelines(quality_log)