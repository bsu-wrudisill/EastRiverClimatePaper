import xarray as xr
from matplotlib import pyplot as plt
import glob
from PlotDifferenceMaps import *
# read in the daymet 

# read in the WRF files 
wrfFile="/scratch/wrudisill/PrecipWhitePaper/WRF/WY2017_RAINSNOW.nc"
WRF = xr.open_dataset(wrfFile)

SeasonDic = {
"OND" : ("2016-10-01","2016-12-30"),
"JFM" : ("2017-01-01","2017-03-31"),
"AMJ" : ("2017-04-01","2017-06-30"),
"JAS" : ("2017-07-01","2017-09-30") 
}

# build the figure...
fig,ax = plt.subplots(4,3)


for row,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	SNOW_MP = WRF['SNOW_MP'].loc[start:end].sum(axis=0)
	SNOW_IND = WRF['SNOW_IND'].loc[start:end].sum(axis=0)
	diff = SNOW_MP - SNOW_IND 
	
	# PLOTTING BELOW HERE
	plist = PlotPar(var="Precip", scale=1, vmin = 0, vmax = 25, cmap='viridis', cblab="mm",extend="max", ticklabels=True)

	plist_diff = PlotPar(var="Precip", scale=1, vmin = -5, vmax = 5, cmap='bwr', cblab="mm",extend="max", ticklabels=True)

	PlotShape('test', SNOW_MP, fig, ax[row,0], plist)
	PlotShape('test', SNOW_IND, fig, ax[row,1], plist)
	PlotShape('test', diff, fig, ax[row, 2], plist_diff)

#fig.set_size_inches(10,10)
# end loop
ax[0,0].set_title("THOMPSON-MICRO")
ax[0,1].set_title("0C THRESHOLD")
ax[0,2].set_title("MICRO - THRESHOLD")

plt.subplots_adjust(hspace=0,wspace=.1)
plt.savefig("SNOW_PRECIP_ALL".format(key), dpi=600)
plt.cla()
plt.close(fig)
print('done with {}'.format(key))
