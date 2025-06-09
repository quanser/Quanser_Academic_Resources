'''hardware_test_csi_cameras.py

This example demonstrates how to read and display images from the CSI cameras.
'''
import time
import cv2
from pal.products.qcar import QCarCameras, IS_PHYSICAL_QCAR

#Initial Setup
runTime = 30.0 # seconds

cameras = QCarCameras(
    enableBack=True,
    enableFront=True,
    enableLeft=True,
    enableRight=True,
)

with cameras:
    t0 = time.time()
    while time.time() - t0 < runTime:
        cameras.readAll()

        for i, c in enumerate(cameras.csi):
            if c is not None:
                cv2.imshow(('CSI '+str(i)+':'), c.imageData)

        cv2.waitKey(100)
