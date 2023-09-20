# Function to rescale images in OpenCV

import cv2
import numpy as np
import pathlib as Path
import os
import imageio as iio
import matplotlib.pyplot as plt
from copy import deepcopy

# Rescale the image
def rescale(image,scale):
    width = int(image.shape[1]*scale)
    height = int(image.shape[0]*scale)

    dimensions = (width,height)

    return cv2.resize(image,dimensions,interpolation=cv2.INTER_AREA)

def norm16bit(image):
    # Normalize to 16bit
    data = image.data
    min = 0
    max = 65535

    scale = (max-min) / (np.max(data)-np.min(data))
    offset = -np.min(data)

    data16 = ((data+offset)*scale).astype(np.uint16)
    return data16

def export_tiff(self, filepath):
    path = filepath
    save_as = f'{filepath}/{self.path.stem}.tiff'

    # Normalize to 16bit
    data = self.data
    data[data < 0] = 0
    # data = data / Absolute_Max_Value
    data = data / np.max(data)
    data = np.round(data * 65535).astype(int)
    data = data.astype(np.uint16)

    iio.imsave(save_as, data, format='tiff')    

class MapIR_tiff:
    def __init__(self, raw_file_path):

        self.stage = "Target_Calibration"
        self.file_path = raw_file_path
        # self.path = Path(raw_file_path)
        # self.file_name = self.path.stem
        # self.file_type = self.path.suffix

        self.data = iio.imread(self.file_path)
        self.data = self.data[:, :, 0:3]
        # print(self.data.shape) #5971 7406 4
        self.data = self.data.astype('float64')

        self.img_y, self.img_x, self.img_bands = self.data.shape[0], self.data.shape[1], 3
        self.g_band, self.r_band, self.ir_band = 550, 660, 850
        self.R_index, self.G_index, self.NIR_index = 0, 1, 2
    
    def display(self):
        data = self.normalize()
        # data = self.data
        plt.figure(figsize=(12,9))
        plt.imshow(data)
        plt.axis('off')
        #plt.title(f'File: {self.path.stem} | Stage: {self.stage}')
        plt.tight_layout(pad=1)
        plt.show()

    def normalize(self):
        if self.stage == 'RAW Form' or self.stage == 'Dark Current Subtraction':
            # print(self.data.dtype)
            # print(np.max(self.data))
            # print(np.min(self.data))
            rgb_stack = ((self.data / self.max_raw_pixel_value) * 255).astype('uint8')
        elif self.stage == 'Band Correction' or self.stage == 'Flat Field Correction':
            # print(self.data.dtype)
            # print(np.max(self.data))
            # print(np.min(self.data))
            if np.min(self.data) < 0:
                rgb_stack = np.round((self.data + abs(np.min(self.data))) * 255).astype('uint8')
            else:
                rgb_stack = np.round((self.data - np.min(self.data)) * 255).astype('uint8')
        elif self.stage == 'Radiance Calibration':
            # print(self.data.dtype)
            # print(np.max(self.data))
            # print(np.min(self.data))
            if np.min(self.data) < 0:
                rgb_stack = np.round((self.data + abs(np.min(self.data))) / (np.max(self.data) + abs(np.min(self.data))) * 255).astype('uint8')
            else:
                rgb_stack = np.round((self.data - np.min(self.data)) / (np.max(self.data - np.min(self.data))) * 255).astype('uint8')
        else:
            # print(self.data.dtype)
            # print(np.max(self.data))
            # print(np.min(self.data))
            rgb_stack = np.round((self.data / np.max(self.data)) * 255).astype('uint8')

        return rgb_stack

def flat_field_correction_target(mapir_object):
    mapir_ob = deepcopy(mapir_object)
    mapir_ob.stage = 'Flat Field Correction'

    red_ff = np.load(
        "C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules/Radiance_Calibration/flat_field/ff_cor_matrix_red.npy")
    green_ff = np.load(
        "C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules/Radiance_Calibration/flat_field/ff_cor_matrix_green.npy")
    nir_ff = np.load(
        "C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules/Radiance_Calibration/flat_field/ff_cor_matrix_nir.npy")

    mapir_ob.data[:, :, 0] = mapir_ob.data[:, :, 0] / red_ff
    mapir_ob.data[:, :, 1] = mapir_ob.data[:, :, 1] / green_ff
    mapir_ob.data[:, :, 2] = mapir_ob.data[:, :, 2] / nir_ff

    return mapir_ob