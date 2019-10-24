import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
from PlotDifferenceMaps import PlotBarbs, PlotPar, PlotShape

# files to work w/
WRF = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/WY2010_WINDS.nc')
SeasonDic = {
	"COLD": ("2016-10-01","2017-04-01"),
	"WARM": ("2017-04-01","2017-09-30")
	}

PlistDic = {"WIND":PlotPar(var="Precip", cblab = 'm/s', scale=1, vmin = 1, vmax = 50, cmap='viridis', extend="max", ticklabels=True), 
            "WIND_DIR":PlotPar(var="Precip", cbFx=-.01, cblab= 'm/s', scale=1, vmin = 1, vmax = 10, cmap='viridis',extend="max", ticklabels=True)}

# calculate DIRUNAL wind speeds..
#DIURNAL = WRF['WIND_DIR'].loc["2016-10-01":"2017-04-01"].groupby('XTIME.hour').mean(dim='XTIME')


fig,ax = plt.subplots(1,2)
for col,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	Mean_V10= WRF['V10'].loc[start:end].mean(axis=0).values
	Mean_U10= WRF['U10'].loc[start:end].mean(axis=0).values
	# PLOTTING BELOW HERE
	# 
	PlotBarbs('test', Mean_U10, Mean_V10, fig, ax[col], PlistDic['WIND_DIR'])

ax[0].set_title('CoolSeason')
ax[1].set_title('WarmSeason')
#plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("EAST_WINDS_BARBS", dpi=600)
plt.cla()
plt.close(fig)

# clean up
del fig
del ax
plt.clf()
