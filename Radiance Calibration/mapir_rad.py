# MapIR Radiance Calibration Processing
# Kevin McKenzie 2023

from MapIR import MapIR
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats



# MapIR class to process RAW images
class MapIR_Radiance(MapIR):
    def __init__(self, raw_file_path):
        super().__init__(raw_file_path)

        self._radiometric_calibration()
        # self._normalize()

    # Function to apply radiometric calibration to images
    def _radiometric_calibration(self):

        # Dark Current Subtraction: 7 for each band
        data = self.data.astype(np.float32)
        data -= 8
        data[data < 0] = 0
        self.data = data.astype(np.uint16)

        # Flat Field Correction


        # Radiometric Calibration




    def dark_current_subtraction(self):
        mean_r = int(np.mean(self.data[:, :, 0]))
        mean_g = int(np.mean(self.data[:, :, 1]))
        mean_n = int(np.mean(self.data[:, :, 2]))

        print(mean_r, mean_g, mean_n)

        # Calculate the maximum and minimum values for each channel
        max_r, min_r = np.max(self.data[:, :, 0]), np.min(self.data[:, :, 0])
        max_g, min_g = np.max(self.data[:, :, 1]), np.min(self.data[:, :, 1])
        max_n, min_n = np.max(self.data[:, :, 2]), np.min(self.data[:, :, 2])

        # Use the variables as needed
        print(f'Max R: {max_r}')
        print(f'Min R: {min_r}')
        print(f'Max G: {max_g}')
        print(f'Min G: {min_g}')
        print(f'Max B: {max_n}')
        print(f'Min B: {min_n}')

        # Find the indices where the value equals the maximum value
        max_indices_R = np.where(self.data[:, :, 0] == np.max(self.data[:, :, 0]))
        max_indices_G = np.where(self.data[:, :, 1] == np.max(self.data[:, :, 1]))
        max_indices_N = np.where(self.data[:, :, 2] == np.max(self.data[:, :, 2]))
        # print(max_indices_R)

        mean_indices_R = np.where(self.data[:, :, 0] <= mean_r)
        mean_indices_G = np.where(self.data[:, :, 1] <= mean_g)
        mean_indices_N = np.where(self.data[:, :, 2] <= mean_n)

        # Create a grayscale image of the matrix
        # plt.imshow(self.data.astype('uint8'))
        plt.imshow(self.rgb_render)


        # Add red spots at the maximum value locations
        plt.scatter(max_indices_R[1], max_indices_R[0], color='red', label=max_r)
        plt.scatter(max_indices_G[1], max_indices_G[0], color='green', label=max_g)
        plt.scatter(max_indices_N[1], max_indices_N[0], color='blue', label=max_n)
        # plt.scatter(mean_indices_R[1], mean_indices_R[0], color='#FFC0CB', label=mean_r, s=1)
        # plt.scatter(mean_indices_G[1], mean_indices_G[0], color='#AEC6CF', label=mean_g, s=1)
        # plt.scatter(mean_indices_N[1], mean_indices_N[0], color='#32CD32', label=mean_n, s=1)
        plt.title(f'{self.path.stem}')
        plt.axis(False)
        plt.legend()
        plt.show()

    def flat_field_correction(self):
        y_mid = 1500
        x_mid = 2000
        size = 50

        mean_r = np.mean(self.data[:, :, 0])
        mean_g = np.mean(self.data[:, :, 1])
        mean_n = np.mean(self.data[:, :, 2])

        average_value_R = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 0])
        # print(f'R Mid Value: {self.data[y_mid, x_mid, 0]} | R Mid Average: {average_value_R}')
        # print(f'R Average: {np.mean(self.data[:,:,0])}')
        # print(f'R Stan Dev: {np.std(self.data[:,:,0])}')
        average_value_G = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 1])
        # print(f'G Mid Value: {self.data[y_mid, x_mid, 1]} | G Mid Average: {average_value_G}')
        # print(f'G Average: {np.mean(self.data[:, :, 1])}')
        # print(f'G Stan Dev: {np.std(self.data[:, :, 1])}')
        average_value_N = np.mean(self.data[(y_mid - size):(y_mid + size), (x_mid - size):(x_mid + size), 2])
        # print(f'N Mid Value: {self.data[y_mid, x_mid, 2]} | N Mid Average: {average_value_N}')
        # print(f'N Average: {np.mean(self.data[:, :, 2])}')
        # print(f'N Stan Dev: {np.std(self.data[:, :, 2])}')
        # print('-' * 50)

        x = [x for x in range(0, 4000)]
        plt.figure(figsize=(14, 4))
        plt.suptitle(f'{self.path.stem}')
        plt.subplot(1, 2, 1)
        plt.scatter(x, self.data[y_mid, :, 0], color='red', s=1)
        # plt.axhline(y=average_value_R, color='r', linestyle='dotted')
        # plt.axhline(y=mean_r, color='r', linestyle='--')
        plt.scatter(x, self.data[y_mid, :, 1], color='green', s=1)
        # plt.axhline(y=average_value_G, color='g', linestyle='dotted')
        # plt.axhline(y=mean_g, color='g', linestyle='--')
        plt.scatter(x, self.data[y_mid, :, 2], color='blue', s=1)
        # plt.axhline(y=average_value_N, color='b', linestyle='dotted')
        # plt.axhline(y=mean_n, color='b', linestyle='--')
        plt.title(f'Horizontal')
        plt.ylim((0, 4096))
        # plt.legend()

        y = [x for x in range(0, 3000)]
        plt.subplot(1, 2, 2)
        plt.scatter(y, self.data[:, x_mid, 0], color='red', s=1, label='Red Band')
        # plt.axhline(y=average_value_R, color='r', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_r, color='r', linestyle='--', label='Average')
        plt.scatter(y, self.data[:, x_mid, 1], color='green', s=1, label='Green Band')
        # plt.axhline(y=average_value_G, color='g', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_g, color='g', linestyle='--', label='Average')
        plt.scatter(y, self.data[:, x_mid, 2], color='blue', s=1, label='NIR Band')
        # plt.axhline(y=average_value_N, color='b', linestyle='dotted', label='Mid Average')
        # plt.axhline(y=mean_n, color='b', linestyle='--', label='Average')
        plt.title(f'Vertical')
        plt.ylim((0, 4096))
        # plt.legend()
        plt.show()

    def radiance_value(self):
        pass

