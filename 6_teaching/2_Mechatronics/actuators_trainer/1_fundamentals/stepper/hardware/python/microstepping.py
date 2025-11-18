import numpy as np
from pal.utilities.timing import Timer
from pal.products.actuators import ActuatorsTrainer
from pal.utilities.math import SignalGenerator


simulationTime = 30 # will run for this amount of seconds
frequency = 500 # Hz 

timer = Timer(sampleRate=frequency, totalTime=simulationTime)

cntr4s = 0

stepperAmplitude = 0.5
angularFrequency = 30  
sineWave = SignalGenerator().sine(stepperAmplitude, angularFrequency)
cosineWave = SignalGenerator().cosine(stepperAmplitude, angularFrequency)
next(sineWave)
next(cosineWave)

forward = True
with ActuatorsTrainer(block = 3) as actuators:

    actuators.enable_motors()
    timer._restart()
    while timer.check():

        actuators.read_outputs()

        sine = sineWave.send(timer.get_current_time())
        cosine = cosineWave.send(timer.get_current_time())
        
        # update variables using the sine and cosine values.
        a_plus = 0
        a_minus = 0
        b_plus = 0
        b_minus = 0

        cntr4s = cntr4s + 1

        if cntr4s == frequency*4:
            # forward = not forward
            cntr4s = 0

        if forward:
            actuators.update_stepper([a_plus, a_minus, b_minus, b_plus])
        else:
            pass # do something

        actuators.write_motors()
        timer.sleep()
