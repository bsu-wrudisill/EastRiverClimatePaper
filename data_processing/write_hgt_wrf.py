from pathlib import Path
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

dataDir = Path("/scratch/wrudisill/EastRiverClimatePaper/data")

# Read geographic data 
topo = xr.open_dataset(dataDir.joinpath('geog','topography.nc'))

# Read precipitation data  
precipWRF = xr.open_dataset(dataDir.joinpath('WRF','PRECIP','WY2017_PCPSUB.nc'))

wrf_var = 'TMIN'
prism_var = 'Band1'

def applyEastMask(
	dataset, 
	var,
	flattenValues = True,
	**kwargs):
	
	# read in the maskFile 
	mask = dataDir.joinpath('geog','EastRiverMask.nc')
	maskFile= xr.open_dataset(mask)
		
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
precip_prism_x = np.empty((365, topo.shape[0]))  # time X points_in_basin
precip_wrf_x = np.empty((365, topo.shape[0]))

for t, date in enumerate(pd.date_range("2016-10-01", "2017-09-30", freq='1D')):
	try:
	#---- prism ----
		prism_t = precipPrism.sel(time=date)
		prism_t = applyEastMask(prism_t, prism_var)
	
		# assign it to the array
		precip_prism_x[t, :] = prism_t

		# ---- wrf ------
		wrf_t = precipWRF.sel(XTIME=date)
		wrf_t = applyEastMask(wrf_t, wrf_var)
		if wrf_t.shape[0] != 757:
			print(t)
		# assign it to the array
		else:	
			precip_wrf_x[t, :] = wrf_t
	except KeyError:
		print(date)
### MISSING WRF DATA??? NAN VALUES @ TIMES 103,104,105. ### WEIRD

np.save('PRISM_wy2017_daily_east_only_tmin', precip_prism_x)
np.save('WRF_wy2017_daily_east_only_tmin', precip_wrf_x)
