

from Band_Correction.hyp_envi import Cube

import matplotlib.pyplot as plt
from copy import deepcopy
import numpy as np
import scipy.io
import random
import os


#-----------------------------------------------------------------
# MAPIR RELATED FUNCTIONS
#-----------------------------------------------------------------
# Function to graph all files from Monochromator
def mapir_graph_all():
    pika_f = np.arange(500, 880, 5)
    for band in pika_f:
        try:
            file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
            image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
            image.reduce_bands(bands=(490,880))
            image.graph_all_mapir_pika(display=False, save=False)
        except:
            continue
    plt.title(f'MC Test: Pika')
    plt.show()

# Function to graph all files from Monochromator
def mapir_graph_mapir():
    pika_f = np.arange(525, 576, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(490,880))
        image.graph_all_mapir_pika(display=False, save=False)

    pika_f = np.arange(635, 686, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(490,880))
        image.graph_all_mapir_pika(display=False, save=False)

    pika_f = np.arange(810, 871, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(490,880))
        image.graph_all_mapir_pika(display=False, save=False)

    plt.title(f'MC Test: Pika like MapIR')
    plt.show()

# Function to graph all files from Monochromator
def pika_to_mapir():
    red = []
    firstr = True
    pika_f = np.arange(520, 581, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayr = image.max_array()
        if firstr:
            red = max_arrayr
            firstr = False
        else:
            for i in range(len(red)):
                red[i] = red[i] + max_arrayr[i]


    green = []
    firstg = True
    pika_f = np.arange(630, 691, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayg = image.max_array()
        if firstg:
            green = max_arrayg
            firstg = False
        else:
            for i in range(len(green)):
                green[i] = green[i] + max_arrayg[i]

    nir = []
    firstn = True
    pika_f = np.arange(810, 871, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayn = image.max_array()
        if firstn:
            nir = max_arrayn
            firstn = False
        else:
            for i in range(len(nir)):
                nir[i] = nir[i] + max_arrayn[i]

    x_values = np.linspace(500, 900, len(red))
    plt.plot(x_values, green, color='r', linewidth=2, label='Red Values')
    plt.plot(x_values, red, color='g', linewidth=2, label='Green Values')
    plt.plot(x_values, nir,color='b', linewidth=2, label='NIR Values')
    plt.vlines(x=[550, 650, 850], ymin=0, ymax=255, colors='black', ls='--', lw=1, label='MapIR Bands')
    plt.xlabel('Bands')
    plt.ylabel('Counts')
    # plt.xticks([x for x in range(500, 900, 25)])
    plt.title(f'MC Test: Pika like MapIR')
    plt.legend(loc='upper left')
    plt.show()

# Function to integrate the response for each band for calibration using numpy
def integrate_np(display, stats, prnt):

    #Integration variables
    ra1 = 0
    ra2 = 0
    ra3 = 0
    ga1 = 0
    ga2 = 0
    ga3 = 0
    na1 = 0
    na2 = 0
    na3 = 0

    green_list = []
    firstg = True
    pika_f = np.arange(520, 581, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayg = image.max_array()
        if firstg:
            green_list = max_arrayg
            firstg = False
        else:
            for i in range(len(green_list)):
                green_list[i] = green_list[i] + max_arrayg[i]


    red_list = []
    firstr = True
    pika_f = np.arange(630, 691, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayr = image.max_array()
        if firstr:
            red_list = max_arrayr
            firstr = False
        else:
            for i in range(len(red_list)):
                red_list[i] = red_list[i] + max_arrayr[i]

    nir_list = []
    firstn = True
    pika_f = np.arange(810, 871, 5)
    for band in pika_f:
        file = f'RGN Files/MonoChrom Test 4/pika/radiance/{band}nm.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        image.reduce_bands(bands=(500,900))
        max_arrayn = image.max_array()
        if firstn:
            nir_list = max_arrayn
            firstn = False
        else:
            for i in range(len(nir_list)):
                nir_list[i] = nir_list[i] + max_arrayn[i]

    if stats:
        print(green_list)
        print(red_list)
        print(nir_list)
    # Integration values from numpy
    #500-600nm
    yr1 = [red_list[8:44]]
    yg1 = [green_list[8:44]]
    yn1 = [nir_list[8:44]]
    ga1 = np.trapz(yr1)
    ga2 = np.trapz(yg1)
    ga3 = np.trapz(yn1)

    # 600-700nm
    yr2 = [0, *red_list[60:98], 0]
    yg2 = [0, *green_list[60:98], 0]
    yn2 = [0, *nir_list[60:98], 0]
    ra1 = np.trapz(yr2)
    ra2 = np.trapz(yg2)
    ra3 = np.trapz(yn2)

    # 700-850nm
    yr3 = [0, *red_list[106:180], 0]
    yg3 = [0, *green_list[106:180], 0]
    yn3 = [0, *nir_list[106:180], 0]
    na1 = np.trapz(yr3)
    na2 = np.trapz(yg3)
    na3 = np.trapz(yn3)

    redn = ['Ra1', 'Ra2', 'Ra3']
    greenn = ['Ga1', 'Ga2', 'Ga3']
    nirn = ['Na1', 'Na2', 'Na3']
    red = [int(ra1), int(ra2), int(ra3)]
    green = [int(ga1), int(ga2), int(ga3)]
    nir = [int(na1), int(na2), int(na3)]

    if display:
        plt.bar(greenn, green, color=['red', 'green', 'blue'])
        plt.bar(redn, red, color=['red', 'green', 'blue'])
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
        plt.title(f'RGN Integration Values: JPGS')
        plt.ylabel('Values')
        plt.show()

    rsum = red[0] + green[0] + nir[0]
    gsum = red[1] + green[1] + nir[1]
    nsum = red[2] + green[2] + nir[2]

    print(f'R{rsum} / G{gsum} / N{nsum}')

    Ra1, Ra2, Ra3 = round((red[0] / rsum), 2), round((red[1] / gsum), 2), round((red[2] / nsum), 2)
    Ga1, Ga2, Ga3 = round((green[0] / rsum), 2), round((green[1] / gsum), 2), round((green[2] / nsum), 2)
    Na1, Na2, Na3 = round((nir[0] / rsum), 2), round((nir[1] / gsum), 2), round((nir[2] / nsum), 2)
    calibration = [[Ra1, Ra2, Ra3], [Ga1, Ga2, Ga3], [Na1, Na2, Na3]]

    if stats:
        print(f'RED: {red}')
        print('-' * 30)
        print(f'GREEN: {green}')
        print('-' * 30)
        print(f'NIR: {nir}')
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
        print(f'        [   R       G       B   ]')
        print(f'RED   = [ {Ra1},    {Ra2},     {Ra3} ]')
        print(f'GREEN = [ {Ga1},    {Ga2},     {Ga3} ]')
        print(f'NIR =   [ {Na1},    {Na2},     {Na3} ]')



    return calibration

# Function to graph all files from Monochromator
def mapir_cor_max(display, save):
    pika_f = np.arange(400, 880, 10)
    max_dict = {}
    for band in pika_f:
        file = f'RGN Files/PikaC T3/{band}nm-Radiance From Raw Data.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        list = image.image_metadata()
        max_dict.update( {list[1]:band } )

    if display:
        plt.scatter(max_dict.values(),max_dict.keys())
        plt.title('Pika-Corrected: Max Values')
        plt.xlabel('Bands')
        plt.ylabel('Values')
        plt.show()

    if save:
        saveas = (f'../../Dropbox/2 Work/1 Optics Lab/2 Projects/MapIR/Autosaves/Pika-Corrected Max Values Dict.txt')
        with open(saveas, 'w') as f:
            for x,y in max_dict.items():
                line = f'{str(y)} : {str(x)}\n'
                f.write(line)
            f.close()

# Function to graph all files from Monochromator
def mapir_cor_av(display, save):
    pika_f = np.arange(400, 880, 10)
    max_dict = {}
    for band in pika_f:
        file = f'RGN Files/PikaC T3/{band}nm-Radiance From Raw Data.bip'
        image = Hyperspectral(file)  # a hyperspectral image object using hyperspectral
        list = image.image_metadata()
        max_dict.update( {list[2]:band } )

    if display:
        plt.scatter(max_dict.values(),max_dict.keys())
        plt.title('Pika-Corrected: Mean Values')
        plt.xlabel('Bands')
        plt.ylabel('Values')
        plt.show()

    if save:
        saveas = (f'../../Dropbox/2 Work/1 Optics Lab/2 Projects/MapIR/Autosaves/Pika-Corrected Mean Values Dict.txt')
        with open(saveas, 'w') as f:
            for x,y in max_dict.items():
                line = f'{str(y)} : {str(x)}\n'
                f.write(line)
            f.close()

# Function to compare the wavelength from monocrhom and pika
def mono_pika_comp():

    folder_path = 'RGN Files/MonoChrom Test 4/pika/radiance'
    diff = []
    # loop through all files in the folder
    for filename in os.listdir(folder_path):
        # get the full path of the file
        file_path = os.path.join(folder_path, filename)
        # check if the file is a regular file
        if os.path.isfile(file_path):
            if filename[-1] != 'r':
            # do something with the file
                image = Hyperspectral(file_path)
                diff.append(image.mono_pika_comp(p=False))
        else:
            print('No File')

    min = np.min(diff)
    max = np.max(diff)
    av = round(np.mean(diff), 1)
    print(f'Min: {min} / Max: {max} / Average: {av}')

# Function to return amounts to adjust wavelength dict
def wavelength_correct(directory):

    folder_path = directory + '/pika/radiance'
    diff = []
    # loop through all files in the folder
    for filename in os.listdir(folder_path):
        # get the full path of the file
        file_path = os.path.join(folder_path, filename)
        # check if the file is a regular file
        if os.path.isfile(file_path):
            if filename[-1] != 'r':
            # do something with the file
                image = Hyperspectral(file_path)
                diff.append(image.mono_pika_comp(p=False))
        else:
            print('No File')

    return diff


# HYPERSPECTRAL CLASS FOR VIEWING, PROCESSING, AND ANALYZING HSI
class Hyperspectral:

    # -------------------------------------------------------------------------------
    # LOGISTIC FUNCTIONS
    # -------------------------------------------------------------------------------
    def __init__(self, raw_file_path, stats=False):
        self.edit_record = []
        self.subcategorization = False
        self.raw_file_path = raw_file_path
        if stats: print(f'Raw File Path: {self.raw_file_path}')

        # File Type & File Name
        try:
            file = raw_file_path.split('.')
            self.file_type = file[1]
            if stats: print(f'File Type: {self.file_type}')

            try:
                file_name = file[0].split('/')
                self.file_name = file_name[-1]
                file_path = file_name[0:-1]
                self.file_path = file_path[0]
                for i in range(1, len(file_path)):
                    self.file_path = f'{self.file_path}/{file_path[i]}'
                if stats: print(f'File Name: {self.file_name}')
                if stats: print(f'File Path: {self.file_path}')

            except:
                file_name = file[0]
                self.file_name = file_name
                self.file_path = file[0]
                if stats: print(f'File Name: {self.file_name}')
                if stats: print(f'File Path: {self.file_path}')
        except:
            self.file_type = 'envi'
            if stats: print(f'File Type: {self.file_type}')
            try:
                file_name = raw_file_path.split('/')
                self.file_name = file_name[-1]
                if stats: print(f'File Name: {file_name[-1]}')
            except:
                file_name = raw_file_path
                self.file_name = file_name
                if stats: print(f'File Name: {self.file_name}')

        # data, x, y, bands
        if self.file_type == 'bil':
            data = Cube.from_path(self.raw_file_path)
            data = data.read()  # load into memory in native format as numpy array
            # or load as memory map by adding as_mmap=True
            # then only the parts of the cube you access will be read into memory
            # if you need just a small part this can be much faster
            # print(data)
            data = np.array(data).astype(np.float32)

            self.img_x = int(data.shape[2])
            self.img_y = int(data.shape[0])
            self.img_bands = int(data.shape[1])
            if stats: print(f'X: {self.img_x} / Y: {self.img_y} / Bands: {self.img_bands}')

            # reshape_data = np.zeros((self.img_y, self.img_x, self.img_bands), dtype=float)
            self.data = data.transpose((0, 2, 1))
            self.open_HDR()

        if self.file_type == 'bip':
            data = Cube.from_path(self.raw_file_path)
            data = data.read()  # load into memory in native format as numpy array
            # or load as memory map by adding as_mmap=True
            # then only the parts of the cube you access will be read into memory
            # if you need just a small part this can be much faster
            # print(data)
            self.data = np.array(data).astype(np.float32)

            self.img_x = int(data.shape[1])
            self.img_y = int(data.shape[0])
            self.img_bands = int(data.shape[2])
            if stats: print(f'X: {self.img_x} / Y: {self.img_y} / Bands: {self.img_bands}')

            # reshape_data = np.zeros((self.img_y, self.img_x, self.img_bands), dtype=float)
            # self.data = data.transpose((0,1,2))
            self.open_HDR()

        if self.file_type == 'mat':
            data = scipy.io.loadmat(self.raw_file_path)
            # print(data)

            name = ''
            for i, k, v in zip(range(len(data.keys())), data.keys(), data.values()):
                # print('k: {}'.format(k))
                # print('v: {}'.format(v))
                if i == 3:
                    name = k

            # print(name)
            data = data.get(name)
            self.data = np.array(data).astype(np.float32)  # dtype='u2'

            # print(self.data.shape)
            self.img_x = int(self.data.shape[1])
            self.img_y = int(self.data.shape[0])
            self.img_bands = int(self.data.shape[2])
            if stats: print(f'X: {self.img_x} / Y: {self.img_y} / Bands: {self.img_bands}')

        if self.file_type == 'envi':
            self.data = open(raw_file_path, 'rb')  # with open as data
            self.data = np.frombuffer(self.data.read(), ">i2").astype(np.float32)  # if with open, remove self from data
            self.open_HDR()

            self.img_x = int(self.header_file_dict.get('samples'))
            self.img_y = int(self.header_file_dict.get('lines'))
            self.img_bands = int(self.header_file_dict.get('bands'))
            self.data = self.data.reshape(self.img_y, self.img_x, self.img_bands)
            if stats: print(f'X: {self.img_x} / Y: {self.img_y} / Bands: {self.img_bands}')

        self.edit_record.append(f'Image Stats : Y Dim-{self.img_y}, X Dim-{self.img_x}, Bands-{self.img_bands}')

    # Function to open header files and create variables
    def open_HDR(self):
        '''
        self.hdr_file_path = self.raw_file_path + '.hdr'
        self.header_file_dict = {}
        self.wavelengths_dict = {}
        self.wavelengths = []
        self.fwhm_dict = {}
        '''

        self.hdr_file_path = self.raw_file_path + '.hdr'
        hdr_file = open(self.hdr_file_path, 'r')  # errors='ignore'
        self.header_file_dict = {}
        self.wavelengths_dict = {}
        self.wavelengths = []
        self.fwhm_dict = {}

        if self.file_type == 'bil' or self.file_type == 'bip':
            task_count = 0
            band_num = 1
            fwhm_num = 1

            for i, line in enumerate(hdr_file):
                if task_count == 0:
                    self.hdr_title = line.strip().upper()
                    task_count = 1

                elif task_count == 1:
                    line_split = line.split('=')
                    j = line_split[0].strip()
                    k = line_split[1].strip()
                    self.header_file_dict.update({j: k})
                    if j.lower() == 'wavelength':
                        k = k.strip('}')
                        k = k.strip('{')
                        wave = k.split(',')
                        for w in wave:
                            val = float(w)
                            self.wavelengths.append(val)
                            val = round(val)
                            self.wavelengths_dict.update({band_num: val})
                            band_num += 1
                        task_count = 3

                elif task_count == 3:
                    line_split = line.split('=')
                    j = line_split[0].strip()
                    k = line_split[1].strip()
                    self.header_file_dict.update({j: k})
                    if j.lower() == 'jwhm':
                        line = line.split(',')
                        wave = line[0].strip()
                        if wave.endswith('}'):
                            line = wave.split('}')
                            task_count = 5
                        wave = float(line[0])
                        band_num = 1
                        self.fwhm_dict.update({fwhm_num: wave})
                        fwhm_num += 1

        else:
            task_count = 0
            band_num = 1
            fwhm_num = 1

            for i, line in enumerate(hdr_file):
                if task_count == 0:
                    self.hdr_title = line.strip().upper()
                    task_count = 1

                elif task_count == 1:
                    line_split = line.split('=')
                    j = line_split[0].strip()
                    k = line_split[1].strip()
                    self.header_file_dict.update({j: k})
                    if j.lower() == 'wavelength':
                        task_count = 2

                elif task_count == 2:
                    line = line.split(',')
                    wave = line[0].strip()
                    if wave.endswith('}'):
                        line = wave.split('}')
                        task_count = 3
                    wave = float(line[0])
                    self.wavelengths.append(wave)
                    wave = round(wave)
                    self.wavelengths_dict.update({band_num: wave})

                    band_num += 1

                elif task_count == 3:
                    line_split = line.split('=')
                    j = line_split[0].strip()
                    k = line_split[1].strip()
                    self.header_file_dict.update({j: k})
                    task_count = 4

                elif task_count == 4:
                    line = line.split(',')
                    wave = line[0].strip()
                    if wave.endswith('}'):
                        line = wave.split('}')
                        task_count = 5
                    wave = float(line[0])
                    band_num = 1
                    self.fwhm_dict.update({fwhm_num: wave})
                    fwhm_num += 1

    # Function to write header files with current info
    def write_HDR(self, filepath_name):

        g = open(f'{filepath_name}.hdr', 'w')
        g.writelines('ENVI\n')
        for x, y in self.header_file_dict.items():
            if x == 'wavelength':
                # print('WAVE LENGTH')
                # print(self.wavelengths)
                for i, a in enumerate(self.wavelengths):
                    if i == len(self.wavelengths) - 1:
                        d = str(a), ' }\n'
                    else:
                        if i == 0:
                            d = 'wavelength = {', str(a), ' ,'
                        else:
                            d = str(a), ', '
                    g.writelines(d)
            else:
                if x == 'samples':
                    y = str(self.img_x)
                if x == 'lines':
                    y = str(self.img_y)
                if x == 'bands':
                    y = str(self.img_bands)
                d = x, ' = ', y, '\n'
                g.writelines(d)

        for i, x in enumerate(self.fwhm_dict.values()):
            if i == len(self.fwhm_dict) - 1:
                d = str(x), ' }\n'
            else:
                d = str(x), ' ,\n'
            g.writelines(d)

    # Function to look if a file exists and writes one if doesnt
    def write_record_file(self, save_to, image_name):
        g = open(save_to + image_name + '-Record.txt', 'w')

        for record in self.edit_record:
            g.writelines(record + '\n')

    # Function to export image to a file
    def export(self, save_name='Untitled'):
        import shutil

        filepath = self.file_path.split('/')
        filepath = filepath[:-1]
        # print(filepath)
        for i in range(1, len(filepath)):
            filepath = f'{filepath[0]}/{filepath[i]}'
        filepath = f'{filepath}/{save_name}'

        if not os.path.isdir(filepath):
            os.makedirs(filepath)

        if os.path.isfile(f'{self.file_path}/{self.file_name}.{self.file_type}.png'):
            shutil.copy(f'{self.file_path}/{self.file_name}.{self.file_type}.png',
                        f'{filepath}/{self.file_name} {save_name}.{self.file_type}.png')

        if self.file_type == 'mat':
            print('File Type is mat: Cannot Export')
        else:
            if self.file_type.lower() == 'envi':
                save_to = f'{filepath}/{self.file_name} {save_name}.{self.file_type}'
                export_im = deepcopy(self)
                data = export_im.data.astype('>i2')
                f = open(save_to, "wb")
                f.write(data)
                self.write_HDR(save_to)
            elif self.file_type.lower() == 'bil':
                save_to = f'{filepath}/{self.file_name} {save_name}.{self.file_type}'
                export_im = deepcopy(self)
                data = export_im.data.astype('>i2')
                f = open(save_to, "wb")
                f.write(data)
                self.write_HDR(save_to)
                # self.write_record_file(save_to, image_name)
            elif self.file_type.lower() == 'bip':
                save_to = f'{filepath}/{self.file_name} {save_name}.{self.file_type}'
                export_im = deepcopy(self)
                data = export_im.data.astype('float32')
                f = open(save_to, "wb")
                f.write(data)
                self.write_HDR(save_to)
                # self.write_record_file(save_to, image_name)
            else:
                print('Could not Export')

    # -------------------------------------------------------------------------------
    # EDITING FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to crop the image
    def crop(self, dimension):
        print('Cropping...')
        im_crop = deepcopy(self)

        new_data = np.zeros(shape=(dimension[3] - dimension[2], dimension[1] - dimension[0], self.img_bands))

        for i in range(self.img_bands):
            new_data[:, :, i] = self.data[dimension[2]:dimension[3], dimension[0]:dimension[1], i]

        im_crop.data = new_data
        im_crop.img_x = dimension[1] - dimension[0]
        im_crop.img_y = dimension[3] - dimension[2]

        if self.file_type == 'envi':
            im_crop.header_file_dict['samples'] = str(im_crop.img_x)
            im_crop.header_file_dict['lines'] = str(im_crop.img_y)

        image = self.raw_file_path.split('/')
        image = image[-1]

        record = 'Image Edit: edit = crop, image = {}, dimensions = {}'.format(
            image, dimension)
        self.edit_record.append(record)
        print(f'New Shape: {im_crop.data.shape}')
        return im_crop

    # Function to crop many images from single image
    def crop_many(self):
        name = input('Base Name: ')
        width = int(input('Width: '))
        height = int(input('Height: '))

        while True:
            num = 1
            x1 = int(input('x1 = '))
            x2 = x1 + width
            y1 = int(input('y1 = '))
            y2 = y1 + height

            image = self.crop([x1, x2, y1, y2])
            # image.display_RGB(display=True)
            image.export(f'{name}-{num}')
            num += 1
            exit = input('Crop Another? ')
            if exit == 'n':
                break

    # Function to change the number of bands
    def reduce_bands(self, bands=(300, 1000), index=66):
        print('Reducing Bands')

        try:
            bottom, top = bands[1], bands[0]
            img = deepcopy(self)
            new_wave_dict = {}
            new_wavelengths = []
            new_fwhm_dict = {}

            new_b = 0

            for x in self.wavelengths:
                if top <= x <= bottom:
                    new_wavelengths.append(x)
                    new_b += 1

            new_data = np.zeros(shape=(self.img_y, self.img_x, new_b))
            self.edit_record.append(f'Reduced Bands : Low Band-{bands[1]}, High Band-{bands[0]}, Bands-{new_b}')

            b = 0
            if len(self.fwhm_dict.values()) > 0:
                for i, ((x, y), z) in enumerate(zip(self.wavelengths_dict.items(), self.fwhm_dict.values())):
                    # print(f'i: {i} / x: {x} / y: {y} / z: {z}')
                    if top <= y <= bottom:
                        new_wave_dict.update({(b + 1): y})
                        new_data[:, :, b] = self.data[:, :, x]
                        new_fwhm_dict.update({(b + 1): z})
                        b += 1
            else:
                for i, (x, y) in enumerate(self.wavelengths_dict.items()):
                    # print(f'i: {i} / x: {x} / y: {y}')
                    if top <= y <= bottom:
                        new_wave_dict.update({(b + 1): y})
                        new_data[:, :, b] = self.data[:, :, x]
                        b += 1

            img.header_file_dict['bands'] = str(new_b)
            img.img_bands = new_b
            img.wavelengths_dict = new_wave_dict
            img.wavelengths = new_wavelengths
            img.fwhm_dict = new_fwhm_dict
            img.data = new_data

            self.header_file_dict['bands'] = str(new_b)
            self.img_bands = new_b
            self.wavelengths_dict = new_wave_dict
            self.wavelengths = new_wavelengths
            self.fwhm_dict = new_fwhm_dict
            self.data = new_data

            image = self.raw_file_path.split('/')
            image = image[-1]
            print(f'New Shape: {new_data.shape}')

        except:
            # print('First Except')
            img = deepcopy(self)
            new_data = np.zeros(shape=(self.img_y, self.img_x, index))

            for i in range(index):
                new_data[:, :, i] = self.data[:, :, i]

            img.img_bands = index
            img.data = new_data

            self.edit_record.append(f'Reduced Bands : Low Band-{bands[1]}, High Band-{bands[0]}, Bands-{index}')

    # Function to add noise to pixels already in image
    def add_noise(self, location, size, variation):

        x_list = [(location[0] - size), (location[0] + size)]
        y_list = [location[1] + size, location[1] - size]

        for i in range(y_list[1], y_list[0]):
            for j in range(x_list[0], x_list[1]):
                for k in range(0, self.img_bands):
                    a = self.data[i, j, k]
                    q = abs(round(variation * a))
                    r = random.randint(-q, q)
                    self.data[i, j, k] = a + r

        record = 'Anomaly Synthesis: anomaly added = None, method = 6, size = {}, location = {}, variation = {}'.format(
            size, location, variation)
        self.edit_record.append(record)

    # -------------------------------------------------------------------------------
    # INFO FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to get metadata for single pixel in area we are going to edit
    def pixel_metadata(self, x, y):
        values_single = []
        for i in range(224):
            values_single.append(self.data[y, x, i])

        nums = np.array(values_single)
        min = nums.min()
        max = nums.max()
        av = nums.mean()
        min_max_av_list = [min, max, av]

        return min_max_av_list

    # Function to get metadata for all pixels we are going to edit to see if they are in similar ranges
    def area_metadata(self, y1, y2, x1, x2):
        area_values = []
        for i in range(224):
            for j in range(y1, y2):
                for k in range(x1, x2):
                    area_values.append(self.data[j, k, i])

        nums = np.array(area_values)
        min = nums.min()
        max = nums.max()
        av = nums.mean()
        min_max_av_list = [min, max, av]

        return min_max_av_list

    # Function to get metadata for all pixels in the image
    def image_metadata(self):
        area_values = []
        min = []
        max = []
        av = []

        for i in range(self.img_bands):
            for j in range(self.img_y):
                for k in range(self.img_x):
                    area_values.append(self.data[j, k, i])

            nums = np.array(area_values)
            min.append(nums.min())
            max.append(nums.max())
            av.append(nums.mean())
            area_values = []

        min = np.array(min)
        max = np.array(max)
        av = np.array(av)
        min_total = min.min()
        max_total = max.max()
        av_total = av.mean()
        min_max_av_list = [min_total, max_total, av_total]

        image = self.raw_file_path.split('/')
        image = image[-1]

        return min_max_av_list

    # -------------------------------------------------------------------------------
    # MAPIR FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to graph all spectral signature for every pixel in image
    def graph_mapir_pika(self, display, save):

        x_list = np.linspace(0, (self.img_x - 1))
        y_list = np.linspace(0, (self.img_y - 1))

        for i in x_list:
            for j in y_list:
                values_single = []
                for k in range(self.img_bands):
                    values_single.append(self.data[int(j), int(i), k])

                plt.plot(list(self.wavelengths_dict.values()), values_single, linewidth=1)
                # plt.ylim((0,50))
                plt.xlabel('Bands')
                plt.ylabel('Counts')

        pika_band = 0
        max_val = 0
        for k in range(self.img_bands):
            values_single = []
            for i in x_list:
                for j in y_list:
                    values_single.append(self.data[int(j), int(i), k])
            max_l = np.max(values_single)
            if max_l > max_val:
                pika_band = k
                max_val = max_l

        wl_list = list(self.wavelengths_dict.values())
        pika_band = wl_list[pika_band]

        band = self.file_name
        band = int(band[0:3])
        plt.vlines(x=[band], colors='black', ls='--', lw=1, ymin=0, ymax=100)
        plt.title(f'MC: {self.file_name} / Pika: {pika_band}nm')

        if save:
            saveas = (f'../../Dropbox/2 Work/1 Optics Lab/2 MapIR/Autosaves/{self.file_name}-Graph')
            plt.savefig(saveas)
            plt.close()
        if display:
            plt.show()

    # Function to graph based on max value
    def graph_all_mapir_pika(self, display, save):

        x_list = np.linspace(0, (self.img_x - 1))
        y_list = np.linspace(0, (self.img_y - 1))
        max_v = 0
        y_values = []
        for i in x_list:
            for j in y_list:
                values_single = []
                for k in range(self.img_bands):
                    values_single.append(int(self.data[int(j), int(i), k]))
                m = np.max(values_single)
                if m > max_v:
                    y_values = values_single
                    max_v = m
        plt.plot(list(self.wavelengths_dict.values()), y_values, linewidth=.5)
        # plt.ylim((0,50))
        plt.xlabel('Bands')
        plt.ylabel('Counts')

        pika_band = 0
        max_val = 0
        for k in range(self.img_bands):
            values_single = []
            for i in x_list:
                for j in y_list:
                    values_single.append(self.data[int(j), int(i), k])
            max_l = np.max(values_single)
            if max_l > max_val:
                pika_band = k
                max_val = max_l

        wl_list = list(self.wavelengths_dict.values())
        pika_band = wl_list[pika_band]

        band = self.file_name
        band = int(band[0:3])
        # plt.vlines(x=[band], colors='black', ls='--', lw=1, ymin=0, ymax=100)
        # plt.title(f'MC: {self.file_name} / Pika: {pika_band}nm')

        if save:
            saveas = (f'../../Dropbox/2 Work/1 Optics Lab/2 MapIR/Autosaves/{self.file_name}-Graph')
            plt.savefig(saveas)
            plt.close()
        if display:
            plt.show()

    # Function to return array
    def max_array(self):

        x_list = np.linspace(0, (self.img_x - 1))
        y_list = np.linspace(0, (self.img_y - 1))
        max_v = 0
        y_values = []
        for i in x_list:
            for j in y_list:
                values_single = []
                for k in range(self.img_bands):
                    values_single.append(int(self.data[int(j), int(i), k]))
                m = np.max(values_single)
                if m > max_v:
                    y_values = values_single
                    max_v = m

        return y_values

    # Function to return the difference between mono and pika
    def mono_pika_comp(self, p):

        x_list = np.linspace(0, (self.img_x - 1))
        y_list = np.linspace(0, (self.img_y - 1))

        pika_band = 0
        max_val = 0

        for k in range(self.img_bands):
            values_single = []
            for i in x_list:
                for j in y_list:
                    values_single.append(self.data[int(j), int(i), k])
            max_l = np.max(values_single)
            if max_l > max_val:
                pika_band = k
                max_val = max_l

        wl_list = list(self.wavelengths_dict.values())
        pika_band = wl_list[pika_band]

        mono_band = self.file_name
        mono_band = int(mono_band[0:3])
        diff = pika_band - mono_band
        if p: print(f'Mono Band: {mono_band} / Pika: {pika_band} / Diff = {diff}')

        return diff

    # Function to display synthesized MapIR Image
    def display_Mapir_Single(self, display, save=False):
        # print(self.wavelengths_dict)
        # 525 - 575 or 550
        # 67 - 91 or 79

        # 625 - 675 or 650
        # 115 - 138 or 127

        # 800 - 875 or 850
        # 196 - 242 or 219

        Ri = 127  # 30 #25  # 35 #25 #29 #32
        Gi = 79  # 20 #20  # 20 #15 #17 #19
        Bi = 219  # 10 #15  # 17 #5 #10 #12

        # get r,g,b arrays
        Ra = self.data[:, :, Ri]
        Ga = self.data[:, :, Gi]
        Ba = self.data[:, :, Bi]

        # set fill values (-9999.) to 0 for each array
        Ra[Ra == -50], Ga[Ga == -50], Ba[Ba == -50] = 0, 0, 0

        # get 8bit arrays for each band
        scale8bit = lambda a: ((a - a.min()) * (1 / (a.max() - a.min()) * 255)).astype('uint8')
        Ra8, Ga8, Ba8 = scale8bit(Ra), scale8bit(Ga), scale8bit(Ba)

        # set rescaled fill pixels back to 0 for each array
        Ra8[Ra == 0], Ga8[Ga == 0], Ba8[Ba == 0] = 0, 0, 0

        # make rgb stack
        rgb_stack = np.zeros((self.img_y, self.img_x, 3), 'uint8')
        rgb_stack[..., 0], rgb_stack[..., 1], rgb_stack[..., 2] = Ra8, Ga8, Ba8

        # apply histogram equalization to each band
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

        self.rgb_graph = rgb_stack

        if save:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            saveas = (f'{self.file_path}/{self.file_name}-RGB')
            plt.savefig(saveas)
            plt.close()

        if display == True:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            plt.show()

    # Function to display synthesized MapIR Image
    def display_Mapir_Range(self, display, save=False):
        # print(self.wavelengths_dict)
        # 525 - 575 or 550
        # 67 - 91 or 79

        # 625 - 675 or 650
        # 115 - 138 or 127

        # 800 - 875 or 850
        # 196 - 242 or 219

        Ri = 127  # 30 #25  # 35 #25 #29 #32
        Gi = 79  # 20 #20  # 20 #15 #17 #19
        Bi = 219  # 10 #15  # 17 #5 #10 #12

        # get r,g,b arrays
        Ra = self.data[:, :, Ri]
        Ga = self.data[:, :, Gi]
        Ba = self.data[:, :, Bi]

        # set fill values (-9999.) to 0 for each array
        Ra[Ra == -50], Ga[Ga == -50], Ba[Ba == -50] = 0, 0, 0

        # get 8bit arrays for each band
        scale8bit = lambda a: ((a - a.min()) * (1 / (a.max() - a.min()) * 255)).astype('uint8')
        Ra8, Ga8, Ba8 = scale8bit(Ra), scale8bit(Ga), scale8bit(Ba)

        # set rescaled fill pixels back to 0 for each array
        Ra8[Ra == 0], Ga8[Ga == 0], Ba8[Ba == 0] = 0, 0, 0

        # make rgb stack
        rgb_stack = np.zeros((self.img_y, self.img_x, 3), 'uint8')
        rgb_stack[..., 0], rgb_stack[..., 1], rgb_stack[..., 2] = Ra8, Ga8, Ba8

        # apply histogram equalization to each band
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

        self.rgb_graph = rgb_stack

        if save:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            saveas = (f'{self.file_path}/{self.file_name}-RGB')
            plt.savefig(saveas)
            plt.close()

        if display == True:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            plt.show()

    # -------------------------------------------------------------------------------
    # GRAPH FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to create a material from single pixel in image
    def graph_spectra_pixel(self, location, title, single):
        values_single = []
        for i in range(self.img_bands):
            values_single.append(self.data[location[1], location[0], i])

        # print(self.wavelengths_dict)
        try:
            plt.plot(list(self.wavelengths_dict.values()), values_single, linewidth=2, label=title)

        except:
            x_a = np.linspace(0, self.img_bands, num=self.img_bands)
            plt.plot(x_a, values_single, linewidth=2, label=title)

        plt.xlabel('Bands')
        plt.ylabel('Counts')
        # plt.legend(loc='upper right')
        if single:
            plt.show()

    # Function to graph all spectral signature for every pixel in image
    def graph_spectra_all_pixels(self):

        x_list = np.linspace(0, (self.img_x - 1), 100)
        y_list = np.linspace(0, (self.img_y - 1), 100)

        for i in x_list:
            for j in y_list:
                self.graph_spectra_pixel([int(i), int(j)], 'Full', False)
        plt.show()


    # -------------------------------------------------------------------------------
    # DISPLAY FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to plot 6 bands of the HSI
    def display_image(self):
        # color_map = 'nipy_spectral'
        # color_map = 'gist_earth'
        # color_map = 'gist_ncar' #fav so far
        color_map = 'Greys_r'
        vmin = -50
        vmax = 7000
        band_list = [50, 39, 24, 18, 12, 8]
        font_size = 12

        # plt.figure(figsize=(18, 8))
        # plt.subplot(161)
        plt.imshow(self.data[:, :, 0], cmap=plt.get_cmap(color_map))
        # plt.title('IR-Band: {} nm'.format(self.wavelengths_dict.get(band_list[0])), fontsize=font_size)
        plt.axis('off')

        plt.show()

    # Function to display the RGB Image
    def display_RGB(self, display, save=False):
        # print(self.wavelengths_dict)
        r, g, b = 650, 550, 450
        switched_dict = {v: k for k, v in self.wavelengths_dict.items()}
        Ri, Gi, Bi = None, None, None

        while Ri is None:
            Ri = switched_dict.get(r)
            r += 1
        while Gi is None:
            Gi = switched_dict.get(g)
            g += 1
        while Bi is None:
            Bi = switched_dict.get(b)
            b += 1

        # print(f'R: {Ri} / G: {Gi} / B: {Bi}')
        # Ri = 29 #30 #25  # 35 #25 #29 #32
        # Gi = 18 #20 #20  # 20 #15 #17 #19
        # Bi = 8 #10 #15  # 17 #5 #10 #12

        # get r,g,b arrays
        Ra = self.data[:, :, Ri]
        Ga = self.data[:, :, Gi]
        Ba = self.data[:, :, Bi]


        # # set fill values (-9999.) to 0 for each array
        # Ra[Ra == -50], Ga[Ga == -50], Ba[Ba == -50] = 0, 0, 0

        # get 8bit arrays for each band
        scale8bit = lambda a: ((a - a.min()) * (1 / (a.max() - a.min()) * 255)).astype('uint8')
        Ra8, Ga8, Ba8 = scale8bit(Ra), scale8bit(Ga), scale8bit(Ba)

        # set rescaled fill pixels back to 0 for each array
        Ra8[Ra == 0], Ga8[Ga == 0], Ba8[Ba == 0] = 0, 0, 0

        # make rgb stack
        rgb_stack = np.zeros((self.img_y, self.img_x, 3), 'uint8')
        rgb_stack[..., 0], rgb_stack[..., 1], rgb_stack[..., 2] = Ra8, Ga8, Ba8

        # apply histogram equalization to each band
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

        self.rgb_graph = rgb_stack

        if save:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            saveas = (f'{self.file_path}/{self.file_name}-RGB')
            plt.savefig(saveas)
            plt.close()

        if display == True:
            plt.imshow(rgb_stack, cmap=plt.get_cmap(None))
            plt.axis('off')
            plt.show()


    # -------------------------------------------------------------------------------
    # VEGETATION INDICES FUNCTIONS
    # -------------------------------------------------------------------------------
    # Function to display the NDVI
    def display_NDVI(self, display, save=False, r=650, n=850):
        print('NDVIing')
        switched_dict = {v: k for k, v in self.wavelengths_dict.items()}
        red, nir = None, None

        while red is None:
            red = switched_dict.get(r)
            r += 1
        while nir is None:
            nir = switched_dict.get(n)
            n += 1

        # print(f'red: {red} / r: {r} / nir: {nir} / n: {n}')
        RED = self.data[:, :, red]
        NIR = self.data[:, :, nir]

        RED, NIR = RED.astype('float'), NIR.astype('float')
        top, bottom = NIR - RED, NIR + RED
        top[top == 0], bottom[bottom == 0] = 0, np.nan

        ndvi_array = np.divide(top, bottom)
        ndvi_array[ndvi_array < 0] = 0
        ndvi_array[ndvi_array > 1] = 1

        self.index_ndvi = np.zeros((self.data.shape[0], self.data.shape[1]), dtype=float)
        self.index_ndvi = ndvi_array

        if save:
            plt.figure(figsize=(20, 25))
            plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
            plt.title('NDVI')
            plt.colorbar()
            plt.axis('off')
            saveas = f'{self.file_path}/{self.file_name}-NDVI'
            plt.savefig(saveas)
            plt.close()

        if display:
            plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
            plt.title('NDVI')
            plt.colorbar()
            plt.axis('off')
            plt.show()

    # Function to tell average values in an area
    def NDVI_area_values(self, middle_pixel, r=650, n=850):
        print('NDVIing')
        switched_dict = {v: k for k, v in self.wavelengths_dict.items()}
        red, nir = None, None

        while red is None:
            red = switched_dict.get(r)
            r += 1
        while nir is None:
            nir = switched_dict.get(n)
            n += 1

        # print(f'red: {red} / r: {r} / nir: {nir} / n: {n}')
        RED = self.data[:, :, red]
        NIR = self.data[:, :, nir]

        RED, NIR = RED.astype('float'), NIR.astype('float')
        top, bottom = NIR - RED, NIR + RED
        top[top == 0], bottom[bottom == 0] = 0, np.nan

        ndvi_array = np.divide(top, bottom)
        ndvi_array[ndvi_array < 0] = 0
        ndvi_array[ndvi_array > 1] = 1

        self.index_ndvi = np.zeros((self.data.shape[0], self.data.shape[1]), dtype=float)
        self.index_ndvi = ndvi_array

        plus_minus = 40
        x1 = (middle_pixel[0]-plus_minus)
        x2 = (middle_pixel[0]+plus_minus)
        y1 = (middle_pixel[1]-plus_minus)
        y2 = (middle_pixel[1]+plus_minus)

        average_value = ndvi_array[y1:y2, x1:x2].mean()
        print(average_value)

# VEGETATION INDICES CLASS
class vegetation_indices:

    def __init__(self, image):
        self.image = image

    # Function to display the NDVI
    def NDVI(self, display, save=False, r=650, n=850):
        print('NDVIing')
        switched_dict = {v: k for k, v in self.image.wavelengths_dict.items()}
        red, nir = None, None

        while red is None:
            red = switched_dict.get(r)
            r += 1
        while nir is None:
            nir = switched_dict.get(n)
            n += 1

        # print(f'red: {red} / r: {r} / nir: {nir} / n: {n}')
        RED = self.image.data[:, :, red]
        NIR = self.image.data[:, :, nir]

        RED, NIR = RED.astype('float'), NIR.astype('float')
        top, bottom = NIR - RED, NIR + RED
        top[top == 0], bottom[bottom == 0] = 0, np.nan

        ndvi_array = np.divide(top, bottom)
        ndvi_array[ndvi_array < 0] = 0
        ndvi_array[ndvi_array > 1] = 1

        self.index_ndvi = np.zeros((self.image.data.shape[0], self.image.data.shape[1]), dtype=float)
        self.index_ndvi = ndvi_array

        if save:
            plt.figure(figsize=(20, 25))
            plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
            plt.title('NDVI')
            plt.colorbar()
            plt.axis('off')
            saveas = f'{self.image.filepath}/{self.image.file_name}-NDVI'
            plt.savefig(saveas)
            plt.close()

        if display:
            plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
            plt.title('NDVI')
            plt.colorbar()
            plt.axis('off')
            plt.show()

# PIXEL CLASS TO STORE LOCATION, VALUES, AND CATEGORY
class pixel_class:

    def __init__(self, location, values):
        self.location = location
        self.values = values
        self.cat_num = 0
        self.subcat_num = 0
        self.subcategory = object