# anomaly decomposition for climate variables

import pandas as pd
from sklearn.linear_model import LinearRegression

from list_files_in_directory import listcoords_csv

def climatevar_anomaly_decomposition(inpath, outpath):
    for coords in listcoords_csv(inpath):
        print(coords)
        var = inpath.split('/')[-3]
        df = pd.read_csv(f"{var}_{coords}.csv", header=None, names=['timestamp', var])

        # 1. detrended = raw data - linear trend
        # linear trend: ordinary least squares ?
        df = df.reset_index()
        features = df.index.to_numpy().reshape(-1, 1)
        lin_reg = LinearRegression().fit(features, df[var])
        df['trend'] = lin_reg.predict(features)
        df['detrended'] = df[var] - lin_reg.predict(features)

        # 2. anomalies = detrended - seasonal cycle
        # seasonal cycle: average of month over all years --> 12 averages (one for each month)
        # ERA (4 months missing):
        if 'ERA' in inpath:
            df['month'] = [i for i in range(1, 13)] * 18 + [i for i in range(1, 9)]
        else:
            df['month'] = [i for i in range(1, 13)] * 19

        monthly_avg = df.groupby('month').mean()['detrended']
        df = df.join(monthly_avg, on='month', rsuffix='_avg')
        df['anomaly'] = df['detrended'] - df['detrended_avg']

        # Write to csv
        cols = ['timestamp', 'month', var, 'trend', 'detrended', 'detrended_avg', 'anomaly']
        df = df[cols]
        df.to_csv(outpath + f"{var}_anom_{coords}.csv", header=None, index=None)