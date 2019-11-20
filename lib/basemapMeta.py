from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.patches import PathPatch
import numpy as np
from netCDF4 import Dataset
import xarray as xr
import datetime
import pandas as pd
from pathlib import Path

class wrfMeta:
	def __init__(self,wrfile):
		''''
		 class wrfMeta: Collect the relevant information from a WRFfile to pass 
		 		into a basemap plotting workflow. compute or ascribe 
				reasonable numbers for zoom scales, parallels/meridians, 
				and the mapscale length/range 
		'''
		ds =  Dataset(wrfile)
		self.xlon    = ds.variables['XLONG'][0, :, :]
		self.xlat    = ds.variables['XLAT'][0, :, :]
		self.HGT     = ds.variables['HGT'][0, :, :]

		# PLOTTING GOES BELOW HERE 
		#Read file attributes
		#atts         = file.ncattrsmap_proj     = ds.getncattr('MAP_PROJ')
		self.dx           = ds.getncattr('DX')
		self.dy           = ds.getncattr('DY')
		self.truelat1     = ds.getncattr('TRUELAT1')
		self.truelat2     = ds.getncattr('TRUELAT2')
		self.cen_lat      = ds.getncattr('MOAD_CEN_LAT')
		self.cen_lon      = ds.getncattr('STAND_LON')
		self.mx           = ds.getncattr('WEST-EAST_GRID_DIMENSION')
		self.my           = ds.getncattr('SOUTH-NORTH_GRID_DIMENSION')
		self.mz           = ds.getncattr('BOTTOM-TOP_GRID_DIMENSION')

		# ------- Calculations needed for map projection -----# 
		self.lat_ll = self.xlat[0,0]
		self.lat_ur = self.xlat[-1,-1]
		self.lon_ll = self.xlon[0,0]
		self.lon_ur = self.xlon[-1,-1]
		self.width_meters  = self.dx * (self.mx - 1)
		self.height_meters = self.dy * (self.my - 1)

		self.zoom_lat_top = 1.75   # latitude to shrink in from top of map
		self.zoom_lat_bot = 1.25   # latitude to shrink in from bottom of map
		self.zoom_lon_lft = 1.75   # '' ''  but for longitude from the left 
		self.zoom_lon_rgt = 1.5    # ''                   ''' from the right 
		
		self.bmap_args = { 'projection':'lcc',
			  'lon_0':    self.cen_lon,
			  'lat_0':    self.cen_lat,
			  'lat_1':    self.truelat1,
			  'lat_2':    self.truelat2,
			  'llcrnrlat':self.lat_ll+self.zoom_lat_top,
			  'urcrnrlat':self.lat_ur-self.zoom_lat_bot,
			  'llcrnrlon':self.lon_ll + self.zoom_lon_lft,
			  'urcrnrlon':self.lon_ur - self.zoom_lon_rgt,
			  'resolution':'h'}
			  #'ax' : ax  ## later on we have to add an axis object 
		
		# compute parallels in a nice way
		# np.arange(star,stop,by)
		self.parallels_by = .2     # spacing of parallels 
		self.meridians_by = .2     # spacing of meridians
		self.parallels = np.round(np.arange(np.round(self.lat_ll), np.round(self.lat_ur), .20), 2)
		self.meridians = np.round(np.arange(np.round(self.lon_ll), np.round(self.lon_ur), .20), 2)	

		# compute the mapscale dimensions in a ncie way (doubt it, lol)
		self.scale = {'lon': -116.25,
			      'lat': 42.85,
			      'lon0': -114.72,
			      'lat0':42.85,
			      'units':'km',
			      'length':200}

	# this will modify the instance when we run it 




class mapPlotter():
	def __init__(self,wrf_meta,**kwargs):
		# set the default params 
		self.wrf_meta = wrf_meta
		self.plot_type = kwargs.get('plot_type', 'scalar') 
		self.title = kwargs.get("title", 0)
		self.var   = kwargs.get("varname", None)
		self.cblab = kwargs.get("cblab", None)
		self.extend = kwargs.get("extend", "both")
		self.ticks = kwargs.get("ticks", None)
		self.ticklabels = kwargs.get("ticklabels", None)
		self.tickadjust = kwargs.get("tickadjust", 1.0)
		self.cbFx = kwargs.get("cbFx", 0)
		
		# Pcolor Parameters 
		self.pcolor_kwargs = {"cmap":plt.cm.get_cmap(kwargs.get("cmap", 'magma')),
			              "vmin":kwargs.get('vmin',None),
				      "vmax":kwargs.get('vmax',None)}
		
		# Wind Barb Parameters 	
		self.quiver_kwargs = {'scale':kwargs.get('quiver_scale',100),
				      'pivot':kwargs.get('quiver_pivot','mid'),
				      'width':kwargs.get('quiver_width',.003)}
		self.quiver_spacing = kwargs.get('quiver_spacing', 2)  # adjust density of quiver 
		
		# Shapefile Parameters 
		self.shppath = None
		self.shpname = None
		self.shape_kwargs = {"facecolor": None, 
				     "edgecolor": 'k', 
				     "linewidths": 1., 
				     "alpha": 0, 
				     "zorder": 2}
		# Point Label Stuff 
		self.points = []
		self.shppath = kwargs.get('shppath',None)	
	
	def addShape(self,ax):	
		shppath = Path(self.shppath)  # full path to shapefile 
		shpname = str(shppath.name)
		shpdir = str(shppath.parent)
		m = Basemap(**self.wrf_meta.bmap_args)
		
		# plot the shapefile if there is one 
		m.readshapefile(str(shppath), shpname)
		patches = []
		for shape in getattr(m, shpname):
			patches.append(Polygon(np.array(shape), True) )
			ax.add_collection(PatchCollection(patches, **self.shape_kwargs))
	
	def createPlot(self, ax, data):
		# ax specifies the matplotlib axis object to plot on
		# data is either a 2-d ndarrary or a tuple. the tuple 
		# is assumed to be u,v = data if the plot type is 'barb'
		
		# write out the plot for a given axis 
		assert self.wrf_meta != None, 'no WRF metadata supplied' 

		if self.plot_type == 'barb':
			assert type(data) == tuple
			u,v = data
			assert (type(u) == np.ndarray) & (type(v) == np.ndarray)

		elif self.plot_type == 'scalar':
			assert type(data) == np.ndarray, type(data)
			assert data.ndim == 2, 'data is not 2-d; ndim = {}'.format(data.ndim) 
			scalar = data 
		
		# create the basemap object 
		m = Basemap(**self.wrf_meta.bmap_args)
		x, y = m(self.wrf_meta.xlon, self.wrf_meta.xlat) # get the ...whatever x an y are
		
		# draw the parallels 
		m.drawparallels(self.wrf_meta.parallels, fontsize=5, linewidth=.8, color='white')
		m.drawmeridians(self.wrf_meta.meridians, fontsize=4, linewidth=.8, color='white')
		
		# plot the data variable 
		if self.plot_type == 'barb':
			yy = np.arange(0, y.shape[0], self.quiver_spacing)
			xx = np.arange(0, x.shape[1], self.quiver_spacing)
			points = np.meshgrid(yy, xx)
			print(self.quiver_kwargs)
			barbs = m.quiver(x[points],y[points],u[points],v[points], **self.quiver_kwargs)
		
		if self.plot_type == 'scalar':
			colormap = m.pcolor(x, y, scalar, **self.pcolor_kwargs)
		
	def addAxes(self, ax, **kwargs):
		# add the appropriate labels, etc to the plot 
		m = Basemap(**self.wrf_meta.bmap_args)



if __name__=='__main__':
	# open up data 
	# wind 
	dataDir = Path('/home/wrudisill/scratch/EastRiverClimatePaper/data')
	ds1 = xr.open_dataset(str(dataDir.joinpath('WY2010_WINDS.nc')))
	U = ds1["U10"].loc['2017-01-01'].values
	V = ds1["V10"].loc['2017-01-01'].values
	
	# temp	
	ds2 = xr.open_dataset(str(dataDir.joinpath('WY2017_PCPSUB.nc')))
	t = ds2['TMEAN'].values[0,:,:]
	
	# create plots 
	fig,ax = plt.subplots()
	
	# read metadata 
	wm = wrfMeta('../data/sample_wrf_file_CO.nc')
	shppath = '/home/wrudisill/scratch/EastRiverClimatePaper/data/EastRiver_Shapefile'
	wind = mapPlotter(wm, plot_type='barb', shppath=shppath)
	temp = mapPlotter(wm, plot_type='scalar')
	
#	temp.createPlot(ax=ax, data=t)   # share the same axis ??? 
	temp.createPlot(ax=ax, data=t)
	wind.addShape(ax=ax)
	wind.createPlot(ax=ax, data=(U,V))

	#wind.addShape(m, ax) 
	plt.savefig('test')	



