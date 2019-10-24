import xarray as xr
from matplotlib import pyplot as plt
import glob
from PlotDifferenceMaps import *
import sys

wrfvar = sys.argv[1] #TMIN, TMAX, PRCP
prismvar = sys.argv[2]

# read in the daymet 
YEAR=2017

pbase='/scratch/wrudisill/PrecipWhitePaper/RegriddedData/PRISM/{}/PRISM_{}_{}.nc'
prismFiles = glob.glob(pbase.format(prismvar,prismvar,YEAR-1)) + glob.glob(pbase.format(prismvar,prismvar,YEAR))  

PRISM = xr.open_mfdataset(prismFiles, concat_dim='time')
PRISM=PRISM.sortby('time')

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
#prismvar = 'prcp' #'prcp'


PlistDic = {"PRCP":PlotPar(var="Precip", scale=1, vmin = 0, vmax = 750, cmap='viridis', cblab="mm",extend="max", ticklabels=True), 
	    "PRCP_DIFF":PlotPar(var="Precip", scale=1, vmin = -250, vmax = 250, cmap='bwr', cblab="mm",extend="max", ticklabels=True),
	    "TMAX":PlotPar(var="t", scale=1, vmin = 0, vmax = 40, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "TMAX_DIFF":PlotPar(var="t", scale=1, vmin = -10, vmax = 10, cmap='bwr', cblab="c",extend="max", ticklabels=True),
	    "TMIN":PlotPar(var="t", scale=1, vmin = -10, vmax = 30, cmap='magma_r', cblab="c",extend="max", ticklabels=True),
	    "TMIN_DIFF":PlotPar(var="t", scale=1, vmin = -10, vmax = 10, cmap='bwr', cblab="c",extend="max", ticklabels=True)}

fig,ax = plt.subplots(4,3)

for row,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	TotalWRF = WRF[wrfvar].loc[start:end].mean(axis=0) - 273.15
	TotalPRISM = PRISM['Band1'].loc[start:end].mean(axis=0)
	diff = TotalWRF - TotalPRISM

	# PLOTTING BELOW HERE
	PlotShape('test', TotalWRF, fig, ax[row,0], PlistDic[wrfvar])
	PlotShape('test', TotalPRISM, fig, ax[row,1], PlistDic[wrfvar])
	PlotShape('test', diff, fig, ax[row,2], PlistDic[wrfvar+'_DIFF'])


ax[0,0].set_title("WRF")
ax[0,1].set_title("PRISM")
ax[0,2].set_title("WRF-PRISM")

plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("{}_PRISM".format(wrfvar,key), dpi=600)
plt.cla()
plt.close(fig)
print('done with {}'.format(key))
# clean up
del fig
del ax
del TotalWRF
del TotalPRISM
plt.clf()

