from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.stats import linregress
import seaborn as sns 


dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')
topo = np.load(dataDir.joinpath('east_topo.npy'))
wrf = np.load(dataDir.joinpath('WRF_wy2017_daily_east_only_tmax.npy'))
prism = np.load(dataDir.joinpath('PRISM_wy2017_daily_east_only_tmax.npy'))
nldas = np.load(dataDir.joinpath('NLDAS_wy2017_daily_east_only_tmax.npy'))
daymet = np.load(dataDir.joinpath('DAYMET_wy2017_daily_east_only_tmax.npy'))


def p_mult(topo, var):
    valley = np.argwhere(topo == topo.min()) 
    hgt_rel_valley = topo - topo[valley] # difference
    var_time_mean = var.mean(axis=0)
#    var_time_med = np.median(var, axis=0)
    stat = var_time_mean
    var_rel_valley = stat / stat[valley]
    return hgt_rel_valley[0, :], var_rel_valley[0,:]


def t_lapserate(topo, var): 
    valley = np.argwhere(topo == topo.min()) 
    hgt_rel_valley = topo - topo[valley] # difference
    var_time_mean = var.mean(axis=0)
#    var_time_med = np.median(var, axis=0)
    stat = var_time_mean
    var_rel_valley = stat - stat[valley]
    return hgt_rel_valley[0, :], var_rel_valley[0,:]


def normBySeason(season, array, fx):
    # assumes array starts oct1
    topo = dataDir.joinpath('east_topo.npy')
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
    data = array[i1:i2, :]
    tnorm, dnorm = fx(topo, data)

    # calc the variance by elevation band
    return tnorm, dnorm


# create long data frame


def precip():
    dflist = []
    for season in ['OND', 'JFM', 'AMJ', 'JAS']:
        df = pd.DataFrame()
        tnorm, pnorm = normBySeason(season, prism, p_mult)
        tnorm, wnorm = normBySeason(season, wrf, p_mult)
        tnorm, nnorm = normBySeason(season, nldas, p_mult)
        tnorm, dnorm = normBySeason(season, daymet, p_mult)
        df['topo'] = tnorm
        df['wrf'] = wnorm
        df['prism'] = pnorm
        df['daymet'] = dnorm
        df['nldas'] = nnorm
        df['season'] = season
        dflist.append(df)

    merged = pd.concat(dflist, ignore_index=True)
    melt = pd.melt(merged, id_vars=['topo', 'season'])

    # rename columns
    melt.columns = ['Height(m)', 'Season', 'Dataset', 'Multiplier']

    # plotting
    g = sns.FacetGrid(melt, col='Season', hue='Dataset', hue_kws={"marker": ["d", "v", "x", "+"]}, col_wrap=2, palette="colorblind")
    g.map(sns.scatterplot, "Multiplier", "Height(m)", alpha=.7)
    g.add_legend()

    for ax in g.axes.flat:
        ax.plot((1, 5), (0, 1500), c=".2", ls="--", alpha=.3)
    plt.savefig('lapse_grid', dpi=600)


topo = np.load(dataDir.joinpath('east_topo.npy'))
daymet = np.load(dataDir.joinpath('DAYMET_wy2017_daily_east_only_tmin.npy'))
nldas = np.load(dataDir.joinpath('NLDAS_wy2017_daily_east_only_tmin.npy'))
prism = np.load(dataDir.joinpath('PRISM_wy2017_daily_east_only_tmin.npy'))
wrf = np.load(dataDir.joinpath('WRF_wy2017_daily_east_only_tmin.npy'))

dflist = []
for season in ['OND', 'JFM', 'AMJ', 'JAS']:
    df = pd.DataFrame()
    tnorm, pnorm = normBySeason(season, prism, t_lapserate)
    tnorm, wnorm = normBySeason(season, wrf, t_lapserate)
    tnorm, nnorm = normBySeason(season, nldas, t_lapserate)
    tnorm, dnorm = normBySeason(season, daymet, t_lapserate)
    
    # fix daymet ...
#    dnorm np.where(dnorm) 
    df['topo'] = tnorm
    df['wrf'] = wnorm
    df['prism'] = pnorm
    df['daymet'] = dnorm
    df['nldas'] = nnorm
    df['season'] = season
    dflist.append(df)

merged = pd.concat(dflist, ignore_index=True)
melt = pd.melt(merged, id_vars=['topo', 'season'])

# rename columns
melt.columns = ['Height(m)', 'Season', 'Dataset', 'T2 difference']
g = sns.FacetGrid(melt, col='Season', hue='Dataset', hue_kws={"marker": ["d", "v", "x", "+"]}, col_wrap=2, palette="colorblind")
g.map(sns.scatterplot, "T2 difference", "Height(m)", alpha=.7)
g.add_legend()
for ax in g.axes.flat:
    ax.plot((0, -6.5*1.5), (0, 1500.),  c=".2", ls="--", alpha=.3)

plt.savefig('min_temp_grid', dpi=600)