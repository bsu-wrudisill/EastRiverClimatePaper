import numpy as np
import xarray as xr
import glob 


#ds = xr.open_dataset("/scratch/wrudisill/PrecipWhitePaper/WRF/WY2010_WINDS.nc")
#q = xr.open_dataset("/scratch/wrudisill/PrecipWhitePaper/WRF/PRECIP/WY2017_PCPSUB.nc")
ds = xr.open_mfdataset(glob.glob("/scratch/leaf/share/CFSR_doeproject/700hpa/*.nc"))


## cfsr
rows = 129
cols = 249 
size = rows*cols 
t = 1461 
variables = 5 

## WRF 
#rows = 390
#cols = 348 
#size = rows*cols 
#t = 425 


vectors = np.empty((t, variables*size))

for i in range(t):
	row = np.hstack((ds.TMP_L100.values[i,:,:].flatten(), 
		         ds.HGT_L100.values[i,:,:].flatten(), 
			 ds.SPF_H_L100.values[i,:,:].flatten(), 
			 ds.U_GRD_L100.values[i,:,:].flatten(),  
			 ds.V_GRD_L100.values[i,:,:].flatten()))
	vectors[i,:] = row
	print(i)
	del row 
#vectors[np.where(np.isfinite(vectors) == False)] = 0.0  # ugh why 
np.save('datacube', vectors)
