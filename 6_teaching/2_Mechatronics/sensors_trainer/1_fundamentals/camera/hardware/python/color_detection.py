# region: Python level imports
import numpy as np
import cv2
# endregion

# region: Quanser Imports
from pal.utilities.timing import Timer
from pal.products.sensors import SensorsCamera
from hal.utilities.image_processing import ImageProcessing 
# endregion 


# region: Experiment constants
simulationTime = 120 # will run for this amount of seconds
frameRate = 30
imageSize = [640,480]
colorDetect = True
bgrValuesLower = np.array([0,0,0])
bgrValuesUpper = np.array([255,255,255]) 
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

            if not colorDetect:
                cv2.imshow("Color image", image)
            else:
                thresholdImage = cv2.inRange(image,bgrValuesLower,bgrValuesUpper)
                newImage = cv2.bitwise_and(image,image,mask=thresholdImage)
                cv2.imshow("Color Detected", newImage)
            cv2.waitKey(1)



        timer.sleep()
    

cv2.destroyAllWindows()
# endregion






