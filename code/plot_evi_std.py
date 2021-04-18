# EVI quick plot
import rasterio as rio
import matplotlib.pyplot as plt

in_path = "C:/EVA/THESIS/data/EVI/low_resolution/2000032_lr.tiff"

with rio.open(in_path) as ds:
    print(ds)
    evi = ds.read(1)
    plt.imshow(evi)
    plt.show()


