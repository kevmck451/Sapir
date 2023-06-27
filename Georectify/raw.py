# MapIR RAW Processing
# Kevin McKenzie 2023

import matplotlib.pyplot as plt
from pathlib import Path
from PIL import Image
import numpy as np
import imageio
import piexif
import cv2
import os

# MapIR class to process_single RAW images
class MapIR_RAW:
    def __init__(self, raw_file_path):
        self.file_path = raw_file_path
        path = Path(raw_file_path)
        self.file_name = path.stem
        self.file_type = path.suffix

        with open(raw_file_path, "rb") as f:
            self.data = f.read()
            # print(self.data)

        # ----------------- UNPACK RAW DATA --------------------
        # Function to unpack MapIR raw image file per-pixel 12 bit values
        try:
            # unpack a mapir raw image file into per-pixel 12 bit values
            # print(len(self.data))
            assert len(self.data) == 1.5 * 4000 * 3000

            # two pixels are packed into each 3 byte value
            # ABC = nibbles of even pixel (big endian)
            # DEF = nibbles of odd pixel (big endian)
            # bytes in data: BC FA DE

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

            self.img_y, self.img_x, self.img_bands = self.data.shape[0], self.data.shape[1], 3
            self.g_band, self.r_band, self.ir_band = 550, 660, 850
            self.R_index, self.G_index, self.NIR_index = 0, 1, 2

            self._debayer()
            self._correct()
            # self._render_RGB()



        except:
            print(f'File Corrupt: {self.file_name}')

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

        self.data = debayered_data

    # Function to apply radiometric calibration to images
    def _radiometic_calibration(self):

        # Dark Current Subtraction: 7 for each band
        data = self.data.astype(np.float32)
        data -= 8
        data[data < 0] = 0
        self.data = data.astype(np.uint16)

    # Function to band_correction leakage in sensor
    def _correct(self):
        # image_matrix = [[336, 33, 275], [74, 347, 261], [37, 41, 286]]
        image_matrix = [[5481.53, 664.44, 4510.03], [1309.98, 5660.94, 4294.08], [740.54, 796.69, 4686.63]]

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

        # get 8bit arrays for each band
        scale8bit = lambda a: ((a - a.min()) * (1 / (a.max() - a.min()) * 255)).astype('uint8')
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

        # self.rgb_render = rgb_stack
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
        plt.tight_layout(pad=1)
        plt.show()

    # Function to extract GPS metadata from corresponding jpg image
    def extract_GPS(self, file_type):

        path = Path(self.file_path)
        jpg_num = int(path.stem) + 1
        if len(str(jpg_num)) < 3:
            jpg_num = '0' + str(jpg_num)
        jpg_filepath = f'{path.parent}/{jpg_num}.jpg'
        image = Image.open(jpg_filepath)

        exif_data = piexif.load(image.info["exif"])

        # Extract the GPS data from the GPS portion of the metadata
        geolocation = exif_data["GPS"]

        # Create a new NumPy array with float32 data type and copy the geolocation data
        geolocation_array = np.zeros((3,), dtype=np.float32)
        if geolocation:
            latitude = geolocation[piexif.GPSIFD.GPSLatitude]
            longitude = geolocation[piexif.GPSIFD.GPSLongitude]
            altitude = geolocation.get(piexif.GPSIFD.GPSAltitude, [0, 1])  # Add this line

            if latitude and longitude and altitude:  # Add altitude check here
                lat_degrees = latitude[0][0] / latitude[0][1]
                lat_minutes = latitude[1][0] / latitude[1][1]
                lat_seconds = latitude[2][0] / latitude[2][1]

                lon_degrees = longitude[0][0] / longitude[0][1]
                lon_minutes = longitude[1][0] / longitude[1][1]
                lon_seconds = longitude[2][0] / longitude[2][1]

                altitude_val = altitude[0] / altitude[1]  # altitude calculation

                geolocation_array[0] = lat_degrees + (lat_minutes / 60) + (lat_seconds / 3600)
                geolocation_array[1] = lon_degrees + (lon_minutes / 60) + (
                            lon_seconds / 3600)  # updated with lon minutes and seconds
                geolocation_array[2] = altitude_val  # assign altitude to array

            # Append the image geolocation to the geo.txt file
            file_path = os.path.join(path.parent.parent, '_processed', 'geo.txt')

            # Check if the file exists
            if not os.path.exists(file_path):
                # If the file doesn't exist, it is the first time it is being opened
                # Write the header "EPSG:4326"
                with open(file_path, 'w') as f:
                    f.write('EPSG:4326\n')

            # Append the data to the file
            with open(file_path, 'a') as f:
                f.write(f'{path.stem}.{file_type}\t-{geolocation_array[1]}\t{geolocation_array[0]}\t{geolocation_array[2]}\n')

    # Function to export image as 16-bit tiff
    def export_tiff(self):
        # Normalize to 16 bit
        data = self.data
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
        data_scaled = data_norm * 65535
        self.data = data_scaled.astype(np.uint16)

        path = Path(self.file_path)
        save_as = f'{path.parent.parent}/_processed/{path.stem}.tiff'
        imageio.imsave(save_as, self.data, format='tiff')

    # Function to export image as 16-bit png
    def export_png(self):
        path = Path(self.file_path)
        save_as = path.parent.parent/'_processed'/(path.stem+'.png')
        imageio.imwrite(save_as, self.data, 'PNG-FI')

    # Function to export image as 8 bit jpg
    def export_jpg(self):
        path = Path(self.file_path)
        save_as = path.parent.parent / '_processed' / (path.stem + '.jpg')
        # change data to 8bit
        data = self.data
        data_norm = (data - np.min(data)) / (np.max(data) - np.min(data))
        data_scaled = data_norm * 255
        data_8 = data_scaled.astype(np.uint8)
        imageio.imwrite(save_as, data_8, 'jpg', quality=100)
















