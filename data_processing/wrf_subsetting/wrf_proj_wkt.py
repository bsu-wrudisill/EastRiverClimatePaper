import salem
import xarray as xr
import os
import sys
import string
import osgeo.osr

# convert the salem pyproj4 to a wkt string 
ds = salem.open_xr_dataset(sys.argv[1])

srs = osgeo.osr.SpatialReference()
srs.ImportFromProj4(ds.pyproj_srs)
print(srs.ExportToWkt())
