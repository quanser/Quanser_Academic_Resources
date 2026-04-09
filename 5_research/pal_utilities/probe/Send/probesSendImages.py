#-----------------------------------------------------------------------------#
# probeSendImages.py
#-----------------------------------------------------------------------------#
# This example demonstrates how to stream, receive, and display image data using 
# the probe and observer module.

# To run this example, 
# 1) open receive.py and comment out the code that opens other displays, plots, 
# and scopes. Keep the code to open the display named "My Image 1"
# 2) run receive.py  
# 3) go to the directory containing this script and run the script (use a 
#  separate terminal if running both scripts on the same machine)

from pal.utilities.probe import Probe
import time
import numpy as np
import cv2

start = time.time()
def elapsed_time():
    return time.time() - start

# Image Parameters
IMAGE_WIDTH = 640
IMAGE_HEIGHT = 480
IMAGE_CHANNELS = 3

# Probe Test Parameters
IP_HOST = 'localhost'
TEST_TIME = 10 # seconds

# Initialize probe
probe = Probe(ip=IP_HOST)
probe.add_display(imageSize = [IMAGE_HEIGHT,IMAGE_WIDTH,IMAGE_CHANNELS],
                  scaling = True,
                  scalingFactor = 2,
                  name = 'my display')

img = cv2.imread('test.png')

try:
    connected = False
    time.sleep(0.1)
    while elapsed_time() < TEST_TIME:
        if not probe.connected:
            probe.check_connection()

        if probe.connected:

            # display image 
            cv2.imshow('Window', img)
            cv2.waitKey(33)

            # send image
            sent = probe.send(name='my display', imageData=img)
            if not sent:
                break

            time.sleep(0.033)

except KeyboardInterrupt:
    print('User Interrupted!')
    pass

finally:
    # Terminate all displays
    probe.terminate()
