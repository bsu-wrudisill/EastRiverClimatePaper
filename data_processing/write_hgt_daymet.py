import xarray as xr
from matplotlib import pyplot as plt
import sys
from pathlib import Path
import pandas as pd 
import numpy as np 

dataDir = Path('/home/wrudisill/scratch/EastRiverClimatePaper/data/')

# read in the daymet 
topo = xr.open_dataset(dataDir.joinpath('geog','topography.nc'))
varlist = ['tmax']#, 'prcp']
drange = pd.date_range("2016-10-01", "2017-09-30", freq='1D')




def applyEastMask(
	dataset, 
	var,
	flattenValues = True,
	**kwargs):
	
	mask = dataDir.joinpath('geog','EastRiverMask.nc')
	# read in the maskFile 
	maskFile = xr.open_dataset(mask)
		
	# Get a list of vars in the dataset ...    
	varlist = list(dataset.variables.keys()) 

	# Assign values to the mask array
	dataset['MASK'] = dataset[var] # create a copy of the var 
	dataset['MASK'].values = maskFile['T2'].values

	data_mask  = dataset.where(dataset.MASK == 1)
	data_mask = data_mask[var]
	# Flatten the values of the array 
	if flattenValues:
		flat = data_mask.values.flatten()
		flat = flat[~np.isnan(flat)]
		return flat
	else:
		twod = data_mask[var]
		return twod

topo = applyEastMask(topo, 'HGT')

for dayvar in varlist:
	# save array
	daymet_x = np.empty((365, topo.shape[0]))  # time X points_in_basin
	
	# read files 
	names = ["{}DayMetRegrid_{}_{}.nc".format(dayvar, dayvar, y) for y in [2016,2017]]
	dayf = [dataDir.joinpath('DAYMET', dayvar,n) for n in names]
	ds = xr.open_mfdataset(dayf, concat_dim='time')

	# check for misssing dates...
	for i in drange:
		try:
			ds.loc[dict(time=i)]
		except KeyError:
			k=i
			print(i)
	
	# resample to get rid of missing dates 
	ds = ds.resample(time='1D').asfreq()
	daymet = ds.loc[dict(time=drange)]
	
	for t, date in enumerate(drange):
		# daymet	
		daymet_t  = daymet.sel(time=date)
		daymet_t = applyEastMask(daymet_t, dayvar)
		
		# missing data returns empty array 
		if daymet_t.shape[0] != 757:
			print('missing data', t)
		# assign it to the array
		else:
			daymet_x[t, :] = daymet_t
			print('date/min/max', date,np.min(daymet_t), np.max(daymet_t))

	# save things ...
	np.save(dataDir.joinpath('npyfiles','DAYMET_wy2017_daily_east_only_{}'.format(dayvar.lower())), daymet_x)
	del daymet_x




