# Analysis for MapIR Data using georectified images

import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from Analysis.mapir_png import MapIR_png
from Data_Paths.data_filepaths import *

# Location of Georectified MapIR image
image_filepath = active_dataset+'/georect.png'
output_filepath =  active_dataset

image = MapIR_png(image_filepath)

# NDVI uses the Red and NIR bands to provide a measure of vegetation health
image.NDVI(display=True, save=True)

# GNDVI may be more sensitive to variations in chlorophyll content than NDVI
image.GNDVI(display=True, save=True)
