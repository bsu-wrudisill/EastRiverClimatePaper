#!/bin/bash

module load gdal

#1 is the .bil file
inname=$1
outname=${inname%.bil}

# unzup the file 
gdal_translate -a_srs EPSG:4269 -a_nodata -9999.0 -sds -ot Float32 -of NetCDF $inname $outname
