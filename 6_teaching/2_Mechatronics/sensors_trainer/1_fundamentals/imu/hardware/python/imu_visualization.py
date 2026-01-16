# IMU - IMU Visualization

from pal.utilities.timing import Timer
from pal.products.sensors import SensorsTrainer, SensorsDisplay
from library_visualization import VisualizeIMU

sampleRate = 480 # Hz
totalTime = 300 # seconds

timer   = Timer(sampleRate=sampleRate, totalTime=totalTime)
viz     = VisualizeIMU()

visualization = 1

with SensorsTrainer() as sensors, \
     SensorsDisplay() as lcd:

    counter = 0
    lcd.clear()

    while timer.check():

        # get updated sensor measurements
        sensors.read_outputs()

        # visualize IMU data (only uncomment one of the next 3 lines)
        if visualization == 1:
            viz.visualize_rotations(sensors.gyro, sensors.buttons)
        elif visualization == 2:
            viz.visualize_acceleration(sensors.accelerometer)
        else:
            viz.visualize_orientation(sensors.accelerometer)

        # draw on LCD
        if counter%16 == 0:  # 480/16 = 30Hz
            lcd.draw_image(viz.img)

        counter += 1
        timer.sleep()

with SensorsDisplay() as lcd:
    lcd.clear()
input('Press the enter key to exit.')