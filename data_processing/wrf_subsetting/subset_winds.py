import xarray as xr
import numpy as np
from varlist import var_list
import time
import glob
from functions import HourlyPrecip

t0 = time.time()

indir = '/scratch/wrudisill/PrecipWhitePaper/WRF/WY2017/d02/wrfout_d02*'
outdir = './'

# Select all files except last (which is a repeat of the first hour of the following water year) for each WY
files = sorted(glob.glob(indir))[:-1]

# open multi-file dataset (this function accepts unix wildcards)
d = xr.open_mfdataset(files, drop_variables=var_list, concat_dim='Time')

# Swap time and XTIME
d = d.swap_dims({'Time':'XTIME'})	
d['PRCP'] = d['RAINNC']
# Get mean/min/max by day of year for desired variables 

new_array = d[['U10','V10']].resample(XTIME = '24H').mean(dim = 'XTIME') # create daily means of few variables

new_array['WIND_DIR'] = d['U10']
new_array['WIND_DIR'].values = np.arctan2(d['U10'].values, d['V10'].values)


new_array['VAR_U10'] = d['V10'].resample(XTIME = '24H').var(dim = 'XTIME')  # create daily maximum temperature
new_array['VAR_V10'] = d['U10'].resample(XTIME = '24H').var(dim = 'XTIME')  # create daily maximum temperature



# Adjust some meta data
new_array['V10'].attrs = [('description','DAILY MEAN V10'), ('units','m/s')]
new_array['U10'].attrs = [('description','DAILY MEAN U10'), ('units','m/s')]
new_array['VAR_U10'].attrs = [('description','DAILY VAR U10'), ('units','m/s')]
new_array['VAR_U10'].attrs = [('description','DAILY VAR U10'), ('units','m/s')]

# assign attributes to the file 
new_array.attrs = d.attrs 

# Write new netcdf file
new_array.to_netcdf(outdir+'/WY2010_WINDS.nc')

del d, new_array	

t1 = time.time()
print("Total time to create this subset was:", t1 - t0, "seconds.")

