
import numpy as np
from copy import deepcopy


def dark_current_subtraction(mapir_object):
    Red_Mean = 7.719953658333334
    Green_Mean = 7.590785783333334
    NIR_Mean = 7.677031808333334

    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Dark Current Subtraction'

    mapir_ob.data[:, :, 0] -= Red_Mean
    mapir_ob.data[:, :, 1] -= Green_Mean
    mapir_ob.data[:, :, 2] -= NIR_Mean

    return mapir_ob

def flat_field_correction(mapir_object):
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Flat Field Correction'

    red_ff = np.load(
        '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR_py/Radiance_Calibration/flat_field/ff_cor_matrix_red.npy')
    green_ff = np.load(
        '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR_py/Radiance_Calibration/flat_field/ff_cor_matrix_green.npy')
    nir_ff = np.load(
        '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR_py/Radiance_Calibration/flat_field/ff_cor_matrix_nir.npy')

    mapir_ob.data[:, :, 0] = mapir_ob.data[:, :, 0] / red_ff
    mapir_ob.data[:, :, 1] = mapir_ob.data[:, :, 1] / green_ff
    mapir_ob.data[:, :, 2] = mapir_ob.data[:, :, 2] / nir_ff

    return mapir_ob

def radiate(mapir_object):
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Radiance Calibration'

    # Normalize
    # mapir_ob.data = np.round(mapir_ob.data * mapir_ob.max_raw_pixel_value).astype('int16')
    # mapir_ob.data = ((mapir_ob.data / np.max(mapir_ob.data)) * mapir_ob.max_raw_pixel_value).astype('int16')

    return mapir_ob
