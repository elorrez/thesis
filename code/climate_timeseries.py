import numpy as np
import csv

def time_series_to_csv(in_array, outpath):
    # create the timestamps

    # ERA interim rad: 2001- aug 2019
    # if 'rad' in in_array:
    #     years = [item for sublist in [[2001 + i] * 12 for i in range(18)] for item in sublist] + [i for i in [2019]]*8
    #     months = [i for i in range(1, 13)] * 18 + [i for i in range(1, 9)]
    # else: # CRU and GPCC: 2001-2019
    years = [item for sublist in [[2001 + i] * 12 for i in range(19)] for item in sublist]
    months = [i for i in range(1, 13)] * 19

    # ERA5: 2000-2020
    #years = [item for sublist in [[2000 + i] * 12 for i in range(21)] for item in sublist]
    #months = [i for i in range(1, 13)] * 21

    timestamps = [int(f"{year}{month:02}") for year, month in zip(years, months)]

    for x in range(40):
        for idx, y in enumerate(range(10, -10, -1)):
            print(idx, y)
            name = f"{outpath.split('/')[-3]}_{y - 0.5},{x + 0.5}.csv"
            table = [[a, b] for a, b in zip(timestamps, in_array[:, idx, x].tolist())]

            with open(outpath + name, "w+", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(table)
