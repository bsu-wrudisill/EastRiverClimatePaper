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
import pandas as pd 

def reduceDimension(vector):
	pca = decomposition.PCA(svd_solver = 'full', n_components=.95)
	pca.fit(vectors)
	vectors_t= pca.transform(vectors)
	print(pca.n_components_)
	return vectors_t

def cluster(vector):
	km = KMeans(n_clusters = n_clusters)
	clusters =  km.fit_predict(vectors_t)

def OptimalK(data, nrefs=3, maxClusters=15):
	"""
	Description: Calculates KMeans optimal K using Gap Statistic from Tibshirani, Walther, Hastie
		      The Gap statistic is basically just a measure of how far apart the sum of square
		      distance from cetner to all points is between kmeans and a random distribution 
	Params:
		data: ndarry of shape (n_samples, n_features)
		nrefs: number of sample reference datasets to create
		maxClusters: Maximum number of clusters to test for
	Returns: (gaps, optimalK)
	"""
	gaps = np.zeros((len(range(1, maxClusters)),))
	resultsdf = pd.DataFrame({'clusterCount':[], 'gap':[]})
	for gap_index, k in enumerate(range(1, maxClusters)):
		# Holder for reference dispersion results
		refDisps = np.zeros(nrefs)
		# For n references, generate random sample and perform kmeans getting resulting dispersion of each loop
		for i in range(nrefs):
			# Create new random reference set
			randomReference = np.random.random_sample(size=data.shape)
			# Fit to it
			km = KMeans(k)
			km.fit(randomReference)
			refDisp = km.inertia_
			refDisps[i] = refDisp
		# Fit cluster to original data and create dispersion
		km = KMeans(k)
		km.fit(data)
		origDisp = km.inertia_
		# Calculate gap statistic
		gap = np.log(np.mean(refDisps)) - np.log(origDisp)
		# Assign this loop's gap statistic to gaps
		gaps[gap_index] = gap

		resultsdf = resultsdf.append({'clusterCount':k, 'gap':gap}, ignore_index=True)
	return (gaps.argmax() + 1, resultsdf)  # Plus 1 because index of 0 means 1 cluster is optimal, index 2 = 3 clusters are optimal



if __name__ == '__main__':
	rows = 129 
	cols = 249 
	size = rows*cols 
	t = 1461 

	n_clusters = 10
	variable_wrapping = ['T','GP','Q','U','V']
	vectors = np.load('datacube.npy')
	# begin 
	vectors_t = reduceDimension(vectors)
	k,gap = OptimalK(vectors_t, nrefs=5, maxClusters=500)
	print(k, gap)
	plt.plot(gap.clusterCount, gap.gap)
	plt.savefig('gapstat')




