import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
from PlotDifferenceMaps import PlotBarbs, PlotPar, PlotShape

# files to work w/
WRF = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/WY2017_hourlyWINDS.nc')
SeasonDic = {
	"COLD": ("2016-10-01","2017-04-01"),
	"WARM": ("2017-04-01","2017-09-30")
	}

PlistDic = {"WIND":PlotPar(var="Precip", scale=1, vmin = 1, vmax = 50, cmap='viridis', extend="max", ticklabels=True), 
            "WIND_DIR":PlotPar(var="Precip", scale=1, vmin = 1, vmax = 10, cmap='viridis',extend="max", ticklabels=True)}

# calculate DIRUNAL wind speeds..
#DIURNAL = WRF['WIND_DIR'].loc["2016-10-01":"2017-04-01"].groupby('XTIME.hour').mean(dim='XTIME')

WRF["MAG"] = WRF["WIND_DIR"]
WRF["MAG"].values = np.sqrt(WRF["U10"]**2 + WRF["V10"]**2)

fig,ax = plt.subplots(2,2)
for row,key in enumerate(list(SeasonDic)):
	start,end = SeasonDic[key]
	#Mean_V10= WRF['V10'].loc[start:end].mean(axis=0).values
	#Mean_U10= WRF['U10'].loc[start:end].mean(axis=0).values
	# PLOTTING BELOW HERE
	DIR_VAR = WRF['WIND_DIR'].loc[start:end].var(dim='XTIME')
	MAG_VAR = WRF['MAG'].loc[start:end].var(dim='XTIME')
	# 
	PlotShape('test', MAG_VAR, fig, ax[0,row], PlistDic['WIND'])
	PlotShape('test', DIR_VAR, fig, ax[1,row], PlistDic['WIND_DIR'])

ax[0,0].set_title('CoolSeason')
ax[0,1].set_title('WarmSeason')
ax[0,0].set_ylabel('Var Wind Speed')
ax[1,0].set_ylabel('Var Wind Direction')
plt.subplots_adjust(hspace=0,wspace=0)
plt.savefig("EAST_WINDS_VAR", dpi=600)
plt.cla()
plt.close(fig)

# clean up
del fig
del ax
plt.clf()
