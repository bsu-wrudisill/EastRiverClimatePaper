from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')
# paths 
# topo = dataDir.joinpath('east_topo.npy')
# wrf = dataDir.joinpath('WRF_wy2017_daily_east_only.npy')
# prism = dataDir.joinpath('PRISM_wy2017_daily_east_only.npy')

#
summer_date_range = pd.date_range("2017-06-01", "2017-09-30", freq='1D')


def valley_normalize(topo, var):
    valley = np.argwhere(topo == topo.min()) 
    hgt_rel_valley = topo - topo[valley] # difference
    var_time_mean = var.mean(axis=0)
#    var_time_med = np.median(var, axis=0)

    stat = var_time_mean
    var_rel_valley = stat/stat[valley]
    return hgt_rel_valley[0,:], var_rel_valley[0,:]


def normBySeason(season):
    topo = dataDir.joinpath('east_topo.npy')
    wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_prcp.npy')
    prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_prcp.npy')
    nldas = dataDir.joinpath('NLDAS_wy2017_daily_east_only_prcp.npy')

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
    topo = np.load(topo)
    wrf = np.load(wrf)[i1:i2, :]
    prism = np.load(prism)[i1:i2, :]
    nldas = np.load(nldas)[i1:i2, :]

    # apply func
    tnorm, pnorm = valley_normalize(topo, prism)
    tnorm, wnorm = valley_normalize(topo, wrf)
    tnorm, nnorm = valley_normalize(topo, nldas)

    # pline = linregress(tnorm, pnorm)
    # wline = linregress(tnorm, wnorm)

    elev_bins = np.linspace(0, 1500, 11)
    mids = np.arange(75, 1500, 150)  # i am dumb...

    # calc the variance by elevation band
    df = pd.DataFrame(data={'topo': tnorm,
                            'wrf': wnorm,
                            'prism': pnorm,
                            'nldas': nnorm
                            })

    df.set_index('topo', inplace=True)

    # to groups between 0-1500m
    grouped = df.groupby(pd.cut(df.index, elev_bins))
    wvar_elev = grouped.var()['wrf'].values
    pvar_elev = grouped.var()['prism'].values
    nvar_elev = grouped.var()['nldas'].values

    # output
    return tnorm, pnorm, wnorm, nnorm, pvar_elev, wvar_elev, nvar_elev, mids


fig, axx = plt.subplots(2, 2)
fig.set_size_inches(12,12)
ax = axx.flatten()

for i, ssn in enumerate(["OND", "JFM", "AMJ", "JAS"]):
    tnorm, pnorm, wnorm, nnorm, pvar_elev, wvar_elev, nvar_elev, mids = normBySeason(ssn)

    ax[i].scatter(wnorm, tnorm, label='wrf',  marker='x', alpha=.85, color='r')
    ax[i].scatter(pnorm, tnorm, label='prism', marker='.', alpha=.85, color='b')
    ax[i].scatter(nnorm, tnorm, label='nldas', marker='+', alpha=.85, color='g')

    tx = ax[i].twiny()
    tx.invert_xaxis()

    tx.plot(wvar_elev, mids, marker='x', color='r')
    tx.plot(pvar_elev, mids, marker='.', color='b')
    tx.plot(nvar_elev, mids, marker='+', color='g')

    tx.set_xlim(1.6, 0)
    # plot regression lines
    # ax[i].plot(tnorm, tnorm*wline.slope + wline.intercept, color='black')
    # ax[i].plot(tnorm, tnorm*pline.slope + pline.intercept, color='black')

    ax[i].set_xlim(.8, 5)
#    ax[i].set_title(ssn, fontsize=10)
    ax[i].set_xlabel(r'$\alpha$', fontsize=10)
    tx.set_xlabel(r'$\sigma^2(\alpha$)', fontsize=10)

    if i == 0:
        ax[i].legend(fontsize=10)
    if i in [0, 2]:
        ax[i].set_ylabel('Elevation (m)')

    # if i in [2, 3]:
    #     ax[i].set_xlabel(r'$\alpha$', fontsize=20)
    #     # tx.set_xticklabels([])
    # if i in [0, 1]:
    #     # ax[i].set_xticklabels([])
    #     tx.set_xlabel(r'$\sigma^2(\alpha$)', fontsize=20)

    # if i in [1, 3]:
    #     ax[i].set_yticklabels([])

plt.savefig('orog_lapse', dpi=800)