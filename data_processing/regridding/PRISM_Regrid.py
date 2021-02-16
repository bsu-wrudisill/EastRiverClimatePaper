import pandas as pd
import xarray as xr
import xesmf as xe
import argparse
import glob 
import datetime
import os 

for var in ['ppt']:
	# loop thru years 
	Range = range(2012,2018)
	# loop thru 
	for YEAR in Range: 
		startDate = datetime.datetime(YEAR, 1, 1)
		dRange = pd.date_range(startDate,periods=365,freq='D')
		# output directory
		# target grid 
		ds_out = xr.open_dataset('sample_wrf_file.nc')
		ds_out.rename({'XLONG': 'lon', 'XLAT': 'lat'}, inplace=True)
		ds_out['lat'] = ds_out['lat'].sel(Time=0, drop=True)
		ds_out['lon'] = ds_out['lon'].sel(Time=0, drop=True)

		def zero_pad(x):
			a = str(x)
			if len(a) == 1:
				return '0'+a
			else:
				return a
		for date in dRange:
			year = date.year
			mo = zero_pad(date.month)
			day = zero_pad(date.day)
			name = "PRISM_{}_stable_4kmD2_{}{}{}_bil.nc".format(var,year,mo,day)
			# read the files... 
			ds = xr.open_dataset('/scratch/wrudisill/VerDatasets/PRISM/{}/{}/{}'.format(var,year,name))
			## create the regridding weight file 
			regridder = xe.Regridder(ds, ds_out, 'bilinear', reuse_weights=True)
			## get data that we want to regrid from the input dataset 
			dr = ds.Band1

			## regrid the data using the 'regridder' function we define above 
			dr_regrid = regridder(dr)
			dr_regrid.coords['time'] = pd.datetime(int(year), int(mo), int(day))
			dr_regrid.to_netcdf('./temporary/PRISM_{}_stable_4kmD2_{}{}{}_REGRID.nc'.format(var,year,mo,day))
			ds.close()
			ds_out.close()

		print('concatenating files..')
		# now concatenate those files..
		flist = glob.glob('temporary/*{}*.nc'.format(YEAR))
		fullds = xr.open_mfdataset(flist, concat_dim='time')
		fullds.to_netcdf('./{}/PRISM_{}_{}.nc'.format(var,var,YEAR))
		for f in flist:
			try:
				os.remove(f)
			except:
				pass

