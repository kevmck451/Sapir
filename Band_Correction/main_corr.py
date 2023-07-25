# File to get all graphs for correction process_single using monochromator experiment

from Analysis import vegetation_index
from correction import *
from hyperspectral import Hyperspectral as hs
import hyperspectral as hype
from MapIR.mapir import MapIR
from band_correction import Band_Correction
from band_correction import generate_correction_matrix
from band_correction import generate_wavelength_responses
from data_filepaths import *


# Display RAW graphs from Monochromator Experiment
def experiment_graphs_raw(directory):
    pixel_sample = (1837, 1330)  # center of monochromator light
    wavelength_adjust_list = hype.wavelength_correct(directory)  # monochromator wavelength correction table from pika

    test4 = Band_Correction(directory, wavelength_adjust_list, corr=False)
    test4.get_values_area(pixel_sample)
    test4.graph()
    # test4.integrate_np(display=True, stats=False, prnt=True)

# Display Corrected graphs from Monochromator Experiment
def experiment_graphs_corrected(directory):
    pixel_sample = (1837, 1330)  # center of monochromator light
    wavelength_adjust_list = hype.wavelength_correct(directory)  # monochromator wavelength correction table from pika
    corr_matrix = generate_correction_matrix(exp_directory)
    test4_corr = Band_Correction(directory, wavelength_adjust_list, corr=True, corr_matrix=corr_matrix)
    test4_corr.get_values_area(pixel_sample)
    print(test4_corr.graph())
    # test4_corr.integrate_np(display=True, stats=False, prnt=False)

# Display Corrected Image with NDVI:
def correction_single_image(filepath):
    image = MapIR(filepath)
    image.display()
    # cor_matrix = generate_correction_matrix(exp_directory)
    # corr_image = band_correction(image, cor_matrix)
    corr_image = band_correction(image)
    corr_image.display()
    # vegetation_index.NDVI(corr_image, display=True, save=False)

# Pika vs MapIR Comparison:
def pika_vs_mapir():
    pika_file = 'Datasets/PikaMapIR/az_cube_2 Processed.bip'
    image_p = hs(pika_file)
    image_p.display_RGB(display=True, save=False)
    image_p.display_Mapir_Single(display=True, save=False)
    image_p.display_NDVI(display=True, save=False)

    mapir_file = 'Datasets/PikaMapIR/MapIR_AZ.RAW'
    image_m = MapIR(mapir_file)
    cor_matrix = generate_correction_matrix(exp_directory)
    corr_image_m = band_correction(image_m, corr_values=cor_matrix)

    image_m.display()
    corr_image_m.display()
    vegetation_index.NDVI(corr_image_m, display=True, save=False)

# Pika vs MapIR NDVI Table Values:
def pika_vs_mapir_NDVI():
    pika_middle_tree = (141, 304)
    pika_middle_fence = (134, 476)
    pika_file = 'Datasets/PikaMapIR/az_cube_2 Processed.bip'
    image_p_fence = hs(pika_file)
    image_p_tree = hs(pika_file)
    image_p_fence.NDVI_area_values(pika_middle_fence)
    image_p_tree.NDVI_area_values(pika_middle_fence)

    mapir_middle_tree = (2480, 756)
    mapir_middle_fence = (2382, 1515)
    mapir_file = 'Datasets/PikaMapIR/MapIR_AZ.RAW'
    image_m = MapIR(mapir_file)
    cor_matrix = generate_correction_matrix(exp_directory)
    corr_image_m = band_correction(image_m, corr_values=cor_matrix)
    vegetation_index.NDVI_area_values(image_m, corr=False, middle_pixel=mapir_middle_tree)
    vegetation_index.NDVI_area_values(corr_image_m, corr=True, middle_pixel=mapir_middle_tree)
    vegetation_index.NDVI_area_values(image_m, corr=False, middle_pixel=mapir_middle_fence)
    vegetation_index.NDVI_area_values(corr_image_m, corr=True, middle_pixel=mapir_middle_fence)



if __name__ == '__main__':

    # print(generate_correction_matrix(exp_directory))

    # experiment_graphs_raw(exp_directory)
    # experiment_graphs_corrected(exp_directory)
    correction_single_image(single_2)
    # pika_vs_mapir()
    # pika_vs_mapir_NDVI()

    # generate_wavelength_responses(MC_Exp_4, corrected=True)
    # generate_wavelength_responses(MC_Exp_4, corrected=False)

