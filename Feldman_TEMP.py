import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
from PlotDifferenceMaps import PlotShape, PlotPar

# files to work w/
WRF = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/PRECIP/WY2017_PCPSUB.nc')
SeasonDic = {
	"COLD": ("2016-10-01","2017-04-01"),
	"WARM": ("2017-04-01","2017-09-30")
	}

PlistDic = {"PRCP":PlotPar(var="Precip", scale=1, vmin = 0, vmax = 750, cmap='viridis', cblab="mm",extend="max", ticklabels=True), 
	    "TMAX":PlotPar(var="t", scale=1, vmin = 0, vmax = 40, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "TMIN":PlotPar(var="t", scale=1, vmin = -10, vmax = 30, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "TMEAN":PlotPar(var="t", scale=1, vmin = -10, vmax = 30, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "TVAR":PlotPar(var="t", scale=1, cmap='Reds', vmin= 20, vmax=70, cblab=r'$c^2$',extend="max", ticklabels=True)
	    }

wrfvar='TMEAN'
fig,ax = plt.subplots(2,2)
for col,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	T2 = WRF[wrfvar] - 273.15 # convert to C...
	Tmean = T2.loc[start:end].mean(axis=0)
	Tvar  = T2.loc[start:end].var(axis=0) 
	# PLOTTING BELOW HERE
	PlotShape('test', Tmean, fig, ax[0,col], PlistDic[wrfvar])
	PlotShape('test', Tvar, fig, ax[1,col], PlistDic["TVAR"])

ax[0,0].set_title("ColdSeason")
ax[0,1].set_title("WarmSeason")
ax[0,0].set_ylabel("Avg. T2")
ax[1,0].set_ylabel("Var. T2")


plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("EAST_TEMP", dpi=600)
plt.cla()
plt.close(fig)
for axx in ax.flatten():
	plt.setp(axx.get_yticklabels(), backgroundcolor="white")
# clean up
del fig
del ax
plt.clf()
