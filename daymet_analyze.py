import xarray as xr
from matplotlib import pyplot as plt
import glob
from PlotDifferenceMaps import *
import sys

wrfvar = sys.argv[1] #TMIN, TMAX, PRCP
dayvar = sys.argv[2] #tmin, tmax, prcp

# read in the daymet 
daymetFiles = glob.glob("/scratch/wrudisill/PrecipWhitePaper/RegriddedData/DAYMET/{}/*".format(dayvar))
DAYMET = xr.open_mfdataset(daymetFiles)

# read in the WRF files 
wrfFile="/scratch/wrudisill/PrecipWhitePaper/WRF/PRECIP/WY2017_PCPSUB.nc"
WRF = xr.open_dataset(wrfFile)

SeasonDic = {
"OND" : ("2016-10-01","2016-12-30"),
"JFM" : ("2017-01-01","2017-03-31"),
"AMJ" : ("2017-04-01","2017-06-30"),
"JAS" : ("2017-07-01","2017-09-30")
}

#wrfvar = 'PRCP' #'PRCP'
#dayvar = 'prcp' #'prcp'


PlistDic = {"prcp":PlotPar(var="Precip", scale=1, vmin = 0, vmax = 750, cmap='viridis', cblab="mm",extend="max", ticklabels=True), 
	    "prcp_diff":PlotPar(var="Precip", scale=1, vmin = -250, vmax = 250, cmap='bwr', cblab="mm",extend="max", ticklabels=True),
	    "tmax":PlotPar(var="t", scale=1, vmin = 0, vmax = 40, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "tmax_diff":PlotPar(var="t", scale=1, vmin = -10, vmax = 10, cmap='bwr', cblab="c",extend="max", ticklabels=True),
	    "tmin":PlotPar(var="t", scale=1, vmin = -10, vmax = 30, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "tmin_diff":PlotPar(var="t", scale=1, vmin = -10, vmax = 10, cmap='bwr', cblab="c",extend="max", ticklabels=True)}


fig,ax = plt.subplots(4,3)


for row,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	TotalWRF = WRF[wrfvar].loc[start:end].sum(axis=0) 
	TotalDAYMET = DAYMET[dayvar].loc[start:end].sum(axis=0)
	diff = TotalWRF - TotalDAYMET

	# PLOTTING BELOW HERE
	
	PlotShape('test', TotalWRF, fig, ax[row,0], PlistDic[dayvar])
	PlotShape('test', TotalDAYMET, fig, ax[row,1], PlistDic[dayvar])
	PlotShape('test', diff, fig, ax[row,2], PlistDic[dayvar+'_diff'])


ax[0,0].set_title("WRF")
ax[0,1].set_title("DAYMET")
ax[0,2].set_title("WRF-DAYMET")

plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("{}_DAYMET".format(wrfvar,key), dpi=600)
plt.cla()
plt.close(fig)
print('done with {}'.format(key))
# clean up
del fig
del ax
del TotalWRF
del TotalDAYMET
plt.clf()

