# ultrasonic_IQ.py
# This script runs the ultrasonic sensor on IQ mode 
# 

# region: Python level imports
from threading import Thread
import numpy as np
import signal 
import time 

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import BatchScope
# endregion

# region: helper function
def resample_data(inputData, targetLength=800):
    """Resample data to target length using interpolation.
    args:
        inputData:  numpy array of data to be resampled.
        targetLength: desired length for the target data.
    returns:
        outputData: numpy array of resampled data in desired length.
    """
    currentLength = len(inputData)
    if currentLength == targetLength:
        outputData = inputData
    else:
        outputData = np.interp(np.linspace(0, currentLength-1, targetLength),
                         np.arange(currentLength),
                         inputData)
    return outputData


# region: set up experiment parameters

# setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

# experiment constants
simulationTime = 600 # will run for 10 seconds
frequency = 100 # Hz
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
ultraMin = 0
ultraMax = 5
dataLength = 340


# set up display scopes
scopeIQ = BatchScope(title="Ultrasonic IQ", 
                    arrayLen=dataLength, 
                   yLim=(-0.5, 0.5),
                   xLim=(ultraMin-0.1, ultraMax+0.1),
                   xLabel = 'Distance',
                   yLabel='Amplitude', 
                   fps=10)
scopeIQ.attachSignal(name="In-phase")
scopeIQ.attachSignal(name="Quadrature")


# region: define and start main ultrasonic loop
def control_loop():
    with SensorsTrainer(ultraService=2, ultraStart= 0, ultraLength= 5) as sensors:     
        sampleCounter = 0

        while timer.check() and not KILL_THREAD:

            # update readings
            sensors.read_outputs()
            ultraPoints = int(sensors.ultraPoints)

            # idle until enough ultrasonic data points are received 
            if ultraPoints > 100:

                # init
                ultraIQDist = sensors.ultraIQDistances[:ultraPoints]                
                ultraIRaw = sensors.ultraIQAmplitudes[:2*ultraPoints-1:2]
                ultraQRaw = sensors.ultraIQAmplitudes[1:2*ultraPoints:2]
                
                # resample data to match array length of scopes
                ultraIQDistResample = resample_data(ultraIQDist, targetLength=dataLength)
                ultraIResample = resample_data(ultraIRaw, targetLength=dataLength)
                ultraQResample = resample_data(ultraQRaw, targetLength=dataLength)
                
                if sampleCounter % 10 == 0:
                    # send data to scopes
                    scopeIQ.sample((ultraIQDistResample, [ultraIResample, 
                                                          ultraQResample]))
                    

                sampleCounter+=1

            else:
                print("Waiting for ultrasonic data...")

            
            timer.sleep()

# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()
while thread.is_alive() and not KILL_THREAD:
    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    scopeIQ.refresh()

    
    time.sleep(0.01)
#endregion
input('Press the enter key to exit.')