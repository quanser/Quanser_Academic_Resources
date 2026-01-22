# Analyzing Raw Load Cell Data	
# This section of the experiment will guide you through collecting and 
# analyzing raw load cell data using the Sensors Trainer. You will visualize 
# the load cell readings in real-time and compute basic statistics to understand 
# the noise characteristics of the sensor.

# region: Python level imports
import numpy as np
import subprocess
import sys
import os
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

# region: set up visualization and experiment parameters
# Set up scope for load cell data visualization and start observer thread.
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Load Cell')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer_scope.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()

# Set up parameters for data collection
frequency = 1000 # Hz
duration = 5 # Second
# endregion

# region: main data collection loop
with SensorsTrainer() as sensors:
    timer = Timer(sampleRate=frequency, totalTime=duration)
    sensorBuffer = np.zeros(frequency*duration)
    counter = 0
    while timer.check():
        sensors.read_outputs()
        loadCell = sensors.loadCell
        sensorBuffer[counter] = loadCell
        if counter % 20 == 0:
            probe.send(name='Load Cell',
                        scopeData=(timer.get_current_time(), np.array([loadCell])))
        counter += 1
        timer.sleep()
# endregion

# region: analyze collected data
print('\nAnalyzing load cell data noise: ')
print('Load Cell:', sensorBuffer.mean(), u"\u00B1", np.std(sensorBuffer))
# endregion

input ("Press Enter to exit...")