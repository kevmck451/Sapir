# MapIR RAW Base Class

import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
import cv2

class MapIR:
    def __init__(self, raw_file_path):
        self.path = Path(raw_file_path)

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

    # Function to unpack the data
    def _unpack(self):
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
        self.data = debayered_data

    # Function to package the data
    def _normalize(self):
        # print(self.data)
        print(type(self.data))
        print(self.data.dtype)

        # Calculate the maximum and minimum values for each channel
        max_r, min_r = np.max(self.data[:, :, 0]), np.min(self.data[:, :, 0])
        max_g, min_g = np.max(self.data[:, :, 1]), np.min(self.data[:, :, 1])
        max_n, min_n = np.max(self.data[:, :, 2]), np.min(self.data[:, :, 2])

        # Use the variables as needed
        print(f'Max R: {max_r}')
        print(f'Min R: {min_r}')
        print(f'Max G: {max_g}')
        print(f'Min G: {min_g}')
        print(f'Max B: {max_n}')
        print(f'Min B: {min_n}')

        # Normalize to 16 bit
        data = self.data
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
        data_scaled = data_norm * 65535
        self.data = data_scaled.astype(np.uint16)

        print(type(self.data))
        print(self.data.dtype)

        # Calculate the maximum and minimum values for each channel
        max_r, min_r = np.max(self.data[:, :, 0]), np.min(self.data[:, :, 0])
        max_g, min_g = np.max(self.data[:, :, 1]), np.min(self.data[:, :, 1])
        max_n, min_n = np.max(self.data[:, :, 2]), np.min(self.data[:, :, 2])

        # Use the variables as needed
        print(f'Max R: {max_r}')
        print(f'Min R: {min_r}')
        print(f'Max G: {max_g}')
        print(f'Min G: {min_g}')
        print(f'Max B: {max_n}')
        print(f'Min B: {min_n}')

    # Function to correct leakage in sensor
    def _correct(self):
        # image_matrix = [[336.68, 74.61, 37.63], [33.52, 347.5, 41.77], [275.41, 261.99, 286.5]]
        # image_matrix = [[7.18, 2.12, 1.02], [0.72, 9.86, 1.12], [5.88, 7.43, 7.74]]
        image_matrix = [[336, 33, 275], [74, 347, 261], [37, 41, 286]]

        # Calculate the inverse of the image matrix
        image_matrix = np.asarray(image_matrix)
        inverse_matrix = np.linalg.inv(image_matrix)

        # Multiply each value in each band by the corresponding value in the inverse matrix
        corrected_data = np.zeros(self.data.shape)
        for i in range(self.data.shape[0]):
            corrected_data[i] = (inverse_matrix @ self.data[i].T).T

        self.data = corrected_data

    # Function to display the data
    def _render_RGB(self, hist=False):
        Ra = self.data[:, :, 0]
        Ga = self.data[:, :, 1]
        Ba = self.data[:, :, 2]

        def scale8bit(a):
            a_min, a_max = a.min(), a.max()

            if a_max == a_min:  # Avoid division by zero
                return np.zeros_like(a, dtype='uint8')
            else:
                return ((a - a_min) * (255.0 / (a_max - a_min))).astype('uint8')

        Ra8, Ga8, Ba8 = scale8bit(Ra), scale8bit(Ga), scale8bit(Ba)

        # set rescaled fill pixels back to 0 for each array
        Ra8[Ra == 0], Ga8[Ga == 0], Ba8[Ba == 0] = 0, 0, 0

        # make rgb stack
        rgb_stack = np.zeros((self.img_y, self.img_x, 3), 'uint8')
        rgb_stack[..., 0], rgb_stack[..., 1], rgb_stack[..., 2] = Ra8, Ga8, Ba8

        # apply histogram equalization to each band
        if hist:
            for i in range(rgb_stack.shape[2]):
                # band i
                b = rgb_stack[:, :, i]
                # histogram from flattened (1d) image
                b_histogram, bins = np.histogram(b.flatten(), 256)
                # cumulative distribution function
                b_cumdistfunc = b_histogram.cumsum()
                # normalize
                b_cumdistfunc = 255 * b_cumdistfunc / b_cumdistfunc[-1]
                # get new values by linear interpolation of cdf
                b_equalized = np.interp(b.flatten(), bins[:-1], b_cumdistfunc)
                # reshape to 2d and add back to rgb_stack
                rgb_stack[:, :, i] = b_equalized.reshape(b.shape)

        self.rgb_render = rgb_stack
        return rgb_stack

    # Function to display the data
    def display(self, hist=False):
        rgb_stack = self._render_RGB()

        # apply histogram equalization to each band
        if hist:
            for i in range(rgb_stack.shape[2]):
                # band i
                b = rgb_stack[:, :, i]
                # histogram from flattened (1d) image
                b_histogram, bins = np.histogram(b.flatten(), 256)
                # cumulative distribution function
                b_cumdistfunc = b_histogram.cumsum()
                # normalize
                b_cumdistfunc = 255 * b_cumdistfunc / b_cumdistfunc[-1]
                # get new values by linear interpolation of cdf
                b_equalized = np.interp(b.flatten(), bins[:-1], b_cumdistfunc)
                # reshape to 2d and add back to rgb_stack
                rgb_stack[:, :, i] = b_equalized.reshape(b.shape)

        plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
        plt.axis('off')
        plt.title(f'{self.path.stem}')
        plt.tight_layout(pad=1)
        plt.show()