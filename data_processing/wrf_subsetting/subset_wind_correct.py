import xarray as xr
import numpy as np
from varlist import var_list
import time
import glob
#from functions import HourlyPrecip
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt 


t0 = time.time()

indir = '/scratch/wrudisill/PrecipWhitePaper/WRF/WY2017/d02/wrfout_d02*'
outdir = './'

# Select all files except last (which is a repeat of the first hour of the following water year) for each WY
files = sorted(glob.glob(indir))[:-1]


# ---- Open a sample wrf file and get all of the metadata needed to do the transformation ----# 
sample = xr.open_dataset('./sample_wrf_file.nc')

# get attributes
cenlat = sample.attrs['CEN_LAT']
cenlon = sample.attrs['CEN_LON']
cenlon = sample.attrs['STAND_LON']
cenlat = sample.attrs['MOAD_CEN_LAT']
lat1   = sample.attrs['TRUELAT1']
lat2   = sample.attrs['TRUELAT2']

# get the actual longitudes, latitudes, and corners
lons = sample['XLONG'][0]
lats = sample['XLAT'][0]
lllon = lons[0,0]
lllat = lats[0,0]
urlon = lons[-1,-1]
urlat = lats[-1,-1]

cosalpha = sample['COSALPHA'][0]
sinalpha = sample['SINALPHA'][0]

# Make our map which is on a completely different projection.
# To illustrate the problems, go to the upper right corner of the domain,
# or lower right corner in the southern hemisphere, where the distortion
# is the greatest

if urlat >= 0:
    map = Basemap(projection='cyl',llcrnrlat=urlat-5,urcrnrlat=urlat+3, llcrnrlon=urlon-10,urcrnrlon=urlon, resolution='h')
else:
    map = Basemap(projection='cyl',llcrnrlat=lllat,urcrnrlat=lllat, llcrnrlon=lllon,urcrnrlon=lllon, resolution='h')
                

x, y = map(lons[:,:], lats[:,:])
ur = sample.variables['U10'][0]
vr = sample.variables['V10'][0]
ve = vr * cosalpha + ur * sinalpha

urot, vrot = map.rotate_vector(ue,ve,lons,lats)

# do the plotting 
map.barbs(x, y, urot, vrot, color='blue',label='Rotated to latlon and then to map - CORRECT')

# bad barbs 
map.barbs(x, y, ue, ve, color='red',label='Rotated to latlon - insufficient')

plt.savefig('map')
#---- Open the real data and do the processing ----# 


# open multi-file dataset (this function accepts unix wildcards)
#d = xr.open_mfdataset(files, drop_variables=var_list, concat_dim='Time')
## Swap time and XTIME
#d = d.swap_dims({'Time':'XTIME'})	
## Get mean/min/max by day of year for desired variables 
#
#new_array = d[['U10','V10']]
#new_array['WIND_DIR'] = d['U10']
#new_array['WIND_DIR'].values = np.arctan2(d['U10'].values, d['V10'].values)
#
#
#
## Adjust some meta data
#new_array['V10'].attrs = [('description','HOURLY V10'), ('units','m/s')]
#new_array['U10'].attrs = [('description','HOURLY U10'), ('units','m/s')]
#new_array['WIND_DIR'].attrs = [('description','HOURLY WIND_DIR'), ('units','rad')]
## assign attributes to the file 
#new_array.attrs = d.attrs 
#
## Write new netcdf file
#new_array.to_netcdf(outdir+'/WY2017_hourlyWINDS.nc')
#
#del d, new_array	
#
#t1 = time.time()
#print("Total time to create this subset was:", t1 - t0, "seconds.")
#
