## example_test_qbot_io.py
# This example lets you drive the QBot 3 hardware or QBot 2e virtual plant in using task mode (timebase API).
# Ensure that you start the Quanser Interactive Labs - QBot 2e Workspace before using the virtual QBot. 
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: imports
from pal.products.qbot import QBot3
import numpy as np
import time
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 240.0
sampleTime = 1/sampleRate
simulationTime = 30 # some large number
print('Simulation rate is set to', sampleRate, '...')

#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Initialize QBot3 object
myQBot       = QBot3(hardware=0, readMode=1, frequency=int(sampleRate))
 
startTime = time.time()
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
#region: Main Loop
try:
    prev = elapsed_time() - sampleTime
    
    while elapsed_time() < simulationTime:
        
        # Start timing this iteration
        start = elapsed_time()
        
        # Set different motion commands based on time
        if elapsed_time() < 5:
            rightWheelVel = 0.1
            leftWheelVel = 0.1
            led1State = 0
            led2State = 1
        elif elapsed_time() < 10:
            rightWheelVel = -0.1
            leftWheelVel = -0.1
            led1State = 1
            led2State = 0
        elif elapsed_time() < 15:
            rightWheelVel = -0.2
            leftWheelVel = 0.2
            led1State = 1
            led2State = 1
        elif elapsed_time() < 20:
            rightWheelVel = 0.2
            leftWheelVel = -0.2
            led1State = 2
            led2State = 2
        elif elapsed_time() < 25:
            rightWheelVel = 0
            leftWheelVel = 0
            led1State = 2
            led2State = 2
        elif elapsed_time() < 30:
            rightWheelVel = 0
            leftWheelVel = 0
            led1State = 0
            led2State = 0
            
        # Write commands and update measurements
        myQBot.read_write_std(rightWheelVel, leftWheelVel, led1State, led2State)        

        # Get wheel distance from encoders. 
        rightWheelDistance = myQBot.estimate_wheel_travel(myQBot.rightEncoder)
        leftWheelDistance = myQBot.estimate_wheel_travel(myQBot.leftEncoder)

        end = elapsed_time()
        prev = start

except KeyboardInterrupt:
    print("User interrupted!")

finally:    
    myQBot.terminate()
#endregion
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 