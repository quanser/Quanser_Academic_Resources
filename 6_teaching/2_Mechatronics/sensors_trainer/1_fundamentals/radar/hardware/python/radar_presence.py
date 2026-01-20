# Radar presence detector
# In this script, you will use the radar in "envelope" mode to determine whether
# there is object present in the environemnt.

# region: Python level imports
from threading import Thread
import signal
import time
import numpy as np
from pal.utilities.scope import BatchScope
from pal.products.sensors import SensorsTrainer
from pal.utilities.timing import Timer
# endregion 

# region: set up experiment parameters
# setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)
# setup parameters
simulationTime = 1000 # will run for 10 seconds
frequency = 100 # Hz
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
radarStart = 0.2
radarLength = 1
# setup display
scope = BatchScope(title="Radar Envelope", 
                   arrayLen=800, 
                   yLim=(0, 0.2),
                   xLim=(radarStart-0.1, radarLength+radarStart+0.1),
                   xLabel = 'Distance',
                   yLabel='Amplitude', 
                   fps=10)
scope.attachSignal(name="Radar Data")
#endregion

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

def presence_detect(distance, amplitude, range=(0.4,0.5)):    
    """A presence detector for specified distance range.
    args:
        distance:  numpy array of distance bins.
        amplitude: numpy array of radar signal amplitude at each distance bin.
        range: tuple of low and high ends of the detection range (low, high).
    returns:
        presenceDetected: whether there is a object present in specified range (bool).
    """
    # ---------- complete your task here -------------
    presenceDetected = False
    # ------------------------------------------------
    return presenceDetected
#endregion

# region: define and start main radar loop
def radar_loop():
    with SensorsTrainer(radarService=4, radarStart=radarStart, radarLength=radarLength) as sensors:
        count = 0
        # set up plotting buffers
        radarDistScope = np.zeros(800, dtype=np.float32)
        radarAmplScope = np.zeros(800, dtype=np.float32)
        while timer.check() and not KILL_THREAD:
            sensors.read_outputs()
            radarPoints = int(sensors.radarPoints)
            # idle until radar receive enough data points
            if radarPoints > 800:
                radarDist = sensors.radarDistances[:radarPoints]
                radarAmpl = sensors.radarAmplitudes[:radarPoints]
                presence = presence_detect(radarDist,radarAmpl)
                print(f"presences detected: {presence}",'\x1b[7l',end='\r',flush=True)
            else:
                print("Waiting for radar data...")
            # plot to scopes
            count += 1
            if count%10 == 0:
                radarDistScope = resample_data(radarDist, targetLength=800)
                radarAmplScope = resample_data(radarAmpl, targetLength=800)
                scope.sample((radarDistScope, [radarAmplScope]))
            timer.sleep()        
# Setup main radar thread and run until complete
thread = Thread(target=radar_loop)
thread.start()
while thread.is_alive() and (not KILL_THREAD):
    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    scope.refresh()
    time.sleep(0.01)
#endregion
input('Press the enter key to exit.')
