
from MapIR.mapir import MapIR
from Band_Correction.correction import correct
from Radiance_Calibration.radiance import radiate
from Radiance_Calibration.radiance import dark_current_subtraction
from Radiance_Calibration.radiance import flat_field_correction

from Analysis.vegetation_index import NDVI

from pathlib import Path

def process(file):
    # Create MapIR Object
    image = MapIR(file)
    # image.dial_in()
    # image.display()

    # Dark Current Subtraction
    image = dark_current_subtraction(image)
    # image.display()

    # Band_Correction
    image = correct(image)
    image.display()

    # Flat Field Correction
    image = flat_field_correction(image)
    image.display()

    # Radiance_Calibration
    image = radiate(image)
    image.display()

    # Reflectance Calibration

    # Georectification
    # image.extract_GPS('tiff')
    # image.export_tiff()
    # image.display()

    # Analysis
    # NDVI(image)

if __name__ == '__main__':
    # filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/Brightness Dial In/2.RAW'
    filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/AC Summer 23/Wheat Field/6-8/raw/177.RAW'
    # filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/AC Summer 23/Wheat Field/6-8/raw/081.RAW'
    # filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/MC Tests/MC Test 4/RAW/850.RAW'

    process(filepath)










