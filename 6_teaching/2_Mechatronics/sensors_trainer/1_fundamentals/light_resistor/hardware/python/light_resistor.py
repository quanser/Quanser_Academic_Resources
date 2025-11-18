# light_resistor.py
# This script reads and displays the input from the light resistor 

# region: Python level imports
import numpy as np
import subprocess
import sys
import os
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion

#region: Scope setup
# Scope for light resistor 
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=3, name='Light Resistor')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 500 # will run for this amount of seconds
frequency = 200 # Hz

counter = 0 # counter to track scopes
lightResistorMin = 3.3
lightResistorMax = 0.0
# endregion

# region: Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors:

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        lightResistor = sensors.lightResistor
        lightResistorMin = np.min([lightResistorMin, lightResistor])
        lightResistorMax = np.max([lightResistorMax, lightResistor])
        
        # Update scopes every 4 samples
        if counter%4 == 0:
            probe.send(name='Light Resistor',
                       scopeData=(currentTime,[lightResistor, 
                                               lightResistorMin, 
                                               lightResistorMax]))
            
        # Print to terminal every 10 samples 
        if counter%10 == 0:
            print(f'Light resistor reading: {lightResistor:.2f} V, '
                  f'Minimum: {lightResistorMin:.2f} V, '
                  f'Maximum: {lightResistorMax:.2f} V')
            
        counter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion
