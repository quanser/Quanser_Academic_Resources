'''This example demonstrates how to read and display data from the QCar Lidar
'''
import time
import matplotlib.pyplot as plt
from pal.products.qcar import QCarLidar,IS_PHYSICAL_QCAR
# from pal.utilities.lidar import Lidar

# polar plot object for displaying LIDAR data later on
ax = plt.subplot(111, projection='polar')
plt.show(block=False)

runTime = 10.0 # seconds
# Lidar settings
numMeasurements 	 = 1000	# Points
lidarMeasurementMode 	 = 2
lidarInterpolationMode = 0

# LIDAR initialization and measurement buffers
myLidar = QCarLidar(
	numMeasurements=numMeasurements,
	rangingDistanceMode=lidarMeasurementMode,
	interpolationMode=lidarInterpolationMode
)


t0 = time.time()
while time.time() - t0  < runTime:
    plt.cla()

    # Capture LIDAR data
    myLidar.read()

    ax.scatter(myLidar.angles, myLidar.distances, marker='.')
    ax.set_theta_zero_location("W")
    ax.set_theta_direction(-1)

    plt.pause(0.1)

myLidar.terminate()

