# MapIR Data Processing Guide

This guide outlines the process of preparing and processing data captured from a MapIR camera, from the initial data backup to data processing and analysis. Follow the steps provided to effectively handle and analyze your captured data.

## Flight Data Selection

1. **Extract Data from SD Card**: Carefully remove the SD card from the MapIR camera. The card should contain both .RAW and .JPG files.

2. **Backup the Files**: Select all files and drag and drop them to a secure backup location on your computer.

3. **Create a Processing Directory**: Create a new directory on your computer where the data will be processed. Add a subfolder named "raw" to this new directory.

4. **Identify Reflectance Target Image**: Go to the backup folder and sort the files by type. Look through the JPG images to find a clear, focused image of the reflectance target. Note that the corresponding RAW file for this image should be one number lower than the JPG file. For example, if the JPG image is "2022_0818_055945_118.JPG", the raw file name will be "2022_0818_055945_117.RAW".

5. **Copy Reflectance Target File**: Copy the RAW file corresponding to the reflectance target to the new directory. Rename this file to "ref_tar.RAW".

6. **Identify Flight Start and End Points**: Navigate through the JPG images in the backup folder to find the point after ascent, right as the flight is about to begin. Note the filename of this image. Also identify the image that represents the end of the flight over the area of interest and note its filename.

7. **Select Relevant Flight Data**: Resort the files by their name and select the files within the range identified in step 6. Remember that the RAW filenames are one number lower than their JPG counterparts.

8. **Move Selected Files**: Move the selected RAW and JPG files to the "raw" subfolder in the new directory. Your directory is now ready for data processing.

## Data Processing

To process your flight data, the directory must contain:

- A 'raw' subfolder containing the RAW and JPG files
- A RAW file of the reflectance target named 'ref_tar.RAW'

Follow these steps to process your data:

1. **Run Processing Script**: From the MapIR package available at [GitHub](https://github.com/JacobsSensorLab/mapir), run the "process.py" file with the filepath to the directory as an argument.

2. **Post Processing Steps**: Once the process script runs, it will perform the following operations:

    - Renaming files in the raw folder for easier processing
    - Debayering and correcting RAW files
    - Applying radiance and reflectance calibration
    - Saving processed files in a '_processed' folder in the directory as TIFF files
    - Generating a 'geo.txt' file for each processed file, used for georectification with WebODM

3. **Georectification**: Upload the contents of the "_processed" folder to WebODM for georectification.

4. **Download Final Image**: After georectification, download the orthomosaic photo as a PNG.

## Data Analysis

Refer to the 'analysis.py' script provided in the MapIR package. This script includes examples of analysis options for the data and serves as a starting point for further analysis. You can modify and extend this script based on your specific requirements.
