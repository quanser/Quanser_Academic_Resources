# Quick Start Guide Test Encoders

import sys

# region: import libraries needed for SensorsTrainer with error messages
try:
    from quanser.hardware import HIL
except ImportError:
    print("Error: Could not find Quanser's python libraries. Make sure you installed Quanser SDK or QUARC (with Python libraries) and followed "
          "the instructions in https://github.com/quanser/Quanser_Academic_Resources/blob/dev-windows/docs/pc_setup.md#completing-the-setup. " \
          "You can install Quanser SDK from https://github.com/quanser/quanser_sdk")
    sys.exit(0)

try:
    from pal.utilities.timing import Timer
    from pal.products.sensors import SensorsTrainer
except ImportError:
    print("Error: Could not import Quanser Academic's libraries. Make sure you followed "
          "the instructions in https://github.com/quanser/Quanser_Academic_Resources/blob/dev-windows/docs/pc_setup.md#completing-the-setup "
          "and restarted your computer afterwards.")
    sys.exit(0)

try:
    import numpy as np
except ImportError:
    print("Error: Could not find numpy library. Please install it with 'pip install numpy'")
    sys.exit(0)

try:
    import sounddevice
except ImportError:
    print("Error: Could not find sounddevice library. Please install it with 'pip install sounddevice'")
    sys.exit(0)

try:
    import scipy
except ImportError:
    print("Error: Could not find scipy library. Please install it with 'pip install scipy'")
    sys.exit(0)

try:
    import matplotlib
except ImportError:
    print("Error: Could not find matplotlib library. Please install it with 'pip install matplotlib'")
    sys.exit(0)

try:
    import cv2
except ImportError:
    print("Error: Could not find openCV (cv2) library. Please install it with 'pip install opencv-python'")
    sys.exit(0)
# endregion

counterHalfSec = 0

with SensorsTrainer(knobEncQuad=1) as sensors:
    timer = Timer(sampleRate=200, totalTime=200)

    while timer.check():
        currentTime = timer.get_current_time()
        sensors.read_outputs()

        encoder = sensors.encoder0

        if counterHalfSec%100 == 0: 
            print(f'Encoder counts: {encoder} ')
            
        counterHalfSec += 1
        timer.sleep()







