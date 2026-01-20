# Color Sensing from Monitor
# In this section of the experiment, we will read color values displayed on a monitor
# and use the calibrated color sensor to detect the displayed colors. The detected colors
# will be shown alongside the source colors for comparison.

# region: Python level imports
import numpy as np
import cv2

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from visualizer import ColorDisplay
from colormath.color_objects import XYZColor, sRGBColor
from colormath.color_conversions import convert_color
# endregion

# region: experiment parameters setup
simulationTime = 60 # will run for this amount of seconds
frequency = 20 # Hz
# sensor to CIE XYZ conversion matrix obtained from calibration
M = np.array(    
    [[  0,  0,  0 ],
     [  0,  0,  0 ],
     [  0,  0,  0 ]]
)
# endregion

# region: main sensor loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
color = ColorDisplay()
with SensorsTrainer() as sensors:

    sourceColor = np.zeros((600, 600, 3), dtype=np.uint8)
    detectedColor = np.zeros((600, 600, 3), dtype=np.uint8)
    color.set_tracker()

    while timer.check():
        
        # Set source color from slider
        rValue,gValue,bValue = color.get_tracker()
        sourceColor[:] = (bValue, gValue, rValue)  # OpenCV uses BGR format

        # Read color sensor data
        sensors.read_outputs()
        
        # Apply calibration matrix M to get CIE XYZ values
        xyzDetected = M@sensors.colorRGB 
        # # Using colormath library to convert XYZ to sRGB for display
        sRGB = convert_color(XYZColor(xyzDetected[0], xyzDetected[1], xyzDetected[2]), sRGBColor)
        sRGBDetected = np.array((sRGB.clamped_rgb_r, sRGB.clamped_rgb_g, sRGB.clamped_rgb_b))
        sRGBDetected= (sRGBDetected*255).astype(np.uint8)

        # display detected color alongside source color
        detectedColor[:] = (sRGBDetected[2], sRGBDetected[1], sRGBDetected[0])
        output_image = np.hstack((sourceColor, detectedColor))
        cv2.imshow('Solid Color', output_image)
        cv2.waitKey(1)
        timer.sleep()
        
cv2.destroyAllWindows()
# endregion
input("Press Enter to continue...")




