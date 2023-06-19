# MapIR Georectified Image Processing
# Kevin McKenzie 2023

import matplotlib.pyplot as plt
from pathlib import Path
import imageio.v2 as iio
import numpy as np
import cv2

# MapIR class to process RAW images
class MapIR:
    def __init__(self, raw_file_path):

        self.file_path = raw_file_path
        path = Path(raw_file_path)
        self.file_name = path.stem
        self.file_type = path.suffix

        self.data = iio.imread(self.file_path)
        self.data = self.data[:, :, 0:3]
        # print(self.data.shape) #5971 7406 4

        self.img_y, self.img_x, self.img_bands = self.data.shape[0], self.data.shape[1], 3
        self.g_band, self.r_band, self.ir_band = 550, 660, 850
        self.R_index, self.G_index, self.NIR_index = 0, 1, 2


