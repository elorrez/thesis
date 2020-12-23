from EVI_mosaic import EVI_mosaic
from pymodis.convertmodis_gdal import createMosaicGDAL
from EVI_mosaic import EVI_timestamps
from EVI_listfiles import listfilepaths

path = "C:/EVA/THESIS/code/testdata/testimes/"

# subset = "0 1 0 0 0 0 0 0 0 0 0"
#
# files = listfilepaths(path)
# print(files)
#
# ms = createMosaicGDAL(files, subset, outformat='GTiff')   # subset : MOD_Grid_monthly_1km_VI:1 km monthly EVI
# print(ms)
# ms.run("2000032.tiff")

EVI_mosaic(path)