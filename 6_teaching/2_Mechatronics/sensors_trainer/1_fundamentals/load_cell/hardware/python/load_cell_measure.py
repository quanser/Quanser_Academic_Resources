# Load Cell Weight Measurement
# This section of the code reads load cell data from the Sensors Trainer,
# applies a moving average filter, and computes the weight using a linear calibration.

# region: Python level imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from collections import deque
# endregion 

# region: set up experiment parameters
frequency = 1000 # Hz
simulationTime = 300 # Second
coefficients  = [0, 0] # fill in with calibration coefficients [slope, intercept]
buffer = deque([],maxlen=100) # buffer to store last 100 samples for moving average
timer = Timer(sampleRate=frequency, totalTime=simulationTime)
# endregion 

# region: main measuring loop
with SensorsTrainer() as sensors:
    while timer.check():
        sensors.read_outputs()
        loadCell = sensors.loadCell
        # --- complete function here ---
        weight = 0
        # ---------------------
        print(f" Weight: {weight:.2f} g   ", end='\r', flush=True)
        timer.sleep()
# endregion 
input ("Press Enter to exit...")