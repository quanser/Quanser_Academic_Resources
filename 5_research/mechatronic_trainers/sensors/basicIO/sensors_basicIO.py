# sensors_basicIO.py
# This example demonstrates how to read and visualize data from the 
# various sensors on the Sensors Trainer. 
# It sets up scopes for different categories of sensors and updates 
# them in real-time as data is read from the trainer. 
# Additionally, it captures and displays video from the trainer's camera.

# to test ultrasonic and radar, see individual examples in this folder. 

# region: system imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsCamera
from pal.utilities.scope import MultiScope
import numpy as np
import cv2
# endregion

#Setup - NOTE THAT THIS EXAMPLE RUNS AT 100 HZ TO ENSURE GOOD PERFORMANCE 
# WITH SO MANY PLOTS AND GRAPHS. FOR FASTER RATES, YOU MAY NEED TO 
# REDUCE THE NUMBER OF SCOPES AND/OR SIGNALS BEING PLOTTED.
frequency = 100  # Hz
simulationTime = 300  # seconds

# Set up fps for the scope updates. Get counts needed to run at that rate.
scopeRefreshRate = 10
scopeCounts = int(round(frequency / scopeRefreshRate))

# region: setup scopes
window = 10
hmiScope = MultiScope(rows= 2, cols = 2,title='HMI',fps=scopeRefreshRate)
distanceScope = MultiScope(rows= 1, cols = 2,title='Distance',fps=scopeRefreshRate)
motionScope = MultiScope(rows= 2, cols = 2,title='Motion',fps=scopeRefreshRate)
lightForceScope = MultiScope(rows= 2, cols = 2,title='Light and Force',fps=scopeRefreshRate)
environmentScope = MultiScope(rows= 2, cols = 2,title='Environment',fps=scopeRefreshRate)

# HMI Scopes
hmiScope.addAxis(row=0, col=0, timeWindow=window, yLabel='Buttons')
hmiScope.axes[0].attachSignal(name='button0')
hmiScope.axes[0].attachSignal(name='button1')
hmiScope.addAxis(row=1, col=0, timeWindow=window, yLabel='Joystick')
hmiScope.axes[1].attachSignal(name='joystick X')
hmiScope.axes[1].attachSignal(name='joystick Y')
hmiScope.axes[1].attachSignal(name='joystick button')
hmiScope.addAxis(row=0, col=1, timeWindow=window, yLabel='Enc Counts')
hmiScope.axes[2].attachSignal(name='counts')
hmiScope.addAxis(row=1, col=1, timeWindow=window, yLabel='Enc Pulses')
hmiScope.axes[3].attachSignal(name='Enc A')
hmiScope.axes[3].attachSignal(name='Enc B')

# Distance Scopes
distanceScope.addAxis(row=0, col=0, timeWindow=window, yLabel='Infrared')
distanceScope.axes[0].attachSignal(name='infrared')
distanceScope.addAxis(row=0, col=1, timeWindow=window, yLabel='TOF')
distanceScope.axes[1].attachSignal(name='TOF')

# Motion Scopes
motionScope.addAxis(row=0, col=0, timeWindow=window, yLabel='Gyro')
motionScope.axes[0].attachSignal(name='Gyro X')
motionScope.axes[0].attachSignal(name='Gyro Y')
motionScope.axes[0].attachSignal(name='Gyro Z')
motionScope.addAxis(row=1, col=0, timeWindow=window, yLabel='Magnetometer')
motionScope.axes[1].attachSignal(name='Mag X')
motionScope.axes[1].attachSignal(name='Mag Y')
motionScope.axes[1].attachSignal(name='Mag Z')
motionScope.addAxis(row=0, col=1, timeWindow=window, yLabel='Accelerometer')
motionScope.axes[2].attachSignal(name='Accel X')
motionScope.axes[2].attachSignal(name='Accel Y')
motionScope.axes[2].attachSignal(name='Accel Z')
motionScope.addAxis(row=1, col=1, timeWindow=window, yLabel='PIR')
motionScope.axes[3].attachSignal(name='PIR')

# Light and Force Scopes
lightForceScope.addAxis(row=0, col=0, timeWindow=window, yLabel='Light Resistor')
lightForceScope.axes[0].attachSignal(name='Light Resistor')
lightForceScope.addAxis(row=1, col=0, timeWindow=window, yLabel='Load Cell')
lightForceScope.axes[1].attachSignal(name='Load Cell')
lightForceScope.addAxis(row=0, col=1, timeWindow=window, yLabel='RGB, Clear & IR')
lightForceScope.axes[2].attachSignal(name='Red')
lightForceScope.axes[2].attachSignal(name='Green')
lightForceScope.axes[2].attachSignal(name='Blue')
lightForceScope.axes[2].attachSignal(name='Clear')
lightForceScope.axes[2].attachSignal(name='IR')
lightForceScope.addAxis(row=1, col=1, timeWindow=window, yLabel='Force Sensing Resistor')
lightForceScope.axes[3].attachSignal(name='FSR')

# Environment Scopes
environmentScope.addAxis(row=0, col=0, timeWindow=window, yLabel='Thermocouple')
environmentScope.axes[0].attachSignal(name='Probe')
environmentScope.axes[0].attachSignal(name='PCB Chip')
environmentScope.addAxis(row=1, col=0, timeWindow=window, yLabel='Weather - Humidity')
environmentScope.axes[1].attachSignal(name='Humidity')
environmentScope.addAxis(row=0, col=1, timeWindow=window, yLabel='Weather - Temperature')
environmentScope.axes[2].attachSignal(name='Temperature')
environmentScope.addAxis(row=1, col=1, timeWindow=window, yLabel='Weather - Pressure')
environmentScope.axes[3].attachSignal(name='Pressure')

#endregion

frameRate = 30  # Camera frame rate in Hz
CameraCounts = int(round(frequency / frameRate))

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

        hmiScope.axes[0].sample(currentTime, sensors.buttons)
        hmiScope.axes[1].sample(currentTime, [sensors.joystick[0], 
                                                sensors.joystick[1], 
                                                sensors.joystickButton])
        hmiScope.axes[2].sample(currentTime, [sensors.encoder0])
        hmiScope.axes[3].sample(currentTime, sensors.encoderPulses)

        distanceScope.axes[0].sample(currentTime, sensors.IRDistance)
        distanceScope.axes[1].sample(currentTime, np.mean(sensors.TOFDistance))

        motionScope.axes[0].sample(currentTime, sensors.gyro)
        motionScope.axes[1].sample(currentTime, sensors.magnetometer)
        motionScope.axes[2].sample(currentTime, sensors.accelerometer)
        motionScope.axes[3].sample(currentTime, sensors.passiveIR)

        lightForceScope.axes[0].sample(currentTime, sensors.lightResistor)
        lightForceScope.axes[1].sample(currentTime, sensors.loadCell)
        lightForceScope.axes[2].sample(currentTime, [sensors.colorRGB[0], 
                                                     sensors.colorRGB[1], 
                                                     sensors.colorRGB[2], 
                                                     sensors.colorClear, 
                                                     sensors.colorIR])
        lightForceScope.axes[3].sample(currentTime, sensors.forceResistor)

        environmentScope.axes[0].sample(currentTime, [sensors.tempThermo,
                                                     sensors.tempThermoChip])
        environmentScope.axes[1].sample(currentTime, sensors.humidity)
        environmentScope.axes[2].sample(currentTime, sensors.tempWeather)
        environmentScope.axes[3].sample(currentTime, sensors.pressure)


        if counter%scopeCounts == 0:
            MultiScope.refreshAll()

        counter += 1

        timer.sleep()

input("Press Enter to exit...")
# endregion