# buttons.py 
# This script reads button inputs and displays them in a scope
# Students will implement latching functionality 

# region: Python level imports
import subprocess
import sys
import os
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion 

#region: Scope or Probe/Observer setup
# Scopes for button inputs
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=3, name='Buttons')
subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer.py')],
    cwd=os.path.dirname(__file__))
while not probe.connected:
    probe.check_connection()
# endregion

# region: Experiment constants
simulationTime = 500 # will run for this amount of seconds
frequency = 100 # Hz

sampleCounter = 0 # counter to track samples for scope 

buttonLatch = 0
prevButton1 = 0
buttonPressCounter = 0
# endregion

# region: Simulation
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

with SensorsTrainer(btn0Pol=1, btn1Pol=1) as sensors:

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        
        buttons = sensors.buttons
        
        # # Toggle buttonLatch when Button 1 is pressed 
        # if buttons[1] == 1:
            
        #     # Switch buttonLatch on or off
        #     if buttonLatch == 0:
        #         buttonLatch = 1
        #     else:
        #         buttonLatch = 0
            
        #     # Increment counter each time button is pressed 
        #     buttonPressCounter += 1
        #     # Print buttonPressCounter and buttonLatch to terminal
             
        # Update scopes every 4 samples
        if sampleCounter%4 == 0:
            # Add offset to plot signals without overlap    
            probe.send(name='Buttons',
                        scopeData=(currentTime,[buttons[0] + 4, buttons[1] + 2, buttonLatch]))
           
        prevButton1 = buttons[1]
        
        sampleCounter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion