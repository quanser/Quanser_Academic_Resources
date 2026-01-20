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
calibrate = False
NUMBER_IMAGES = 15
savedImages = []
imageCount = 0
imageSize = [640,480]
intrinsicParameters = []
distortionCoefficients = []
calibrated = False

# Complete by students
chessboardDim =[9,7]
boxSize = 20 #mm
# endregion


# region: Main Loop
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
            # convert frame to grayscale
            grayscale_image = cv2.cvtColor(camera.imageData, cv2.COLOR_BGR2GRAY)

            if not calibrated:
                cv2.imshow('Bloqs Camera', grayscale_image)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    imageCount +=1
                    print("saving Image #: ", imageCount)
                    savedImages.append(grayscale_image)
    
                if imageCount == NUMBER_IMAGES and np.size(intrinsicParameters) == 0  and np.size(distortionCoefficients) == 0:
                    print("Implement calibration for Mechatronics sensor camera.... ")

                    print("\nCamera calibration results are: ")
                    # Quanser's use of OpenCV for camera calibration
                
                    intrinsicParameters, distortionCoefficients = \
                        imageProcessingTool.calibrate_camera(
                            savedImages,
                            chessboardDim,
                            boxSize)
                    

                    # Printed output for students
                    text = "Mechatronics sensors camera intrinsic matrix at resolution {} is:"
                    print(text.format(imageSize))
                    print(intrinsicParameters)

                    text = ("Mechatronics sensors camera camera distortion parameters "
                        + "at resolution {} are: ")
                    print(text.format(imageSize))
                    print(distortionCoefficients)
                    calibrated = True

            else:
                grayscle_calibrated = imageProcessingTool.undistort_img(grayscale_image, intrinsicParameters, distortionCoefficients)
                cv2.imshow('Bloqs Camera', grayscle_calibrated)
                cv2.waitKey(1)




        timer.sleep()
    

cv2.destroyAllWindows()
# endregion






