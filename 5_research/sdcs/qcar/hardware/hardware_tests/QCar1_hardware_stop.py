'''hardware_stop.py

This example correctly terminates the Lidar and QCar DAQ if they are still
in use. If the LIDAR is still spinning, or the QCar motor drive did not shut
off properly, use this script.
'''
from pal.products.qcar import QCar, QCarLidar


# Initializing QCar and Lidar
myLidar = QCarLidar()
myCar = QCar()

# Terminating DAQs if currently running
myCar.terminate()
myLidar.terminate()
