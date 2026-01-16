# Encoder 

# Understanding encoder values and the driving signals for it.

# region: Python level imports
from threading import Thread
import time 
import signal 

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import MultiScope
# endregion 


# region: Experiment constants
simulationTime = 500 # will run for this amount of seconds
frequency = 300 # Hz
window = 10

counter = 0 # counter to track scopes
counterHalfSec = 0
#endregion

#region: Scope setup
scope = MultiScope(
    rows= 2, 
    cols =1,
    title='Encoder Signals',
    fps=60 
)

# Distance scope
scope.addAxis(
    row=0,
    col=0,
    timeWindow=window,
    yLabel='Pulse',
    yLim=(0, 1)
)
scope.axes[0].attachSignal(name = 'Channel A', color = [255,100,100], width = 2)
scope.axes[0].attachSignal(name = 'Channel B', color = [100,240,240], width = 2)

scope.addAxis(
    row=1,
    col=0,
    timeWindow=window,
    yLabel='Counts'
)
scope.axes[1].attachSignal(name='Counts', color =[200,200,200])

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
    with SensorsTrainer(knobEncQuad=1) as sensors:
        counter = 0 
        counterHalfSec = 0 
        
        while timer.check() and not KILL_THREAD:
            
            currentTime = timer.get_current_time()

            sensors.read_outputs()

            encoder = sensors.encoder0
            encoderPulses = sensors.encoderPulses
            
            # update scopes every 4 samples
            if counter%4 == 0:
                scope.axes[0].sample(currentTime, [encoderPulses[0],
                                                   encoderPulses[1]])
                scope.axes[1].sample(currentTime, encoder)
                
            # Output encoder counts and angle every half second 
            if counterHalfSec%150 == 0:  # half of the frequency will give us half a second.
                countsPerRev = 0 
                
                
            counter += 1
            counterHalfSec += 1
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





