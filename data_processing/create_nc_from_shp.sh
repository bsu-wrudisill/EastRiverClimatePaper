
f=$1
noext="${f%.*}"

ogr2ogr -t_srs "+proj=merc +lat_ts=38.76100158691406 +lon_0=-107.09716796875 +x_0=0 +y_0=0 +a=6370000 +b=6370000 +units=m +no_defs" ${noext}_reproj.shp $f

gdal_rasterize -te -50605.048 -377500.000 297394.952 12500.000 -of netcdf -a GAGE_ID -tr 1000.0 1000.0 ${noext}_reproj.shp  ${noext}.nc -ot Int64
