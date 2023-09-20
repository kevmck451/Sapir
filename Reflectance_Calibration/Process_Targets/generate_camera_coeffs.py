import sys
sys.path.append('C:/Users/Ainee/Desktop/Work/MapIR/mapir-main/Modules')
import cv2
import numpy as np
import os
from cv2_image_adjustments import *
from Data_Paths.data_filepaths import *

chessboardSize = (10,7)
frameSize = (4000,3000)

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER,30,0.001)

objp = np.zeros((chessboardSize[0]*chessboardSize[1],3),np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

objPoints = []
imgPoints = []

folder_path = 'C:/Users/Ainee/Desktop/Work/MapIR/Data/Distortion Calibration/outdoor/data_set'
file_list = os.listdir(folder_path)

## DETECT CORNERS IN THE IMAGES ##

for file in file_list:
    img_file = folder_path+'/'+file
    image = cv2.imread(img_file,cv2.IMREAD_UNCHANGED)
    #image8 = (image/256).astype('uint8')
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray,chessboardSize,None)

    if ret == True:
        objPoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgPoints.append(corners)

        cv2.drawChessboardCorners(image,chessboardSize,corners2,ret)
        img = rescale(image,.25)
        cv2.imshow('img',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

## CALIBRATION ##

ret, cameraMatrix, dist, rvecs, tvecs = cv2.calibrateCamera(objPoints,imgPoints,frameSize,None,None)

print("Camera Calibrate: ", ret)
print("\nCamera Matrix: \n",cameraMatrix)
print("\nDistortion Parameters: \n", dist)
print("\nRotation Vectors: \n", rvecs)
print("\nTranslation Vectors: \n",tvecs)

camMat_array = np.array(cameraMatrix)
dist_array = np.array(dist)

save_path1 = main_path + '/Data/Distortion Calibration/arrays/cameraMatrix'
save_path2 = main_path + '/Data/Distortion Calibration/arrays/distCoeff'

np.save(save_path1,camMat_array)
np.save(save_path2,dist_array)