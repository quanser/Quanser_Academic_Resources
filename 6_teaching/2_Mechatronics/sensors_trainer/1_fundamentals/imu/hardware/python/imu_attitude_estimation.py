# IMU - IMU Attitude Estimation

# Estimating the roll & pitch angles from the accelerometer data

# region: Python level imports
import subprocess
import sys
import os
import math
import numpy as np
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scoping
# Scopes for Attitude data
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=5, name='Attitude')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer_attitude_estimation.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
sampleRate = 480 # Hz
totalTime = 300 # seconds
attitude = np.zeros(5, dtype=np.float64)
# endregion

# region: Main Loop
with SensorsTrainer() as sensors:
    timer   = Timer(sampleRate=sampleRate, totalTime=totalTime)
    counter = 0
    while timer.check():
        # get current timestamp
        currentTime = timer.get_current_time()

        # get updated sensor measurements
        sensors.read_outputs()

        # convert gyro data to degrees/s & get accelerometer data
        bias = (math.pi/180)*np.array([ 0.00, 0.00, 0.00], dtype=np.float64) # bias from imu_scope.py file.
        gyro = sensors.gyro  - bias
        accelerometer = sensors.accelerometer

        # estimate the roll & pitch angles from the accelerometer data in deg
        attitude[0] = 0
        attitude[1] = 0
        attitude[2] = 0
        attitude[3] = 0
        attitude[4] = 0

        # plot IMU data
        if counter%5 == 0:
            probe.send(name='Attitude',
                        scopeData=(currentTime, attitude))

        counter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion