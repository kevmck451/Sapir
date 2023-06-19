# file to apply available Vegetation Indices for MapIR camera bands

import matplotlib.pyplot as plt
import numpy as np

def NDVI(mapir_object, display=True, save=False):
    NIR = mapir_object.data[:, :, mapir_object.NIR_index]
    RED = mapir_object.data[:, :, mapir_object.R_index]

    RED, NIR = RED.astype('float'), NIR.astype('float')
    # RED[RED == 0], NIR[NIR == 0] = np.nan, np.nan
    top, bottom = NIR - RED, NIR + RED
    top[top == 0], bottom[bottom == 0] = 0, np.nan

    ndvi_array = np.divide(top, bottom)
    ndvi_array[ndvi_array < 0] = 0
    ndvi_array[ndvi_array > 1] = 1

    plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
    plt.title(f'NDVI: {mapir_object.file_name}')
    # plt.colorbar()
    plt.axis('off')
    plt.tight_layout(pad=1)

    if save:
        saveas = (f'{mapir_object.path.parent}/{mapir_object.file_name} NDVI.pdf')
        plt.savefig(saveas)
        plt.close()
    if display:
        plt.show()


def GNDVI(mapir_object):
        pass


def NDRE(mapir_object):
        pass