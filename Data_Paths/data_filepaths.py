# File to house all the data directories for iteration

# SOURCE PATH:
main_path = 'C:/Users/Ainee/Desktop/Work/MapIR_Data'

#-------------------------

active_dataset = main_path+'/Data/Summer_023/AC Wheat Field 6-20'
target_panel = active_dataset+'/ref_target.RAW'

#------------------------


# ---------------------------
# LABSPHERE EXPERIMENTS ----
# ---------------------------

labsphere_doc = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/LabSphere_Values.csv'
labsphere_bands = main_path+'/mapir-main/Process/Radiance_Calibration/labsphere/labsphere_bands.npy'
labsphere_rad_values = main_path+'/mapir-main/Process/Radiance_Calibration/labsphere/labsphere_rad_vals.npy'

# Labsphere Experiment 1
labsphere_experiment_1_dial_ins = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/Experiments/Exp 1/Dial In'
labsphere_experiment_1_raw = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/Experiments/Exp 1/raw'

# Labsphere Experiment 2
labsphere_experiment_2_dial_ins = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/Experiments/Exp 2/Dial In'
labsphere_experiment_2_raw = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/Radiance Calibration/Experiments/Exp 2/raw'


# -------------------------------
# MONOCHROMATOR EXPERIMENTS -----
# -------------------------------

# Monochromator Experiment 4
MC_Exp_4 = '/Users/KevMcK/Dropbox/2 Work/1 Optics Lab/2 Imaging/Data/MapIR/MC Tests/MC Test 4'

# Wavelength Response Corrected
MC_Test_Bands = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_Corr/MapIR_Bands.npy'
MC_Test_Reds_Corr = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_Corr/MapIR_Rvalues.npy'
MC_Test_Greens_Corr = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_Corr/MapIR_Gvalues.npy'
MC_Test_NIR_Corr = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_Corr/MapIR_Nvalues.npy'

# Wavelength Response RAW
MC_Test_Reds = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_RAW/MapIR_Rvalues.npy'
MC_Test_Greens = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_RAW/MapIR_Gvalues.npy'
MC_Test_NIR = main_path+'/mapir-main/Process/Band_Correction/Wavelengths_RAW/MapIR_Nvalues.npy'


# ----------------------
# ---- AINEE PATHS -----
# ----------------------

Test_For_Aruco_Exp = main_path + '/Data/Summer 23/Test Files (Reflectance)/Trial 2/Sunny'
Distorion_Cal_Experiment = main_path+'/Data/Distortion Calibration'
Test_Reflectance_Set1 = main_path+'/Data/Summer 23/Test Files (Reflectance)/AC Wheatfield 7-27'

AC_WF_6_8 = main_path+'/Data/Summer 23/AC Wheat Field 6-8'
AC_WF_6_20 = main_path+'/Data/Summer 23/AC Wheat Field 6-20'
AC_WF_7_27 = main_path+'/Data/Summer 23/7-27-23 Agri Center'
