
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

from list_files_in_directory import listcoords_csv

def anomaly_decomposition(inpath, outpath):
    # plot raw data
    for coords in listcoords_csv(inpath):
        print(coords)
        df = pd.read_csv(f"evi_{coords}.csv", header=None, names=['timestamp', 'evi'])
        # plt.plot(df.index, df['evi'])
        # plt.show()


        # 1. detrended = raw data - linear trend
        # linear trend: ordinary least squares ?
        df = df.reset_index()
        features = df.index.to_numpy().reshape(-1, 1)
        lin_reg = LinearRegression().fit(features, df['evi'])
        df['trend'] = lin_reg.predict(features)
        df['detrended'] = df['evi'] - lin_reg.predict(features)
        # plt.plot(df.index, lin_reg.predict(features))
        # plt.show()

        # 2. anomalies = detrended - seasonal cycle
        # seasonal cycle: average of month over all years --> 12 averages (one for each month)
        df['year'] = df['timestamp'].astype(str).str.slice(stop = 4)
        df['month'] = df['timestamp'].astype(str).str.slice(start = 4)
        mapping_dict = {
            '001': 1,
            '032': 2,
            '060': 3,
            '061': 3,
            '092': 4,
            '091': 4,
            '122': 5,
            '121': 5,
            '153': 6,
            '152': 6,
            '183': 7,
            '182': 7,
            '214': 8,
            '213': 8,
            '245': 9,
            '244': 9,
            '275': 10,
            '274': 10,
            '306': 11,
            '305': 11,
            '336': 12,
            '335': 12
        }
        df['month'] = df['month'].map(mapping_dict)
        monthly_avg = df.groupby('month').mean()['detrended']
        df = df.join(monthly_avg, on='month', rsuffix='_avg')
        df['anomaly'] = df['detrended'] - df['detrended_avg']

        cols = ['timestamp', 'year', 'month', 'evi', 'trend', 'detrended', 'detrended_avg', 'anomaly']
        df = df[cols]
        df.to_csv(outpath + f"evi_anom_{coords}.csv", header=None, index=None)
        # plt.plot(df.index, df['anomaly'])
        # plt.show()
