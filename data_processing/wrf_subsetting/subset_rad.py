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

# ------ Apply Temperature threshold to partition Rain/Snow-------# 

# ------ Aggregate to Daily; Create the new file --------# 


d.to_netcdf(outdir+'/SFC_EBAL.nc')
#
del d, new_array	
#
t1 = time.time()
print("Total time to create this subset was:", t1 - t0, "seconds.")
#
