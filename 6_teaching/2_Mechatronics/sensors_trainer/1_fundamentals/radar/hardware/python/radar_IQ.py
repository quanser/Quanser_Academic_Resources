# Radar IQ Mode Experiment
# In this script, the sensor trainer is configure to run the Radar sensor in 
# "IQ" mode, and the received data will be plotted and displayed. Simple processing
# and filtering techniques will also be implemented in this script.

# region: Python level imports
from threading import Thread
import signal
import time
import numpy as np
from pal.utilities.scope import BatchScope
from pal.products.sensors import SensorsTrainer
from pal.utilities.timing import Timer
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

def unwarp(phase):
    """Unwrap phase signals such that thye are not bounded between -pi to pi.
    args:
        phase_array: phase array bounded between -pi to pi.
    returns:
        unwrapped: numpy array of unwrapped phase array.
    """
    unwrapped = np.zeros_like(phase, dtype=float)
    unwrapped[0] = phase[0]
    offset = 0.0
    for i in range(1, len(phase)):
        diff = phase[i] - phase[i - 1]
        # Detect wrap-around discontinuities and adjust offset based on the 
        # direction of the jump
        if diff > 3:
            offset -= 2 * np.pi
        elif diff < -3:
            offset += 2 * np.pi
        unwrapped[i] = phase[i] + offset
    return unwrapped

class ExpSmoother:
    def __init__(self, alpha=0.7):
        self.alpha = alpha
        self.prev = None
    def update(self, x):
        # ---------- complete your task here -------------
        self.prev = x
        #-------------------------------------------------
        return self.prev
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
# set up exponential smoothing filter
smootherI = ExpSmoother(alpha=0.7)
smootherQ = ExpSmoother(alpha=0.7)
# setup displays
scopeIQ = BatchScope(title="Radar IQ", 
                   arrayLen=800, 
                   yLim=(-0.1, 0.1),
                   xLim=(radarStart-0.1, radarLength+radarStart+0.1),
                   xLabel = 'Distance',
                   yLabel='Amplitude', 
                   fps=10)
scopeIQ.attachSignal(name="In-phase")
scopeIQ.attachSignal(name="Quandrature")
# scopeAmp = BatchScope(title="Radar Amplitude", 
#                    arrayLen=800, 
#                    yLim=(0, 0.05),
#                    xLim=(radarStart-0.1, radarLength+radarStart+0.1),
#                    xLabel = 'Distance',
#                    yLabel='Amplitude |IQ|', 
#                    fps=10)
# scopeAmp.attachSignal(name="Amplitude |IQ|")
# scopePhase = BatchScope(title="Radar Phase", 
#                    arrayLen=800, 
#                    yLim=(-np.pi, 5*np.pi),
#                    xLim=(radarStart-0.1, radarLength+radarStart+0.1),
#                    xLabel = 'Distance',
#                    yLabel='Raw Phase (angle IQ)', 
#                    fps=10)
# scopePhase.attachSignal(name="Phase (angle IQ)")
# scopePhase.attachSignal(name="Unwrapped Phase (angle IQ)")
#endregion

# region: define and start main radar loop
def control_loop():
    with SensorsTrainer(radarService=5, radarStart=radarStart, radarLength=radarLength) as sensors:     
        count = 0
        # set up plotting buffers
        radarDistScope = np.zeros(800, dtype=np.float32)
        amplitude = np.zeros(800, dtype=np.float32)
        phase = np.zeros(800, dtype=np.float32)
        while timer.check() and not KILL_THREAD:
            sensors.read_outputs()
            radarPoints = int(sensors.radarPoints)
            # idle until radar receive enough data points
            if radarPoints > 800:
                radarDist = sensors.radarDistances[:radarPoints]                
                radarIRaw = sensors.radarAmplitudes[:2*radarPoints-1:2]
                radarQRaw = sensors.radarAmplitudes[1:2*radarPoints:2]
                
                # IQ processing
                radarI = smootherI.update(radarIRaw)
                radarQ = smootherQ.update(radarQRaw)
                # ---------- complete your task here -------------
                amplitude = np.zeros_like(radarI)
                phase = np.zeros_like(radarI)
                # ------------------------------------------------
                unwrapPhase=unwarp(phase)

            else:
                print("Waiting for radar data...")

            # plot to scopes
            count += 1
            if count%10 == 0:
                radarDistScope = resample_data(radarDist, targetLength=800)
                radarIScope = resample_data(radarI, targetLength=800)
                radarQScope = resample_data(radarQ, targetLength=800)
                scopeIQ.sample((radarDistScope, [radarIScope,radarQScope]))

                # ampScope = resample_data(amplitude, targetLength=800)
                # phaseScope = resample_data(phase, targetLength=800)
                # unwrapPhaseScope = resample_data(unwrapPhase, targetLength=800)
                # scopeAmp.sample((radarDistScope, [ampScope]))
                # scopePhase.sample((radarDistScope, [phaseScope,unwrapPhaseScope]))
            timer.sleep()
# Setup data generation thread and run until complete
thread = Thread(target=control_loop)
thread.start()
while thread.is_alive():# and (not KILL_THREAD):
    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    scopeIQ.refresh()
    # scopeAmp.refresh()
    # scopePhase.refresh()
    time.sleep(0.01)
#endregion
input('Press the enter key to exit.')
