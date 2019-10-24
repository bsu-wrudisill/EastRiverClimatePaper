import numpy as np

def hillshade(array, azimuth, angle_altitude):

	# Source: http://geoexamples.blogspot.com.br/2014/03/shaded-relief-images-using-gdal-python.html
	x, y = np.gradient(array)
	slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
	aspect = np.arctan2(-x, y)
	azimuthrad = azimuth*np.pi / 180.
	altituderad = angle_altitude*np.pi / 180.
	shaded = np.sin(altituderad) * np.sin(slope) \
	+ np.cos(altituderad) * np.cos(slope) \
	* np.cos(azimuthrad - aspect)
	return 255*(shaded + 1)/2
