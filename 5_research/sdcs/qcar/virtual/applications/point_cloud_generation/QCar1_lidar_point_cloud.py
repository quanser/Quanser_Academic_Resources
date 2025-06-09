'''LIDAR_Point_Cloud.py
This example uses the LiDAR point cloud to construct a temporary local map
of the QCar's environment.To troubleshoot the physical LiDAR use the
 hardware_test_rp_lidar_a2.py found in the hardware_tests directory
'''
from pal.products.qcar import QCarLidar
from pal.utilities.math import *
import time
import numpy as np
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
	return time.time() - startTime

sampleRate 	   = 30
sampleTime 	   = 1/sampleRate
simulationTime = 30.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Additional parameters and buffers
pixelsPerMeter 	  = 50 # pixels per meter
sideLengthScale   = 8*pixelsPerMeter # 8 meters width, or 400 pixels side length
decay 		      = 0.9 # 90% decay rate on old map data
maxDistance  	  = 2.9 # m
map    		  	  = np.zeros((sideLengthScale,
			  				sideLengthScale), dtype=np.float32) # map object

# Lidar settings
numMeasurements 	 = 360	# Points


# LIDAR initialization and measurement buffers
myLidar = QCarLidar(numMeasurements=numMeasurements)


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Main Loop
try:
	while elapsed_time() < simulationTime:
		# decay existing map
		map = decay*map

		# Start timing this iteration
		start = time.time()

		# Capture LIDAR data
		myLidar.read()

		# convert angles from lidar frame to body frame
		anglesInBodyFrame = myLidar.angles * -1


		# Find the points where it exceed the max distance and drop them off
		idx = [i for i, v in enumerate(myLidar.distances) if v < maxDistance]

		# convert distances and angles to XY contour
		x = myLidar.distances[idx]*np.cos(anglesInBodyFrame[idx])
		y = myLidar.distances[idx]*np.sin(anglesInBodyFrame[idx])

		# convert XY contour to pixels contour and update those pixels in the map
		pX = (sideLengthScale/2 - x*pixelsPerMeter).astype(np.uint16)
		pY = (sideLengthScale/2 - y*pixelsPerMeter).astype(np.uint16)

		map[pX, pY] = 1

		# End timing this iteration
		end = time.time()

		# Calculate the computation time, and the time that the thread should pause/sleep for
		computationTime = end - start
		sleepTime = sampleTime - ( computationTime % sampleTime )

		# Display the map at full resolution
		cv2.imshow('Map', map)

		# Pause/sleep for sleepTime in milliseconds
		msSleepTime = int(1000*sleepTime)
		if msSleepTime <= 0:
			# this check prevents an indefinite sleep as cv2.waitKey waits indefinitely if input is 0
			msSleepTime = 1
		cv2.waitKey(msSleepTime)


except KeyboardInterrupt:
	print("User interrupted!")

finally:
	# Terminate the LIDAR object
	myLidar.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --