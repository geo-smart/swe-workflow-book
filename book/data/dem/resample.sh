#!/bin/bash
# This script will reproject and resample the western US DEM, clip it, to match the exact spatial extent and resolution as the template TIFF.

cd  ./book/data/dem/

mkdir template_shp/

cp western_us_geotiff_template.tif template_shp/

# Generate the template shape
gdaltindex template.shp template_shp/*.tif

# Reproject and resample the DEM
gdalwarp -s_srs EPSG:4326 -t_srs EPSG:4326 -tr 0.036 0.036 -cutline template.shp -crop_to_cutline -overwrite output_4km.tif output_4km_clipped.tif

# Check the output
gdalinfo output_4km_clipped.tif
