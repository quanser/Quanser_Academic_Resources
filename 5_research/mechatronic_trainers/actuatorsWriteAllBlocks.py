# actuatorsWriteAllBlocks.py
# This script demonstrates how to control DC, BLDC, Servo, and Stepper motors
# on all four actuator blocks of the Mechatronic Actuators Trainer simultaneously.

# If the encoder cable of the DC motor is connected, the speed prints will update accordingly.

# The DC, BLDC, Servo and Stepper motor could be connected to any of the four blocks
# and they would all work the same way since all 4 blocks
# are commanded at the same time.

import numpy as np

from pal.products.actuators import ActuatorsTrainer
from pal.utilities.timing import Timer
from pal.utilities.math import SignalGenerator

simulationTime = 200 # will run for this amount of seconds
frequency = 400 # Hz

stepperAmplitude = 0.3
dcCommand = 0.3
bldcAmplitude = 0.3

servoCommand = SignalGenerator().sine(1, 1)
next(servoCommand)

stepper = np.array([[1, 0, 0, 0],
                    [0, 0, 1, 0],
                    [0, 1, 0, 0],
                    [0, 0, 0, 1]])

stepperCmd = stepper[0] * stepperAmplitude

counter = 0
stepCounter = 0

cntr2s = 0

# Initialize timer
timer = Timer(frequency, simulationTime)

# Open all actuator blocks
with (ActuatorsTrainer(block = 0, bldcSensorless=1) as block0,
      ActuatorsTrainer(block = 1, bldcSensorless=1) as block1,
      ActuatorsTrainer(block = 2, bldcSensorless=1) as block2,
      ActuatorsTrainer(block = 3, bldcSensorless=1) as block3):

    # Enable motors on all blocks
    block0.enable_motors()
    block1.enable_motors()
    block2.enable_motors()
    block3.enable_motors()

    while timer.check():

        # get current timestamp
        currentTime = timer.get_current_time()

        # individually read outputs from each block
        # Even if encoders or currents are not used,
        # this is necessary to keep the communication active and not trigger
        # a watchdog timeout.
        block0.read_outputs()
        block1.read_outputs()
        block2.read_outputs()
        block3.read_outputs()

        dcCmd = dcCommand

        servoCmd = abs(servoCommand.send(currentTime))

        # loop through stepper sequence
        counter = counter + 1
        if counter == 4:
            stepCounter = stepCounter + 1
            counter = 0
        stepperCmd = stepper[stepCounter % len(stepper)] * stepperAmplitude

        cntr2s = cntr2s + 1
        # code running once a second
        if cntr2s == frequency:

            print(f'motor speed block 0: {block0.tach:.2f} counts/s    '
                  f'motor speed block 1: {block1.tach:.2f} counts/s    '
                  f'motor speed block 2: {block2.tach:.2f} counts/s    '
                  f'motor speed block 3: {block3.tach:.2f} counts/s')

            cntr2s = 0


        # update motor per block
        block0.update_dc(dcCmd, limitCmd=False)
        block1.update_dc(dcCmd, limitCmd=False)
        block2.update_dc(dcCmd, limitCmd=False)
        block3.update_dc(dcCmd, limitCmd=False)

        block0.update_servo(servoCmd)
        block1.update_servo(servoCmd)
        block2.update_servo(servoCmd)
        block3.update_servo(servoCmd)

        block0.update_stepper(stepperCmd)
        block1.update_stepper(stepperCmd)
        block2.update_stepper(stepperCmd)
        block3.update_stepper(stepperCmd)

        block0.update_bldc_sensorless(bldcAmplitude)
        block1.update_bldc_sensorless(bldcAmplitude)
        block2.update_bldc_sensorless(bldcAmplitude)
        block3.update_bldc_sensorless(bldcAmplitude)

        # write motor commands to all blocks
        block0.write_motors()
        block1.write_motors()
        block2.write_motors()
        block3.write_motors()

        timer.sleep()
