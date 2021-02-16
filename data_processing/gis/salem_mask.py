import salem
import xarray as xr
import os
import sys

# convert the salem pyproj4 to a wkt string 
ds = salem.open_xr_dataset('/scratch/wrudisill/EastRiverClimatePaper/data/geog/sample_wrf_file_CO.nc')

t2 = ds.T2.isel(Time=2)

#
East='/scratch/wrudisill/PrecipWhitePaper/gis_data/EastRiver_Shapefile.shp'
Gunnison='/scratch/wrudisill/EastRiverClimatePaper/data/geog/Gunnison.shp'
CoHeadwaters='/scratch/wrudisill/EastRiverClimatePaper/data/geog/CoHeadwaters.shp'

t2_roi = t2.salem.roi(shape=CoHeadwaters)

# simply assign all of the non-nan values a value of 1 
t2_roi = t2_roi*0 + 1.0

t2_roi.to_netcdf('CoHeadwatersMask.nc')
