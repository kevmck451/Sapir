
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from MapIR.mapir import MapIR
from Data_Paths.data_filepaths import *
import numpy as np
from pathlib import Path
from tabulate import tabulate
from Radiance_Calibration.radiance import flat_field_correction
import matplotlib.pyplot as plt

def generate_radiance_function():

    # detector current values from calibration report
    detector_current = [0.000132826,
                        0.000263499,
                        0.000393443,
                        0.000512208,
                        0.000522517,
                        0.000935106] 
    
    red_ls = [7.45,14.8,22.33,29.3,29.78,53.2]
    green_ls = [4.696,9.38,14.1,18.146,18.79,33.14]
    nir_ls = [9.995,19.84,29.755,39.085,39.805,70.915]

    red_ls_coeffs = np.polyfit(detector_current,red_ls,1)
    green_ls_coeffs = np.polyfit(detector_current,green_ls,1)
    nir_ls_coeffs = np.polyfit(detector_current,nir_ls,1)

    return red_ls_coeffs,green_ls_coeffs,nir_ls_coeffs

def convert_current_to_radiance(amps,r_coff,g_coff,n_coff):
    
    # convert current detector values from experiment
    radiance_r = (amps * r_coff[0]) + r_coff[1]
    radiance_g = (amps * g_coff[0]) + g_coff[1]
    radiance_n = (amps * n_coff[0]) + n_coff[1]

    return radiance_r, radiance_g,radiance_n

def process_single_test(file):
    # Create MapIR Object
    image = MapIR(file)
    image = flat_field_correction(image)
    # image.display()

    # print("red:",np.mean(image.data[:,:,0]))
    # print("green:",np.mean(image.data[:,:,1]))
    # print("nir:",np.mean(image.data[:,:,2]))

    # Analysis
    # NDVI(image)
    return image


amps60 = np.array([0.00000000013322060,
        0.00000000014780200,
        0.00000029473750000,
        0.00000208570000000,
        0.00000698258000000,
        0.00001703260000000,
        0.00003436630000000,
        0.00005942530000000,
        0.00009118910000000,
        0.00012820580000000,
        0.00016834750000000,
        0.00021011670000000,
        0.00025302500000000,
        0.00029458190000000,
        0.00033507800000000,
        0.00037349480000000,
        0.00041130250000000,
        0.00044810380000000,
        0.00048220630000000,
        0.00051192270000000,
        0.00053341110000000])

amps90 = np.array([0.0000000001160526,
                    0.0000000001262803,
                    0.0000002869190000,
                    0.0000020991000000,
                    0.0000068457000000,
                    0.0000167304000000,
                    0.0000337963000000,
                    0.0000544875000000,
                    0.0000897689000000,
                    0.0001261711000000,
                    0.0001657562000000,
                    0.0002068762000000,
                    0.0002492660000000,
                    0.0002902741000000,
                    0.0003302688000000,
                    0.0003682346000000,
                    0.0004057166000000,
                    0.0004420617000000,
                    0.0004758152000000,
                    0.0005048749000000,
                    0.0005261540000000])

amps125 = np.array([0.0000000001088331,
                    0.0000000001171515,
                    0.0000002882892000,
                    0.0000020498000000,
                    0.0000068829000000,
                    0.0000168170000000,
                    0.0000339796000000,
                    0.0000587882000000,
                    0.0000902964000000,
                    0.0001299019000000,
                    0.0001667077000000,
                    0.0002080554000000,
                    0.0002507906000000,
                    0.0002922172000000,
                    0.0003323881000000,
                    0.0003707058000000,
                    0.0004084017000000,
                    0.0004450141000000,
                    0.0004790280000000,
                    0.0005083569000000,
                    0.0005296947000000])

amps250 = np.array([0.0000000001205128,
                    0.0000000001222266,
                    0.0000002889536000,
                    0.0000020598000000,
                    0.0000069015000000,
                    0.0000168734000000,
                    0.0000340768000000,
                    0.0000589441000000,
                    0.0000904885000000,
                    0.0001271960000000,
                    0.0001670341000000,
                    0.0002084913000000,
                    0.0002511334000000,
                    0.0002925033000000,
                    0.0003227816000000,
                    0.0003709608000000,
                    0.0004086730000000,
                    0.0004453854000000,
                    0.0004792665000000,
                    0.0005086587000000,
                    0.0005300312000000])


r_coeff,g_coeff,n_coeff = generate_radiance_function()
rad_r, rad_g, rad_n = convert_current_to_radiance(amps250,r_coeff,g_coeff,n_coeff)

stage_list = []
stage = 100
red = []
green = []
nir = []

bd = Path(active_dataset)
directory = bd/'raw'
for file in directory.iterdir():
    if file.suffix == '.RAW':
        img = process_single_test(file)
        stage_list.append(stage)

        red.append(np.mean(img.data[:,:,0]))
        green.append(np.mean(img.data[:,:,1]))
        nir.append(np.mean(img.data[:,:,2]))

        stage = stage-5
       

plt.plot(rad_r,red,label = 'Red DNs',color='red')
plt.ylabel('DN')
plt.xlabel('Radiance (uW/cm2-sr-nm)')
plt.title('Mean DNs (with Flat Field Correction) vs Radiance Red')
plt.legend()
plt.show()


plt.plot(rad_g,green,label = 'Green DNs',color='green')
plt.ylabel('DN')
plt.xlabel('Radiance (uW/cm2-sr-nm)')
plt.title('Mean DNs (with Flat Field Correction) vs Radiance Green')
plt.legend()
plt.show()


plt.plot(rad_n,nir,label = 'Near IR DNs',color='purple')
plt.ylabel('DN')
plt.xlabel('Radiance (uW/cm2-sr-nm)')
plt.title('Mean DNs (with Flat Field Correction) vs Radiance NIR')
plt.legend()
plt.show()


