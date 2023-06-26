
from raw import MapIR_RAW
from pathlib import Path

# base_directory = '../Data/MapIR/Test/raw/-1.RAW'
# base_directory = '../Data/MapIR/Test/raw/0.RAW'
base_directory = '../Data/MapIR/Test/raw/dark1.RAW'
# base_directory = '../Data/MapIR/Test/raw/850.RAW'
# base_directory = '../Data/MapIR/Test/raw/107.RAW'

bd = Path(base_directory)
# image = MapIR_RAW(bd)
# image.display()


from mapir import MapIR
from Band_Correction.correction import correct
from Analysis.vegetation_index import NDVI

image = MapIR(bd)
# image.dial_in()
image.display()
# NDVI(image)
image_1 = correct(image)
image_1.display()
# NDVI(image_1)
# image.export_tiff()
