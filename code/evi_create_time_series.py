import rasterio as rio
import numpy as np

from list_files_in_directory import listfilepaths_tiff

inpath = "C:/EVA/THESIS/data/EVI/low_resolution/"
# outpath = "C:/EVA/THESIS/data/EVI/time_series/"

def create_time_series(inpath, outpath):
    paths = listfilepaths_tiff(inpath)

    # for x in range(40):
    #     for y in range(-10, 10):
    #         name = f"evi_{y + 0.5},{x + 0.5}.csv"
    #         with open(outpath + name, 'w+') as f:
    #             f.write("timestamp,evi")

    for path in paths:
        timestamp = path.split('/')[-1].split('_')[0]
        print(timestamp)
        with rio.open(path) as ds:
            evi = ds.read(1)


            for x in range(40):
                for idx, y in enumerate(range(10, -10,-1)):
                    name = f"evi_{y - 0.5},{x + 0.5}.csv"
                    with open(outpath + name, 'a+') as f:
                        f.write(f"{timestamp},{evi[idx][x]}\n")


files = listfilepaths_tiff(inpath)
with rio.open(files[0]) as ds:
    evi = ds.read(1)
    print(evi[15,5])