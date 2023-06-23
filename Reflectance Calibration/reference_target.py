# File to test the functionality of get reflectance values from reflectance target


from raw import MapIR_RAW
from pathlib import Path
from reflectance_cal import *

# base_directory = '../Data/MapIR/AC Summer 23/Wheat Field/6-8'
base_directory = '../Data/MapIR/AC Summer 23/Wheat Field/6-20'
# base_directory = '../Data/MapIR/AC Summer 23/Main Sub Field/6-20'

bd = Path(base_directory)

reflection_target_path = bd / 'ref_tar.RAW'

image = MapIR_RAW(reflection_target_path)
image.display()



image2 = MapIR_RAW(reflection_target_path)
image2 = reflectance_calibration(image2)
image2.display()