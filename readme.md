## MapIR Post-Processing Code v4

![Poster Image](media/mapir_poster.jpeg)

The MapIR Survey3 is a multispectral camera which captures images in the red, green and near-infrared
bands for the purpose of argicultural assessment. This program is meant to unpack and post-process RAW files from the Survey3. 

Post-processing steps:
- Image unpacking and debayering (unmodified)
- Dark current subtraction
- Flat field correction
- Band correction
- Radiance calibration
- Reflectance calibration
- NDVI analysis
- Geodata extraction
- .tiff exporting

Major changes versus previous version of the code (as of 01/22/24):
-  Two processing options based on MapIR recommended settings: 1/125 & 1/250
-  Updated dark current subtraction data
-  Small revisions to band correction
-  Reworked flat field correction
-  Reworked radiance calibration
-  Added eflectance calibration process
-  Removal of unused functions & files

## Instructions:

#### Preparation
This guide will assume that the user has their own preferred IDE & knows how to manage virtual environments & install modules.

1. Prepare a folder for the program in your preferred directory & extract all files AS IS into the directory

2. Within this folder, add another folder named **Flat Field Data**. Download the files within [THIS LINK](https://livememphis-my.sharepoint.com/:f:/g/personal/vfvorito_memphis_edu/Em3T5vGwQjpEl6jkluGkzS8B0VQzfPmb0C8zhwv5swP2rw?e=hSC3KJ) and save within the Flat Field Data folder. Update the **flat_field_data** variable within **data_filepaths.py** with the pathway towards this folder.

3. Prepare a folder for the MapIR data you wish to process. This is a separate folder from 1.
   This folder will contain subfolders containing all MapIR data you wish to process. Ex:
    
        THIS FOLDER 
          |-- Cover Crop Dec 06
          |-- Agricenter Wheat Field Jan 27
          |-- Library Field March 2

4. Load the project in your preferred IDE and create a virtual environment for it. Activate the environment and install the contents of requirements.txt

5. Create a file named **root_loc.py** under **/data_filepaths** (same folder as the data_filepaths.py file). In the file, include the following:
    ```python
    main_path = '[INSERT FILE DIRECTORY OF MAPIR FILES]'

    # Example:
    main_path = 'C:/Users/Ainee Favorito/OneDrive - The University of Memphis/Work - UofM Lab/Data'
#### Processing

**For first time:** Download the test file located here [LINK TO FILE](https://livememphis-my.sharepoint.com/:f:/g/personal/vfvorito_memphis_edu/EtqRZ7UqHZVGk2m2gT0kWAMBbYCqjLLqlIGT7yPx1Azplg?e=Ma252c) and save into the main folder created (main_path). Try out the following steps using the test files before using your actual data. 
1. Add file location to **data_filepaths.py**. Append to the main path as shown in the example below:

    ```python
    #------------#
    #  DATASETS  #
    #------------#

    # Cover Crop (Agricenter)
    mapir_test = main_path+'/MapIR Test'
2. **Always check for the shutter speed used to capture the dataset.** You can check this by right-clicking any .jpg file in the **raw** folder, or the reflectance target's .jpg file
3. Open **_main_process.py** and edit the **speed** variable as needed. Edit the **folder** variable by assigning it the name of your folder's pathway (in data_filepaths.py)
4. Run the file via command line OR by pressing the 'run' action on the upper right corner of the file. *Example:*
    ```python
    PS C:\Users\Ainee Favorito\Desktop\Work (Code)\MapIR\mapir-main\mapir-v4> python3 _mapir_process.py
5. If any images appear during the reflectance_target_processing stage, simply close the image and the process will continue. This is normal and used to ensure the process is moving forward. 

#### Additional Steps

1. For georectification, request assistance from Ainee or Kevin as it requires login credentials. 
2. The NDVI file can be used to convert georectified images to NDVI. 


[Poster Image](media/wheat_ndvi.jpg)

