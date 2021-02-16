import xarray as xr
import numpy as np
from varlist import var_list
import time
import glob
from functions import HourlyPrecip, PrecipPartition

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
d['SNOW_IND'] = d['RAINNC']
d['RAIN_IND'] = d['RAINNC']
d['SNOW_MP'] = d['RAINNC']
d['GRAUPEL_MP'] = d['RAINNC']
d['RAIN_MP'] = d['RAINNC']

# ------ Apply Temperature threshold to partition Rain/Snow-------# 
d['PRCP'].values = HourlyPrecip(d['RAINNC'],bucket_precip = d['I_RAINNC'])
RAIN,SNOW = PrecipPartition(d['PRCP'], d['T2'])
# assign the new vars 
d['SNOW_IND'].values = SNOW
d['RAIN_IND'].values = RAIN


# ------- Apply WRF Microphysics ------# 
d['GRAUPEL_MP'].values = HourlyPrecip(d['GRAUPELNC'])
d['SNOW_MP'].values = HourlyPrecip(d['SNOWNC'])
d['RAIN_MP'].values = d['PRCP'] - (d['GRAUPEL_MP'] + d['SNOW_MP']) 


# ------ Aggregate to Daily; Create the new file --------# 
new_array = d[['PRCP','SNOW_IND','RAIN_IND','SNOW_MP','GRAUPEL_MP','RAIN_MP']].resample(XTIME = '24H').sum(dim = 'XTIME')
## Adjust some meta data
new_array['PRCP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE PRECIPITATION'), ('units','mm')]
#
new_array['SNOW_MP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE SNOW--THOMPSON MICROPHYS'), ('units','mm')]

new_array['GRAUPEL_MP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE GRAUPEL--THOMPSON MICROPHYS'), ('units','mm')]

new_array['RAIN_MP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE LIQUID RAIN--THOMPSON MICROPHYS'), ('units','mm')]
## Write new netcdf file

# 
new_array['SNOW_IND'].attrs = [('description','DAILY ACCUMULATED GRID SCALE FROZEN PRECIP--0C threshold'), ('units','mm')]


new_array['RAIN_IND'].attrs = [('description','DAILY ACCUMULATED GRID SCALE LIQUID RAIN--0C threshold'), ('units','mm')]

new_array.to_netcdf(outdir+'/WY2017_PCPSUB.nc')
#
del d, new_array	
#
t1 = time.time()
print("Total time to create this subset was:", t1 - t0, "seconds.")
#
