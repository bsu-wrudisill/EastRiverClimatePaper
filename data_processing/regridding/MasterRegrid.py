import pandas as pd
import xarray as xr
import xesmf as xe
import argparse
import glob 
import datetime
import os 
import pathlib

base = pathlib.Path('/home/wrudisill/scratch/EastRiverClimatePaper/data/geog/DEMS/')

reslist = [('GunnisonDEM_UTM13N_500mLatLonClipped.nc', '500m'),
	   ('GunnisonDEM_UTM13N_1kmLatLonClipped.nc', '1km'),
	   ('GunnisonDEM_UTM13N_4kmLatLonClipped.nc', '4km'),
	   ('GunnisonDEM_UTM13N_8kmLatLonClipped.nc', '8km')]

output_path = pathlib.Path('/home/wrudisill/scratch/EastRiverClimatePaper/DataGUNNISON/PRISM')

for resf,res in reslist:
	filepath = base.joinpath(resf)
	ds_out = xr.open_dataset(filepath)
	#for var in ['ppt']:
	for var in ['tmin','tmax','tmean']:
		# loop thru years 
		Range = range(2017)
		# loop thru 
		for YEAR in [2017]: 
			startDate = datetime.datetime(YEAR-1, 10, 1)
			dRange = pd.date_range(startDate,periods=365,freq='D')
			# output directory
			# target grid 
			#ds_out = xr.open_dataset('sample_wrf_file.nc')
			#ds_out.rename({'Band3': 'lon', 'Band2': 'lat'}, inplace=True)

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
				name = "PRISM_{}_stable_4kmD1_{}{}{}_bil.nc".format(var,year,mo,day)
				# read the files...
				print(year,mo,day)
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
			flist = glob.glob('temporary/*.nc')
			fullds = xr.open_mfdataset(flist, concat_dim='time')
			name='PRISM_{}_WY{}_{}.nc'.format(var,YEAR,res)
			fullds.to_netcdf(output_path.joinpath(name))
			for f in flist:
				try:
					os.remove(f)
				except:
					pass
	# done with res...
	ds_out.close()
