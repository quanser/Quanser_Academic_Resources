# Calibrate Color Sensor
# This section of the experiment is used to compute the calibration matrix M
# that maps raw sensor readings to CIE 1931 XYZ tristimulus values.

# region: Python level imports
import numpy as np
# endregion 

# region: main calibration function
def main():
    sensorReadings = np.array(
        [[0.0,0.0,0.0], # sensor readings for Red LED
         [0.0,0.0,0.0], # sensor readings for Green LED
         [0.0,0.0,0.0], # sensor readings for Blue LED
        ]
    )
    rgbWavelengths = [0,0,0] # Wavelengths for Red, Green, Blue LEDs in nm

    xyzValues = []
    for wl in rgbWavelengths:
        xyz = wavelength_to_xyz(wl)
        xyzValues.append(xyz)
    
    # create matrices S and T
    S = np.zeros((3,3))
    T = np.zeros((3,3))

    # --- complete your task here---
    
    M = np.ones((3,3))
    # ---------------------
    print(f"Calibration matrix M:\n{M}")
# endregion

# region: helper function to convert wavelength to CIE XYZ values
def wavelength_to_xyz(wl,path='CIE_xyz_1931_2deg.csv'):
    """Convert a wavelength in nm to CIE 1931 XYZ tristimulus values.
    args: 
        wl: wavelength in nm
        path: path to CIE xyz csv file
    returns:
        XYZ: numpy array of [X, Y, Z] values"""
    
    # Load wavelength and XYZ values
    xyzCsv = np.loadtxt(path, delimiter=',')
    wavelengths = xyzCsv[:, 0]
    xBar = xyzCsv[:,1]
    yBar = xyzCsv[:,2]
    zBar = xyzCsv[:,3]

    # --- complete your taks here---
    
    XYZ = np.array([0, 0, 0])
    # ---------------------

    print(f"Wavelength {wl} nm -> CIE XYZ: {XYZ}")
    return XYZ
# endregion

# region: run main function
if __name__=="__main__":
    main()
# endregion
input("Press Enter to exit...")


