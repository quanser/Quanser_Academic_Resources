# force_resistor.py
# This script reads and displays the input from the force resistor
# Students use the force resistor input to control the brightness of an LED  

# region: Python level imports
import subprocess
import os
import sys
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scope setup
# Scope for force resistor reading
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Force Resistor')

subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 500 # will run for this duration in seconds
frequency = 200 # Hz

counter = 0 # counter to track samples
# endregion

# region:  Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer() as sensors:

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()

        forceResistor = sensors.forceResistor

        # Turn on colour sensor LED based on the force resistor input
        # if (True):
        #     sensors.write_leds(rgb=0.5)
        # else:
        #     sensors.write_leds(rgb=0)
        
        # Set LED brightness based on force resistor input
        # Add your code to set the LED brightness here    
        
        # Update scopes every 4 samples
        if counter%4 == 0:
            probe.send(name='Force Resistor', 
                       scopeData= (currentTime, 
                                    [forceResistor]))

            # Print to terminal
            print(f"Time: {currentTime:.2f} s, Force Resistor Value: {forceResistor:.2f} ")
            
        counter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion