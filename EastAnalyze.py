import salem
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 

SeasonDic = {
"OND" : ("2016-10-01","2016-12-30"),
"JFM" : ("2017-01-01","2017-03-31"),
"AMJ" : ("2017-04-01","2017-06-30"),
"JAS" : ("2017-07-01","2017-09-30")
}

# files to work w/
ds = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/WY2017_RAINSNOW.nc')
timelen = ds['PRCP'].shape[0]
#
#
## read the mask. there's no time dimension... so we need to add one 
maskFile = xr.open_dataset('EastRiverMask.nc')
extendMask = np.expand_dims(maskFile['T2'].values, axis=0)
extendMask = np.repeat(extendMask, timelen, axis=0)
#
## assign the mask to the dataset so we can work w/ it easily 
ds['MASK'] = ds['PRCP']
ds['MASK'].values = extendMask


EastRiv = ds.where(ds.MASK == 1) 

moGroup = EastRiv.groupby('XTIME.month').sum()
moGroup['RSFRAC_MP'] = moGroup['SNOW_MP']/moGroup['PRCP']
moGroup['RSFRAC_IND'] = moGroup['SNOW_IND']/moGroup['PRCP']

fig, ax = plt.subplots(1)
# PLOTTING
ax.set_title('East River Monthly Snow Fraction')
ax.plot(moGroup['RSFRAC_MP'], label='Microphysics')
ax.plot(moGroup['RSFRAC_IND'], label='0C Threshold')
ax.legend()
plt.savefig('testme')

#mp = EastRiv['SNOW_MP'].loc["2016-12-01":"2017-02-28"].sum(axis=0).compute()
#plt.imshow(mp)
#plt.savefig('testme')
