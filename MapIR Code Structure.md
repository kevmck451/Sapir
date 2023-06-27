# MapIR Application

## Process:

- **MapIR**
    - Unpack RAW
    - Debayer
    - 12bit Data in uint16 package
    - 8bit Normalization
    - Display
    - Dial In

- **Band Correction --> Experiment**
    - Correction: correction function
    - Band_Correction--> Experiment
        - Get Values Area
        - Graph
        - Integrate_NP
    - Hyperspectral
        - ENVI I/O
        - Monochromator Wavelength Adjustment
        - Comparisons
        - 
- **Radiance Calibration**
    - Radiance
    - Radiance_Calibration--> Experiment
        - Dark Current Subtraction
        - Flat Field H vs V
        - Radiance Values Center
        
- **Reflectance Calibration**
    - Reflectance: radiance calibration function
    - Reflectance_Calibration
    
- **Georectification**
    - Extract GPS
    - Export
    - Georectify
    
- **Vegetation Analysis**
    - NDVI Display
    - GNDVI Display
    - NDVI Area Values