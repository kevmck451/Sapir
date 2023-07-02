
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

def radiance_calibration(mapir_object):
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Radiance Calibration'

    # print(np.max(mapir_ob.data))
    # print(np.min(mapir_ob.data))

    R_Slope, R_Intercept = 0.45000359476277024, -0.0012624439662755338
    G_Slope, G_Intercept = 0.31061146127160233, 0.00013542136642994557
    N_Slope, N_Intercept = 0.39404739979907694, -0.0017325589151608728

    # Rad = (DN - b) / m
    mapir_ob.data[:, :, 0] = (mapir_ob.data[:, :, 0] - R_Intercept) / R_Slope
    mapir_ob.data[:, :, 1] = (mapir_ob.data[:, :, 1] - G_Intercept) / G_Slope
    mapir_ob.data[:, :, 2] = (mapir_ob.data[:, :, 2] - N_Intercept) / N_Slope

    # print(f'min: {np.min(mapir_ob.data)}\t |\t Max: {np.max(mapir_ob.data)}')

    Absolute_Min_Value = -1.234929393
    Absolute_Max_Value = 2.768087011
    Absolute_Range = 4.003016404

    # Normalize
    # mapir_ob.data = np.round(mapir_ob.data * mapir_ob.max_raw_pixel_value).astype('int16')
    # mapir_ob.data = (((mapir_ob.data - Absolute_Min_Value) / Absolute_Max_Value) * mapir_ob.max_raw_pixel_value).astype('int16')

    return mapir_ob
