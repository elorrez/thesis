import pandas as pd
import matplotlib.pyplot as plt


def plot_EVI_time_series(inpath, coordinates):
    #fig, axs = plt.subplots(2, 2)
    for coord in coordinates:
        print(coord)
        df = pd.read_csv(f"{inpath}evi_anom_{coord}.csv", names = ['timestamp', 'year', 'month', 'evi', 'trend', 'detrended', 'detrended_avg', 'anomaly'])
        df.plot('timestamp', 'anomaly')
        #plt.plot('timestamp', 'evi', data=df, marker='', markerfacecolor='blue', markersize=12, color='skyblue',
        #        linewidth=4)
        # plt.plot('timestamp', 'evi', data=df, marker='', color='olive', linewidth=2,
        #          label="raw")
        # plt.plot('timestamp', 'anomaly', data=df, marker='', linewidth=2, label="anomaly")
        #
        # # show legend
        # plt.legend()
        #
        # # show graph
        plt.show()



inpath = "C:/EVA/THESIS/data/EVI/anomaly_time_series/"
coordinates = ["-9.5,25.5", "0.5,20.5", "0.5,26.5", "5.5,30.5"]
plot_EVI_time_series(inpath,coordinates)