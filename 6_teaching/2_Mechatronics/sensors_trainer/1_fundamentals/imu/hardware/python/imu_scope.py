# IMU - IMU Scope

# Visualizing the IMU data

# region: Python level imports
import subprocess
import math
import sys
import os
import statistics
import numpy as np
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scoping
# Scopes for Gyroscope & Accelerometer data
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=3, name='Gyroscope')
probe.add_scope(numSignals=3, name='Accelerometer')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer_scope.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
sampleRate = 480 # Hz
totalTime = 20 # sec
# endregion

# region: Main Loop
with SensorsTrainer() as sensors:
    gyroData  = [[], [], []]
    accelData = [[], [], []]
    counter = 0
    timer   = Timer(sampleRate=sampleRate, totalTime=totalTime)

    while timer.check():
        # get current timestamp
        currentTime = timer.get_current_time()

        # get updated sensor measurements
        sensors.read_outputs()
        bias = np.array([ 0.00, 0.00, 0.00], dtype=np.float64)
        gyro = sensors.gyro * (180/math.pi) - bias
        accelerometer = sensors.accelerometer
        gyroData[0].append(gyro[0])
        gyroData[1].append(gyro[1])
        gyroData[2].append(gyro[2])
        accelData[0].append(accelerometer[0])
        accelData[1].append(accelerometer[1])
        accelData[2].append(accelerometer[2])

        # plot IMU data
        if counter%5 == 0:
            probe.send(name='Gyroscope',
                        scopeData=(currentTime, gyro))
            probe.send(name='Accelerometer',
                        scopeData=(currentTime, accelerometer))

        counter += 1
        timer.sleep()

print('Analyzing IMU data noise: \n')
print('Gyro X:', statistics.mean(gyroData[0]), u"\u00B1", statistics.stdev(gyroData[0]))
print('Gyro Y:', statistics.mean(gyroData[1]), u"\u00B1", statistics.stdev(gyroData[1]))
print('Gyro Z:', statistics.mean(gyroData[2]), u"\u00B1", statistics.stdev(gyroData[2]))
print('Accel X:', statistics.mean(accelData[0]), u"\u00B1", statistics.stdev(accelData[0]))
print('Accel Y:', statistics.mean(accelData[1]), u"\u00B1", statistics.stdev(accelData[1]))
print('Accel Z:', statistics.mean(accelData[2]), u"\u00B1", statistics.stdev(accelData[2]))
input('Press the enter key to exit.')
probe.terminate()

# endregion