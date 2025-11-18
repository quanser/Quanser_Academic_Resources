# Load Cell Calibration
# In this section of the experiment, you will calibrate the load cell by placing 
# known weights. You will record the load cell voltage readings for each weight and
# perform a linear fit to determine the calibration coefficients that map voltage
# readings to actual weights.

# region: Python level imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
import numpy as np
import matplotlib.pyplot as plt
# endregion 

# region: set up experiment parameters
frequency = 1000 # Hz
recordedData=[]
# endregion 

# region: define helper functions
def process(sensors,weightTime,frequency):
    '''
    Process load cell data for a given weight.
    Args:
        sensors: SensorsTrainer object
        weightTime: time to record data for this weight (seconds)
        frequency: sampling frequency (Hz)
    Returns:
        mean_voltage: mean load cell voltage for this weight
    '''

    duration = weightTime # seconds
    timer = Timer(sampleRate=frequency, totalTime=duration)
    sensorDataBuffer = np.zeros(int(frequency*duration)) 
    counter = 0
    while timer.check():
        sensors.read_outputs()
        loadCell = sensors.loadCell
        # --- complete function here ---

        # ---------------------
        timer.sleep()

def calibrate(recordedData):
    '''
    Calibrate load cell using recorded data.
    Args:
        recordedData: list of tuples (weight, mean_voltage)
    Returns:
        coefficients: calibration coefficients [slope, intercept]
    '''
    # --- complete function here --- 
    coefficients = [0,0]

    # ---------------------
    print(f"Calibration complete. Calibration coefficients: {coefficients}")
    return coefficients    
# endregion 

# region: main calibration loop
with SensorsTrainer() as sensors:
    while True:
        weight = input(f"Enter the weight of the item on load cell and press enter to continue (Enter q to quit):")
        if not weight or weight.lower() == 'q':
            break
        mean_voltage = process(sensors,frequency)
        print(mean_voltage)
        recordedData.append((weight, mean_voltage))
    calibrate(recordedData)
# endregion
input ("Press Enter to exit...")