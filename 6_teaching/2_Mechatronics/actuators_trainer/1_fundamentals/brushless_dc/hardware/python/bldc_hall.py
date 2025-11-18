import numpy as np
from pal.utilities.timing import Timer
from pal.products.actuators import ActuatorsTrainer

simulationTime = 30 # will run for this amount of seconds
frequency = 60 # Hz
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

cntr1s = 0
cntr3s = 0

bldc = np.array([[1, 0, 0], # enable A
                 [0, 1, 0], # enable B
                 [0, 0, 1]]) # enable C

bldcAmplitude = 0.1

bldcCmd = bldc[0]
index = 0

with ActuatorsTrainer(block = 2) as actuators:

    actuators.enable_motors()
    while timer.check():

        actuators.read_outputs()

        # hall sensors [1, 2, 3]
        hallSensors = actuators.hallSensor

        cntr1s = cntr1s + 1
        cntr3s = cntr3s + 1

        # once a second, print the hall effect sensor reading
        if cntr1s == frequency:
            print(f'BLDC cmd: {bldcCmd}   Hall Sensors out: {hallSensors}')
            cntr1s = 0

        # change active coil every 3 seconds
        if cntr3s == frequency*3:
            index = index + 1
            bldcCmd = bldc[index%3]
            cntr3s = 0
            

        encoderCounts = actuators.encoder

        actuators.enable_bldc([1, 1, 1])
        actuators.update_bldc(bldcCmd*bldcAmplitude)
        actuators.write_motors()

        timer.sleep()

print(f'Encoder Counts: {encoderCounts}')



