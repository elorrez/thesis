import pandas as pd
import matplotlib.pyplot as plt


def plot_climate_time_series(inpath, coordinates):
    var_list = []
    anomaly_list = []
    trend_list = []
    var_name = inpath.split('/')[-3]
    for coord in coordinates:
        #print(coord)
        print(f"{inpath}{var_name}_anom_{coord}.csv")
        df = pd.read_csv(f"{inpath}{var_name}_anom_{coord}.csv", names = ['timestamp', 'month', var_name, 'trend', 'detrended', 'detrended_avg', 'anomaly'])
        var_list.append(df[var_name])
        anomaly_list.append(df['anomaly'])
        trend_list.append(df['trend'])
    print(len(var_list))
    print((var_list[0]))

    fig, axs = plt.subplots(4,3)
    fig.suptitle(f'{var_name}: raw')
    fig.subplots_adjust(hspace=0.5)
    for var, anomaly, coord, ax in zip(var_list,anomaly_list, coordinates,axs.flatten()):
        ax.plot(var)
        #ax.plot(anomaly)
        ax.set_title(coord, fontsize= 11)
        fig.savefig(f'C:/EVA/THESIS/data/climate_data/{var_name}_raw.jpg')
        plt.show()

    fig, axs = plt.subplots(4,3)
    fig.suptitle(f'{var_name}: anomalies')
    fig.subplots_adjust(hspace=0.5)
    for var, anomaly, coord, ax in zip(var_list,anomaly_list, coordinates,axs.flatten()):
        #ax.plot(evi)
        ax.plot(anomaly)
        ax.set_title(coord, fontsize= 11)
        fig.savefig(f'C:/EVA/THESIS/data/climate_data/{var_name}_anomaly.jpg')
        plt.show()

    # fig, axs = plt.subplots(4,3)
    # fig.suptitle(f'{var_name}: trend')
    # fig.subplots_adjust(hspace=0.5)
    # for trend, coord, ax in zip(trend_list, coordinates,axs.flatten()):
    #     #ax.plot(evi)
    #     ax.plot(trend)
    #     ax.set_title(coord, fontsize= 11)
    #     fig.savefig(f'C:/EVA/THESIS/data/climate_data/{var_name}_trend.jpg')
    #     plt.show()




