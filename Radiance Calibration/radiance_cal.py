# File to find radiance calibration values
from pathlib import Path
from mapir_rad import MapIR_Radiance as MapIR

# Make sure values are in range
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/Radiance Calibration/Brightness Dial In/2.RAW'
# image = MapIR(filepath).display()

# Dark Current Graphs
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/Radiance Calibration/Dark/dark1.RAW'
# image_1 = MapIR(filepath).dark_current_subtraction()
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/Radiance Calibration/Dark/dark2.RAW'
# image_2 = MapIR(filepath).dark_current_subtraction()

# Flat Field Correction
filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/Radiance Calibration/LSExperiment/Experiment'
sorted_files = sorted(Path(filepath).iterdir())

for i, file in enumerate(sorted_files):
    if file.suffix == '.RAW':
        image = MapIR(file)
        image.flat_field_correction()



# amp_values = { 0:557.2368, 1:534.7504, 2:503.9878, 3:468.3653, 4:429.8584,
#                5:390.1801, 6:349.9428, 7:308.6331, 8:265.2019, 9:220.3712}
#
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/Radiance Calibration/LSExperiment/Experiment'
# sorted_files = sorted(Path(filepath).iterdir())
#
# for i, file in enumerate(sorted_files):
#     if file.suffix == '.RAW':
#         image = MapIR(file)
#         image.radiance_value()




