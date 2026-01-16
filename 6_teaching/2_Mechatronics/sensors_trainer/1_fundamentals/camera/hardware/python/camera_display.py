# camera_display.py
# This script captures video from a camera and displays it in a window.
# Students can use this as a starting point for more complex image processing tasks.

# region: Python level imports
import cv2
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsCamera
from hal.utilities.image_processing import ImageProcessing
# endregion


# region: Experiment constants
simulationTime = 120 # will run for this amount of seconds
frameRate = 30
imageSize = [640,480]
# endregion


# region:  Main Loop
timer = Timer(sampleRate=frameRate, totalTime=simulationTime)
imageProcessingTool = ImageProcessing()


with  SensorsCamera(frameWidth=imageSize[0],
                    frameHeight=imageSize[1],
                    frameRate=frameRate,
                    cameraID=0) as camera: # modify cameraID if needed

    while timer.check():

        currentTime = timer.get_current_time()


        # read camera for 30Hz
        frame = camera.read()
        if frame:

            # obtain image information
            image = camera.imageData

            cv2.imshow("Color Image", image)
            cv2.waitKey(1)



        timer.sleep()


cv2.destroyAllWindows()
# endregion

input ("Press Enter to exit...")





