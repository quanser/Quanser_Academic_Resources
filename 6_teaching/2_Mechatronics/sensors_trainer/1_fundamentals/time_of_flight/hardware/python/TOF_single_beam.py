#TOF_single_beam.py
# This script reads Time-of-Flight (TOF) sensor data from a Sensors Trainer
# and plots the distance, sigma, and reflectance of a single beam over time using MultiScope.

# region: Python level imports
import numpy as np
from threading import Thread
import time
import signal

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import MultiScope
# endregion


# region: Experiment constants

simulationTime = 60 # will run for this amount of seconds
frequency =  300 #Hz
window = simulationTime/6
counter = 0 # counter to track scopes

# perform correction
sample_flat_surface = np.zeros((8,8,3), dtype=np.float64)

# Define scope
scope = MultiScope(rows= 3, cols =1,
            title='Time of Flight measurement',
            fps=60 )

# Distance scope
scope.addAxis(row=0,
            col=0,
            timeWindow=window,
            yLabel='Distance (m)',
            yLim=(0, 0.6))
scope.axes[0].attachSignal(name='distance meas (m)')

# Sigma scope
scope.addAxis(row=1,
            col=0,
            timeWindow=window,
            yLabel='sigma (m)',
            yLim=(-0.02, 0.02))
scope.axes[1].attachSignal(name='sigma (m)')

# Reflectance scope
scope.addAxis(row=2,
            col=0,
            timeWindow=window,
            yLabel='Reflectance (%)',
            yLim=(0, 0.005))
scope.axes[2].attachSignal(name='Reflectance (%)')

# endregion

# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

# region: Main Loop
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

def control_loop():
    with SensorsTrainer() as sensors:
        while timer.check() and not KILL_THREAD:
            currentTime = timer.get_current_time()
            sensors.read_outputs()

            TOFSensor = sensors.TOFDistance

            ToFMeasurements = np.flip((TOFSensor * sensors.TOFNumberOfTargets).reshape(8,8), axis=0)

            ReflectanceSquare = np.flip(sensors.TOFReflectance.reshape(8,8), axis=0)
            SigmaSquare = np.flip(sensors.TOFSigma.reshape(8,8), axis=0)

            single_beam_distance = ToFMeasurements[3,3]
            single_beam_reflectance = ReflectanceSquare[3,3]
            single_beam_sigma = SigmaSquare[3,3]

            scope.axes[0].sample(currentTime, single_beam_distance)
            scope.axes[1].sample(currentTime, single_beam_sigma)
            scope.axes[2].sample(currentTime, single_beam_reflectance)

            timer.sleep()

thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    MultiScope.refreshAll()

    time.sleep(0.01)

input('Press the enter key to exit.')

# endregion







