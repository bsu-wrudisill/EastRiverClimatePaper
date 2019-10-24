import salem
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 

# files to work w/
#ds = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/WY2017_RAINSNOW.nc')
#timelen = ds['PRCP'].shape[0]
#
#
## read the mask. there's no time dimension... so we need to add one 
#maskFile = xr.open_dataset('EastRiverMask.nc')
#extendMask = np.expand_dims(maskFile['T2'].values, axis=0)
#extendMask = np.repeat(extendMask, timelen, axis=0)
#
## assign the mask to the dataset so we can work w/ it easily 
#ds['MASK'] = ds['PRCP']
#ds['MASK'].values = extendMask


# --- WOW THIS IS EASY---
East='/scratch/wrudisill/PrecipWhitePaper/gis_data/EastRiver_Shapefile.shp'
shp = salem.read_shapefile(East)
g = salem.GoogleVisibleMap(x=[shp.min_x, shp.max_x], y=[shp.min_y, shp.max_y+.1], scale=2, maptype='satellite')  # try out also: 'terrain'
ggl_img = g.get_vardata()

fig,ax = plt.subplots(1)

sm = salem.Map(g.grid, factor=2, countries=False)
sm.set_shapefile(shp, facecolor=(1,0,0,0.1))  # add basin outline 
sm.set_rgb(ggl_img)
#sm.set_scale_bar(location=(1.0, 1.0))  # add scale

sm.visualize(ax=ax)  # plot it
ax.set_title('East River Watershed')
plt.savefig("EastRiv_GoogleImg", dpi=800)
