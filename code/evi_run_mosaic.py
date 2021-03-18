from evi_mosaic import EVI_mosaic
from pymodis.convertmodis_gdal import createMosaicGDAL
from evi_mosaic import EVI_timestamps
from evi_mosaic import listfilepaths
import glob
import re
import os

inpath = "C:/EVA/THESIS/data/EVI/"
outpath = "C:/EVA/THESIS/data/tiff_tweedekans/"

# allhdf = listfilepaths(path)
#
# alltiff = []
# for file in glob.glob("*.tiff"):
#     time = re.split(".tiff",file)[0]
#     alltiffi = [i for i in allhdf if time in i]
#     alltiff.append(alltiffi[0])
#
# print(type(alltiff))
# #print(allhdf)
# #print(alltiff)
# todo =list(set(allhdf).difference(alltiff))
# print(len(todo))
# print(len(list(set(todo))))
# # subset = "0 1 0 0 0 0 0 0 0 0 0"
# #
# # files = listfilepaths(path)
# # print(files)
# #
# # ms = createMosaicGDAL(files, subset, outformat='GTiff')   # subset : MOD_Grid_monthly_1km_VI:1 km monthly EVI
# # print(ms)
# # ms.run("2000032.tiff")
# p,t =EVI_timestamps(todo)
# print(t)
error = EVI_mosaic(inpath, outpath)

print(error)