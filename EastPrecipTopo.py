import salem
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
import pandas as pd 
import glob 

SeasonDic = {
"OND" : ("2016-10-01","2016-12-30"),
"JFM" : ("2017-01-01","2017-03-31"),
"AMJ" : ("2017-04-01","2017-06-30"),
"JAS" : ("2017-07-01","2017-09-30")
}

# ---------------- Read files ------------------# 
# -- WRF 
WRF = xr.open_dataset('/home/wrudisill/scratch/PrecipWhitePaper/WRF/PRECIP/WY2017_PCPSUB.nc')

# -- prism -- 
YEAR=2017
prismvar = 'ppt'
PRISM = xr.open_dataset('RegriddedData/PRISM/ppt/PRISM_WY2017_ppt.nc')

# -- daymet --
dayvar='prcp'
daymetFiles = glob.glob("/scratch/wrudisill/PrecipWhitePaper/RegriddedData/DAYMET/{}/*".format(dayvar))
DAYMET = xr.open_mfdataset(daymetFiles)

# -- mask files --
topo = xr.open_dataset('topography.nc')
maskFile = xr.open_dataset('EastRiverMask.nc')

# ----------- calculate watershed topography stats ------------# 
topo['MASK'] = topo['HGT'] # create a copy of the var 
topo['MASK'].values = maskFile['T2'].values
topo_mask  = topo.where(topo.MASK == 1)
wshed = topo_mask['HGT'].values.flatten()
wshed = wshed[~np.isnan(wshed)]

# ------------- mask the precip file ---------------------------# 
## read the mask. there's no time dimension... so we need to add one 
#timelen = WRF['PRCP'].shape[0]
#extendMask = np.expand_dims(maskFile['T2'].values, axis=0)
#extendMask = np.repeat(extendMask, timelen, axis=0)

def FlattenMask(var,mask):
	# returned a flattened array of 
	# desired locations 
	varmask = var.where(mask == 1) ## desired locations in mask ==1
	varflatten = varmask.values.flatten()
	varflatten = varflatten[~np.isnan(varflatten)]
	return varflatten

## assign the mask to the dataset so we can work w/ it easily 

#pcpEast = pcp.where(topo.MASK == 1)
#pcpEast = pcpEast.values.flatten() 
#pcpEast = pcpEast[~np.isnan(pcpEast)] 

wrfEast = FlattenMask(WRF['PRCP'].loc["2016-10-01":"2017-09-30"].sum(dim='XTIME'), topo.MASK)
prismEast = FlattenMask(PRISM['Band1'].loc["2016-10-01":"2017-09-30"].sum(dim='time'), topo.MASK)
dayEast = FlattenMask(DAYMET['prcp'].loc["2016-10-01":"2017-09-30"].sum(dim='time'), topo.MASK)

# ---------- Create a padas dataframe for plotting --------# 
df = pd.DataFrame({'WRF Precip (mm)':wrfEast,
		   'Prism Precip (mm)':prismEast,
		   'Daymet Precip (mm)':dayEast,
		   'Elevation (m)':wshed
		   })

totals = df.sum()/len(df.index)/1000. # convert to m of precip
sns.set(color_codes=True)
#
#
def percentile(n):
	def percentile_(x):
		return np.percentile(x,n)
	percentile_.__name__ = 'percentile_%s' % n
	return percentile_


df.set_index('Elevation (m)', inplace=True)
df = df.sort_index()
df2 = pd.melt(df.reset_index(), id_vars='Elevation (m)')
df2['Elevation Range (m)'] = pd.cut(df2['Elevation (m)'],np.arange(2500,4000,250))
df2.columns = ['Elevation (m)', 'variable', 'Precip (mm)', 'Elevation Range (m)']

# create a boxplot 
sns.boxplot(x='Elevation Range (m)', y='Precip (mm)', hue='variable', data=df2)
plt.savefig('PrecipBoxPlots', dpi=600)

#elevp = df.rolling(100).aggregate(["min", "median","mean","max", percentile(25), percentile(75)])
#fig,ax = plt.subplots()
# do the plotting 

#ax.plot(elevp.index, elevp['WRF Precip (mm)']['median'])
#ax.plot(elevp.index, elevp['WRF Precip (mm)']['mean'], linestyle=':')
#ax.fill_between(elevp.index, elevp['WRF Precip (mm)']['percentile_25'], elevp['WRF Precip (mm)']['percentile_75'], alpha=.25)
#
#ax.plot(elevp.index, elevp['Prism Precip (mm)']['median'])
#ax.plot(elevp.index, elevp['Prism Precip (mm)']['mean'], linestyle=':')
#ax.fill_between(elevp.index, elevp['Prism Precip (mm)']['percentile_25'], elevp['Daymet Precip (mm)']['percentile_75'], alpha=.25, color='red')
#
#ax.plot(elevp.index, elevp['Daymet Precip (mm)']['median'])
#ax.plot(elevp.index, elevp['Daymet Precip (mm)']['mean'], linestyle=':')
#ax.fill_between(elevp.index, elevp['Daymet Precip (mm)']['percentile_25'], elevp['Daymet Precip (mm)']['percentile_75'], alpha=.25, color='green')
#
