# sensorsAndActuators.py
# This example demonstrates reading encoder values from the Sensors Trainer
# and using those values to control a DC motor on the Actuators Trainer in block 0.
# This example is meant to be used as a reference on how to use both devices together.

import numpy as np

from pal.products.actuators import ActuatorsTrainer
from pal.products.sensors import SensorsTrainer
from pal.utilities.timing import Timer

simulationTime = 150 # will run for this amount of seconds
frequency = 400 # Hz

counter = 0

printRate = 2 # Print at 2Hz (2 times per second)
printCounts = int(round(frequency / printRate))

# Initialize timer
timer = Timer(frequency, simulationTime)

# Open actuators block0 and the sensors trainer
with (ActuatorsTrainer(block = 0) as block0,
      SensorsTrainer(knobEncQuad=4) as sensors):

    # Enable motors on all blocks
    block0.enable_motors()

    while timer.check():

        # get current timestamp
        currentTime = timer.get_current_time()

        # read outputs from block 0
        # Even if encoders or currents are not used,
        # this is necessary to keep the communication active and not trigger
        # a watchdog timeout.
        block0.read_outputs()

        # read sensors output data
        sensors.read_outputs()

        # read encoder counts and clip them from -100 to 100
        # to use as a percentage to control the DC motor
        encoderCounts = np.clip(sensors.encoder0, -100, 100)

        # motor command will be between -0.5 to 0.5 (-1 to 1 is equal to -12 to 12 V)
        dcCmd = 0.5 * encoderCounts/100

        # print twice a second.
        if counter%printCounts == 0:
            print(f"Time: {currentTime:.2f} s | Encoder Counts: {encoderCounts}  | DC Motor Command {dcCmd:.2f} V")


        # update DC motor
        block0.update_dc(dcCmd, limitCmd=False)

        # write motor commands
        block0.write_motors()

        counter += 1
        timer.sleep()
