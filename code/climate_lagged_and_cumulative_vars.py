# add 22 columns to the csv files with lagged and cumulative variables.
import pandas as pd

from list_files_in_directory import listcoords_csv

def create_lagged_vars(df, lag):
    new_dict ={}
    for col_name in df:
        new_dict[col_name] = df[col_name]
        for l in range(1, lag):
            new_dict[f'{col_name}_lag_{l+1}'] = df[col_name].shift(l)
    df_lag = pd.DataFrame(new_dict, index=df.index)
    return df_lag

def create_cum_vars(df,lag):
    new_dict = {}
    for col_name in df:
        new_dict[col_name] = df[col_name]
        for l in range(1,lag):
            new_dict[f'{col_name}_cum_{l+1}'] = df[col_name].shift(1).rolling(l).sum()
    df_cum = pd.DataFrame(new_dict, index=df.index)
    return df_cum

def add_lag_cum_vars(inpath, outpath):
# import the anomaly decomposition time series csv as panda
    for coords in listcoords_csv(inpath):
        print(coords)
        var = inpath.split('/')[-3]
        df = pd.read_csv(f"{var}_anom_{coords}.csv", header=None, names=['timestamp', 'month', var, f'{var}_trend', f'{var}_detrended', f'{var}_detrended_avg', f'{var}_anomaly'])

        df_lag = create_lagged_vars(df, 12)
        df_cum = create_cum_vars(df, 12)
        df_full = pd.concat([df_lag, df_cum], axis=1)

        # Select the right columns
        # timestamp, month, var, trend, detrended, detrended_avg, anomaly
        col_names = []
        for col in df_full.columns:
            col_names.append(col)
        #print(col_names)
        col_drop = []
        for col in col_names:
            if 'timestamp_lag' in col or 'timestamp_cum' in col or 'month_lag' in col or 'month_cum' in col:
                col_drop.append(col)
        #print(col_drop)
        df = df_full.drop(col_drop, axis=1)

        #print(df.columns)

        # Write to csv
        df.to_csv(outpath + f"{var}_lag_{coords}.csv", index=None)

