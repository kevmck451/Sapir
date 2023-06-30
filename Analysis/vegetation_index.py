
import matplotlib.pyplot as plt
import numpy as np


# Function to calculate and display the Normalized Difference Vegetation Index
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

    plt.figure(figsize=(12, 9))
    plt.imshow(ndvi_array, cmap=plt.get_cmap("RdYlGn"))
    plt.title(f'NDVI: {mapir_object.path.stem}')
    # plt.colorbar()
    plt.axis('off')
    plt.tight_layout(pad=1)

    if save:
        saveas = (f'{mapir_object.path.parent}/{mapir_object.path.stem} NDVI.pdf')
        plt.savefig(saveas)
        plt.close()
    if display:
        plt.show()

# Function to calculate and display the Green Normalized Difference Vegetation Index
def GNDVI(mapir_object, display=True, save=False):
    NIR = mapir_object.data[:, :, mapir_object.NIR_index]
    GREEN = mapir_object.data[:, :, mapir_object.G_index]

    GREEN, NIR = GREEN.astype('float'), NIR.astype('float')

    top, bottom = NIR - GREEN, NIR + GREEN
    top[top == 0], bottom[bottom == 0] = 0, np.nan

    gndvi_array = np.divide(top, bottom)
    gndvi_array[gndvi_array < 0] = 0
    gndvi_array[gndvi_array > 1] = 1

    plt.figure(figsize=(12, 12))
    plt.imshow(gndvi_array, cmap=plt.get_cmap("RdYlGn"))
    plt.title(f'GNDVI: {mapir_object.file_name}')
    plt.axis('off')
    plt.tight_layout(pad=1)

    if save:
        saveas = (f'{mapir_object.path.parent}/{mapir_object.file_name} GNDVI.pdf')
        plt.savefig(saveas)
        plt.close()
    if display:
        plt.show()

# Function to tell average values in an area
def NDVI_area_values(mapir_object, corr, middle_pixel):

        if corr: name = 'Corrected'
        else: name = 'Original'

        NIR = mapir_object.data[:, :, mapir_object.NIR_index]
        RED = mapir_object.data[:, :, mapir_object.R_index]

        RED, NIR = RED.astype('float'), NIR.astype('float')
        # RED[RED == 0], NIR[NIR == 0] = np.nan, np.nan
        top, bottom = NIR - RED, NIR + RED
        top[top == 0], bottom[bottom == 0] = 0, np.nan

        ndvi_array = np.divide(top, bottom)
        # ndvi_array[ndvi_array < 0] = 0
        # ndvi_array[ndvi_array > 1] = 1

        plus_minus = 100
        x1 = (middle_pixel[0] - plus_minus)
        x2 = (middle_pixel[0] + plus_minus)
        y1 = (middle_pixel[1] - plus_minus)
        y2 = (middle_pixel[1] + plus_minus)

        average_value = ndvi_array[y1:y2, x1:x2].mean()
        print(average_value)

# OSAVI