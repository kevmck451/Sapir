# Analysis for MapIR Data using georectified images

from georectified import MapIR

# Location of Georectified MapIR image
image_filepath = '../Data/MapIR/AC Summer 23/Wheat Field/6-8/Ag Wheat 6-8-23.png'

image = MapIR(image_filepath)

# NDVI uses the Red and NIR bands to provide a measure of vegetation health
image.NDVI(display=True, save=False)

# GNDVI may be more sensitive to variations in chlorophyll content than NDVI
image.GNDVI(display=True, save=False)


