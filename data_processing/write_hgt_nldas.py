from pathlib import Path
import xarray as xr 
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 

#dataDir = Path('/home/wrudisill/Documents/EastRiverPaper/data')
dataDir = Path('/home/wrudisill/scratch/EastRiverClimatePaper/data')
# Read geographic data 
topo = xr.open_dataset(dataDir.joinpath('geog','topography.nc'))


# Read precipitation data  
nldas = xr.open_dataset(dataDir.joinpath('NLDAS','aggregates', '2017NLDAS.nc'))

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

for var in ['TMEAN', 'TMIN', 'TMAX', 'PRCP']:
	nldas_x = np.empty((365, topo.shape[0]))  # time X points_in_basin
	for t, date in enumerate(pd.date_range("2016-10-01", "2017-09-30", freq='1D')):
		#---- prism ----
		nldas_t = nldas.sel(time=date)
		nldas_t = applyEastMask(nldas_t, var)
		
		# assign it to the array
		nldas_x[t, :] = nldas_t
		print(date)	
	# save things ...
	print(var)
	np.save(dataDir.joinpath('npyfiles','NLDAS_wy2017_daily_east_only_{}'.format(var.lower())), nldas_x)
	del nldas_x
