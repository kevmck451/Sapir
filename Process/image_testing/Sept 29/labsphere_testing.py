
import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from MapIR.mapir import MapIR
from Data_Paths.data_filepaths import *
import numpy as np
from pathlib import Path
from tabulate import tabulate
from Radiance_Calibration.radiance import flat_field_correction
import matplotlib.pyplot as plt

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
       
amps = [0.00000000013322060,
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
0.00053341110000000]

print(red)
print(nir)

plt.plot(amps,red,label = 'Red DNs',color='red')
plt.plot(amps,green,label = 'Green DNs',color='green')
plt.plot(amps,nir,label = 'Near IR DNs',color='purple')
plt.ylabel('DN')
plt.xlabel('Amps')
plt.title('Mean DNs (with Flat Field Correction) vs Amps')
plt.legend()
plt.show()





