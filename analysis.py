# Analysis for MapIR Data using georectified images

from MapIR_Geo import MapIR
from indices import *

image_filepath = ''

image = MapIR(image_filepath)

NDVI(image, display=True, save=False)


