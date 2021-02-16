import xarray as xr
import numpy as np
from varlist import var_list
import time
import glob
from functions import HourlyPrecip

t0 = time.time()

indir = '/scratch/wrudisill/PrecipWhitePaper/WRF/WY2017/d02/wrfout_d02*09*'
outdir = './'

# Select all files except last (which is a repeat of the first hour of the following water year) for each WY
files = sorted(glob.glob(indir))[:-1]

# open multi-file dataset (this function accepts unix wildcards)
d = xr.open_mfdataset(files, drop_variables=var_list, concat_dim='Time')

# Swap time and XTIME
d = d.swap_dims({'Time':'XTIME'})	
d['PRCP'] = d['RAINNC']
#d['PRCP'].values = HourlyPrecip(d['RAINNC'],d['I_RAINNC'])
# Get mean/min/max by day of year for desired variables 

new_array = d[['T2','Q2']].resample(XTIME = '24H').mean(dim = 'XTIME') # create daily means of few variables
#new_array['TMIN'] = d['T2'].resample(XTIME = '24H').min(dim = 'XTIME') # create daily minimum temperature
#new_array['TMAX'] = d['T2'].resample(XTIME = '24H').max(dim = 'XTIME')  # create daily maximum temperature
#new_array = new_array.rename({'T2' : 'TMEAN'}) # rename T2 as TMEAN
#new_array['PRCP'] = d['PRCP'].resample(XTIME = '24H').sum(dim = 'XTIME')

# Adjust some meta data
#new_array['TMEAN'].attrs = [('description','DAILY MEAN GRID SCALE TEMPERATUTE'), ('units','K')]
#new_array['TMIN'].attrs = [('description','DAILY MINIMUM GRID SCALE TEMPERATURE'), ('units','K')]
#new_array['TMAX'].attrs = [('description','DAILY MAXIMUM GRID SCALE TEMPERATURE'), ('units','K')]
#new_array['PRCP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE PRECIPITATION'), ('units','mm')]


# Write new netcdf file
#new_array.to_netcdf(outdir+'/FOO.nc')

#del d, new_array	

#t1 = time.time()
#print("Total time to create this subset was:", t1 - t0, "seconds.")

