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
daymet = dataDir.joinpath('DAYMET_wy2017_daily_east_only_prcp.npy')

# topo = np.load(topo)
# wrf = np.load(wrf)
# prism = np.load(prism)
# nldas = np.load(nldas)
# daymet = np.load(daymet)


def npytoxr(path):
    data = np.load(path)
    time, space = data.shape
    locs = list(range(space))
    times = pd.date_range('2016-10-01', '2017-09-30', freq='1D')
    foo = xr.DataArray(data, coords=[times, locs], dims=['time', 'space'])
    return foo


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


storms_ordered = [('2016-12-15', '2016-12-18'),
                  ('2017-01-07', '2017-01-11'),
                  ('2017-01-19', '2017-01-26'),
                  ('2017-02-09', '2017-02-14'),
                  ('2017-05-05', '2017-05-08'),
                  ('2017-07-09', '2017-07-17')]


def zoom_map(a1):
    # flip and zoom in
    # remove masked values
    zoom = [(202, 247), (170, 205)]
    zoom_x = zoom[0]
    zoom_y = zoom[1]
    new_arr = a1[zoom_x[0]:zoom_x[1], zoom_y[0]:zoom_y[1]]
    new_arr = np.where(new_arr == 0, np.nan, new_arr)
    return new_arr[::-1, :]


wrf = npytoxr(wrf) #- 273.15
#wrf = wrf.where(wrf == -273.15, np.nan)

prism = npytoxr(prism)
daymet = npytoxr(daymet)
fig, ax = plt.subplots(2, 3)
axx = ax.flatten()

# do stuff and plot
# for i, dates in enumerate(storms['over_predicted']):

for i, dates in enumerate(storms_ordered):
    start = dates[0]
    end = dates[1]
    drange = pd.date_range(start, end, freq='1D')
    wmean = wrf.loc[drange]
    pmean = prism.loc[drange]
    # dmean = daymet.loc[drange]
    diff = wmean.mean(axis=0) - pmean.mean(axis=0)

    # read this in so that we can reshape the data correctly
    ds = xr.open_dataset(dataDir.joinpath('EastRiverMask.nc'))
    ds['data'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
    ds['wtemp'] = (['south_north', 'west_east'], np.zeros_like(ds.T2))
    locs = np.where(ds.T2.values == 1)
    ds['data'].values[locs] = diff
    ds['wtemp'].values[locs] = wmean.mean(axis=0)
    # zoom in, return array
    mapp = zoom_map(ds['data'])

    # now plot
    im = axx[i].imshow(mapp, vmin=-15, vmax=15., cmap='seismic')
#    axx[i].contour(zoom_map(ds['wtemp']), levels=[-10, -5, 0, 5, 10], colors='black')
    axx[i].set_title("{} :: {}".format(start, end), fontsize=8)
    axx[i].set_xticklabels([])
    axx[i].set_yticklabels([])
    axx[i].set_xticks([])
    axx[i].set_yticks([])
    axx[i].set_axis_off()
plt.savefig('over_predicted_maps_prcp')
plt.show()


fig = plt.figure()
cx = fig.add_axes([.1, .1, .015, .8])
fig.colorbar(im, cax=cx, orientation='vertical')
plt.savefig('over_predicted_cbar_prcp')