from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import xarray as xr
from itertools import combinations
#from functools import reduce
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy.stats import pearsonr

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')

topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_tmax.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_tmax.npy')
nldas = dataDir.joinpath('NLDAS_wy2017_daily_east_only_tmax.npy')
daymet = dataDir.joinpath('DAYMET_wy2017_daily_east_only_tmax.npy')

ds = xr.open_dataset(dataDir.joinpath('EastRiverMask.nc'))
topo = np.load(topo)
wrf = np.load(wrf) - 273.15
prism = np.load(prism)
nldas = np.load(nldas) -273.15
daymet = np.load(daymet)

data_dict = {"daymet": daymet,
             "wrf": wrf,
             "nldas": nldas,
             "prism": prism,
             }


def kge(a1, a2):
    s = np.std(a1)/np.std(a2)
    m = np.mean(a1)/np.mean(a2)
#    c = pearsonr(a1, a2)[0]
    c = np.corrcoef(a1,a2)[0, 1]
    return 1 - np.sqrt((s-1)**2 + (m-1)**2 + (c-1)**2)


def rmse(a1, a2):
    mse = np.mean((a1-a2)**2)
    return np.sqrt(mse)


def corr(a1, a2):
    c = np.corrcoef(a1, a2)[0, 1]
    return c


def spatial_corr(a1, a2):
    cmat = np.zeros_like(topo)
    for i in range(len(topo)):
        cmat[i] = corr(a1[:, i], a2[:, i])
    return cmat


def spatial_kge(a1, a2):
    kmat = np.zeros_like(topo)
    for i in range(len(topo)):
        kmat[i] = kge(a1[:, i], a2[:, i])
    return kmat


def spatial_rmse(a1, a2):
    rmat = np.zeros_like(topo)
    for i in range(len(topo)):
        rmat[i] = rmse(a1[:, i], a2[:, i])
    return rmat


def MAD(a1, a2):
    # mean absolute difference
    diff = np.abs(a1.sum(axis=0) - a2.sum(axis=0))
    return diff


def bias(a1, a2):
    # mean absolute difference
    diff = a1.mean(axis=0) - a2.mean(axis=0)
    return diff

def ens_mean(*args):
    # ensemblse_mean
    return np.mean(args, axis=0)


def calcvar(a1):
    # calculate the temporal variance
    return np.var(a1, axis=0)


def calcstd(a1):
    # calculate the temporal variance
    return np.std(a1, axis=0)


def calcsum(a1):
    # calculate the temporal variance
    return np.mean(a1, axis=0)


def MAD_anomaly(data):
    # compute the mean absolute difference anomaly for ALL combinations of products
    all_combos = list(combinations(data_dict.keys(), 2))
    temporary = []
    for i in all_combos:
        temporary.append(MAD(data_dict[i[0]], data_dict[i[1]]))
    total_mean = np.mean(temporary, axis=0)  # temporal mean of all datasets 

    # mean MAD for the single product
    copy = list(data_dict.keys())
    copy.remove(data)
    sub = []
    for i in copy:
        sub.append(MAD(data_dict[data], data_dict[i]))
    sub_mean = np.mean(sub, axis=0)
    return total_mean - sub_mean

locs = np.where(ds.T2.values == 1)


# top diag
ds['wrf-nldas-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['wrf-prism-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['wrf-daymet-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-nldas-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-nldas-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-daymet-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['nldas-daymet-kge'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))

ds['wrf-prism-kge'].values[locs] = spatial_kge(wrf, prism)
ds['wrf-nldas-kge'].values[locs] = spatial_kge(wrf, nldas)
ds['wrf-daymet-kge'].values[locs] = spatial_kge(wrf, daymet)
ds['prism-nldas-kge'].values[locs] = spatial_kge(prism, nldas)
ds['prism-daymet-kge'].values[locs] = spatial_kge(prism, daymet)
ds['nldas-daymet-kge'].values[locs] = spatial_kge(nldas, daymet)


# center
ds['wrf-MADE'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['nldas-MADE'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-MADE'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['daymet-MADE'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))

ds['wrf-MADE'].values[locs] = calcsum(wrf)
ds['nldas-MADE'].values[locs] = calcsum(nldas)
ds['prism-MADE'].values[locs] = calcsum(prism)
ds['daymet-MADE'].values[locs] = calcsum(daymet)


# bottom diag
ds['wrf-nldas-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['wrf-prism-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['wrf-daymet-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-nldas-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-nldas-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-daymet-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['nldas-daymet-MAD'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))

ds['wrf-prism-MAD'].values[locs] = bias(wrf, prism)
ds['prism-nldas-MAD'].values[locs] = bias(nldas, prism)
ds['prism-daymet-MAD'].values[locs] = bias(daymet, prism)
ds['wrf-nldas-MAD'].values[locs] = bias(nldas, wrf)
ds['wrf-daymet-MAD'].values[locs] = bias(daymet, wrf)
ds['nldas-daymet-MAD'].values[locs] = bias(daymet, nldas)


zoom = [(202, 247), (170, 205)]


def zoom_map(a1, zoom):
    # flip and zoom in
    # remove masked values
    zoom_x = zoom[0]
    zoom_y = zoom[1]
    new_arr = a1[zoom_x[0]:zoom_x[1], zoom_y[0]:zoom_y[1]]
    new_arr = np.where(new_arr == 0, np.nan, new_arr)
    return new_arr[::-1, :]


fig, ax = plt.subplots(4,4)

# grid = AxesGrid(fig, 111,
#                 nrows_ncols=(4, 4),
#                 axes_pad=0.05,
#                 cbar_mode='single',
#                 cbar_location='bottom',
#                 cbar_pad=0.1
#                 )

# ax = np.array(grid.axes_all).reshape(4, 4)

# the middle --variance
c0 = ax[0, 0].imshow(zoom_map(ds['prism-MADE'], zoom), vmin=-10, vmax=10., cmap='viridis')
ax[1, 1].imshow(zoom_map(ds['wrf-MADE'], zoom), vmin=-10, vmax=10., cmap='viridis')
ax[2, 2].imshow(zoom_map(ds['nldas-MADE'], zoom), vmin=-10, vmax=10., cmap='viridis')
ax[3, 3].imshow(zoom_map(ds['daymet-MADE'], zoom), vmin=-10, vmax=10., cmap='viridis')

# # top-right
c1 = ax[0, 1].imshow(zoom_map(ds['wrf-prism-kge'], zoom), vmin=0., vmax=1., cmap='magma')
ax[0, 2].imshow(zoom_map(ds['prism-nldas-kge'], zoom), vmin=0., vmax=1., cmap='magma')
ax[0, 3].imshow(zoom_map(ds['prism-daymet-kge'], zoom), vmin=0., vmax=1., cmap='magma')
ax[1, 2].imshow(zoom_map(ds['wrf-nldas-kge'], zoom), vmin=0., vmax=1., cmap='magma')
ax[1, 3].imshow(zoom_map(ds['wrf-daymet-kge'], zoom), vmin=0., vmax=1., cmap='magma')
ax[2, 3].imshow(zoom_map(ds['nldas-daymet-kge'], zoom), vmin=0., vmax=1., cmap='magma')


c2 = ax[1, 0].imshow(zoom_map(ds['wrf-prism-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')
ax[2, 0].imshow(zoom_map(ds['prism-nldas-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')
ax[3, 0].imshow(zoom_map(ds['prism-daymet-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')
ax[2, 1].imshow(zoom_map(ds['wrf-nldas-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')
ax[3, 1].imshow(zoom_map(ds['wrf-daymet-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')
ax[3, 2].imshow(zoom_map(ds['nldas-daymet-MAD'], zoom), vmin=-20, vmax=20., cmap='seismic')

names = ['prism', 'wrf', 'nldas', 'daymet']
for i, axx in enumerate(ax.flatten()):
    axx.set_xticklabels([])
    axx.set_yticklabels([])
    axx.set_xticks([])
    axx.set_yticks([])
    axx.set_axis_off()
    # if i in [0, 1, 2, 3]:
    #     axx.set_title(names[i])
    # if i in [0, 4, 8, 12]:
    #     axx.set_ylabel(names[int(i/4)])
plt.savefig('maps_maxtemp', dpi=600)

fig = plt.figure()
cx0 = fig.add_axes([.1, .1, .8, .015])
cx1 = fig.add_axes([.1, .37, .8, .015])
cx2 = fig.add_axes([.1, .7, .8, .015])
fig.colorbar(c0, cax=cx0, orientation='horizontal')
fig.colorbar(c1, cax=cx1, orientation='horizontal')
fig.colorbar(c2, cax=cx2, orientation='horizontal')

plt.savefig('cbar_maxtemp', dpi=600)


plt.show()
