from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')


topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_tmean.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_tmean.npy')


topo = np.load(topo)
wrf = np.load(wrf)
prism = np.load(prism)


pfilt = np.where(prism.mean(axis=1) > 4, 1, 0)
wfilt = np.where(wrf.mean(axis=1) > 4, 1, 0)


df = pd.DataFrame(data={'PrismMean': prism.mean(axis=1),
                        'PrismVar': prism.var(axis=1),
                        'PrismMedian': np.median(prism, axis=1),
                        'WRFMean': wrf.mean(axis=1),
                        'WRFVar': wrf.var(axis=1),
                        'WRFMedian': np.median(wrf, axis=1)
                        })

drange = pd.date_range("2016-10-01", "2017-09-30", freq='1D')
df['date'] = drange
df.set_index('date', inplace=True)


def group_timeseries(array,
                     min_length=3,
                     min_value=0,
                     ):
    # create discrete  groups of a precip timeseries
    # or other wise
    group_list = []
    i = 0
    while i < len(array)-1:
        k = 1
        group = []
        if array[i] > min_value:
            # allow a certain number of zeros in the sequence
            while (array[i+k] > min_value) and (i+k < len(array)-2):
                k = k+1
            # while has ended -- how long was k?
            if k >= min_length:
                group = [i+k for k in range(k)]
                group_list.append(group)
                # now skip ahead by k -- we have already checked these
                i = i + k
            else:  # reset k
                k = 1
                i = i + k
        else:
            i = i + k
        # print(i, k, group)
    return group_list


def group_dataframe(df, var, newcol, min_length=2, min_value=10):
    groups = group_timeseries(df[var], min_length=min_length, min_value=min_value)
    df[newcol] = [0]*len(df.index)
    k = 1
    for group in groups:
        for integer in group:
            df[newcol].iloc[integer] = k
        k = k+1
    return df


def sensitivity(df, var):
    p_test = np.linspace(0, 50, 200)
    day_test = 5
    array = df[var]
    num_groups = np.zeros((4, len(p_test)))

    for i in range(1, day_test):
        for j in range(len(p_test)):
            groups = group_timeseries(array, min_length=i, min_value=p_test[j])
            num_groups[i-1, j] = len(groups)
    return num_groups, p_test


# df = group_dataframe(df, 'PrismMedian', 'PrismStorm')
# df = group_dataframe(df, 'WRFMedian', 'WRFStorm')

def plot_sensitivity():
    pg, mv = sensitivity(df, 'PrismMedian')
    wg, mv = sensitivity(df, 'WRFMedian')
    fig, ax = plt.subplots()
    color = ['red', 'blue', 'green', 'black']
    for i in range(4):
        if i == 3:
            ax.plot(mv, pg[i, :], linestyle='--', label='PRISM', color=color[i])
            ax.plot(mv, wg[i, :], label='WRF', color=color[i])
        else:
            ax.plot(mv, pg[i, :], linestyle='--', color=color[i])
            ax.plot(mv, wg[i, :], color=color[i])
    ax.set_xlabel('Preciptation Intensity (mm/day)')
    ax.set_ylabel('Number of Events')
    ax.legend()
    return fig, ax

# fig, ax = plot_sensitivity()
# fig.set_size_inches(6, 6)
# plt.savefig('precip_intensity', dpi=800)

fig, ax = plt.subplots(2, 1)
fig.set_size_inches(8, 3)

# ax.plot(df.index, df.WRFMedian-273.15, color='black', marker='.', alpha=.9, label='WRF')
# ax.plot(df.index, df.PrismMedian, linestyle='--', color='red', alpha=.9, label="Prism")


# ax.plot(df.index, df.WRFVar, color='black', marker='.', alpha=.9, label='WRF')
# ax.plot(df.index, df.PrismVar, linestyle='--', color='red', alpha=.9, label="Prism")


ax[0].plot(df.index, df.WRFMean-273.15, color='blue', alpha=.9, label='WRF')
ax[0].plot(df.index, df.WRFMedian-273.15, color='blue', linestyle='--', alpha=.9)
ax[0].plot(df.index, df.PrismMean, color='red', alpha=.9, label="Prism")
ax[0].plot(df.index, df.PrismMedian, linestyle='--', color='red', alpha=.9)
ax[0].set_ylim(-20,20)
ax[0].axhline(0, linestyle='--', color='black')
ax[0].legend()

ax[1].plot(df.index, df.WRFVar, color='blue', alpha=.9, label="Prism")
ax[1].plot(df.index, df.PrismVar, color='red', alpha=.9, label="Prism")


plt.savefig('temp_timeseries', dpi=800)
plt.show()


# fig.set_size_inches(6, 2.5)
# plt.savefig('precip_timeseries', dpi=800)
# df = group_dataframe(df, 'PrismMedian', 'PrismStorm')
# df = group_dataframe(df, 'WRFMedian', 'WRFStorm')
# def plot_spans(df, col, ax, color='red'):
#     groups = df.groupby(col).groups
#     for i in range(1, len(groups)):
#         start = groups[i][0] - datetime.timedelta(hours=12)
#         end = groups[i][-1] + datetime.timedelta(hours=12)
#         ax.axvspan(start, end, color=color, alpha=0.15)
# plot_spans(df, 'WRFStorm', ax, color='blue')
# plot_spans(df, 'PrismStorm', ax, color='red')
# plt.show()