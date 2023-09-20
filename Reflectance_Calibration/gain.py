from PIL import Image
from PIL.ExifTags import TAGS
import cv2
import numpy as np
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')
from Data_Paths.data_filepaths import *

# Open the image
image = Image.open(target_panel)

# Extract EXIF data
exif_data = image._getexif()

# Look for gain-related tags
for tag, value in exif_data.items():
    tag_name = TAGS.get(tag, tag)
    if "gain" in tag_name.lower():
        print(f"{tag_name}: {value}")