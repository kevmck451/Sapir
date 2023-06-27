'''Analysis of Data from MapIR Camera'''

import matplotlib.pyplot as plt
import numpy as np
import imageio.v3 as iio
from MapIR import MapIR_jpg as mir
from MapIR import MapIRChromTest as mct
from Hyperspectral_1_2 import Hyperspectral as h
import Hyperspectral_1_2 as hs
import time

#------------------------------------------------
# Calibration Process: Integrate based on Test 3
#------------------------------------------------
# middle = (1881, 1154)
# test3 = mct('RGN Files/MonoChrom Test 3')
# test3.get_values_pixel(middle)
# cali_values = test3.integrate_bw(100, True) #returns list [red_scale_val, green_scale_val, nir_scale_val]

#------------------------------------------------
# Calibration Process: Integrate based on Test 4
#------------------------------------------------
# middle = (1837, 1330)
# wavelength_adjust_list = hs.wavelength_correct()
# test4 = mct('RGN Files/MonoChrom Test 4/jpgs', wavelength_adjust_list)
# test4.get_values_pixel(middle)
# cali_values = test4.integrate_np(display=False, stats=False)

#------------------------------------------------
# Image Analysis:
#------------------------------------------------
# raw_file_path = 'RGN Files/727 Section-Cal.png'
# raw_file_path = 'RGN Files/727 Section.png'
# raw_file_path = 'RGN Files/818 Section.png'
# raw_file_path = 'RGN Files/818 Large Area.png'
# raw_file_path = 'RGN Files/Beets.png'
# raw_file_path = 'RGN Files/Oranges.png'
# raw_file_path = 'RGN Files/Rapini.png'
# raw_file_path = 'RGN Files/Corn.png'
# raw_file_path = 'RGN Files/AZ Anomalies.png'
# raw_file_path = 'RGN Files/727 Section-KCal.png'
# raw_file_path = 'RGN Files/818 Section-KCal.png'
# raw_file_path = 'RGN Files/818 Large Area-KCal.png'
# raw_file_path = 'RGN Files/Beets-KCal.png'
# raw_file_path = 'RGN Files/Oranges-KCal.png'
# raw_file_path = 'RGN Files/Rapini-KCal.png'
# raw_file_path = 'RGN Files/Corn-KCal.png'

file_list = ['RGN Files/727 Section.png',
             'RGN Files/818 Section.png',
             'RGN Files/Beets.png',
             'RGN Files/Oranges.png',
             'RGN Files/Rapini.png',
             'RGN Files/727 Section-KCal.png',
             'RGN Files/818 Section-KCal.png',
             'RGN Files/Beets-KCal.png',
             'RGN Files/Oranges-KCal.png',
             'RGN Files/Rapini-KCal.png']

# for file in file_list:
#     image = mir(file)
#     image.display_image()
#     image.NDVI(threshold=False, display=False, save=True)
    # image.NDVI_Mm()

# image = mir(raw_file_path)
# image.calibrate_2(calibration=cali_values, save=False, name='KCal')
# image.display_image()
#
# image.NDVI(threshold=True, display=True, save=False)
# image.NDVI_Mm()
# image.NDVI_Mm(max_val=0.50)

# image.graph_mapir_pika(display=True, save=False)

# location = [0, 0]
# title = ''
# t = time.time()
# for x in range(100):
#     location[0] = location[0] + x
#     location[1] = location[1] + x
#     image.graph_spectra_pixel(location, title, False)
# print(f'{time.time() - t} seconds')
# plt.show()


#------------------------------------------------
# Test 1
#------------------------------------------------

# raw_file_path = 'RGN Files/MonoChrom Test/650.jpg'
# image = mir(raw_file_path)
# image.display_image()

# middle = (1840, 1480)
# middle = (1990, 1520)
#
# samples = [(1951,1188), (1991,1285), (2000,1415), (2008,1529), (2000,1667),
#             (1943,1813), (1862,1886), (1707,1845), (1626,1707), (1634,1561),
#             (1642,1431), (1659,1285), (1724,1212), (1780,1139), (2089,1099),
#             (2121,1277), (2129,1512), (2113,1707), (2048,1918), (1886,2089),
#             (1683,2040), (1529,1910), (1504,1707), (1488,1464), (1529,1245),
#             (1642,1107), (1764,936), (1951,928)]

# test = mct('RGN Files/MonoChrom Test')
# test.get_values_pixel(middle)
# test.graph()

# test2 = mct('RGN Files/MonoChrom Test')
# test2.get_values_area(samples)
# test2.graph()

#------------------------------------------------
# Test 2
#------------------------------------------------
# raw_file_path = 'RGN Files/MonoChrom Test 2/650.jpg'
# image = mir(raw_file_path)
# image.display_image()

# middle = (1912, 1162)
#
# samples = [(1571,1146), (1618,1138), (1672,1138), (1734,1146), (1788,1154),
#             (1850,1154), (1896,1162), (1935,1169), (2020,1169), (2059,1169),
#             (2113,1169), (2190,1177)]
#
#
# test = mct('RGN Files/MonoChrom Test 2')
# test.get_values_pixel(middle)
# test.graph()
#
# test2 = mct('RGN Files/MonoChrom Test 2')
# test2.get_values_area(samples)
# test2.graph()

#------------------------------------------------
# Test 3
#------------------------------------------------
# raw_file_path = 'RGN Files/MonoChrom Test 3/550.jpg'
# image = mir(raw_file_path)
# image.display_image()

# middle = (1881, 1154)
#
# test3 = mct('RGN Files/MonoChrom Test 3')
# test3.get_values_pixel(middle)
# test3.graph()

#------------------------------------------------
# Test 4
#------------------------------------------------
# raw_file_path = 'RGN Files/MonoChrom Test 4/jpgs/550.JPG'
# image = mir(raw_file_path)
# image.display_image()
#
# middle = (1837, 1330)
#
# wavelength_adjust_list = hs.wavelength_correct()
# # print(wavelength_adjust_list)
#
# test4 = mct('RGN Files/MonoChrom Test 4/jpgs', wavelength_adjust_list)
# test4.get_values_pixel(middle)
# test4.graph()


#------------------------------------------------
# Pika Info
#------------------------------------------------

# file = 'RGN Files/MonoChrom Test 4/pika/radiance/550nm.bip'
# image = h(file) #a hyperspectral image object using hyperspectral
# image.graph_mapir_pika(display=True, save=False)
# wavelength_adjust_list = hs.wavelength_correct()
# print(wavelength_adjust_list)

#------------------------------------------------
# Pika Corrected Info
#------------------------------------------------

# file = 'RGN Files/MonoChrom Test 4/pika/radiance/550nm.bip'
# image = h(file) #a hyperspectral image object using hyperspectral
# image.graph_mapir_pika(display=True, save=False)

# hs.mapir_graph_all()
# hs.mapir_graph_mapir()
# hs.pika_to_mapir()
# cal = hs.integrate_np(True, True, True)


# file = 'RGN Files/PikaC T3/550nm-Radiance From Raw Data.bip'
# image = h(file) #a hyperspectral image object using hyperspectral
# image.graph_mapir_cor_max(display=True, save=False)

# list = image.image_metadata()
# print(list)

# hs.mapir_cor_max(display=False, save=True)
# hs.mapir_cor_av(display=True, save=True)




# ------ MONO TEST 4 with JPG -------------
# pixel_sample = (1837, 1330)
# wavelength_adjust_list = hs.wavelength_correct()
# directory = 'RGN Files/MonoChrom Test 4/jpgs'
# test4 = mct(directory, wavelength_adjust_list)
# test4.get_values_pixel(pixel_sample)
# test4.graph()
# correction_matrix = test4.integrate_np(display=True, stats=False, prnt=True)
# RED   = [ 0.51,   0.01,   0.16 ]
# GREEN = [ 0.0,    0.67,   0.01 ]
# NIR =   [ 0.48,   0.32,   0.83 ]








