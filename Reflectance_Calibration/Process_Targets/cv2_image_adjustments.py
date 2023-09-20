# Function to rescale images in OpenCV

import cv2
import numpy as np
import pathlib as Path
import os
import imageio as iio

# Rescale the image
def rescale(image,scale):
    width = int(image.shape[1]*scale)
    height = int(image.shape[0]*scale)

    dimensions = (width,height)

    return cv2.resize(image,dimensions,interpolation=cv2.INTER_AREA)

def norm8bit(image):
    min_val = np.min(image)
    max_val = np.min(image)

    image_8bit = ((image-min_val) / (max_val-min_val) * 255).astype(np.uint8)

    return image_8bit

def export_tiff(self, filepath):
    path = filepath
    save_as = f'{filepath}/{self.path.stem}.tiff'

    Absolute_Min_Value = -1.234929393
    Absolute_Max_Value = 2.768087011
    Absolute_Range = 4.003016404

    # Normalize to 16 bit
    data = self.data
    data[data < 0] = 0
    # data = data / Absolute_Max_Value
    data = data / np.max(data)
    data = np.round(data * 65535).astype(int)
    data = data.astype(np.uint16)

    iio.imsave(save_as, data, format='tiff')

class MapIR_tiff:
    def __init__(self, raw_file_path):

        self.file_path = raw_file_path
        self.path = Path(raw_file_path)
        self.file_name = self.path.stem
        self.file_type = self.path.suffix

        self.data = iio.imread(self.file_path)
        self.data = self.data[:, :, 0:3]
        # print(self.data.shape) #5971 7406 4

        self.img_y, self.img_x, self.img_bands = self.data.shape[0], self.data.shape[1], 3
        self.g_band, self.r_band, self.ir_band = 550, 660, 850
        self.R_index, self.G_index, self.NIR_index = 0, 1, 2