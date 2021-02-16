import xarray as xr
import numpy as np
from varlist import var_list
import time
import glob
#from functions import HourlyPrecip
from mpl_toolkits.basemap import Basemap

t0 = time.time()

indir = '/scratch/wrudisill/PrecipWhitePaper/WRF/WY2017/d02/wrfout_d02*'
outdir = './'

# Select all files except last (which is a repeat of the first hour of the following water year) for each WY
files = sorted(glob.glob(indir))[:-1]

# open multi-file dataset (this function accepts unix wildcards)
d = xr.open_mfdataset(files, drop_variables=var_list, concat_dim='Time')

# get attributes
cenlat = nc.getncattr('CEN_LAT')
cenlon = nc.getncattr('CEN_LON')
cenlon = nc.getncattr('STAND_LON')
cenlat = nc.getncattr('MOAD_CEN_LAT')
lat1   = nc.getncattr('TRUELAT1')
lat2   = nc.getncattr('TRUELAT2')
#
# get the actual longitudes, latitudes, and corners
lons = nc.variables['XLONG'][0]
lats = nc.variables['XLAT'][0]
lllon = lons[0,0]
lllat = lats[0,0]
urlon = lons[-1,-1]
urlat = lats[-1,-1]
# Swap time and XTIME
d = d.swap_dims({'Time':'XTIME'})	
d['PRCP'] = d['RAINNC']
# Get mean/min/max by day of year for desired variables 

new_array = d[['U10','V10']]
new_array['WIND_DIR'] = d['U10']
new_array['WIND_DIR'].values = np.arctan2(d['U10'].values, d['V10'].values)



# Adjust some meta data
new_array['V10'].attrs = [('description','HOURLY V10'), ('units','m/s')]
new_array['U10'].attrs = [('description','HOURLY U10'), ('units','m/s')]
new_array['WIND_DIR'].attrs = [('description','HOURLY WIND_DIR'), ('units','rad')]
# assign attributes to the file 
new_array.attrs = d.attrs 

# Write new netcdf file
new_array.to_netcdf(outdir+'/WY2017_hourlyWINDS.nc')

del d, new_array	

t1 = time.time()
print("Total time to create this subset was:", t1 - t0, "seconds.")

