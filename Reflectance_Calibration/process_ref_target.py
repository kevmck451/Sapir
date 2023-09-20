# File to test the functionality of get reflectance values from reflectance target

import cv2
import math
import numpy as np
import sys
import pathlib as Path
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')

from pyzbar.pyzbar import decode
from copy import deepcopy
from MapIR.mapir import MapIR
from MapIR.mapir import *
from Data_Paths.data_filepaths import *
from Radiance_Calibration.radiance import *
from Band_Correction.band_correction import band_correction
from Radiance_Calibration.radiance import dark_current_subtraction
from PIL import Image
from Radiance_Calibration.radiance import dark_current_subtraction
from Reflectance_Calibration.Process_Targets.cv2_image_adjustments import *

# Run initial corrections on reference image.
def process_ref_target(mapir_object):

    image = MapIR(mapir_object)
    #image.display()

    # Dark Current Subtraction
    image = dark_current_subtraction(image)
    #image.display()

    # Band_Correction
    image = band_correction(image)
    #image.display()

    # Flat Field Correction
    image = flat_field_correction(image)
    #image.display()

    # Radiance_Calibration
    image = radiance_calibration(image)
    #image.display()

    image.display()
    export_tiff(image,active_dataset)

    return image

def perspective_correction(mapir_object):

    process_ref_target(mapir_object)

    tiff_img = active_dataset+'/ref_target.tiff'
    img = cv2.imread(tiff_img,cv2.IMREAD_UNCHANGED)

    img_smal = rescale(img,.25)
    cv2.imshow("Image",img_smal)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Make the 8-bit duplicate
    img8 = (img/256).astype('uint8')
    #img8_small = rescale(img8,0.25)
    # Setup aruco parameter things
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
    marker_params = cv2.aruco.DetectorParameters()
    marker_corners, marker_IDs, _ = cv2.aruco.detectMarkers(img8,aruco_dict,parameters=marker_params)
    cv2.aruco.detectMarkers(img8,aruco_dict)
    print(marker_IDs)
    cv2.aruco.drawDetectedMarkers(img8,marker_corners,marker_IDs,borderColor=(0,255,0))


    if marker_IDs is not None:

        marker_corners = marker_corners[0][0]
        marker_width = np.linalg.norm(marker_corners[0] - marker_corners[1])
        marker_height = np.linalg.norm(marker_corners[0] - marker_corners[3])

        # Position of 
        center_x = (marker_corners[0][0] + marker_corners[2][0]) / 2
        center_y = (marker_corners[0][1] + marker_corners[2][1]) / 2

        padding = 50  # Additional space around the marker
        dst_points = np.array([
            [center_x - marker_width / 2 - padding, center_y - marker_height / 2 - padding],
            [center_x + marker_width / 2 + padding, center_y - marker_height / 2 - padding],
            [center_x + marker_width / 2 + padding, center_y + marker_height / 2 + padding],
            [center_x - marker_width / 2 - padding, center_y + marker_height / 2 + padding]
        ], dtype=np.float32)

        src_points = np.array(marker_corners, dtype=np.float32)
        perspective_matrix = cv2.getPerspectiveTransform(src_points, dst_points)

        transformed_img8 = cv2.warpPerspective(img8, perspective_matrix, (img8.shape[1], img8.shape[0]))
        transformed_img = cv2.warpPerspective(img, perspective_matrix, (img8.shape[1], img8.shape[0]))

        # Display the original and transformed images
        og_img = rescale(img,0.25)
        tr_img8 = rescale(transformed_img8,0.25) #8bit image
        tr_img = rescale(transformed_img,0.25) #16bit

        cv2.imshow('Original Image', og_img)
        cv2.imshow('Transformed Image 8bit', tr_img8)
        cv2.imshow('Transformed Image', tr_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        return transformed_img
    else:
        print("No ArUco marker detected.")
        return None
   
def crop_target(mapir_object):
    tr_img = perspective_correction(mapir_object)

    # Create image duplicate
    tr_img8 = (tr_img/256).astype('uint8')

    # Detect marker on transformed image
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
    marker_params = cv2.aruco.DetectorParameters()
    marker_corners, marker_IDs, rejected_cand = cv2.aruco.detectMarkers(tr_img8,aruco_dict,parameters=marker_params)
    cv2.aruco.detectMarkers(tr_img8,aruco_dict)
    #print(marker_IDs)
    cv2.aruco.drawDetectedMarkers(tr_img8,marker_corners,marker_IDs,borderColor=(0,255,0))
    #print(marker_corners[0][0][0])

    distance_unit = marker_corners[0][0][1][0]-marker_corners[0][0][0][0]
    #print(distance_unit)
    corner_x = marker_corners[0][0][0][0]
    corner_y = marker_corners[0][0][0][1]

    x1 = int(corner_x-((distance_unit*1.58)+(distance_unit*0.5163)))
    x2 = int(corner_x-(distance_unit*0.5163))
    y1 = int(corner_y-(distance_unit*0.5223))
    y2 = int(corner_y+(distance_unit*2.07)-(distance_unit*0.5223))

    # Calculate distance relative to aruco marker
    target_area = tr_img[y1:y2,x1:x2]

    cv2.imwrite(active_dataset+'/cropped_img.tiff',target_area)

    # display image 
    cv2.imshow("target",target_area)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    print(np.min(target_area[:,:,1]))
    print(np.max(target_area[:,:,2]))

    return target_area

def isolate_panels(mapir_object):
    image = crop_target(mapir_object)
    image = image.astype(np.float32)
    
    x = image.shape[1]
    y = image.shape[0]

    padding = x*0.02
    for i in range(0,4):
        if i == 0:
            x1 = int((x/2)+padding)
            x2 = int(x-padding)
            y1 = int((y/2)+padding)
            y2 = int(y-padding)

            black_panel = image[y1:y2,x1:x2]

            cv2.imshow("panel",black_panel)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        if i == 1:
            x1 = int(0+padding)
            x2 = int((x/2)-padding)
            y1 = int((y/2)+padding)
            y2 = int(y-padding)

            dgray_panel = image[y1:y2,x1:x2]

            cv2.imshow("panel",dgray_panel)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        if i == 2:
            x1 = int((x/2)+padding)
            x2 = int(x-padding)
            y1 = int(0+padding)
            y2 = int((y/2)-padding)

            lgray_panel = image[y1:y2,x1:x2]

            cv2.imshow("panel",lgray_panel)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

        # if i == 3:
        #     x1 = int(0+padding)
        #     x2 = int((x/2)-padding)
        #     y1 = int(0+padding)
        #     y2 = int((y/2)-padding)

        #     white_panel = image[y1:y2,x1:x2]

        #     cv2.imshow("panel",white_panel)
        #     cv2.waitKey(0)
        #     cv2.destroyAllWindows()
            
    return black_panel,dgray_panel,lgray_panel

def extract_dn_mean(image):
    black,dgray,lgray = isolate_panels(image)

    target_rad_r = []
    target_rad_g = []
    target_rad_n = []

    for i in range(0,4):
        if i == 0:
            target_rad_r.append(np.mean(black[:,:,0]))
            target_rad_g.append(np.mean(black[:,:,1]))
            target_rad_n.append(np.mean(black[:,:,2]))
        
        if i == 1:
            target_rad_r.append(np.mean(dgray[:,:,0]))
            target_rad_g.append(np.mean(dgray[:,:,1]))
            target_rad_n.append(np.mean(dgray[:,:,2])) 

        if i == 2:
            target_rad_r.append(np.mean(lgray[:,:,0]))
            target_rad_g.append(np.mean(lgray[:,:,1]))
            target_rad_n.append(np.mean(lgray[:,:,2])) 

        # if i == 3:
        #      target_rad_r.append(np.mean(white[:,:,0]))
        #      target_rad_g.append(np.mean(white[:,:,1]))
        #      target_rad_n.append(np.mean(white[:,:,2])) 

    # print(target_rad_r)
    # print(target_rad_g)
    # print(target_rad_n)
    return target_rad_r, target_rad_g, target_rad_n

def ref_coefficients(mapir_object):

    target_rad_r,target_rad_g,target_rad_n = extract_dn_mean(mapir_object)

    # Calibration target values provided by MapIR
                        #B     DG     LG 
    target_refl_r = [.01919,.20255,.26632]
    target_refl_g = [.01953,.19648,.26582]
    target_refl_n = [.01890,.23549,.27964]
    
    # Fitting to a line
    regression_coeff_r = np.polyfit(target_rad_r,target_refl_r,1)
    regression_coeff_g = np.polyfit(target_rad_g,target_refl_g,1)
    regression_coeff_n = np.polyfit(target_rad_n,target_refl_n,1)

    folder_path = active_dataset+'/coeffs'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print("Folder created.")
    else:
        print('Already exists.')

    print(regression_coeff_r,regression_coeff_g,regression_coeff_n)

    np.save(active_dataset+'/coeffs/r_coeffs.npy',regression_coeff_r)
    np.save(active_dataset+'/coeffs/g_coeffs.npy',regression_coeff_g)
    np.save(active_dataset+'/coeffs/n_coeffs.npy',regression_coeff_n)

    # Option to view graphs 
    show_plots = 'y'
    if show_plots == 'y':
        print(target_rad_r)
        print(target_refl_r)
        plt.plot(target_rad_r,target_refl_r,label = 'Reflectance')
        plt.ylabel('Target Reflectance Level')
        plt.xlabel('Radiance at Sensor (L)')
        plt.title('Red')
        plt.legend()
        plt.show()   

        plt.plot(target_rad_g,target_refl_g,label = 'Reflectance')
        plt.ylabel('Target Reflectance Level')
        plt.xlabel('Radiance at Sensor (L)')
        plt.title('Green')
        plt.legend()
        plt.show()   

        plt.plot(target_rad_n,target_refl_n,label = 'Reflectance')
        plt.ylabel('Target Reflectance Level')
        plt.xlabel('Radiance at Sensor (L)')
        plt.title('NIR')
        plt.legend()
        plt.show()   

ref_coefficients(target_panel)

