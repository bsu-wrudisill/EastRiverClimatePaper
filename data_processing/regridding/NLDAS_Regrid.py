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

base = Path('/home/wrudisill/scratch/EastRiverClimatePaper/data/geog/DEMS/')

reslist = [('GunnisonDEM_UTM13N_500mLatLonClipped.nc', '500m'),
	   ('GunnisonDEM_UTM13N_1kmLatLonClipped.nc', '1km'),
	   ('GunnisonDEM_UTM13N_4kmLatLonClipped.nc', '4km'),
	   ('GunnisonDEM_UTM13N_8kmLatLonClipped.nc', '8km')]
#ds_read = xr.open_dataset(sampledir.joinpath('sample_wrf_file_CO.nc'))
#ds_read.rename({'XLONG': 'lon', 'XLAT': 'lat'}, inplace=True)
#ds_read['lat'] = ds_read['lat'].sel(Time=0, drop=True)  # this way we drop the time dimension assigned to lat/lon
#ds_read['lon'] = ds_read['lon'].sel(Time=0, drop=True)

#
# loop thru 
for resf,res in reslist:
	filepath = base.joinpath(resf)
	ds_read = xr.open_dataset(filepath)
	x,y = ds_read.lat.shape
	for YEAR in Range: 
		startDate = datetime.datetime(YEAR-1, 10, 1)
		dRange = pd.date_range(startDate,periods=365*24,freq='h')

		# loop through each date, regrid, and assign to the correct timeslot 	
		for date in dRange:
			ymd = date.strftime('%Y%m%d')
			hr = date.strftime('%H')
			name_fmt = "NLDAS_FORA0125_H.A{}.{}00.002.nc".format(ymd,hr)
			infile = datadir.joinpath('2017', name_fmt)
				
			# read the files... 
			try:
				ds = xr.open_dataset(infile)
			except FileNotFoundError:
				print('%s not found',infile)
				continue

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
	
	# now write out the files...
	dropvar= ['PRES_110_SFC',
		   'U_GRD_110_HTGL',
		   'V_GRD_110_HTGL',
		   'SPF_H_110_HTGL',
		   'NCRAIN_110_SFC_acc1h',
		   'CAPE_110_SPDY',
		   'DSWRF_110_SFC',
		   'DLWRF_110_SFC',
		   'PEVAP_110_SFC_acc1h']

	startDate = datetime.datetime(2016, 10, 1)
	dRange = pd.date_range(startDate,periods=365*24,freq='h')

	# loop through each date, regrid, and assign to the correct timeslot 	
	#found_files = 0


	## nldas t2 varname
	t2 = 'TMP_110_HTGL'
	prcp = 'A_PCP_110_SFC_acc1h'

	files = list(datadir.glob('NLDAS_*'))
	files.sort()

	d = xr.open_mfdataset(files, drop_variables=dropvar ,concat_dim='time')

	new_array = d[[t2]].resample(time = '24H').mean(dim = 'time') # create daily means of few variables
	new_array['TMIN'] = d[t2].resample(time = '24H').min(dim = 'time') # create daily minimum temperature
	new_array['TMAX'] = d[t2].resample(time = '24H').max(dim = 'time')  # create daily maximum temperature
	new_array = new_array.rename({t2 : 'TMEAN'}) # rename T2 as TMEAN
	new_array['PRCP'] = d[prcp].resample(time = '24H').sum(dim = 'time')

	## Adjust some meta data
	new_array['TMEAN'].attrs = [('description','DAILY MEAN GRID SCALE TEMPERATUTE'), ('units','K')]
	new_array['TMIN'].attrs = [('description','DAILY MINIMUM GRID SCALE TEMPERATURE'), ('units','K')]
	new_array['TMAX'].attrs = [('description','DAILY MAXIMUM GRID SCALE TEMPERATURE'), ('units','K')]
	new_array['PRCP'].attrs = [('description','DAILY ACCUMULATED GRID SCALE PRECIPITATION'), ('units','mm')]


	new_array.to_netcdf('2017NLDAS_{}.nc'.format(res))
			## get data that we want to regrid from the input dataset 
			## regrid the data using the 'regridder' function we define above 
