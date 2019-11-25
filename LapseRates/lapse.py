from pathlib import Path
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

dataDir = Path('/home/wrudisill/Documents/EastRiverPaper/data')

# paths 
topo = dataDir.joinpath('east_topo.npy')
wrf = dataDir.joinpath('WRF_wy2017_daily_east_only.npy')
prism = dataDir.joinpath('PRISM_wy2017_daily_east_only.npy')

#
summer_date_range = pd.date_range("2017-06-01", "2017-09-30", freq='1D')



def valley_normalize(topo, var):
	valley = np.argwhere(topo == topo.min()) 
	hgt_rel_valley = topo - topo[valley] # difference
	var_time_mean = var.mean(axis=0)
	var_rel_valley = var_time_mean/var_time_mean[valley]
	return hgt_rel_valley[0,:], var_rel_valley[0,:]



def normBySeason(season):
	topo = dataDir.joinpath('east_topo.npy')
	wrf = dataDir.joinpath('WRF_wy2017_daily_east_only.npy')
	prism = dataDir.joinpath('PRISM_wy2017_daily_east_only.npy')

	SeasonDic = {
		"OND" : ("2016-10-01","2016-12-30"),
		"JFM" : ("2017-01-01","2017-03-31"),
		"AMJ" : ("2017-04-01","2017-06-30"),
		"JAS" : ("2017-07-01","2017-09-30")
		}
	start, end = SeasonDic[season]
	doy=pd.date_range(start, end, freq='1D').dayofyear
	i1=doy[0]
	i2=doy[-1]

	# read the data 
	topo = np.load(topo)
	wrf = np.load(wrf)[i1:i2, :]
	prism = np.load(prism)[i1:i2, :]

	# apply func
	tnorm,pnorm = valley_normalize(topo, prism)
	tnorm,wnorm = valley_normalize(topo, wrf)

	return tnorm, pnorm, wnorm

fig,axx = plt.subplots(2,2)
ax = axx.flatten()
for i,ssn in enumerate(["OND","JFM","AMJ","JAS"]):
	tnorm, pnorm, wnorm = normBySeason(ssn)
	ax[i].scatter(tnorm, pnorm, label='prism')
	ax[i].scatter(tnorm, wnorm, label='wrf')
	ax[i].legend()
	ax[i].set_title(ssn)
	if i in [0,2]:
		ax[i].set_ylabel('Precip. Relative to Valley')
	if i in [2,3]:
		ax[i].set_xlabel('Elevation Difference (m)')

plt.show()