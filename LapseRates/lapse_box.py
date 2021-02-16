from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import matplotlib.cbook as cbook
import seaborn as sns

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')
# paths 
# topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_prcp.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_prcp.npy')
nldas = dataDir.joinpath('NLDAS_wy2017_daily_east_only_prcp.npy')

summer_date_range = pd.date_range("2017-06-01", "2017-09-30", freq='1D')

wrf = np.load(wrf)
prism = np.load(prism)
nldas = np.load(nldas)


def valley_normalize(topo, var):
    valley = np.argwhere(topo == topo.min()) 
    hgt_rel_valley = topo - topo[valley] # difference
    var_time_mean = var.mean(axis=0)
#    var_time_med = np.median(var, axis=0)

    stat = var_time_mean
    var_rel_valley = stat/stat[valley]
    return hgt_rel_valley[0,:], var_rel_valley[0,:]


def normBySeason(season, data):
    topo = dataDir.joinpath('east_topo.npy')
    topo = np.load(topo)

    SeasonDic = {
        "OND": ("2016-10-01", "2016-12-30"),
        "JFM": ("2017-01-01", "2017-03-31"),
        "AMJ": ("2017-04-01", "2017-06-30"),
        "JAS": ("2017-07-01", "2017-09-30")
        }

    start, end = SeasonDic[season]
    doy = pd.date_range(start, end, freq='1D').dayofyear
    i1 = doy[0]
    i2 = doy[-1]

    # read the data
    data = data[i1:i2, :]

    # apply func
    tnorm, dnorm = valley_normalize(topo, data)
    return tnorm, dnorm

# def BoxStat(data):
topo = dataDir.joinpath('east_topo.npy')
topo = np.load(topo)


tnorm, wnorm = normBySeason("OND", wrf)
tnorm, pnorm = normBySeason("OND", prism)
tnorm, nnorm = normBySeason("OND", nldas)

df = pd.DataFrame(data={'topo': tnorm,
                        'wrf': wnorm,
                        'prism': pnorm,
                        'nldas': nnorm
                        })

df.set_index('topo', inplace=True)

# df.set_index('Elevation (m)', inplace=True)
df = df.sort_index()
df2 = pd.melt(df.reset_index(), id_vars='topo')
df2['Elevation difference (m)'] = pd.cut(df2['topo'], np.arange(0, 2000, 250))
df2.columns = ['Elevation (m)', 'variable', 'Precip (mm)', 'Elevation Range (m)']

# create a boxplot
ax = sns.boxplot(y='Elevation Range (m)', x='Precip (mm)', hue='variable', data=df2)

# plt.savefig('PrecipBoxPlots', dpi=600)
plt.ylim(reversed(plt.ylim()))
plt.show()

#     # output
#     return tnorm, pnorm, wnorm, nnorm, pvar_elev, wvar_elev, nvar_elev, mids

# fig, axx = plt.subplots(2, 2)
# fig.set_size_inches(12,12)
# ax = axx.flatten()

# for i, ssn in enumerate(["OND", "JFM", "AMJ", "JAS"]):
#     tnorm, pnorm, wnorm, nnorm, pvar_elev, wvar_elev, nvar_elev, mids = normBySeason(ssn)

#     ax[i].scatter(wnorm, tnorm, label='wrf',  marker='x', alpha=.85, color='r')
#     ax[i].scatter(pnorm, tnorm, label='prism', marker='.', alpha=.85, color='b')
#     ax[i].scatter(nnorm, tnorm, label='nldas', marker='+', alpha=.85, color='g')

#     tx = ax[i].twiny()
#     tx.invert_xaxis()

#     tx.plot(wvar_elev, mids, marker='x', color='r')
#     tx.plot(pvar_elev, mids, marker='.', color='b')
#     tx.plot(nvar_elev, mids, marker='+', color='g')

#     tx.set_xlim(1.6, 0)


# plt.savefig('orog_lapse', dpi=800)