'''hardware_test_intelrealsense.py

This example demonstrates how to read and display depth & RGB image data
from the Intel Realsense camera.
'''
import time
import cv2
from pal.products.qcar import QCarRealSense

#Initial Setup
runTime = 30.0 # seconds

with QCarRealSense(mode='RGB, Depth') as myCam:
    t0 = time.time()
    while time.time() - t0 < runTime:

        myCam.read_RGB()
        cv2.imshow('My RGB', myCam.imageBufferRGB)

        myCam.read_depth()
        cv2.imshow('My Depth', myCam.imageBufferDepthPX)

        cv2.waitKey(100)
