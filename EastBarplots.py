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
#sns.set_style("whitegrid")
#sns.pairplot(df, kind='reg')
# ---------- Plotting -----------# 
# seaborn plotting...
# pair-grid plot
g = sns.PairGrid(df, aspect=1.0)
g.map_diag(sns.kdeplot,shade=True)
g.map_offdiag(plt.scatter, color='gray', marker='+', alpha=.7, s=2, linewidth = 1.2)
g.map_offdiag(sns.kdeplot,shade=True, n_levels=10, shade_lowest=False,cmap='Reds',alpha=.7)

for i in range(4):
	for j in range(3):
		g.axes[i,j].set_xlim(250.,2000.)

for i in range(3):
	for j in range(4):
		g.axes[i,j].set_ylim(250.,2000.)

for i in range(4):
	g.axes[i,i].text(600, 410,  "{} (m)".format(list(totals.round(3))[i]), fontsize=12)

plt.savefig('pariplot.png', dpi=600)


#jp = sns.jointplot(x='hgt', y='prism', data=df, kind="kde")
#jp.plot_joint(plt.scatter, c='w', s=30, linewidth=1, marker='+',alpha=.5)
#jp.ax_joint.collections[0].set_alpha(0)
#jp.set_axis_labels("Elevation(m)", "Annual Precip(mm)")
#plt.savefig('prismtest')
