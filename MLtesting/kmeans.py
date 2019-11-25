from sklearn.cluster import MiniBatchKMeans
from sklearn.manifold import TSNE
import seaborn as sns 
from matplotlib import pyplot as plt 
from sklearn import decomposition
import numpy as np
from sklearn import datasets
import xarray as xr
from sklearn.cluster import KMeans
from sklearn.cluster import SpectralClustering
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd 

def colorbar(mappable):
	ax = mappable.axes
	fig = ax.figure
	divider = make_axes_locatable(ax)
	cax = divider.append_axes("right", size="5%", pad=0.05)
	return fig.colorbar(mappable, cax=cax)


cold_season = pd.date_range("2016-10-01","2017-04-01", freq='6h')
warm_season = pd.date_range("2017-04-01","2017-10-01", freq='6h')
season = cold_season

n_clusters = 6
rows = 129 
cols = 249 
size = rows*cols 
t = 1461 

#n_pcacomp = 100

variable_wrapping = ['T','GP','Q','U','V']
vectors = np.load('datacube.npy')[0:len(season),:]

time_mean = vectors.mean(axis=0)


pca = decomposition.PCA(svd_solver = 'full', n_components=.95)
pca.fit(vectors)
vectors_t= pca.transform(vectors)

print(pca.n_components_)
### np.dot(vectors_t, pca.components_) + mean_mat == pca.inverse_transform(vectors_t) ----> TRUE
#
### ------- KMEANS  -------
km = KMeans(n_clusters = n_clusters)
clusters =  km.fit_predict(vectors_t)
#
#
x = np.arange(0, rows, 10)
y = np.arange(0, cols, 10)
xx,yy = np.meshgrid(x, y)
points = np.meshgrid(x,y)
#
## load coast 
#
coast = np.load('coastlines.npy')
coast = np.where(coast == 0, np.nan, 1)

for i in range(n_clusters):
	fig,ax = plt.subplots(2,2)
	indices = np.argwhere(clusters == i)[:,0]  # not sure why arghwere is [n,1]...
	collection = vectors[indices].mean(axis=0) 
	T = (collection[:size]-time_mean[:size]).reshape(rows,cols)
	Gp = (collection[size:size*2]-time_mean[size:size*2]).reshape(rows,cols)
	q = (collection[size*2:size*3]-time_mean[size*2:size*3]).reshape(rows,cols)
	u = collection[size*3:size*4].reshape(rows,cols)
	v = collection[size*4:size*5].reshape(rows,cols)
	
	# show
	imgp = ax[0,0].imshow(Gp, cmap='bwr', vmin=-100, vmax=100)
	immag = ax[1,1].imshow(np.sqrt(u**2+v**2), vmin=0,vmax=20.)
	imbarb = ax[1,1].quiver(yy,xx, u[points],v[points], scale=200, pivot='mid', width=.003)
	imt = ax[0,1].imshow(T, vmin=-5.,vmax=5., cmap='bwr')
	imq = ax[1,0].imshow(q, vmin=-.002, vmax=.002, cmap='bwr')
	colorbar(imt)
	colorbar(immag)
	colorbar(imgp)
	colorbar(imq)
	for ax in ax.flatten():
		ax.imshow(coast, alpha=.9, cmap='BuGn')

	plt.savefig('test{}'.format(i), dpi=600)
	plt.clf()
	del fig,ax
	print(i)
#





#km.cluster_centers_.shape
## transform the cluster centers back into the primary space 
#center_images = np.dot(km.cluster_centers_, pca.components_)
##
##
#fig,ax = plt.subplots(2,2)
##
##
##
##ver(xx, yy, u[xx],v[yy], scale=100, pivot='mid', width=.003)s
#for i,axx in enumerate(ax.flatten()):
#	u = center_images[i,:size].reshape(rows,cols)
#	v = center_images[i,size:size*2].reshape(rows,cols)
#	q = center_images[i,size*2:].reshape(rows,cols)
#	mag = np.sqrt(u**2+v**2)
#	axx.imshow(q)
#	
#
#
##plt.savefig('test')
#
## now do the inverse transform ....
##test = pca.inverse_transform(km.cluster_centers_)
###print(test.shape)
##
##
##
##
###plt.scatter(vectors_t[:,0], vectors_t[:,2], c=km, cmap='viridis')
###plt.show()
#plt.savefig('test')
