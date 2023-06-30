# MapIR RAW Base Class

import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import cv2
import imageio

class MapIR:
    def __init__(self, raw_file_path):

        self.stage = 'RAW Form'
        self.path = Path(raw_file_path)
        self.max_raw_pixel_value = 3950

        if self.path.suffix != '.RAW':
            print(f'Wrong File Type: {self.path}')
        else:
            # self.file_name = self.path.stem
            # self.file_type = self.path.suffix

            self.img_y, self.img_x, self.img_bands = 3000, 4000, 3
            self.g_band, self.r_band, self.ir_band = 550, 660, 850
            self.R_index, self.G_index, self.NIR_index = 0, 1, 2

            with open(raw_file_path, "rb") as f:
                self.data = f.read()
                # print(self.data)

            # print(len(self.data))
            if len(self.data) != (1.5 * 4000 * 3000):
                print(f'File Corrupt: {self.path.stem}')
            else:
                self._unpack()
                self._debayer()
                self.check_over_exposure()

    # Function to unpack the data
    def _unpack(self):
        # two pixels are packed into each 3 byte value
        # ABC = nibbles of even pixel (big endian)
        # DEF = nibbles of odd pixel (big endian)
        # bytes in data: BC FA DE

        # Function to unpack MapIR raw image file per-pixel 12 bit values
        self.data = np.frombuffer(self.data, dtype=np.uint8).astype(np.uint16)

        # pull the first of every third byte as the even pixel data
        even_pixels = self.data[0::3]
        # pull the last of every third byte as the odd pixel data
        odd_pixels = self.data[2::3]
        # the middle byte has bits of both pixels
        middle_even = self.data[1::3].copy()
        middle_even &= 0xF
        middle_even <<= 8
        middle_odd = self.data[1::3].copy()
        middle_odd &= 0xF0
        middle_odd >>= 4
        odd_pixels <<= 4

        # combine middle byte data into pixel data
        even_pixels |= middle_even
        odd_pixels |= middle_odd
        pixels = np.stack((even_pixels, odd_pixels), axis=-1)

        # reshape to form camera image 4000x3000 pixels
        image = pixels.reshape((3000, 4000))
        self.data = image
        # print(self.data.shape)

    # Function to debayer image matrix
    def _debayer(self):
        # the bayer pattern is
        # R G
        # G B

        # use opencv's debayering routine on the data
        # COLOR_BAYER_RG2RGB # Company
        # COLOR_BAYER_BG2RGB # Thomas
        debayered_data = cv2.cvtColor(self.data, cv2.COLOR_BAYER_BG2RGB)
        # print(self.data[1330:1332, 1836:1838])
        # print(output_data.mean(axis=(0, 1)))

        # self.data is uint16 but in 12 bit range
        # self.data = debayered_data
        self.data = debayered_data.astype('float64')

    # Function to plot the max values for brightness setting
    def dial_in(self):
        # Calculate the maximum and minimum values for each channel
        max_r, min_r = np.max(self.data[:, :, 0]), np.min(self.data[:, :, 0])
        max_g, min_g = np.max(self.data[:, :, 1]), np.min(self.data[:, :, 1])
        max_n, min_n = np.max(self.data[:, :, 2]), np.min(self.data[:, :, 2])

        max_indices_R = np.where(self.data[:, :, 0] == np.max(self.data[:, :, 0]))
        max_indices_G = np.where(self.data[:, :, 1] == np.max(self.data[:, :, 1]))
        max_indices_N = np.where(self.data[:, :, 2] == np.max(self.data[:, :, 2]))
        # print(max_indices_R)

        threshold = lambda x: 0 if (x - 5) < 0 else (x - 5)
        threshold_r = threshold(max_r)
        threshold_g = threshold(max_g)
        threshold_n = threshold(max_n)

        threshold_indices_R = np.where(self.data[:, :, 0] >= threshold_r)
        threshold_indices_G = np.where(self.data[:, :, 1] >= threshold_g)
        threshold_indices_N = np.where(self.data[:, :, 2] >= threshold_n)

        # amount_r = len(threshold_indices_R[0])
        # amount_g = len(threshold_indices_G[0])
        # amount_n = len(threshold_indices_N[0])

        plt.figure(figsize=(14, 6))
        plt.suptitle('Max Stats')

        plt.subplot(1, 2, 1)
        plt.imshow(self.normalize())
        plt.scatter(max_indices_R[1], max_indices_R[0], color='red', label=max_r)
        plt.scatter(max_indices_G[1], max_indices_G[0], color='green', label=max_g)
        plt.scatter(max_indices_N[1], max_indices_N[0], color='blue', label=max_n)
        plt.title(f'{self.path.stem}')
        plt.axis(False)
        plt.legend()

        plt.subplot(1, 2, 2)
        x = ['R', 'G', 'N']
        mx = [max_r, max_g, max_n]
        color = ['red', 'green', 'blue']
        plt.bar(x, mx, color=color)
        plt.ylim((0, 4096))
        plt.axhline(self.max_raw_pixel_value, color='black', linestyle='dotted')
        plt.tight_layout(pad=1)
        plt.title(f'Range')
        plt.show()

    # Function to check for over exposure
    def check_over_exposure(self):
        if np.max(self.data) >= (self.max_raw_pixel_value-3):
            # print('image contains over exposed pixels')
            self.over_exposure = True
        else: self.over_exposure = False

    # Function to convert data to 8 bit range
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
                rgb_stack = np.round((self.data - np.min(self.data)) / np.max(self.data) * 255).astype('uint8')
        else:
            # print(self.data.dtype)
            # print(np.max(self.data))
            # print(np.min(self.data))
            rgb_stack = np.round((self.data / np.max(self.data)) * 255).astype('uint8')

        return rgb_stack

    # Function to display the data
    def display(self):
        data = self.normalize()
        # data = self.data
        plt.figure(figsize=(12,9))
        plt.imshow(data)
        plt.axis('off')
        plt.title(f'File: {self.path.stem} | Stage: {self.stage}')
        plt.tight_layout(pad=1)
        plt.show()

    # Function to export image as 16-bit tiff
    def export_tiff(self, filepath):
        # Normalize to 16 bit
        data = self.data
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
        data_scaled = data_norm * 65535
        self.data = data_scaled.astype(np.uint16)

        path = Path(filepath)
        imageio.imsave(path, self.data, format='tiff')