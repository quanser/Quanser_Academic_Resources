# Color Mathcing using linear fitting
# In this section of the experimen, we will perform color matching using linear regression
# to compute the color matching matrix and bias vector that maps sensor readings to sRGB values.

# region: Python level imports
import numpy as np
import cv2
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
# endregion

# region: experiment parameters setup
simulationTime = 60 # will run for this amount of seconds
frequency = 20 # Hz
screenColors = [  
    (  0,  0,  0),
    (  0,  0,  0),
    (  0,  0,  0)
]
N=len(screenColors)
sensorBuffer = np.zeros((100,3))
#end region

# region: main data collection loop
def main():
    with SensorsTrainer() as sensors:

        sourceColor = np.zeros((600, 600, 3), dtype=np.uint8)
        results = [] # to store (target color, sensor reading) tuples for linear fitting
        
        cv2.imshow('Solid Color', sourceColor)
        input('press the sensor against the Solid Color window and press Enter to start calibration...')
        timer = Timer(sampleRate=frequency, totalTime=simulationTime)
        count = 0
        while timer.check():
            
            # set source color from predefined list
            sourceColor[:] = screenColors[(count//100)%N]  # OpenCV uses BGR format
            cv2.imshow('Solid Color', sourceColor)

            # read color sensor data
            sensors.read_outputs()
            print(f"Screen Color: {screenColors[(count//100)%N]}, Sensor Reading: {sensors.colorRGB}")
            sensorBuffer[count%100,:] = sensors.colorRGB

            # every 100 samples, average the last 50 samples and store the result
            if (count+1)%100==0:
                avg_reading = np.mean(sensorBuffer[50:],axis=0)
                results.append((screenColors[(count//100)%N],avg_reading))
            count +=1
            
            # stop after collecting N color samples
            if count>=N*100:
                break
            cv2.waitKey(1)
            timer.sleep()

    linear_fit(results)
    cv2.destroyAllWindows()
# end region

# region: compute color matching matrix
def linear_fit(results):
    """Perform linear fitting to find color matching matrix M that maps sensor 
       readings to sRGB values.
    args:
        results: list of tuples (target_color, sensor_reading)
    returns:
        M: 3x3 color matching matrix
    """
    # arrange collected data into matrices for linear fitting
    S = np.zeros((N,3))
    T = np.zeros((N,3))
    # --- Complete your task here ---
    for i,result in enumerate(results):
        pass
    
    M = np.zeros((3,3))
    #----------------------------

    print(f'color matching matrix M:\n{M}')
# endregion

# region: run main function
if __name__=="__main__":
    main()
# endregion
input("Press Enter to exit...")



