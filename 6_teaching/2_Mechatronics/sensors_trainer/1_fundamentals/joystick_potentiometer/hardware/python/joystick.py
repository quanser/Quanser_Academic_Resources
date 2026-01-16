# joystick.py
# This script reads and displays the input from the potentiometer and joystick 

# region: Python level imports
import subprocess
import os
import sys
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
# endregion

#region: Scope or Probe/Observer setup
# Scopes for potentiometer and joystick 
probe = Probe(ip = 'localhost')
probe.add_scope(numSignals=1, name='Potentiometer Angle' )
probe.add_scope(numSignals=4, name='Joystick')

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
potAngle = 0
# endregion

# Function to perform dead zone correction
def correct_deadzone(joystickIn, lowerLimit = -0.05, upperLimit = 0.05 ):
    joystickOut = 0
    # Add your code to implement dead zone correction here 
    return joystickOut

# region: Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
with SensorsTrainer() as sensors:

    while timer.check():
        
        currentTime = timer.get_current_time()

        sensors.read_outputs()
        
        potentiometer = sensors.forceResistor
        joystick0 = sensors.joystick[0]
        joystick1 = sensors.joystick[1]
        joystickButton = sensors.joystickButton

        # Estimate potentiometer angle
        # potAngle = 

        correctedJoy0 = correct_deadzone(joystick0)
        correctedJoy1 = correct_deadzone(joystick1)
        
        # update scopes every 4 samples
        if counter%4 == 0:
            
            probe.send(name='Potentiometer Angle',
                       scopeData=(currentTime, [potAngle]))
            
            probe.send(name='Joystick', 
                       scopeData=(currentTime,
                                  [potentiometer, 
                                   joystick0, 
                                   joystick1, 
                                   joystickButton]))
            
            
            # Print potentiometer values
            # print(f'Potentiometer voltage: {potentiometer:.2f}, Estimated angle: {potAngle:.2f}')

            # Print joystick readings
            # Add your code to print joystick readings here
            
            
        counter += 1
        timer.sleep()

input('Press the enter key to exit.')
probe.terminate()
# endregion

