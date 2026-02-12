## QCar2_lane_following_keyboard.py
# This example combines both the front csi and motor commands to
# allow the QCar to follow a yellow lane. Use the keyboard to manually drive the QCar,
# use the WASD keys to control the throttle and steering, 
# and hold the space bar to enable the line follower (W key will still have to be pressed to go forward).

from pal.utilities.vision import Camera2D
from pal.products.qcar import QCar, QCarCameras
from pal.utilities.math import Filter
from pal.utilities.keyboard import KeyboardDrive,QKeyboard
from hal.utilities.image_processing import ImageProcessing

import time
import numpy as np
import cv2
import math

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
sampleRate = 60
sampleTime = 1/sampleRate
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#Setting Filter
steeringFilter = Filter().low_pass_first_order_variable(25, 0.033)
next(steeringFilter)
dt = 0.033

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Initialize the CSI cameras
imageWidth  = 1640
imageHeight = 820
QCarCamera = QCarCameras(frameWidth=imageWidth, frameHeight=imageHeight, enableFront=True)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## QCar, Gamepad, and probe Initialization
myCar = QCar(readMode=1, frequency=60)

kb = QKeyboard()
kbdrive = KeyboardDrive(mode=0,maxThrottle=0.05,maxSteer=0.3)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Main Loop
try:
	while True:
		start = time.time()
		# Capture RGB Image from CSI
		QCarCamera.readAll()
		# Crop out a piece of the RGB to improve performance
		croppedRGB = QCarCamera.csiFront.imageData[524:674, 0:820]

		# Convert to HSV and then threshold it for yellow
		hsvBuf = cv2.cvtColor(croppedRGB, cv2.COLOR_BGR2HSV)

		binaryImage = ImageProcessing.binary_thresholding(frame= hsvBuf,
													lowerBounds=np.array([10, 50, 100]),
													upperBounds=np.array([45, 255, 255]))


		# Overlay detected yellow lane over raw RGB image
		binaryImage=binaryImage/255
		processed = QCarCamera.csiFront.imageData
		processed[524:674, 0:820,2]=processed[524:674, 0:820,2]+(255-processed[524:674, 0:820,2])*binaryImage
		processed[524:674, 0:820,1]=processed[524:674, 0:820,1]*(1-binaryImage)
		processed[524:674, 0:820,0]=processed[524:674, 0:820,0]*(1-binaryImage)

		# Display the RGB cropped RGB Image and the resized binary image
		cv2.imshow('Detection Overlay', cv2.resize(processed, (820,410)) )

		# Find slope and intercept of linear fit from the binary image
		slope, intercept = ImageProcessing.find_slope_intercept_from_binary(binary=binaryImage)

		# steering from slope and intercept
		rawSteering = 1.5*(slope - 0.3419) + (1/150)*(intercept+5)
		steering = steeringFilter.send((np.clip(rawSteering, -0.5, 0.5), dt))

		kb.update()

		steering_kbd, throttle_kbd = kbdrive.update(kb)
		QCarCommand = np.array([throttle_kbd, steering_kbd])

		if kb.states[kb.K_SPACE]:
			if math.isnan(steering):
				QCarCommand[1] = 0
			else:
				QCarCommand[1] = steering
			QCarCommand[0] = QCarCommand[0]*np.cos(steering)

		LEDs = np.array([0, 0, 0, 0, 0, 0, 0, 0])
		myCar.read_write_std(QCarCommand[0],QCarCommand[1],LEDs)
		cv2.waitKey(1)
		end = time.time()
		dt = end - start

except KeyboardInterrupt:
	print("User interrupted!")
		
finally:
	# Terminate camera and QCar
	QCarCamera.terminate()
	myCar.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
