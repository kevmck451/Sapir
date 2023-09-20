import matplotlib.pyplot as plt
import math as math
import numpy as np
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')
import cv2

from copy import deepcopy
from MapIR.mapir import *
from Data_Paths.data_filepaths import *
from Process_Targets.cv2_image_adjustments import *

regression_coeff_r = np.load(active_dataset+'/coeffs/r_coeffs.npy')
regression_coeff_g = np.load(active_dataset+'/coeffs/g_coeffs.npy')
regression_coeff_n = np.load(active_dataset+'/coeffs/n_coeffs.npy')

print(regression_coeff_r,regression_coeff_g,regression_coeff_n)

file = active_dataset + '/_processed/99067.tiff'

image = cv2.imread(file,cv2.IMREAD_UNCHANGED)

image_small = rescale(image,0.25)
cv2.imshow("Image",image_small)
cv2.waitKey(0)
cv2.destroyAllWindows()

image = image.astype(np.float32)

print(np.min(image[:,:,0]),np.max(image[:,:,0]))
print(np.min(image[:,:,1]),np.max(image[:,:,1]))
print(np.min(image[:,:,2]),np.max(image[:,:,2]))

print(f'Image Data Type: {image.dtype}')

image[:,:,0] = (image[:,:,0] * regression_coeff_r[0]) + regression_coeff_r[1]
image[:,:,1] = (image[:,:,1] * regression_coeff_g[0]) + regression_coeff_g[1]
image[:,:,2] = (image[:,:,2] * regression_coeff_n[0]) + regression_coeff_n[1]

print(f'Image Data Type: {image.dtype}')
image_small = rescale(image,0.25)

min_max_r = f'{np.max(image[:,:,0]):.10f}'
min_max_g = f'{np.max(image[:,:,1]):.10f}'

print(min_max_r,min_max_g)
print(np.min(image[:,:,0]),np.max(image[:,:,0]))
print(np.min(image[:,:,1]),np.max(image[:,:,1]))
print(np.min(image[:,:,2]),np.max(image[:,:,2]))


cv2.imshow("Image",image_small)
cv2.waitKey(0)
cv2.destroyAllWindows()