# Color Sensor Reading and LED Control
# In this section of the experiment, we read color sensor data while controlling the
# LED color using OpenCV sliders. The sensor data is visualized using PAL Probe.

# region: Python level imports
import numpy as np
import subprocess
import cv2
import os
import sys

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer
from pal.utilities.probe import Probe
from visualizer import ColorDisplay
# endregion

# region: define main loop function
def main():
    totalTime = 50 # will run for this amount of seconds
    sampleRate = 20 # Max sample rate of the color sensor is 20 Hz
    sourceColor = np.zeros((400, 400, 3), dtype=np.uint8) 

    # set up probe to show data
    probe = Probe(ip = 'localhost')
    probe.add_scope(numSignals=5, name='Color Sensor')
    subprocess.Popen(
    [sys.executable, 
     os.path.join(os.path.dirname(__file__), 'observer_sensor.py')],
    cwd=os.path.dirname(__file__))
    while not probe.connected:
        probe.check_connection()

    # set up display and slider for LED color
    ledDisplay = ColorDisplay("LED Control")
    with SensorsTrainer() as sensors:
        ledDisplay.set_tracker()
        timer = Timer(sampleRate=sampleRate, totalTime=totalTime)
        count = 0
        while timer.check():
            
            # Get LED rbg values from slider
            rValue,gValue,bValue = ledDisplay.get_tracker()
            # gValue = rValue

            sourceColor[:] = (bValue, gValue, rValue)  # OpenCV uses BGR format
            cv2.imshow("LED Control", sourceColor)

            # Write LED color to Sensor Trainer (normalize to [0,1])
            rgb=np.array((rValue,gValue,bValue))/255
            sensors.write_leds(rgb=rgb)

            # Read color sensor data and send to probe for visualization
            sensors.read_outputs()
            currentTime = timer.get_current_time()
            rgbc = np.hstack((sensors.colorRGB,sensors.colorClear))
            print(f" Color Sensor RGBC: {rgbc}")
            # print(f"RGB to clear ratio: {sensors.colorRGB / sensors.colorClear}")

            if count % 2 == 0: # send data at 10 Hz
                probe.send(name='Color Sensor',
                            scopeData=(currentTime, rgbc[[0,3,1,2]]))
            count += 1
            timer.sleep()
            
            # # Estimated color
            # rawRGBEstimate = np.zeros((200,200,3))
            # rawRGBEstimate[:,:,:] = sensors.colorRGB[[2,1,0]]
            # colorRatioEstimate = np.zeros((200,200,3))
            # colorRatio = sensors.colorRGB / sensors.colorClear
            # colorRatio = np.clip(colorRatio, 0, 1)
            # colorRatioEstimate[:,:,:] = colorRatio[[2,1,0]]
            # combinedEstimate = np.hstack((rawRGBEstimate, colorRatioEstimate))
            # cv2.imshow("Color Estimate", combinedEstimate)

            cv2.waitKey(1)
    cv2.destroyAllWindows()
# endregion

# region: run main function
if __name__ == "__main__":
    main()
# endregion
input("Press Enter to exit...")



