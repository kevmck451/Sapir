# File to test the functionality of get reflectance values from reflectance target

import matplotlib.pyplot as plt
import math as math
import numpy as np
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from copy import deepcopy
from MapIR.mapir import *
from Data_Paths.data_filepaths import *
from Reflectance_Calibration.Process_Targets.cv2_image_adjustments import *

# Function to apply reflectance calibration onto the image.
def reflectance_calibration(mapir_object):
    
    regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
    regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
    regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')
    
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = "Reflectance Calibration"

    mapir_ob.data = mapir_ob.data.astype(np.float32)

    print(np.max(mapir_ob.data[:,:,0]),np.min(mapir_ob.data[:,:,0]))
    print(np.max(mapir_ob.data[:,:,1]),np.min(mapir_ob.data[:,:,1]))
    print(np.max(mapir_ob.data[:,:,2]),np.min(mapir_ob.data[:,:,2]))

    mapir_ob.data[:, :, 0] = ((mapir_ob.data[:, :, 0] * regression_coeff_r[0]) + regression_coeff_r[1])
    mapir_ob.data[:, :, 1] = ((mapir_ob.data[:, :, 1] * regression_coeff_g[0]) + regression_coeff_g[1])
    mapir_ob.data[:, :, 2] = ((mapir_ob.data[:, :, 2] * regression_coeff_n[0]) + regression_coeff_n[1])

    # print(np.max(mapir_ob.data[:,:,0]),np.min(mapir_ob.data[:,:,0]))
    # print(np.max(mapir_ob.data[:,:,1]),np.min(mapir_ob.data[:,:,1]))
    # print(np.max(mapir_ob.data[:,:,2]),np.min(mapir_ob.data[:,:,2]))

    return mapir_ob

def reflectance_calibration2(image):
    regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
    regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
    regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')

    print(regression_coeff_r,regression_coeff_g,regression_coeff_n)

    print(np.max(image[:,:,0]),np.min(image[:,:,0]))
    print(np.max(image[:,:,1]),np.min(image[:,:,1]))
    print(np.max(image[:,:,2]),np.min(image[:,:,2]))

    image = image.astype(np.float32)

    image[:,:,0] = (image[:,:,0] * regression_coeff_r[0]) + regression_coeff_r[1]
    image[:,:,1] = (image[:,:,1] * regression_coeff_g[0]) + regression_coeff_g[1]   
    image[:,:,2] = (image[:,:,2] * regression_coeff_n[0]) + regression_coeff_n[1]

    image[image<0] = 0
    image[image>1] = 1

    print(np.max(image[:,:,0]),np.min(image[:,:,0]))
    print(np.max(image[:,:,1]),np.min(image[:,:,1]))
    print(np.max(image[:,:,2]),np.min(image[:,:,2]))

    img_s = rescale(image,0.25)
    cv2.imshow("Image",img_s)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    img16 = image/np.max(image)
    img16 = np.round(img16*65535).astype(int)
    img16 = img16.astype(np.uint16)

    cv2.imwrite(active_dataset+'/tests/1.tiff',img16)    

image = active_dataset+'/_processed/99967.tiff'

image = cv2.imread(image,cv2.IMREAD_UNCHANGED)
img_s = rescale(image,0.25)
cv2.imshow("Image",img_s)
cv2.waitKey(0)
cv2.destroyAllWindows()

reflectance_calibration2(image)
