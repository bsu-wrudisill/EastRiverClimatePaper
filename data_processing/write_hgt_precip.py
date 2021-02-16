from pathlib import Path
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

#dataDir = Path('/home/wrudisill/Documents/EastRiverPaper/data')
dataDir = Path('/home/wrudisill/scratch/EastRiverClimatePaper/data')

# Read geographic data 
topo = xr.open_dataset(dataDir.joinpath('topography.nc'))


# Read precipitation data  
precipPrism = xr.open_dataset(dataDir.joinpath('PRISM_WY2017_ppt.nc'))
precipWRF = xr.open_dataset(dataDir.joinpath('WY2017_PCPSUB.nc'))



def applyEastMask(
	dataset, 
	var,
	flattenValues = True,
	**kwargs):
	
	mask = dataDir.joinpath('EastRiverMask.nc')
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
precip_prism_x = np.empty((365, topo.shape[0]))  # time X points_in_basin
precip_wrf_x = np.empty((365, topo.shape[0]))

for t, date in enumerate(pd.date_range("2016-10-01", "2017-09-30", freq='1D')):
	
	#---- prism ----
	prism_t = precipPrism.sel(time=date)
	prism_t = applyEastMask(prism_t, 'Band1')
	
	# assign it to the array
	precip_prism_x[t, :] = prism_t

	# ---- wrf ------
	wrf_t = precipWRF.sel(XTIME=date)
	wrf_t = applyEastMask(wrf_t, 'PRCP')
	if wrf_t.shape[0] != 757:
		print(t)
	# assign it to the array
	else:	
		precip_wrf_x[t, :] = wrf_t

### MISSING WRF DATA??? NAN VALUES @ TIMES 103,104,105. ### WEIRD

np.save('PRISM_wy2017_daily_east_only', precip_prism_x)
np.save('WRF_wy2017_daily_east_only', precip_wrf_x)
np.save('east_topo', topo)
