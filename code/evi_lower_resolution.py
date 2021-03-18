import rasterio as rio
import numpy as np
from skimage.util.shape import view_as_windows

from list_files_in_directory import listfilepaths_tiff

# inpath = "C:/EVA/THESIS/code/testdata/mosaic_quality_controlled/2000032_qc.tiff"

def lower_resolution(inpath, outpath):
    paths = listfilepaths_tiff(inpath)

    for path in paths:
        low_res_grid = np.empty((20, 40))

        with rio.open(path) as ds:
            evi = ds.read(1)

            kernel = np.ones((120, 120))
            sub_matrices = view_as_windows(evi, kernel.shape, kernel.shape)
            # print(sub_matrices)
            # print(np.shape(sub_matrices))

            for x in range(40):
                for y in range(20):
                    teller = np.sum(np.where(sub_matrices[y, x] < 0, 0, sub_matrices[y, x]))
                    noemer = (sub_matrices[y, x] > 0).sum()
                    # print(x, y)
                    # print(teller)
                    # print(noemer)
                    # print('------')
                    low_res_grid[y, x] = teller / noemer

            print(low_res_grid)
            # print(np.shape(low_res_grid))
            low_res_grid = np.where(np.isnan(low_res_grid), -3000, low_res_grid)

            # Write new .tiff file from masked output
            name_oldtiff = path.split('/')[-1].split('.')[0].split('_')[0]
            path_newtiff = outpath + name_oldtiff + '_lr.tiff'

            with rio.Env():
                profile = ds.profile
                profile['width'] = 40
                profile['height'] = 20
                with rio.open(path_newtiff, 'w', **profile) as dst:
                    dst.write(low_res_grid.astype(rio.int16), 1)