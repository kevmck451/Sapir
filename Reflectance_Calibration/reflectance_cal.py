# File to test the functionality of get reflectance values from reflectance target

import matplotlib.pyplot as plt
import math as math
import numpy as np
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from copy import deepcopy
from MapIR.mapir import *
from Data_Paths.data_filepaths import *

# Function to apply reflectance calibration onto the image.
def reflectance_calibration(mapir_object):
    
    regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
    regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
    regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')
    
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = "Reflectance Calibration"

    mapir_ob.data[:, :, 0] = ((mapir_ob.data[:, :, 0] * regression_coeff_r[0]) + regression_coeff_r[1])
    mapir_ob.data[:, :, 1] = ((mapir_ob.data[:, :, 1] * regression_coeff_g[0]) + regression_coeff_g[1])
    mapir_ob.data[:, :, 2] = ((mapir_ob.data[:, :, 2] * regression_coeff_n[0]) + regression_coeff_n[1])

    print(np.max(mapir_ob.data[:,:,0]),np.min(mapir_ob.data[:,:,0]))
    print(np.max(mapir_ob.data[:,:,1]),np.min(mapir_ob.data[:,:,1]))
    print(np.max(mapir_ob.data[:,:,2]),np.min(mapir_ob.data[:,:,2]))

    return mapir_ob

