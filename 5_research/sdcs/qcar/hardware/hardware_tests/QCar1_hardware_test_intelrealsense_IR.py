'''hardware_test_intelrealsense.py

This example demonstrates how to read and display depth & RGB image data
from the Intel Realsense camera.
'''
import time
import cv2
from pal.products.qcar import QCarRealSense, IS_PHYSICAL_QCAR

if not IS_PHYSICAL_QCAR:
    import qlabs_setup
    qlabs_setup.setup()


#Initial Setup
runTime = 20.0 # seconds

with QCarRealSense(mode='IR') as myCam:
    t0 = time.time()
    while time.time() - t0 < runTime:

        myCam.read_IR()

        cv2.imshow('Left IR Camera', myCam.imageBufferIRLeft)
        cv2.imshow('Right IR Camera', myCam.imageBufferIRRight)

        cv2.waitKey(100)