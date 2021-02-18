import pandas as pd
import numpy as np
import rasterio as rio
from EVI_listfiles import listfilepaths_tiff

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