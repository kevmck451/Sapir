# MapIR Radiance_Calibration Processing

from MapIR.mapir import MapIR
from Band_Correction.correction import band_correction
from Radiance_Calibration.radiance import dark_current_subtraction
from Radiance_Calibration.radiance import flat_field_correction
from data_filepaths import *

import matplotlib.pyplot as plt
from pathlib import Path
from scipy.interpolate import interp1d
import numpy as np



# Function to Generate the Dark Current Subtraction Amount for Each Band
def generate_dark_current_values(directory):
    r_mean_values = []
    g_mean_values = []
    n_mean_values = []

    files = Path(directory).iterdir()
    for file in files:
        if file.suffix == '.RAW':
            image = MapIR(file)
            # image = band_correction(image)

            r_mean_values.append(np.mean(image.data[:, :, 0]))
            g_mean_values.append(np.mean(image.data[:, :, 1]))
            n_mean_values.append(np.mean(image.data[:, :, 2]))


    print(f'Red Mean: {r_mean_values}')
    print(f'Green Mean: {g_mean_values}')
    print(f'NIR Mean: {n_mean_values}')

    r_dcs = np.mean(r_mean_values)
    g_dcs = np.mean(g_mean_values)
    n_dcs = np.mean(n_mean_values)

    print(f'Red_Mean = {r_dcs}')
    print(f'Green_Mean = {g_dcs}')
    print(f'NIR_Mean = {n_dcs}')

    return r_dcs, g_dcs, n_dcs

# Function to Generate the Flat Field Correction Matrix for Each Band
def generate_flat_field_correction(filepath, save=False):
    image = MapIR(filepath)
    image = dark_current_subtraction(image)
    image = band_correction(image)

    red_flat = image.data[:, :, 0]
    green_flat = image.data[:, :, 1]
    nir_flat = image.data[:, :, 2]

    red_ff_cor_matrix = red_flat / np.mean(red_flat)
    green_ff_cor_matrix = green_flat / np.mean(green_flat)
    nir_ff_cor_matrix = nir_flat / np.mean(nir_flat)

    if save:
        np.save('flat_field/ff_cor_matrix_red.npy', red_ff_cor_matrix)
        np.save('flat_field/ff_cor_matrix_green.npy', green_ff_cor_matrix)
        np.save('flat_field/ff_cor_matrix_nir.npy', nir_ff_cor_matrix)

    return red_ff_cor_matrix, green_ff_cor_matrix, nir_ff_cor_matrix

# Function to dot product correction bands
def generate_rad_val_fully_open():

    mbands = np.load(MC_Test_Bands)
    reds = np.load(MC_Test_Reds_Corr)
    greens = np.load(MC_Test_Greens_Corr)
    nirs = np.load(MC_Test_NIR_Corr)

    lab_bands = np.load(labsphere_bands)
    lab_rad_values = np.load(labsphere_rad_values)

    # for band, r, g, n in zip(mbands, mreds, mgreens, mnir):
    #     print(f'B: {band} \t |\t R: {r} \t |\t G: {g} \t |\t N: {n}')
    #
    # for band, val in zip(lab_bands, lab_rad_values):
    #     print(f'B: {band} \t |\t V: {val}')

    # interpolate values
    red_interp = interp1d(mbands, reds, kind='linear')
    green_interp = interp1d(mbands, greens, kind='linear')
    nir_interp = interp1d(mbands, nirs, kind='linear')

    red_rad = sum(red_interp(band) * rad for band, rad in zip(lab_bands, lab_rad_values))
    green_rad = sum(green_interp(band) * rad for band, rad in zip(lab_bands, lab_rad_values))
    nir_rad = sum(nir_interp(band) * rad for band, rad in zip(lab_bands, lab_rad_values))

    print(red_rad)
    print(green_rad)
    print(nir_rad)

    '''
    radiance values at fully open:
    R = 150.11074734882624
    G = 96.22091612057928
    N = 223.14803041806604
    '''

    return red_rad, green_rad, nir_rad

# Function to Generate the Slope and Intercept values for Radiance Calibration
def generate_radiance_equation_values(directory):
    pass


# MapIR class to process_single RAW images
class MapIR_Radiance(MapIR):
    def __init__(self, raw_file_path):
        super().__init__(raw_file_path)

    # Function to show max values specifically for dark images
    def dark_current_subtraction(self, display=True):
        mean_r = int(np.mean(self.data[:, :, 0]))
        mean_g = int(np.mean(self.data[:, :, 1]))
        mean_n = int(np.mean(self.data[:, :, 2]))

        print(mean_r, mean_g, mean_n)

        # Calculate the maximum and minimum values for each channel
        max_r, min_r = np.max(self.data[:, :, 0]), np.min(self.data[:, :, 0])
        max_g, min_g = np.max(self.data[:, :, 1]), np.min(self.data[:, :, 1])
        max_n, min_n = np.max(self.data[:, :, 2]), np.min(self.data[:, :, 2])

        # Use the variables as needed
        # print(f'Max R: {max_r}')
        # print(f'Min R: {min_r}')
        # print(f'Max G: {max_g}')
        # print(f'Min G: {min_g}')
        # print(f'Max B: {max_n}')
        # print(f'Min B: {min_n}')

        # Find the indices where the value equals the maximum value
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

        amount_r = len(threshold_indices_R[0])
        amount_g = len(threshold_indices_G[0])
        amount_n = len(threshold_indices_N[0])

        return [threshold_indices_R, threshold_indices_G, threshold_indices_N,
                f'Values: {threshold_r}-{max_r}(max)',
                f'Values: {threshold_g}-{max_g}(max)',
                f'Values: {threshold_n}-{max_n}(max)',
                amount_r, amount_g, amount_n]

    # Function to show horizontal vs vertical brightness in image
    def flat_field_hori_vert(self):
        y_mid = 1500
        x_mid = 2000
        size = 50

        mean_r = np.mean(self.data[:, :, 0])
        mean_g = np.mean(self.data[:, :, 1])
        mean_n = np.mean(self.data[:, :, 2])

        average_value_R = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 0])
        # print(f'R Mid Value: {self.data[y_mid, x_mid, 0]} | R Mid Average: {average_value_R}')
        # print(f'R Average: {np.mean(self.data[:,:,0])}')
        # print(f'R Stan Dev: {np.std(self.data[:,:,0])}')
        average_value_G = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 1])
        # print(f'G Mid Value: {self.data[y_mid, x_mid, 1]} | G Mid Average: {average_value_G}')
        # print(f'G Average: {np.mean(self.data[:, :, 1])}')
        # print(f'G Stan Dev: {np.std(self.data[:, :, 1])}')
        average_value_N = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 2])
        # print(f'N Mid Value: {self.data[y_mid, x_mid, 2]} | N Mid Average: {average_value_N}')
        # print(f'N Average: {np.mean(self.data[:, :, 2])}')
        # print(f'N Stan Dev: {np.std(self.data[:, :, 2])}')
        # print('-' * 50)

        x = [x for x in range(0, 4000)]
        plt.figure(figsize=(14, 4))
        plt.suptitle(f'{self.path.name}')
        plt.subplot(1, 2, 1)
        plt.scatter(x, self.data[y_mid, :, 0], color='red', s=1)
        # plt.axhline(y=average_value_R, color='r', linestyle='dotted')
        # plt.axhline(y=mean_r, color='r', linestyle='--')
        plt.scatter(x, self.data[y_mid, :, 1], color='green', s=1)
        # plt.axhline(y=average_value_G, color='g', linestyle='dotted')
        # plt.axhline(y=mean_g, color='g', linestyle='--')
        plt.scatter(x, self.data[y_mid, :, 2], color='blue', s=1)
        # plt.axhline(y=average_value_N, color='b', linestyle='dotted')
        # plt.axhline(y=mean_n, color='b', linestyle='--')
        plt.title(f'Horizontal')
        plt.ylim((0, 4096))
        # plt.legend()

        y = [x for x in range(0, 3000)]
        plt.subplot(1, 2, 2)
        plt.scatter(y, self.data[:, x_mid, 0], color='red', s=1, label='Red Band')
        # plt.axhline(y=average_value_R, color='r', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_r, color='r', linestyle='--', label='Average')
        plt.scatter(y, self.data[:, x_mid, 1], color='green', s=1, label='Green Band')
        # plt.axhline(y=average_value_G, color='g', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_g, color='g', linestyle='--', label='Average')
        plt.scatter(y, self.data[:, x_mid, 2], color='blue', s=1, label='NIR Band')
        # plt.axhline(y=average_value_N, color='b', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_n, color='b', linestyle='--', label='Average')
        plt.title(f'Vertical')
        plt.ylim((0, 4096))
        # plt.legend()

        plt.show()

    # Function to get the flat field correction matrix for each band
    def flat_field_correction(self, display=False):
        red_flat = self.data[:, :, 0]
        green_flat = self.data[:, :, 1]
        nir_flat = self.data[:, :, 2]

        red_flat_mean = red_flat / np.mean(red_flat)
        green_flat_mean = green_flat / np.mean(green_flat)
        nir_flat_mean = nir_flat / np.mean(nir_flat)

        # print('RED')
        # print(red_flat_mean)
        # print('-' * 40)
        # print('GREEN')
        # print(green_flat_mean)
        # print('-' * 40)
        # print('NIR')
        # print(nir_flat_mean)
        # print('-' * 40)

        np.save('flat_field/red_ff_cor_matrix.npy', red_flat_mean)
        np.save('flat_field/green_ff_cor_matrix.npy', green_flat_mean)
        np.save('flat_field/nir_ff_cor_matrix.npy', nir_flat_mean)

        red_corrected = red_flat / red_flat_mean
        green_corrected = green_flat / green_flat_mean
        nir_corrected = nir_flat / nir_flat_mean


        # Plot Originals vs Corrected
        if display:
            plt.figure(figsize=(14, 5))
            plt.suptitle(f'Flat Field Correction - File: {self.path.stem} / Stage: {self.stage}')

            rows, cols = 2, 3
            plt.subplot(rows, cols, 1)
            plt.imshow(self.data[:, :, 0], cmap='Reds', vmin=0, vmax=4095)
            plt.title(f'Red Original')
            plt.colorbar()
            plt.axis(False)

            plt.subplot(rows, cols, 2)
            plt.imshow(self.data[:, :, 1], cmap='Greens', vmin=0, vmax=4095)
            plt.title(f'Green Original')
            plt.colorbar()
            plt.axis(False)

            plt.subplot(rows, cols, 3)
            plt.imshow(self.data[:, :, 2], cmap='Blues', vmin=0, vmax=4095)
            plt.title(f'NIR Original')
            plt.colorbar()
            plt.axis(False)

            plt.subplot(rows, cols, 4)
            plt.imshow(red_corrected, cmap='Reds', vmin=0, vmax=4095)
            plt.title(f'Red Adjusted')
            plt.colorbar()
            plt.axis(False)

            plt.subplot(rows, cols, 5)
            plt.imshow(green_corrected, cmap='Greens', vmin=0, vmax=4095)
            plt.title(f'Green Adjusted')
            plt.colorbar()
            plt.axis(False)

            plt.subplot(rows, cols, 6)
            plt.imshow(nir_corrected, cmap='Blues', vmin=0, vmax=4095)
            plt.title(f'NIR Adjusted')
            plt.colorbar()
            plt.axis(False)

            plt.tight_layout(pad=1)
            plt.show()

    # Function to get average center values from images
    def radiance_values_center(self):
        y_mid = 1500
        x_mid = 2000
        size = 50

        average_value_R = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 0])
        average_value_G = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 1])
        average_value_N = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 2])

        # print(f'R: {average_value_R}\t |\t G: {average_value_G}\t |\t N: {average_value_N}')
        return average_value_R, average_value_G, average_value_N

    # Function to get average center values from images
    def radiance_values(self):
        average_value_R = np.mean(self.data[:, :, 0])
        average_value_G = np.mean(self.data[:, :, 1])
        average_value_N = np.mean(self.data[:, :, 2])

        print(f'All: {average_value_R} | {average_value_G} | {average_value_N}')
        return average_value_R, average_value_G, average_value_N

