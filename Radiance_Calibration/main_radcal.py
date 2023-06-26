# File to find radiance calibration values
from pathlib import Path
from radiance_calibration import MapIR_Radiance as MapIR
from radiance_calibration import generate_flat_field_correction
from radiance_calibration import generate_dark_current_values
from Radiance_Calibration.radiance import dark_current_subtraction
import matplotlib.pyplot as plt
import numpy as np
from radiance import radiate
from Band_Correction.correction import correct


# Max Pixel Value is 3947

# Base Process for Data
base_path = Path('/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration')

# Brightness Dial In: make sure values are in range
def dial_in_graphs():
    filepath = base_path / 'Brightness Dial In/2.RAW'
    # filepath = base_path / 'Brightness Dial In/2.RAW'
    # filepath = Path('/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/MapIR/_Radiance Calibration')
    image = MapIR(filepath).dial_in()

# Dark Current Graphs
def dark_current_graphs():
    filepath = base_path / 'Dark'
    sorted_files = sorted(Path(filepath).iterdir())

    image = None
    stats = []
    name = []

    for i, file in enumerate(sorted_files):
        if file.suffix == '.RAW':
            image = MapIR(file)
            stats.append(image.dark_current_subtraction(display=False))
            name.append(f'File: {image.path.name} / Stage: {image.stage}')

    rgb_stack = np.zeros((image.img_y, image.img_x, 3), 'uint8')
    text_1 = f'R: {stats[0][6]} | G: {stats[0][7]} | N: {stats[0][8]} (pixels above threshold)'
    text_2 = f'R: {stats[1][6]} | G: {stats[1][7]} | N: {stats[1][8]} (pixels above threshold)'

    plt.figure(figsize=(14, 6))
    plt.suptitle('Dark Current Max Values')
    rows, cols = 1, 2
    s = 20

    plt.subplot(rows, cols, 1)
    plt.imshow(rgb_stack)
    plt.scatter(stats[0][0][1], stats[0][0][0], color='red', label=stats[0][3], s=s)
    plt.scatter(stats[0][1][1], stats[0][1][0], color='green', label=stats[0][4], s=s)
    plt.scatter(stats[0][2][1], stats[0][2][0], color='blue', label=stats[0][5], s=s)
    plt.title(f'{name[0]}: {text_1}')
    plt.axis(False)
    plt.legend(loc='upper right')

    plt.subplot(rows, cols, 2)
    plt.imshow(rgb_stack)
    plt.scatter(stats[1][0][1], stats[1][0][0], color='red', label=stats[1][3], s=s)
    plt.scatter(stats[1][1][1], stats[1][1][0], color='green', label=stats[1][4], s=s)
    plt.scatter(stats[1][2][1], stats[1][2][0], color='blue', label=stats[1][5], s=s)
    plt.title(f'{name[1]}: {text_2}')
    plt.axis(False)
    plt.legend(loc='upper right')

    plt.tight_layout(pad=1)
    plt.show()

# Flat Field Hori vs Vert Graphs
def flat_field_Hori_vs_Vert():
    filepath = base_path / 'Experiments/Exp 1/raw'
    sorted_files = sorted(Path(filepath).iterdir())

    for i, file in enumerate(sorted_files):
        if file.suffix == '.RAW':
            image = MapIR(file)
            # image = radiate(image)
            image.flat_field_hori_vert()

# Flat Field Hori vs Vert OG / Corr Comp Graphs
def flat_field_HV_Comp():
    filepath = base_path / 'Experiments/Exp 1/raw'
    sorted_files = sorted(Path(filepath).iterdir())

    y_mid = 1500
    x_mid = 2000

    for i, file in enumerate(sorted_files):
        if file.suffix == '.RAW':
            image = MapIR(file)
            image_rad = radiate(image)

            mean_r = np.mean(image.data[:, :, 0])
            mean_g = np.mean(image.data[:, :, 1])
            mean_n = np.mean(image.data[:, :, 2])

            x = [x for x in range(0, 4000)]
            plt.figure(figsize=(14, 8))
            plt.suptitle(f'{image.path.name} Hori vs Vert')
            rows, cols = 2, 2

            plt.subplot(rows, cols, 1)
            plt.scatter(x, image.data[y_mid, :, 0], color='red', s=1)
            plt.axhline(y=mean_r, color='r', linestyle='--')
            plt.scatter(x, image.data[y_mid, :, 1], color='green', s=1)
            plt.axhline(y=mean_g, color='g', linestyle='--')
            plt.scatter(x, image.data[y_mid, :, 2], color='blue', s=1)
            plt.axhline(y=mean_n, color='b', linestyle='--')
            plt.title(f'Horizontal-Original')
            plt.ylim((0, 4096))

            y = [x for x in range(0, 3000)]
            plt.subplot(rows, cols, 2)
            plt.scatter(y, image.data[:, x_mid, 0], color='red', s=1, label='Red Band')
            plt.axhline(y=mean_r, color='r', linestyle='--')
            plt.scatter(y, image.data[:, x_mid, 1], color='green', s=1, label='Green Band')
            plt.axhline(y=mean_g, color='g', linestyle='--')
            plt.scatter(y, image.data[:, x_mid, 2], color='blue', s=1, label='NIR Band')
            plt.axhline(y=mean_n, color='b', linestyle='--')
            plt.title(f'Vertical-Original')
            plt.ylim((0, 4096))

            plt.subplot(rows, cols, 3)
            plt.scatter(x, image_rad.data[y_mid, :, 0], color='red', s=1)
            plt.axhline(y=mean_r, color='r', linestyle='--')
            plt.scatter(x, image_rad.data[y_mid, :, 1], color='green', s=1)
            plt.axhline(y=mean_g, color='g', linestyle='--')
            plt.scatter(x, image_rad.data[y_mid, :, 2], color='blue', s=1)
            plt.axhline(y=mean_n, color='b', linestyle='--')
            plt.title(f'Horizontal-Flat Field')
            plt.ylim((0, 4096))

            y = [x for x in range(0, 3000)]
            plt.subplot(rows, cols, 4)
            plt.scatter(y, image_rad.data[:, x_mid, 0], color='red', s=1, label='Red Band')
            plt.axhline(y=mean_r, color='r', linestyle='--')
            plt.scatter(y, image_rad.data[:, x_mid, 1], color='green', s=1, label='Green Band')
            plt.axhline(y=mean_g, color='g', linestyle='--')
            plt.scatter(y, image_rad.data[:, x_mid, 2], color='blue', s=1, label='NIR Band')
            plt.axhline(y=mean_n, color='b', linestyle='--')
            plt.title(f'Vertical-Flat Field')
            plt.ylim((0, 4096))

            plt.show()

# Heat Map Display of Image for FF Correction
def flat_field_correction_graphs():
    filepath = base_path / 'Experiments/Exp 1/raw'
    sorted_files = sorted(Path(filepath).iterdir())

    for i, file in enumerate(sorted_files):
        if i > 0: continue
        if file.suffix == '.RAW':
            image = MapIR(file)
            image.flat_field_correction()

# Test FF Corr on actual image
def flat_field_correction_test():

    file = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/AC Summer 23/Wheat Field/6-8/raw/081.RAW'
    # file = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/AC Summer 23/Wheat Field/6-8/raw/177.RAW'
    image = MapIR(file)
    # image.display()
    image = dark_current_subtraction(image)
    # image.display()
    image = correct(image)
    image.display()

    red_ff = np.load('flat_field/ff_cor_matrix_red.npy')
    green_ff = np.load('flat_field/ff_cor_matrix_green.npy')
    nir_ff = np.load('flat_field/ff_cor_matrix_nir.npy')

    image.data[:, :, 0] = image.data[:, :, 0] / red_ff
    image.data[:, :, 1] = image.data[:, :, 1] / green_ff
    image.data[:, :, 2] = image.data[:, :, 2] / nir_ff

    print(image.stage)
    # image.data = ((image.data / np.max(image.data)) * image.max_raw_pixel_value).astype('uint16')

    image.display()

# Radiance Value Graphs
def radiance_values():
    amp_values_exp1 = {0: 557.2368, 1: 534.7504, 2: 503.9878, 3: 468.3653, 4: 429.8584,
                  5: 390.1801, 6: 349.9428, 7: 308.6331, 8: 265.2019, 9: 220.3712}

    exp_1_shutter = '1/250'
    exp_2_shutter = '1/500'

    filepath = base_path / 'Experiments/Exp 1/raw'
    sorted_files = sorted(Path(filepath).iterdir())

    x_values = []
    R_values = []
    G_values = []
    N_values = []

    for i, file in enumerate(sorted_files):
        if file.suffix == '.RAW':
            image = MapIR(file)
            image = dark_current_subtraction(image)
            image = correct(image)
            R, G, N = image.radiance_values_center()
            # R, G, N = image.radiance_values()
            x = int(image.path.stem)
            x = amp_values_exp1.get(x)
            x_values.append(x)
            R_values.append(R)
            G_values.append(G)
            N_values.append(N)

    plt.figure(figsize=(10, 6))
    plt.title('Radiance Plot')
    plt.plot(x_values, R_values, color='red', marker='s', label='Red')
    plt.plot(x_values, G_values, color='green', marker='s', label='Green')
    plt.plot(x_values, N_values, color='blue', marker='s', label='NIR')
    plt.xlabel('LapSphere Amp Values')
    plt.ylabel('Digital Numbers')
    plt.legend()
    plt.xticks([x for x in amp_values_exp1.values()])
    # plt.ylim((0, 4096))
    plt.tight_layout()
    plt.show()




if __name__ == '__main__':
    # generate_dark_current_values(base_path / 'Dark')
    # generate_flat_field_correction(base_path / 'Experiments/Exp 1/raw/0.RAW', save=True)

    # dial_in_graphs()
    # dark_current_graphs()

    # flat_field_Hori_vs_Vert()
    # flat_field_HV_Comp()
    # flat_field_correction_graphs()
    # flat_field_correction_test()
    radiance_values()
