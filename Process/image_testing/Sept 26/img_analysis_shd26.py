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
from tabulate import tabulate

def process_single_test(file, save_directory):
    # Create MapIR Object
    image = MapIR(file)
    # image.dial_in()
    image.display()

    # # # Dark Current Subtraction
    image = dark_current_subtraction(image)
    # # # # # image.display()

    # # # # Band_Correction
    image = band_correction(image)
    # # # # # image.display()

    # # # # Flat Field Correction
    image = flat_field_correction(image)
    # # # # image.display()

    # # # # Radiance_Calibration
    # image = radiance_calibration(image)
    # # image.display()
 
    # # Reflectance Calibration
    image = reflectance_calibration2(image)
    # image.display()

    # Georectification
    # image.extract_GPS('tiff')
    image.export_tiff(save_directory)
    #image.display()

    # Analysis
    # NDVI(image)

    return image

def reflectance_calibration2(mapir_object):
    
    regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
    regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
    regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')
    
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = "Reflectance Calibration"

    mapir_ob.data[:, :, 0] = ((mapir_ob.data[:, :, 0] * regression_coeff_r[0]) + regression_coeff_r[1])
    mapir_ob.data[:, :, 1] = ((mapir_ob.data[:, :, 1] * regression_coeff_g[0]) + regression_coeff_g[1])
    mapir_ob.data[:, :, 2] = ((mapir_ob.data[:, :, 2] * regression_coeff_n[0]) + regression_coeff_n[1])

    return mapir_ob

active_dataset = active_dataset+'/shade'
save_directory = active_dataset+'/outputs'

test_image = process_single_test(active_dataset+'/raw/5.RAW',save_directory)

# Coordinates

# Paper
x1 = 1793; y1 = 1656; x2 = 1977; y2 = 1948

# Board
x3 = 2239; y3 = 1511; x4 = 2755; y4 = 2027

# Foam
x5 = 994; y5 = 1629; x6 = 1234; y6 = 1955

# Check squares

paper_square = deepcopy(test_image)
paper_square.data = test_image.data[y1:y2,x1:x2]
paper_square.display()

board_square = deepcopy(test_image)
board_square.data = test_image.data[y3:y4,x3:x4]
board_square.display()

foam_square = deepcopy(test_image)
foam_square.data = test_image.data[y5:y6,x5:x6]
foam_square.display()

# Check stuff

print("Paper Square Slice Shape:", paper_square.data[y1:y2, x1:x2].shape)
print("Board Square Slice Shape:", board_square.data[y3:y4, x3:x4].shape)
print("Foam Square Slice Shape:", foam_square.data[y5:y6, x5:x6].shape)


#  Calculate values of squares

paper_square_meanr = np.mean(paper_square.data[:,:,0])
paper_square_meang = np.mean(paper_square.data[:,:,1])
paper_square_meann = np.mean(paper_square.data[:,:,2])

board_square_meanr = np.mean(board_square.data[:,:,0])
board_square_meang = np.mean(board_square.data[:,:,1])
board_square_meann = np.mean(board_square.data[:,:,2])

foam_square_meanr = np.mean(foam_square.data[:,:,0])
foam_square_meang = np.mean(foam_square.data[:,:,1])
foam_square_meann = np.mean(foam_square.data[:,:,2])

# Display

table_data = [
            ["","Paper","Board","Foam"],
            ["red",paper_square_meanr,board_square_meanr,foam_square_meanr],
            ["green",paper_square_meang,board_square_meang,foam_square_meang],
            ["near_IR",paper_square_meann,board_square_meann,foam_square_meann]]

table = tabulate(table_data,headers="firstrow",tablefmt="grid")

print()
print("Shaded image:")
print(table)