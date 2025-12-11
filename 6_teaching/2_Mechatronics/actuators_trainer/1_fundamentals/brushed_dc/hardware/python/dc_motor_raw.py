# DC Motor - raw signals 

# Understanding how DC motors get driven.

# region: Python level imports
from pal.products.actuators import ActuatorsTrainer
from pal.utilities.timing import Timer
# endregion 

# region: Experiment constants
frequency = 120 # Hz
simulationTime = 5 # seconds
# endregion

# region: Main Loop
with ActuatorsTrainer(block = 2) as actuators:
    timer = Timer(frequency, simulationTime)

    actuators.enable_motors()

    while timer.check():

        # Get current timestamp and read data from encoder & tach
        currentTime = timer.get_current_time()
        actuators.read_outputs()

        # The update_dc function accepts commands from -1 to 1 that
        # map to -12 to 12 V. This is the conversion.
        actuators.update_dc_individual(left=0.0, right=0.0)
        actuators.write_motors()

        timer.sleep()
    
#endregion
