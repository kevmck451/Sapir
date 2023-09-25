
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

    # # Dark Current Subtraction
    image = dark_current_subtraction(image)
    # # # image.display()

    # # Band_Correction
    image = band_correction(image)
    # # # image.display()

    # # Flat Field Correction
    image = flat_field_correction(image)
    # # image.display()

    # # Radiance_Calibration
    image = radiance_calibration(image)
    # image.display()
 
    # Reflectance Calibration
    image = reflectance_calibration(image)
    # image.display()

    # Georectification
    # image.extract_GPS('tiff')
    image.export_tiff(save_directory)
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

def reflectance_calibration(mapir_object):
    
    regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
    regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
    regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')
    
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = "Reflectance Calibration"

    mapir_ob.data[:, :, 0] = ((mapir_ob.data[:, :, 0] * regression_coeff_r[0]) + regression_coeff_r[1])
    mapir_ob.data[:, :, 1] = ((mapir_ob.data[:, :, 1] * regression_coeff_g[0]) + regression_coeff_g[1])
    mapir_ob.data[:, :, 2] = ((mapir_ob.data[:, :, 2] * regression_coeff_n[0]) + regression_coeff_n[1])

    return mapir_ob

# Coefficients without band correction
coeffs_shade_a = (
    (0.00065233, -0.0294142),
    (0.00026794, -0.01806295),
    (0.00120418, -0.04747603)
)
coeffs_shade_a = (
    (6.65820238e-05, -2.97332827e-02),
    (3.26244147e-05, -2.17883460e-02),
    (0.00012158, -0.04402203) 
)

# Coefficients with band correction

save_directory = main_path+'/Trials & Experiments/Images'

sunny = process_single_test(active_dataset+'/raw/1.RAW',save_directory)
shade = process_single_test(active_dataset+'/raw/3.RAW',save_directory)

# Coordinates
x1 = 79; y1 = 34; x2 = 3955; y2 = 1241
x3 = 44; y3 = 24; x4 = 3934; y4 = 934

# Check squares

no_paper_square = deepcopy(no_paper)
no_paper_square.data = no_paper.data[y1:y2,x1:x2]
no_paper_square.display()

paper_square = deepcopy(paper)
paper_square.data = paper.data[y3:y4,x3:x4]
paper_square.display()

# Calculate values of squares

no_paper_meanr = np.mean(no_paper.data[y1:y2,x1:x2,0])
no_paper_meang = np.mean(no_paper.data[y1:y2,x1:x2,1])
no_paper_meann = np.mean(no_paper.data[y1:y2,x1:x2,2])
no_paper_min = np.min(no_paper.data)
no_paper_max = np.max(no_paper.data)

paper_meanr = np.mean(paper.data[y3:y4,x3:x4,0])
paper_meang = np.mean(paper.data[y3:y4,x3:x4,1])
paper_meann = np.mean(paper.data[y3:y4,x3:x4,2])
paper_min = np.min(paper.data)
paper_max = np.max(paper.data)

# Differences

r_diff = no_paper_meanr/paper_meanr
g_diff = no_paper_meang/paper_meang
n_diff = no_paper_meann/paper_meann

# Display

table_data = [
            ["","Foam Only","With Paper","Difference"],
            ["red",no_paper_meanr,paper_meanr,r_diff],
            ["green",no_paper_meang,paper_meang,g_diff],
            ["near_IR",no_paper_meann,paper_meann,n_diff],
            ["min",no_paper_min,paper_min],
            ["max",no_paper_max,paper_max]]

table = tabulate(table_data,headers="firstrow",tablefmt="grid")


print()
print("Data from a sample square in both images:")
print(table)


