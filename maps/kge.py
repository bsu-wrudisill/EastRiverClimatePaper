from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import numpy as np
import xarray as xr

dataDir = Path('/Volumes/Transcend/EastRiverClimatePaper/data')

topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only_prcp.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only_prcp.npy')
nldas = dataDir.joinpath('NLDAS_wy2017_daily_east_only_prcp.npy')

ds = xr.open_dataset(dataDir.joinpath('EastRiverMask.nc'))

topo = np.load(topo)
wrf = np.load(wrf)
prism = np.load(prism)
nldas = np.load(nldas)


def kge(a1, a2):
    s = np.std(a1)/np.std(a2)
    m = np.mean(a1)/np.mean(a2)
    c = np.corrcoef(a1, a2)[0, 1]
    return 1 - np.sqrt((1 - s)**2 + (1-m)**2 + (1-c)**2)


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


def calcvar(a1):
    # calculate the temporal variance
    return np.var(a1, axis=0)


def calcsum(a1):
    # calculate the temporal variance
    return np.sum(a1, axis=0)


# # for i in range(757):
# #     kval = kge(np.mean(wrf[:, i]), np.mean(prism[:, i]))
# sort_arg = np.argsort(topo)
# wrf_sort = wrf[:, sort_arg]
# prism_sort = prism[:, sort_arg]

# mean-abs-difference

ds['wrf-nldas'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['wrf-prism'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-nldas'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))

ds['wrf-total'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['nldas-total'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
ds['prism-total'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))


locs = np.where(ds.T2.values == 1)
# assign things
ds['wrf-prism'].values[locs] = spatial_kge(wrf, prism)
ds['wrf-nldas'].values[locs] = spatial_kge(wrf, nldas)
ds['prism-nldas'].values[locs] = spatial_kge(prism, nldas)

ds['wrf-total'].values[locs] = calcsum(wrf)
ds['nldas-total'].values[locs] = calcsum(nldas)
ds['prism-total'].values[locs] = calcsum(prism)


zoom = [(202, 247), (170, 205)]


def zoom_map(a1, zoom):
    # flip and zoom in
    # remove masked values
    zoom_x = zoom[0]
    zoom_y = zoom[1]
    new_arr = a1[zoom_x[0]:zoom_x[1], zoom_y[0]:zoom_y[1]]
    new_arr = np.where(new_arr == 0, np.nan, new_arr)
    return new_arr[::-1, :]


fig, ax = plt.subplots(3,3)

# the middle --variance
ax[0, 0].imshow(zoom_map(ds['prism-total'], zoom), vmin=200, vmax=1200.)
ax[1, 1].imshow(zoom_map(ds['wrf-total'], zoom), vmin=200, vmax=1200.)
ax[2, 2].imshow(zoom_map(ds['nldas-total'], zoom), vmin=200, vmax=1200.)

# top-right
ax[0, 1].imshow(zoom_map(ds['wrf-nldas'], zoom), vmin=0., vmax=1., cmap='magma')
ax[0, 2].imshow(zoom_map(ds['wrf-prism'], zoom), vmin=0., vmax=1., cmap='magma')
ax[1, 2].imshow(zoom_map(ds['prism-nldas'], zoom), vmin=0., vmax=1., cmap='magma')

ax[1, 0].imshow(zoom_map(ds['wrf-nldas'], zoom), vmin=0., vmax=1., cmap='magma')
ax[2, 0].imshow(zoom_map(ds['wrf-prism'], zoom), vmin=0., vmax=1., cmap='magma')
ax[2, 1].imshow(zoom_map(ds['prism-nldas'], zoom), vmin=0., vmax=1., cmap='magma')


for axx in ax.flatten():
    axx.set_xticklabels([])
    axx.set_yticklabels([])
    axx.set_xticks([])
    axx.set_yticks([])


# ax[1,0].imshow(zoom_map(ds['wrf-prism'], zoom))
# ax[2,0].imshow(zoom_map(ds['wrf-prism'], zoom))
# ax[0,0].imshow(zoom_map(ds['wrf-prism'], zoom))
# ax[0,0].imshow(zoom_map(ds['wrf-prism'], zoom))
# ax[0,0].imshow(zoom_map(ds['wrf-prism'], zoom))
