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
        self.path = Path(raw_file_path)
        self.file_name = self.path.stem
        self.file_type = self.path.suffix

        self.data = iio.imread(self.file_path)
        self.data = self.data[:, :, 0:3]
        # print(self.data.shape) #5971 7406 4

        self.img_y, self.img_x, self.img_bands = self.data.shape[0], self.data.shape[1], 3
        self.g_band, self.r_band, self.ir_band = 550, 660, 850
        self.R_index, self.G_index, self.NIR_index = 0, 1, 2

    # Function to calculate and display the Normalized Difference Vegetation Index
    def NDVI(self, display=True, save=False):
        NIR = self.data[:, :, self.NIR_index]
        RED = self.data[:, :, self.R_index]

        RED, NIR = RED.astype('float'), NIR.astype('float')
        # RED[RED == 0], NIR[NIR == 0] = np.nan, np.nan
        top, bottom = NIR - RED, NIR + RED
        top[top == 0], bottom[bottom == 0] = 0, np.nan

        ndvi_array = np.divide(top, bottom)
        ndvi_array[ndvi_array < 0] = 0
        ndvi_array[ndvi_array > 1] = 1

        plt.figure(figsize=(12, 12))
        plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
        plt.title(f'NDVI: {self.file_name}')
        # plt.colorbar()
        plt.axis('off')
        plt.tight_layout(pad=1)

        if save:
            saveas = (f'{self.path.parent}/{self.file_name} NDVI.pdf')
            plt.savefig(saveas)
            plt.close()
        if display:
            plt.show()

    # Function to calculate and display the Green Normalized Difference Vegetation Index
    def GNDVI(self):
        pass

    # Function to calculate and display the Red Edge Normalized Difference Vegetation Index
    def NDRE(self):
        pass