import pandas as pd
import xarray as xr
import xesmf as xe
import argparse
import glob 
import datetime
import os 
from pathlib import Path
import numpy as np


datadir = Path('/scratch/wrudisill/EastRiverClimatePaper/data/NLDAS/')
outputdir = datadir.joinpath('tmp')
sampledir = Path('/scratch/wrudisill/EastRiverClimatePaper/data/geog/')

# as of...whatever version of nldas this is 
nldasvar= ['PRES_110_SFC',
	   'TMP_110_HTGL',
	   'U_GRD_110_HTGL',
	   'V_GRD_110_HTGL',
	   'SPF_H_110_HTGL',
	   'A_PCP_110_SFC_acc1h',
	   'NCRAIN_110_SFC_acc1h',
	   'CAPE_110_SPDY',
	   'DSWRF_110_SFC',
	   'DLWRF_110_SFC',
	   'PEVAP_110_SFC_acc1h']


# loop thru years 
Range = [2017]

ds_read = xr.open_dataset(sampledir.joinpath('sample_wrf_file_CO.nc'))
ds_read.rename({'XLONG': 'lon', 'XLAT': 'lat'}, inplace=True)
ds_read['lat'] = ds_read['lat'].sel(Time=0, drop=True)  # this way we drop the time dimension assigned to lat/lon
ds_read['lon'] = ds_read['lon'].sel(Time=0, drop=True)
x,y = ds_read.lat.shape




# loop thru 
for YEAR in Range: 
	startDate = datetime.datetime(YEAR-1, 10, 1)
	dRange = pd.date_range(startDate,periods=365*24,freq='h')

	# loop through each date, regrid, and assign to the correct timeslot 	
	for date in dRange:
		ymd = date.strftime('%Y%m%d')
		hr = date.strftime('%H')
		name_fmt = "NLDAS_FORA0125_H.A{}.{}00.002.nc".format(ymd,hr)
		infile = datadir.joinpath('2017', name_fmt)
		outfile = outputdir.joinpath(name_fmt)	
		
		if outfile.is_file():
			print('found %s', outfile)
		else:
			print('regridding ...')
			# read the files... 
			ds = xr.open_dataset(infile)

			ds.rename({'lon_110': 'lon', 'lat_110': 'lat'}, inplace=True)

			## create the regridding weight file 
			regridder = xe.Regridder(ds, ds_read, 'bilinear', reuse_weights=True)
		

			# create output dataset
			ds_out = xr.Dataset(coords={'lon': (['x', 'y'], ds_read['lat']),
						    'lat': (['x', 'y'], ds_read['lon']),
						    'time': [date]})
			# loop through variables 
			for var in nldasvar: 
				var_regrid = regridder(ds[var])
				ds_out[var] = (['time', 'x','y'], np.zeros((1,x,y)))
				ds_out[var][0,:,:] = var_regrid
				print('done with...{}'.format(var))
		
			# write file out
			print('write')
			ds_out.to_netcdf(datadir.joinpath('tmp',infile.name))

		## get data that we want to regrid from the input dataset 
		## regrid the data using the 'regridder' function we define above 
