# Stepper - microstepping

# Understanding microstepping with sine waves.

# region: Python level imports
from pal.utilities.timing import Timer
from pal.products.actuators import ActuatorsTrainer
from pal.utilities.math import SignalGenerator
# endregion 

# region: Experiment constants

simulationTime = 30 # will run for this amount of seconds
frequency = 500 # Hz # keep same angular frequency/speed, but change frequency
# at 30rad/s, 200Hz gives 41 samples per period
# at 400Hz it gives 83 and at 60, it gives 10
cntr4s = 0

stepperAmplitude = 0.5
angularFrequency = 30 # up to 380 at 500 HZ for 8 samples per period
# samples per period = 2pi/(angularFrequency*sampleTime) or # samples per period = 2pi* frequency /(angularFrequency)
sineWave = SignalGenerator().sine(stepperAmplitude, angularFrequency)
cosineWave = SignalGenerator().cosine(stepperAmplitude, angularFrequency)
next(sineWave)
next(cosineWave)

# endregion


# region: Main Loop
forward = True
with ActuatorsTrainer(block = 2) as actuators:

    timer = Timer(sampleRate=frequency, totalTime=simulationTime)
    
    actuators.enable_motors()

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
            # do something
            cntr4s = 0

        if forward:
            actuators.update_stepper([a_plus, a_minus, b_minus, b_plus])
        else:
            pass # do something

        actuators.write_motors()
        timer.sleep()
# endregion