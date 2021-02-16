import xarray as xr
import numpy as np


def HourlyPrecip(cum_precip, **kwargs):
	bucket_precip = kwargs.get("bucket_precip", 0)
	total_precip = cum_precip + bucket_precip * 100.0
	PRCP = np.zeros(total_precip.shape)
	for i in np.arange(1,PRCP.shape[0]):
		PRCP[i,:,:] = total_precip[i,:,:].values - total_precip[i-1,:,:].values
	return PRCP

def PrecipPartition(precip, temperature):
	# partition precpitation into rain and snow 
	# assign to the 'soli
	RAIN = np.where(temperature >= 273.15, precip, 0.0)
	SNOW = np.where(temperature < 273.15, precip, 0.0)
	return RAIN,SNOW

