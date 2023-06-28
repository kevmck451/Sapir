# MapIR Application

### Documents
    - Data Collection Guide: step by step guide to collecting field data with Mavic Pro and MapIR camera
    - Data Processing Guide: step by step guide to processing field data after aquisition
    - MapIR Code Structure: Contents of MapIR python module

### MapIR
    - Unpack RAW
    - Debayer: 12bit Data in float64 package
    - 8bit Normalization for Display
    - Display
    - Dial In
    - Export tiff normalized in 16bit

### Band Correction
    - Correction: Band Correction Function
    - Band_Correction
        - Generate Correction Matrix from Exp
        - Generate Wavelength Response from Exp
    - Band_Correction--> Experiment
        - Get Values Area
        - Graph
        - Integrate_NP
    - Hyperspectral
        - ENVI I/O
        - Monochromator Wavelength Adjustment
        - Comparisons
      
### Radiance Calibration
    - Radiance: 
      - Dark Current Subtraction Function
      - Flat Field Correction Function
      - Radiance Calibration Function
    - Radiance_Calibration
      - Generate Dark Current Values
      - Generate Flat Field Correction Matrix
      - Generate Radiance Band Values 
      - Generate Radiance Equation Values
    - Radiance_Calibration--> Experiment
      - Dark Current Subtraction
      - Flat Field H vs V
      - Flat Field Correction
      - Radiance Values Center
        
### Reflectance Calibration
    - Reflectance: radiance calibration function
    - Reflectance_Calibration
    
### Georectification
    - Extract GPS
    - Export
    - Georectify

### Process
    - Process: steps for processing single image

### Vegetation Analysis
    - MapIR for PNG files (after georect)
    - NDVI Display
    - GNDVI Display
    - NDVI Area Values