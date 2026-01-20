# Stepper 

# Understanding stepper motor drive modes.

# region: Python level imports
import numpy as np
from pal.utilities.timing import Timer
from pal.products.actuators import ActuatorsTrainer
# endregion 


# region: Experiment constants
simulationTime = 90 # will run for this amount of seconds
frequency = 300 # Hz

cntr4s = 0
loopCounter = 0
stepperFwd = True

                       # a+ a- b+ b-
waveDrive =   np.array([[0, 0, 0, 0],  
                        [0, 0, 0, 0],  
                        [0, 0, 0, 0],  
                        [0, 0, 0, 0]]) 

                         # a+ a- b+ b-
fullStepDrive = np.array([[0, 0, 0, 0],  
                          [0, 0, 0, 0],  
                          [0, 0, 0, 0],  
                          [0, 0, 0, 0]]) 

                         # a+ a- b+ b-
halfStepDrive = np.array([[0, 0, 0, 0], 
                          [0, 0, 0, 0], 
                          [0, 0, 0, 0], 
                          [0, 0, 0, 0], 
                          [0, 0, 0, 0], 
                          [0, 0, 0, 0],  
                          [0, 0, 0, 0],  
                          [0, 0, 0, 0],
                          [0, 0, 0, 0]]) 


stepperAmplitude = 0.3 # 12V * 0.3 = 3.6 V
stepsPerSecond = 10

nextStep = 1
stepCounter = 0
# endregion

# region: Main Loop
with ActuatorsTrainer(block = 2) as actuators:
    timer = Timer(sampleRate=frequency, totalTime=simulationTime)

    actuators.enable_motors()
    while timer.check():

        actuators.read_outputs()

        loopCounter = loopCounter + 1  
        cntr4s = cntr4s + 1

        if loopCounter == nextStep:
            stepCounter = stepCounter + 1 
            loopCounter = 0

        if cntr4s == frequency*4:
            
            cntr4s = 0
    
        cmd = waveDrive[0] * stepperAmplitude
        #cmd = fullStepDrive[0] * stepperAmplitude
        #cmd = halfStepDrive[0] * stepperAmplitude

        actuators.update_stepper(cmd)
        actuators.write_motors()

        timer.sleep()
# endregion
