import pandas as pd
import matplotlib.pyplot as plt


def plot_EVI_time_series(inpath, coordinates):
    evi_list = []
    anomaly_list = []
    for coord in coordinates:
        #print(coord)
        df = pd.read_csv(f"{inpath}evi_anom_{coord}.csv", names = ['timestamp', 'year', 'month', 'evi', 'trend', 'detrended', 'detrended_avg', 'anomaly'])
        evi_list.append(df['evi'])
        anomaly_list.append(df['anomaly'])
    #print(len(evi_list))
    #print((evi_list[0]))

    fig, axs = plt.subplots(4,4)
    fig.suptitle('EVI: raw')
    fig.subplots_adjust(hspace=0.5)
    for evi, anomaly, coord, ax in zip(evi_list,anomaly_list, coordinates,axs.flatten()):
        ax.plot(evi)
        #ax.plot(anomaly)
        ax.set_title(coord, fontsize= 11)
        fig.savefig(f'C:/EVA/THESIS/data/EVI/evi_raw.jpg')
        plt.show()

    fig, axs = plt.subplots(4,4)
    fig.suptitle('EVI: anomalies')
    fig.subplots_adjust(hspace=0.5)
    for evi, anomaly, coord, ax in zip(evi_list,anomaly_list, coordinates,axs.flatten()):
        #ax.plot(evi)
        ax.plot(anomaly)
        ax.set_title(coord, fontsize= 11)
        fig.savefig(f'C:/EVA/THESIS/data/EVI/evi_anomaly.jpg')
        plt.show()



