from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
from scipy.signal import find_peaks

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')


topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_prcp.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_prcp.npy')
nldas = dataDir.joinpath('NLDAS_wy2017_daily_east_only_prcp.npy')
daymet = dataDir.joinpath('DAYMET_wy2017_daily_east_only_prcp.npy')


topo = np.load(topo)
wrf = np.load(wrf)
prism = np.load(prism)
nldas = np.load(nldas)
daymet = np.load(daymet)


# pfilt = np.where(prism.mean(axis=1) > 4, 1, 0)
# wfilt = np.where(wrf.mean(axis=1) > 4, 1, 0)
# nldas = np.where(wrf.mean(axis=1) > 4, 1, 0)

df = pd.DataFrame(data={'WRFMean': wrf.mean(axis=1),
                        'PrismMean': prism.mean(axis=1),
                        'DaymetMean': daymet.mean(axis=1),
                        'NldasMean': nldas.mean(axis=1),
                        })

drange = pd.date_range("2016-10-01", "2017-09-30", freq='1D')
df['date'] = drange
df.set_index('date', inplace=True)

dfcolor = ['blue', 'goldenrod', 'green', 'peru']
# compupte rolling mean with hamming window
roll = df.rolling(7, win_type='hamming', closed='both').sum()
roll = roll.shift(1, datetime.timedelta(days=-3))
roll = roll.reindex(df.index)
# timeseries plots
fig, ax = plt.subplots(2,1)
fig.set_size_inches(14,4)

# plot 
df.plot(ax=ax[0], color=dfcolor)
roll.plot(ax=ax[1], color=dfcolor, linestyle='--')

ax[0].set_xticklabels([])
ax[0].set_xticks([])


storms = {"over_predicted": [('2017-01-07', '2017-01-12'),
                             ('2017-02-09', '2017-02-14'),
                             ('2017-05-05', '2017-05-08'),    # Only WRF-PRISM have precip
                             ],

          "under_predicted": [('2016-11-01', '2016-11-03'),
                              ('2017-08-13', '2017-08-16'),
                              ('2017-09-14', '2017-09-16')],

          "well_predicted": [('2016-12-15', '2016-12-18'),
                             ('2017-01-19', '2017-01-26'),
                             ('2017-07-09', '2017-07-17')
                             ]}

chosen = storms["over_predicted"] + storms["well_predicted"]
for i in chosen:

    start = pd.to_datetime(i[0]) - datetime.timedelta(hours=12)
    end = pd.to_datetime(i[1]) + datetime.timedelta(hours=12)
    ax[1].axvspan(start, end, color='gray', alpha=0.15)
    ax[0].axvspan(start, end, color='gray', alpha=0.15)
#plt.show()
plt.savefig('timeseries', dpi=800)


# wrf_indices = np.where(df.WRFMean > 0, 1, 0)
# prism_indices = np.where(df.PrismMean > 0, 1, 0)
# nldas_indices = np.where(df.NldasMean > 0, 1, 0)
# daymet_indices = np.where(df.DaymetMean > 0, 1, 0)

# plt.barh([0, 1, 2, 3],
#         [wrf_indices.sum(),
#          prism_indices.sum(),
#          nldas_indices.sum(),
#          daymet_indices.sum()],
#          tick_label=['WRF', 'PRISM', 'NLDAS', 'DAYMET'])




# # find indices
# wrf_indices = find_peaks(df.WRFMean)[0]
# prism_indices = find_peaks(df.PrismMean)[0]
# nldas_indices = find_peaks(df.NldasMean)[0]
# daymet_indices = find_peaks(df.DaymetMean)[0]




# common = []
# wrf_only = []
# prism_only = []

# for i in wrf_indices:
#     if i in prism_indices:
#         common.append(i)
#     else:
#         wrf_only.append(i)

# for j in prism_indices:
#     if j not in wrf_indices:
#         prism_only.append(j)


# plt.scatter(df.index, df.WRFMean)
# plt.scatter([df.index[j] for j in prism_only], [df.WRFMean[j] for j in prism_only], marker='x')

# def group_timeseries(array,
#                      min_length=3,
#                      min_value=0,
#                      ):
#     # create discrete  groups of a precip timeseries
#     # or other wise
#     group_list = []
#     i = 0
#     while i < len(array)-1:
#         k = 1
#         group = []
#         if array[i] > min_value:
#             # allow a certain number of zeros in the sequence
#             while (array[i+k] > min_value) and (i+k < len(array)-2):
#                 k = k+1
#             # while has ended -- how long was k?
#             if k >= min_length:
#                 group = [i+k for k in range(k)]
#                 group_list.append(group)
#                 # now skip ahead by k -- we have already checked these
#                 i = i + k
#             else:  # reset k
#                 k = 1
#                 i = i + k
#         else:
#             i = i + k
#         # print(i, k, group)
#     return group_list


# def group_dataframe(df, var, newcol, min_length=2, min_value=10):
#     groups = group_timeseries(df[var], min_length=min_length, min_value=min_value)
#     df[newcol] = [0]*len(df.index)
#     k = 1
#     for group in groups:
#         for integer in group:
#             df[newcol].iloc[integer] = k
#         k = k+1
#     return df


# def sensitivity(df, var):
#     p_test = np.linspace(0, 50, 200)
#     day_test = 5
#     array = df[var]
#     num_groups = np.zeros((4, len(p_test)))

#     for i in range(1, day_test):
#         for j in range(len(p_test)):
#             groups = group_timeseries(array, min_length=i, min_value=p_test[j])
#             num_groups[i-1, j] = len(groups)
#     return num_groups, p_test


# df = group_dataframe(df, 'PrismMedian', 'PrismStorm')
# df = group_dataframe(df, 'WRFMedian', 'WRFStorm')
# df = group_dataframe(df, 'NldasMedian', 'NldasStorm')

# def plot_sensitivity():
#     pg, mv = sensitivity(df, 'PrismMedian')
#     wg, mv = sensitivity(df, 'WRFMedian')
#     ng, mv = sensitivity(df, 'NldasMedian')

#     fig, ax = plt.subplots()
#     color = ['purple', 'black', 'orange', 'grey']
#     for i in range(4):
#         if i == 3:
#             ax.plot(mv, pg[i, :], linestyle='--', label='PRISM', color=color[i])
#             ax.plot(mv, wg[i, :], linestyle=':', label='WRF', color=color[i])
#             ax.plot(mv, ng[i, :], label='NLDAS', color=color[i])

#         else:
#             ax.plot(mv, pg[i, :], linestyle='--', color=color[i])
#             ax.plot(mv, wg[i, :], linestyle=':', color=color[i])
#             ax.plot(mv, ng[i, :], color=color[i])

#     ax.set_xlabel('Preciptation Intensity (mm/day)')
#     ax.set_ylabel('Number of Events')
#     ax.legend()
#     return fig, ax

# fig, ax = plot_sensitivity()
# #fig.set_size_inches(6, 6)
# #plt.savefig('precip_intensity', dpi=800)

# plt.show()
# # fig, ax = plt.subplots()
# ax.plot(df.index, df.WRFMedian, color='black', marker='.', alpha=.9, label='WRF')
# ax.plot(df.index, df.PrismMedian, linestyle='--', color='red', alpha=.9, label="Prism")
# ax.set_ylabel('Precip (mm/day)')
# ax.set_xlabel('date')
# ax.legend()
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



