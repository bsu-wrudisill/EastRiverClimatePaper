import pandas as pd
import xarray as xr
import xesmf as xe
import argparse
import glob 
import datetime
import os 
from pathlib import Path
import numpy as np


datadir = Path('/scratch/wrudisill/EastRiverClimatePaper/data/NLDAS/tmp')

#otherdir = Path('/scratch/wrudisill/VerDatasets/NLDAS/NLDAS_grib/')

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


new_array.to_netcdf('2017NLDAS.nc')
