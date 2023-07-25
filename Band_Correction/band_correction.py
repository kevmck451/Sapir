# Monochromator Experiment

# Need documentation for how data should be
from Radiance_Calibration.radiance import dark_current_subtraction
from Band_Correction.correction import band_correction
from MapIR.mapir import MapIR
from Band_Correction import hyperspectral as hype



import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Function to generate correction matrix from monochromator experiment
def generate_correction_matrix(directory):
    pixel_sample = (1837, 1330) # center of monochromator light
    wavelength_adjust_list = hype.wavelength_correct(directory) # monochromator wavelength correction table from pika

    test4 = Band_Correction(directory, wavelength_adjust_list, corr=False)
    test4.get_values_area(pixel_sample)
    correction_matrix = test4.integrate_np(display=False, stats=False, prnt=False)

    return correction_matrix


def generate_wavelength_responses(directory, corrected):
    pixel_sample = (1837, 1330)  # center of monochromator light
    wavelength_adjust_list = hype.wavelength_correct(directory)

    if corrected:
        test4 = Band_Correction(directory, wavelength_adjust_list, corr=True)
        filepath = 'Wavelengths_Corr'
    else:
        test4 = Band_Correction(directory, wavelength_adjust_list, corr=False)
        filepath = 'Wavelengths_RAW'

    test4.get_values_area(pixel_sample)

    mbands = np.array(test4.band_list)
    mreds = np.array(test4.red_values)
    mgreens = np.array(test4.green_values)
    mnir = np.array(test4.nir_values)


    np.save(f'{filepath}/MapIR_Bands.npy', mbands)
    np.save(f'{filepath}/MapIR_Rvalues.npy', mreds)
    np.save(f'{filepath}/MapIR_Gvalues.npy', mgreens)
    np.save(f'{filepath}/MapIR_Nvalues.npy', mnir)


# MAPIR MONOCHROMATOR TEST CLASS FOR RAW
class Band_Correction:
    def __init__(self, dir, adjust, corr, corr_matrix=None):
        adjustment = adjust
        directory = Path(dir + '/RAW')
        self.image_list_all = []
        self.band_list = []

        for filename in directory.iterdir():
            if filename.suffix=='.RAW':
                im = MapIR(filename)
                im = dark_current_subtraction(im)
                if corr:
                    if corr_matrix is not None:
                        im = band_correction(im, corr_matrix)
                    else: im = band_correction(im)
                    im.band = int(filename.stem)
                    self.image_list_all.append(im)
                    self.corrected = True
                else:
                    im.band = int(filename.stem)
                    self.image_list_all.append(im)
                    self.corrected = False

                self.band_list.append(int(filename.stem))

        self.band_list.sort()
        new_band_list = []
        if len(adjustment) > 0:
            for band, new_band in zip(self.band_list, adjustment):
                new_band_list.append(band + new_band)
        self.band_list = new_band_list
        self.red_list = []
        self.green_list = []
        self.nir_list = []

    # Function to create list of values from single pixel
    def get_values_pixel(self, pixel):
        for im in self.image_list_all:
            try:
                self.red_list.append( [ int(im.band), im.data[pixel[1], pixel[0], im.R_index] ] )  # 0
                self.green_list.append( [ int(im.band), im.data[pixel[1], pixel[0], im.G_index] ] )  # 1
                self.nir_list.append( [ int(im.band), im.data[pixel[1], pixel[0], im.NIR_index] ] ) # 2

            except:
                print(f'EXCEPTION: {im.file_name}')
        self.red_list.sort()
        self.green_list.sort()
        self.nir_list.sort()

        self.red_values = []
        self.green_values = []
        self.nir_values = []

        for i in range(len(self.red_list)):
            self.red_values.append(self.red_list[i][1])
            self.green_values.append(self.green_list[i][1])
            self.nir_values.append(self.nir_list[i][1])

    # Function to create list of values from single pixel
    def get_values_area(self, pixel):

        for im in self.image_list_all:
            try:
                y1 = pixel[1]-20
                y2 = pixel[1]+20
                x1 = pixel[0]-20
                x2 = pixel[0]+20
                self.red_list.append([int(im.band), im.data[y1:y2, x1:x2, im.R_index].mean()])  # 0
                self.green_list.append([int(im.band), im.data[y1:y2, x1:x2, im.G_index].mean()])  # 1
                self.nir_list.append([int(im.band), im.data[y1:y2, x1:x2, im.NIR_index].mean()])  # 2
            except:
                print(f'EXCEPTION: {im.file_name}')

        # print(self.red_list)

        self.red_list.sort()
        self.green_list.sort()
        self.nir_list.sort()

        self.red_values = []
        self.green_values = []
        self.nir_values = []

        for i in range(len(self.red_list)):
            self.red_values.append(self.red_list[i][1])
            self.green_values.append(self.green_list[i][1])
            self.nir_values.append(self.nir_list[i][1])

    # Function to graph each values in each band
    def graph(self):
        max = np.max(self.red_values)
        if not self.corrected:
            self.red_values.append(1)
            self.green_values.append(1)
            self.nir_values.append(1)
            self.red_values.append(0)
            self.green_values.append(0)
            self.nir_values.append(0)
            self.band_list.append(880)
            self.band_list.append(890)

        plt.figure(figsize=(8,6))
        plt.plot(self.band_list, self.red_values, color='r', linewidth=2, label='Red Values')
        plt.plot(self.band_list, self.green_values, color='g', linewidth=2, label='Green Values')
        plt.plot(self.band_list, self.nir_values, color='b', linewidth=2, label='NIR Values')
        plt.vlines(x=[550, 660, 850], ymin=0, ymax=max, colors='black', ls='--', lw=1, label='MapIR Bands')
        plt.xlabel('Bands')
        plt.ylabel('Counts')
        plt.xticks([x for x in range(500, 900, 25)])
        plt.title('MapIR Monochromator Test: RAW', fontsize=20)
        plt.legend(loc='upper right')
        plt.show()

    # Function to integrate the response for each band for calibration using numpy
    def integrate_np(self, display, stats, prnt):

        # Integration variables
        ra1, ra2, ra3, ga1, ga2, ga3, na1, na2, na3 = 0, 0, 0, 0, 0, 0, 0, 0, 0

        # Integration values from numpy
        # 500-600nm
        yr1 = [0, *self.red_values[4:20], 0]
        yg1 = [0, *self.green_values[4:20], 0]
        yn1 = [0, *self.nir_values[6:20], 0]
        ga1 = np.trapz(yr1)
        ga2 = np.trapz(yg1)
        ga3 = np.trapz(yn1)

        # 600-700nm
        yr2 = [0, *self.red_values[25:40], 0]
        yg2 = [0, *self.green_values[25:40], 0]
        yn2 = [0, *self.nir_values[25:40], 0]
        ra1 = np.trapz(yr2)
        ra2 = np.trapz(yg2)
        ra3 = np.trapz(yn2)

        # 700-850nm
        yr3 = [0, *self.red_values[41:56], 0]
        yg3 = [0, *self.green_values[41:56], 0]
        yn3 = [0, *self.nir_values[41:56], 0]
        na1 = np.trapz(yr3)
        na2 = np.trapz(yg3)
        na3 = np.trapz(yn3)

        redn = ['Ra1', 'Ra2', 'Ra3']
        greenn = ['Ga1', 'Ga2', 'Ga3']
        nirn = ['Na1', 'Na2', 'Na3']
        # red = [int(ra1), int(ra2), int(ra3)]
        # green = [int(ga1), int(ga2), int(ga3)]
        # nir = [int(na1), int(na2), int(na3)]

        red = [round(ra1, 2), round(ra2, 2), round(ra3, 2)]
        green = [round(ga1, 2), round(ga2, 2), round(ga3, 2)]
        nir = [round(na1, 2), round(na2, 2), round(na3, 2)]

        if display:
            plt.figure(figsize=(8, 6))
            plt.bar(redn, red, color=['red', 'green', 'blue'])
            plt.bar(greenn, green, color=['red', 'green', 'blue'])
            plt.bar(nirn, nir, color=['red', 'green', 'blue'])
            plt.text(redn[0], red[0], red[0], ha='center', )
            plt.text(redn[1], red[1], red[1], ha='center')
            plt.text(redn[2], red[2], red[2], ha='center')
            plt.text(greenn[0], green[0], green[0], ha='center', )
            plt.text(greenn[1], green[1], green[1], ha='center')
            plt.text(greenn[2], green[2], green[2], ha='center')
            plt.text(nirn[0], nir[0], nir[0], ha='center', )
            plt.text(nirn[1], nir[1], nir[1], ha='center')
            plt.text(nirn[2], nir[2], nir[2], ha='center')
            plt.title(f'RGN Integration Values: RAW')
            plt.ylabel('Values')
            plt.show()

        Ra1, Ra2, Ra3 = round((red[0]), 2), round((green[0]), 2), round((nir[0]), 2)
        Ga1, Ga2, Ga3 = round((red[1]), 2), round((green[1]), 2), round((nir[1]), 2)
        Na1, Na2, Na3 = round((red[2]), 2), round((green[2]), 2), round((nir[2]), 2)

        calibration = [[Ra1, Ra2, Ra3], [Ga1, Ga2, Ga3], [Na1, Na2, Na3]]

        if stats:
            print(f'RED: {self.red_values}')
            print('-' * 30)
            print(f'GREEN: {self.green_values}')
            print('-' * 30)
            print(f'NIR: {self.nir_values}')
            print(f'Y-R: {yr1}')
            print(f'Y-G: {yg1}')
            print(f'Y-N: {yn1}')
            print(ga1, ga2, ga3)
            print(f'Y-R: {yr2}')
            print(f'Y-G: {yg2}')
            print(f'Y-N: {yn2}')
            print(ra1, ra2, ra3)
            print(f'Y-R: {yr3}')
            print(f'Y-G: {yg3}')
            print(f'Y-N: {yn3}')
            print(na1, na2, na3)
            print(calibration)

        if prnt:
            # print(f'        [ R    G    N   ]')
            # print(f'RED   = [{Ra1}, {Ra2}, {Ra3}]')
            # print(f'GREEN = [{Ga1}, {Ga2}, {Ga3}]')
            # print(f'NIR =   [{Na1}, {Na2}, {Na3}]')
            print(f'Calibration   = [[{Ra1}, {Ra2}, {Ra3}], [{Ga1}, {Ga2}, {Ga3}], [{Na1}, {Na2}, {Na3}]]')

        return calibration


