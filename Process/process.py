
from MapIR.mapir import MapIR
from Band_Correction.correction import band_correction
from Radiance_Calibration.radiance import radiance_calibration
from Radiance_Calibration.radiance import dark_current_subtraction
from Radiance_Calibration.radiance import flat_field_correction
from Analysis.vegetation_index import NDVI
from data_filepaths import *

from pathlib import Path


def process_single(file):
    # Create MapIR Object
    image = MapIR(file)
    # image.dial_in()
    # image.display()

    # Dark Current Subtraction
    image = dark_current_subtraction(image)
    # image.display()

    # Band_Correction
    image = band_correction(image)
    # image.display()

    # Flat Field Correction
    image = flat_field_correction(image)
    # image.display()

    # Radiance_Calibration
    image = radiance_calibration(image)
    image.display()

    # Reflectance Calibration
    # image = reflectance_calibration(image)
    # image.display()

    # Georectification
    # image.extract_GPS('tiff')
    # filepath = ''
    # image.export_tiff(filepath)
    # image.display()

    # Analysis
    # NDVI(image)




if __name__ == '__main__':

    # process_single(WF_68_81)
    process_single(WF_68_177)










