# Correction File

import numpy as np
from copy import deepcopy

exp_directory = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/MC Tests/MC Test 4'

single_1 = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/AC Summer 23/Wheat Field/6-8/raw/081.RAW'
single_2 = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/MC Tests/MC Test 4/RAW/850.RAW'

# Function to apply correction to MapIR Object
def correct(mapir_object, corr_values=None):
    if corr_values is None:
        # Monochromator Exp 4 Values from paper
        # image_matrix = [[336, 33, 275], [74, 347, 261], [37, 41, 286]]
        # Monochromator Exp 4 Values after data (changed data type / ratios same)
        image_matrix = [[5481.53, 664.44, 4510.03], [1309.98, 5660.94, 4294.08], [740.54, 796.69, 4686.63]]

    else:
        # Values injected from Experiment
        image_matrix = corr_values

    # Calculate the inverse of the image matrix
    image_matrix = np.asarray(image_matrix)
    inverse_matrix = np.linalg.inv(image_matrix)
    # print(inverse_matrix)

    # print(mapir_object.data.dtype)
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Band Correction'

    # Multiply each value in each band by the corresponding value in the inverse matrix
    corrected_data = np.zeros(mapir_ob.data.shape)
    for i in range(mapir_ob.data.shape[0]):
        corrected_data[i] = (inverse_matrix @ mapir_ob.data[i].T).T

    # print(f'{mapir_ob.data.dtype} Raw Data Dtype')
    # print(f'{np.max(mapir_ob.data)} Raw Data Max')
    # print(f'{np.min(mapir_ob.data)} Raw Data Min')
    # print(f'{corrected_data.dtype} Corrected Data Dtype')
    # print(f'{np.max(corrected_data)} Corrected Data Max')
    # print(f'{np.min(corrected_data)} Corrected Data Min')
    # mapir_ob.data = np.round(corrected_data * mapir_ob.max_raw_pixel_value).astype('int16')
    mapir_ob.data = corrected_data
    # print(f'{mapir_ob.data.dtype} Raw Data Dtype')
    # print(f'{np.max(mapir_ob.data)} Raw Data Max')
    # print(f'{np.min(mapir_ob.data)} Raw Data Min')


    return mapir_ob







