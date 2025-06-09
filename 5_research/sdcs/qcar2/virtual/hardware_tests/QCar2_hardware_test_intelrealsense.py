'''hardware_test_intelrealsense.py

This example demonstrates how to read and display depth & RGB image data
from the Intel Realsense camera.
'''
import time
import cv2
from pal.products.qcar import QCarRealSense, IS_PHYSICAL_QCAR

#Initial Setup
runTime = 30.0 # seconds
max_distance = 150 # meters (for depth camera)

with QCarRealSense(mode='RGB, Depth') as myCam:
    t0 = time.time()
    while time.time() - t0 < runTime:

        myCam.read_RGB()
        cv2.imshow('My RGB', myCam.imageBufferRGB)

        myCam.read_depth(dataMode='PX')
        cv2.imshow('My Depth', myCam.imageBufferDepthPX/max_distance)

        cv2.waitKey(100)
