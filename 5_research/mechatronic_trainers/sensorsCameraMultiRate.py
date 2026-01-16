# sensorsCameraMultiRate.py
# This script demonstrates how to read from the Mechatronic Sensors Trainer's
# sensors and camera at different rates, displaying sensor data on scopes
# while capturing camera images at a specified frame rate.

# region: system imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsCamera
from pal.utilities.scope import MultiScope
import cv2
# endregion

#Make sure to set frequency to a value higher than all individual rates
frequency = 200  # Hz

simulationTime = 150  # seconds

# Set up fps for the scope updates. Get counts needed to run at that rate.
scopeRefreshRate = 30
scopeCounts = int(round(frequency / scopeRefreshRate))

scope = MultiScope(rows= 1, cols = 2,
            title='Sensors Data',
            fps=scopeRefreshRate)

# Voltage scope
window = 10
scope.addAxis(row=0,
            col=0,
            timeWindow=window,
            yLabel='Voltage of IR Distance Sensor (V)',
            yLim=(0, 3.3))
scope.axes[0].attachSignal(name='voltage')

scope.addAxis(row=0,
            col=1,
            timeWindow=window,
            title = "IR Distance",
            yLabel='Temperature of Weather Sensor (°C)',
            yLim=(15, 35))
scope.axes[1].attachSignal(name='temp')


# Set up fps for the camera and different sensors.
# Get counts needed to run at that rate.

frameRate = 30  # Camera frame rate in Hz
CameraCounts = int(round(frequency / frameRate))

irRate = 75 # IR Distance print rate in Hz
IRCounts = int(round(frequency / irRate))

tempRate = 3 # temperature print rate in Hz
tempCounts = int(round(frequency / tempRate))

counter = 0


# region: experiment
timer = Timer(sampleRate=frequency, totalTime=simulationTime)

# initialize sensors trainer and its camera
with (SensorsTrainer() as sensors,
      SensorsCamera(frameRate=frameRate,
                    cameraID=0) as camera): # Camera ID may need to be 1 if your computer has a webcam

    while timer.check():
        currentTime = timer.get_current_time()
        sensors.read_outputs()

        infrared = sensors.IRDistance
        temperature = sensors.tempWeather

        if counter%CameraCounts == 0:
            frame = camera.read()
            if frame:
                image = camera.imageData
                cv2.imshow("Color Image", image)
                cv2.waitKey(1)

        if counter%IRCounts == 0:
            # print(f"Time: {currentTime:.2f} s | IR Distance Measurement: {infrared:.3f} V")
            scope.axes[0].sample(currentTime, infrared)

        if counter%tempCounts == 0:
            # print(f"Time: {currentTime:.2f} s | Temperature: {infrared:.1f} °C")
            scope.axes[1].sample(currentTime, temperature)

        if counter%scopeCounts == 0:
            MultiScope.refreshAll()

        counter += 1

        timer.sleep()

input("Press Enter to exit...")
# endregion