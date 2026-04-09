# actuatorsSensorlessBLDC.py
# This script demonstrates how to control the BLDC motor in sensorless mode. 
# This means that the channels dont have to be enabled in sequence or periodically. 
# It uses current from the channels to figure out the rotation. 

# Connect the BLDC connector to Block 2. 
# The encoder cable does not have to be connected for this to work.  

# region: Python level imports
import numpy as np
from pal.utilities.timing import Timer
from pal.products.actuators import ActuatorsTrainer
# endregion 

# region: Experiment constants
simulationTime = 30 # will run for this amount of seconds
frequency = 400 # Hz

cntr1s = 0
cntr3s = 0

bldcAmplitude = 0.3
direction = 1
# endregion

# region: Main Loop
with ActuatorsTrainer(block = 2, bldcSensorless=1) as actuators:
    
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)

    actuators.enable_motors()
    while timer.check():

        actuators.read_outputs()

        cntr1s = cntr1s + 1
        cntr3s = cntr3s + 1

        # code running once a second
        if cntr1s == frequency:
            rads = actuators.sensorlessTach * 2 * np.pi / 16
            rpm = actuators.sensorlessTach/16 * 60
            print(f'motor speed: {actuators.sensorlessTach:.2f} counts/s    {rads:.2f} rad/s   {rpm:.1f} rpm')
            cntr1s = 0

        # every 3 seconds switch direction
        if cntr3s == 3*frequency:
            direction = direction * -1
            cntr3s = 0

        cmd = bldcAmplitude * direction
        actuators.update_bldc_sensorless(cmd)
        actuators.write_motors()

        timer.sleep()

# endregion
