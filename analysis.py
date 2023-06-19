# Analysis for MapIR Data using georectified images

from MapIR_Geo import MapIR
from indices import *

image_filepath = '../Data/MapIR/AC Summer 23/Wheat Field/6-8/Ag Wheat 6-8-23.png'

image = MapIR(image_filepath)

NDVI(image, display=True, save=False)


