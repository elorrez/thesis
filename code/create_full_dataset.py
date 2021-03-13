# Add the different climate variables and the EVI together in a full dataset per pixel
import pandas as pd

from EVI_listfiles import listfilenames_csv
from EVI_listfiles import listcoords_csv

def create_full_datset(outpath):
    in_EVI = "C:/EVA/THESIS/data/EVI/anomaly_time_series/"
    in_CRU_HR_tmp = "C:/EVA/THESIS/data/Climate_data/CRU_HR_tmp/time_series_lagged/"
    in_CRU_HR_pre = "C:/EVA/THESIS/data/Climate_data/CRU_HR_pre/time_series_lagged/"
    in_ERA_rad = "C:/EVA/THESIS/data/Climate_data/ERA_rad/time_series_lagged/"
    in_GPCC_pre = "C:/EVA/THESIS/data/Climate_data/GPCC_pre/time_series_lagged/"


    coordinates_list = listcoords_csv(in_EVI)
    list_EVI = listfilenames_csv(in_EVI)
    list_CRU_tmp = listfilenames_csv(in_CRU_HR_tmp)
    list_CRU_pre = listfilenames_csv(in_CRU_HR_pre)
    list_ERA_rad = listfilenames_csv(in_ERA_rad)
    list_GPCC_pre = listfilenames_csv(in_GPCC_pre)

    for coord in range(len(list_EVI)):
        coordinates = coordinates_list[coord]
        EVI = pd.read_csv(in_EVI+list_EVI[coord], names = ['timestamp', 'year', 'month', 'evi', 'trend', 'detrended', 'detrended_avg', 'anomaly'])
        col_drop_EVI = ['timestamp','year','month']
        EVI.drop(col_drop_EVI, axis = 1, inplace=True)
        print(EVI.head())

        CRU_tmp = pd.read_csv(in_CRU_HR_tmp + list_CRU_tmp[coord], header=0)
        CRU_pre = pd.read_csv(in_CRU_HR_pre+list_CRU_pre[coord])
        ERA_rad = pd.read_csv(in_ERA_rad+list_ERA_rad[coord])
        GPCC_pre = pd.read_csv(in_GPCC_pre+list_GPCC_pre[coord], header=0)
        print(GPCC_pre.columns)

        time = CRU_tmp[['timestamp','month']].copy()
        col_drop = ['timestamp','month']
        print(time)
        CRU_tmp.drop(col_drop, axis=1, inplace=True)
        CRU_pre.drop(col_drop, axis=1, inplace=True)
        ERA_rad.drop(col_drop, axis=1, inplace=True)
        GPCC_pre.drop(col_drop, axis=1, inplace=True)

        # Get the right amount of columns: 1/2001 - 8/2019 = 224 rows
        print(f'CRU_tmp: {CRU_tmp.shape}')
        print(f'CRU_pre: {CRU_pre.shape}')
        print(f'ERA_rad: {ERA_rad.shape}')
        print(f'GPCC_pre: {GPCC_pre.shape}')
        print(f'EVI: {EVI.shape}')

        EVI.drop(range(235,251), axis = 0, inplace = True)
        print(f'EVI: {EVI.shape}')
        EVI.drop(range(0,11), axis = 0, inplace = True)
        print(f'EVI: {EVI.shape}')
        CRU_tmp.drop(range(224,228), axis = 0, inplace = True)
        print(f'CRU_tmp: {CRU_tmp.shape}')
        CRU_pre.drop(range(224,228), axis = 0, inplace = True)
        print(f'CRU_pre: {CRU_pre.shape}')
        GPCC_pre.drop(range(224,228), axis = 0, inplace = True)
        print(f'GPCC_pre: {GPCC_pre.shape}')

        df_full = pd.concat([time,CRU_tmp,CRU_pre, ERA_rad,GPCC_pre,EVI], axis=1)
        print(df_full.shape) # (235, 495)

        df_full.to_csv(outpath + f"{coordinates}.csv", index=None)
