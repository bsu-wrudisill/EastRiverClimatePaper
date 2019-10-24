import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
from PlotDifferenceMaps import PlotShape, PlotPar
import sys 


wrfvar = sys.argv[1]
# files to work w/
WRF = xr.open_dataset('/home/wrudisill/scratch/Xarray_subset/SFC_EBAL.nc')

SeasonDic = {
	"COLD": ("2016-10-01","2017-04-01"),
	"WARM": ("2017-04-01","2017-09-30")
	}

PlistDic = {"SWNORM":PlotPar(var="SWNORM", scale=1, vmin = 0, vmax = 600, cmap='viridis', cblab="w/m2",extend="max", ticklabels=True), 
	    "SWNORM_VAR":PlotPar(var="SWNORM", scale=1, vmin=0, vmax= 10000, cmap='magma_r', cblab="",extend="max", ticklabels=True),
	    "GLW":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 400, cmap='viridis', cblab="w/m2",extend="max", ticklabels=True),
	    "GLW_VAR":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 400, cmap='magma_r', cblab="w/m2",extend="max", ticklabels=True),
	    "LH":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 100, cmap='viridis', cblab="",extend="max", ticklabels=True),
	    "LH_VAR":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 1500, cmap='magma_r', cblab="",extend="max", ticklabels=True),
	    "HFX":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 200, cmap='viridis', cblab="",extend="max", ticklabels=True),
	    "HFX_VAR":PlotPar(var="GLW", scale=1, vmin = 0, vmax = 10000, cmap='magma_r', cblab="",extend="max", ticklabels=True)}


fig,ax = plt.subplots(2,2)
for col,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	MEAN = WRF[wrfvar].loc[start:end].mean(dim='XTIME')
	VVAR = WRF[wrfvar].loc[start:end].resample(XTIME='24H').mean(dim='XTIME').var(dim='XTIME')
	PlotShape('test', MEAN, fig, ax[0,col], PlistDic[wrfvar])
	PlotShape('test', VVAR, fig, ax[1,col], PlistDic[wrfvar+'_VAR'])

ax[0,0].set_title("ColdSeason")
ax[0,1].set_title("WarmSeason")
ax[0,0].set_ylabel("Avg")
ax[1,0].set_ylabel("Var")


plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("EAST_{}".format(wrfvar), dpi=600)
plt.cla()
plt.close(fig)
for axx in ax.flatten():
	plt.setp(axx.get_yticklabels(), backgroundcolor="white")
# clean up
del fig
del ax
plt.clf()
