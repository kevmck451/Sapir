# File to find radiance calibration values
from pathlib import Path
from mapir_rad import MapIR_Radiance as MapIR
import matplotlib.pyplot as plt

# Make sure values are in range
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/' \
#            '_Radiance Calibration/LSExperiment/Experiment/0.RAW'
# image = MapIR(filepath).dial_in()

# Dark Current Graphs
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/_Radiance Calibration/Dark/dark1.RAW'
# image_1 = MapIR(filepath).dark_current_subtraction()
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/_Radiance Calibration/Dark/dark2.RAW'
# image_2 = MapIR(filepath).dark_current_subtraction()

# Flat Field Correction
# filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/_Radiance Calibration/LSExperiment/Experiment'
# sorted_files = sorted(Path(filepath).iterdir())
#
# for i, file in enumerate(sorted_files):
#     if file.suffix == '.RAW':
#         image = MapIR(file)
#         image.flat_field_correction()



amp_values = { 0:557.2368, 1:534.7504, 2:503.9878, 3:468.3653, 4:429.8584,
               5:390.1801, 6:349.9428, 7:308.6331, 8:265.2019, 9:220.3712}

filepath = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/_Radiance Calibration/LSExperiment/Experiment'
sorted_files = sorted(Path(filepath).iterdir())
# print(sorted_files)

x_values = []
R_values = []
G_values = []
N_values = []

for i, file in enumerate(sorted_files):
    if file.suffix == '.RAW':
        image = MapIR(file)
        R, G, N = image.radiance_values_center()
        x = int(image.path.stem)
        # print(file.stem)
        # print(x)
        x_values.append(x)
        R_values.append(R)
        G_values.append(G)
        N_values.append(N)

print(x_values)
print(R_values)
print(G_values)
print(N_values)

plt.figure(figsize=(10, 6))
plt.title('Radiance Plot')
plt.plot(x_values, R_values, color='red', marker='s', label='Red')
plt.plot(x_values, G_values, color='green', marker='s', label='Green')
plt.plot(x_values, N_values, color='blue', marker='s', label='NIR')
plt.xlabel('100% Brightness <------------- Amp Values -------------> 45% Brightness')
plt.ylabel('Digital Numbers')
plt.legend()
plt.xticks(range(min(x_values), max(x_values) + 1, 1))
plt.ylim((0, 4096))
plt.tight_layout()
plt.show()





