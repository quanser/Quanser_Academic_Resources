# ultrasonic_single_distance.py
# This script runs the ultrasonic sensor on distance mode
# 

# region: Python level imports
from threading import Thread
import signal 
import time 

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.scope import MultiScope
# endregion


# Setup to enable killing the data generation thread using keyboard interrupts
global KILL_THREAD
KILL_THREAD = False
def sig_handler(*args):
    global KILL_THREAD
    KILL_THREAD = True
signal.signal(signal.SIGINT, sig_handler)

# region: Experiment constants
simulationTime = 300 # will run for this amount of seconds
frequency =  100 #Hz
window = 10
counter = 0 # counter to track scopes

ultraDistanceMin = 0
ultraDistanceMax = 5

# endregion

# Define scope to display measured distance 
scope = MultiScope(rows=1, cols =1,
            title='Ultrasonic Sensor Measurement',
            fps=60 )

scope.addAxis(row=0,
            col=0,
            timeWindow=window,
            yLabel='Distance (m)',
            yLim=(ultraDistanceMin, ultraDistanceMax + 0.2))

scope.axes[0].attachSignal(name='Distance (m)', 
                           color=[255,100,100])
scope.axes[0].attachSignal(name='Range start', 
                           color=[0, 100, 0])
scope.axes[0].attachSignal(name='Range end',
                           color=[80, 255, 80])


timer = Timer(sampleRate=frequency, totalTime=simulationTime)
# endregion

# region:  Main Loop
def control_loop():
    with SensorsTrainer(ultraService=1, ultraStart = ultraDistanceMin, ultraLength=ultraDistanceMax-ultraDistanceMin) as sensors:
        sampleCounter = 0
        
        while timer.check() and not KILL_THREAD:
            currentTime = timer.get_current_time()

            sensors.read_outputs()
            ultraDistanceData = sensors.ultraDistance
            
            # print to terminal every 0.5 s
            if sampleCounter%50 == 0:
                print(f'Ultrasonic reading: {ultraDistanceData}')

            scope.axes[0].sample(currentTime,[ultraDistanceData, ultraDistanceMin, ultraDistanceMax])
            
            sampleCounter += 1
            timer.sleep()

thread = Thread(target=control_loop)
thread.start()

while thread.is_alive() and (not KILL_THREAD):

    # This must be called regularly or the scope windows will freeze
    # Must be called in the main thread.
    MultiScope.refreshAll()

    time.sleep(0.01)

input("Press any key to terminate the experiment\n")

# endregion