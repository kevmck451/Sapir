
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')
from copy import deepcopy

from MapIR.mapir import MapIR
from Band_Correction.correction import band_correction
from Radiance_Calibration.radiance import radiance_calibration
from Radiance_Calibration.radiance import dark_current_subtraction
from Radiance_Calibration.radiance import flat_field_correction
from Reflectance_Calibration.reflectance_calibration import reflectance_calibration
from Analysis.vegetation_index import NDVI
from Data_Paths.data_filepaths import *
import numpy as np


def process_single_test(file, save_directory=''):
    # Create MapIR Object
    image = MapIR(file)
    # image.dial_in()
    image.display()

    # Dark Current Subtraction
    # image = dark_current_subtraction(image)
    # #image.display()

    # # Band_Correction
    # image = band_correction(image)
    # #image.display()

    # # Flat Field Correction
    # image = flat_field_correction(image)
    # #image.display()

    # # Radiance_Calibration
    # image = radiance_calibration(image)
    # # image.display()
 
    # # Reflectance Calibration
    # image = reflectance_calibration(image)
    # image.display()

    # # Georectification
    # image.extract_GPS('tiff')
    # image.export_tiff(save_directory)
    # #image.display()

    # snippetr = image.data[384:1122,389:1167,0]
    # snippetg = image.data[384:1122,389:1167,1]
    # snippetn = image.data[384:1122,389:1167,2]

    # print(np.mean(snippetr))
    # print(np.mean(snippetg))
    # print(np.mean(snippetn))

    # Analysis
    # NDVI(image)

    return image


aluminum = process_single_test(active_dataset+'/raw/3.RAW')
paper = process_single_test(active_dataset+'/raw/5.RAW')

x1 = 2649; y1 = 853; x2 = 3309; y2 = 1570
aluminum_square = deepcopy(aluminum)
aluminum_square.data = aluminum.data[y1:y2,x1:x2]
aluminum_square.display()

x3 = 2473; y3 = 698; x4 = 3080; y4 = 1428
paper_square = deepcopy(paper)
paper_square.data = paper.data[y3:y4,x3:x4]
paper_square.display()

aluminum_mean = np.mean(aluminum_square.data)
paper_mean = np.mean(paper_square.data)

print(aluminum_mean,paper_mean)