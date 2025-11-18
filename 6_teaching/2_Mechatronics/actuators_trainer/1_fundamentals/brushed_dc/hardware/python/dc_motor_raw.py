from pal.products.actuators import ActuatorsTrainer
from pal.utilities.timing import Timer

frequency = 120 # Hz
simulationTime = 5 # seconds

# Initialize timer
timer = Timer(frequency, simulationTime)

with ActuatorsTrainer(block = 2) as actuators:
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
