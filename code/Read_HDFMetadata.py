import rasterio as rio
import numpy as np

path = 'C:/EVA/THESIS/code/testdata/hdf/MOD13A3.A2000032.h19v08.006.2015138123529.hdf'

# view metadata
with rio.open(path) as ds:
 #   print(ds)
    ds_meta = ds.meta
    print(ds.profile)
    print(ds.read_crs)
    print(ds.read_transform)
    print(ds)
print(ds_meta)


with rio.open(path) as ds:
    for name in ds.subdatasets:
         print(name)


# with rio.open('HDF4_EOS:EOS_GRID:C:/EVA/THESIS/code/testdata/hdf/MOD13A3.A2000032.h19v08.006.2015138123529.hdf:MOD_Grid_monthly_1km_VI:1 km monthly VI Quality') as quality:
#     data = quality.read(1)
#     print(data)
#     print(np.unique(data))
#
# with rio.open('HDF4_EOS:EOS_GRID:C:/EVA/THESIS/code/testdata/hdf/MOD13A3.A2000032.h19v08.006.2015138123529.hdf:MOD_Grid_monthly_1km_VI:1 km monthly EVI') as evi:
#     data = evi.read(1)
#     print(data)
#
# with rio.open('HDF4_EOS:EOS_GRID:C:/EVA/THESIS/code/testdata/hdf/MOD13A3.A2000032.h19v08.006.2015138123529.hdf:MOD_Grid_monthly_1km_VI:1 km monthly NDVI') as ndvi:
#     data = ndvi.read(1)
#     print(data)
#
# with rio.open('HDF4_EOS:EOS_GRID:C:/EVA/THESIS/code/testdata/hdf/MOD13A3.A2000032.h19v08.006.2015138123529.hdf:MOD_Grid_monthly_1km_VI:1 km monthly pixel reliability') as pixel_reliability:
#     data = pixel_reliability.read(1)
#     print(data)
