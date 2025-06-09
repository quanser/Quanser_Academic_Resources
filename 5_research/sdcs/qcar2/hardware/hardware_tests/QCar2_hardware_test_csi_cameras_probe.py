'''hardware_test_csi_cameras.py

This example demonstrates how to read and display image data
from the 4 csi cameras.
'''
import time
import cv2
from pal.products.qcar import QCarCameras, IS_PHYSICAL_QCAR
import os
from pal.utilities.probe import Probe

# Initial Setup
ipObserver = '192.168.3.10' #ip of the local machine that runs the observer.py
runTime = 30.0 # seconds
counter = 0
cameras = QCarCameras(
    enableBack=True,
    enableFront=True,
    enableLeft=True,
    enableRight=True,
)

try:
    t0 = time.time()
    probe = Probe(ip = ipObserver)
    for i in range(4):
        probe.add_display(imageSize = [410, 820, 3], scaling = True,
                            scalingFactor= 2, name="CSI"+str(i))
    while time.time() - t0 < runTime:
        # print(probe.agents)
        if not probe.connected:
            probe.check_connection()
        if probe.connected:
            flags = cameras.readAll()
            if all(flags): counter +=1
            if counter % 40 == 0:
                for i, c in enumerate(cameras.csi):
                    sending = probe.send(name="CSI"+str(i),
                                    imageData=c.imageData)
except KeyboardInterrupt:
    print('User interrupted.')
finally:
    # Termination
    cameras.terminate()
    probe.terminate()