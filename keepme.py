import xarray as xr
from matplotlib import pyplot as plt
import glob
from PlotDifferenceMaps import *

# read in the daymet 
prismFiles = glob.glob("/scratch/wrudisill/PrecipWhitePaper/RegriddedData/PRISM/ppt/PRISM_WY2017_PPT.nc")
PRISM = xr.open_mfdataset(prismFiles)

# read in the WRF files 
wrfFile="/scratch/wrudisill/PrecipWhitePaper/WRF/PRECIP/WY2017_PCPSUB.nc"
WRF = xr.open_dataset(wrfFile)

SeasonDic = {
"OND" : ("2016-10-01","2016-12-30"),
"JFM" : ("2017-01-01","2017-03-31"),
"AMJ" : ("2017-04-01","2017-06-30"),
"JAS" : ("2017-07-01","2017-09-30") 
}

wrfvar = "PRCP"
prismvar = "Band1"

fig,ax = plt.subplots(4,3)
for row,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	TotalWRF_Prcp = WRF[wrfvar].loc[start:end].sum(axis=0)
	TotalPRISM_Prcp = PRISM[prismvar].loc[start:end].sum(axis=0)
	diff = TotalWRF_Prcp - TotalPRISM_Prcp

	# PLOTTING BELOW HERE
	plist = PlotPar(var="Precip", scale=1, vmin = 0, vmax = 750, cmap='viridis', cblab="mm",extend="max", ticklabels=True)

	plist_diff = PlotPar(var="Precip", scale=1, vmin = -250, vmax = 250, cmap='bwr', cblab="mm",extend="max", ticklabels=True)

	PlotShape('test', TotalWRF_Prcp, fig, ax[row,0], plist)
	PlotShape('test', TotalPRISM_Prcp, fig, ax[row,1], plist)
	PlotShape('test', diff, fig, ax[row,2], plist_diff)
ax[0,0].set_title("WRF")
ax[0,1].set_title("PRISM")
ax[0,2].set_title("WRF-PRISM")


plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("PRISM_PRECIP_ALL".format(key), dpi=600)
plt.cla()
plt.close(fig)
print('done with {}'.format(key))
