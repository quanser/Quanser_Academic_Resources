# BLDC - bldc

# Learning to drive a BLDC motor

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

          #phases A, B, C
bldc = np.array([[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]])

bldcAmplitude = 0.15
# endregion

# region: Main Loop
with ActuatorsTrainer(block = 2) as actuators:
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)

    actuators.enable_motors()
    while timer.check():

        actuators.read_outputs()

        hallSensors = actuators.hallSensor

        # convert from binary to decimal
        hallState = 0


        #commands based on hall sensors.
        match hallState:
            case 1:
                bldcCmd = 0
            case 2:
                bldcCmd = 0
            case 3:
                bldcCmd = 0
            case 4:
                bldcCmd = 0
            case 5:
                bldcCmd = 0
            case 6:
                bldcCmd = 0
            case _:
                bldcCmd = [0, 0, 0]

        # enable high and low motors, disable floating one
        enablePhase = 0

        # Command only high phase, make sure to decrease the amplitude of the signal
        commandToPhase = 0

        #make sure command is never outside the 0-1 range
        commandToPhase = np.clip(commandToPhase, 0, 1)

        cntr1s = cntr1s + 1
        cntr3s = cntr3s + 1

        # code running once a second
        if cntr1s == frequency:
            rads = 0
            rpm = 0
            print(f'motor speed: {actuators.tach:.2f} counts/s    {rads:.2f} rad/s    {rpm:.1f} rpm')
            cntr1s = 0

        # code running every 3 second
        if cntr3s == frequency*3:
            # add your code here
            cntr3s = 0

        actuators.enable_bldc(enablePhase)
        actuators.update_bldc(commandToPhase)
        actuators.write_motors()

        timer.sleep()

# endregion