#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#---------------------Lab 3 - Vision - Image Processing-----------------------#
#-----------------------------------------------------------------------------#

# imports
from pal.products.qarm_mini import QArmMini
from pal.utilities.timing import QTimer
from hal.content.qarm_mini import QArmMiniImageProcessing as IP
import cv2
from pal.utilities.vision import Camera2D

## Section A - Initialization
myMiniArm   = QArmMini(hardware=1, id=3)
timer       = QTimer(sampleRate=10.0, totalTime=300.0)
myProcessor = IP()
boxed_image = None
myCam = Camera2D("0", frameWidth=640, frameHeight=360, frameRate=30)

try:
    while timer.check():
        
        ## Section B - QArm Mini hardware I/O
        myMiniArm.read_write_std(joints=myMiniArm.HOME_POSE)

        ## Section C - Image Processing
        myCam.read()
        blur        = myProcessor.guassian_blur(myCam.imageData)
        # hsv         = myProcessor.convert(blur, cv2.COLOR_BGR2HSV)
        # colorThresh = myProcessor.threshold_color(hsv,(80, 180, 150), (50, 40, 70))
        # mask_opened = myProcessor.open(colorThresh, 7, 5)
        # mask_closed = myProcessor.close(mask_opened, 7, 5)
        # grayscale   = myProcessor.convert(blur, cv2.COLOR_BGR2GRAY)
        # highlight   = myProcessor.highlight(blur, colorThresh)
        
        imgdata_1   = myCam.imageData
        imgdata_2   = blur 

        cv2.imshow('Image Data 1', imgdata_1)
        cv2.imshow('Image Data 2', imgdata_2)

        # c, r, area  = myProcessor.find_objects(mask_closed, 8, 500, 5000)  
        # if c is not None and r is not None:
        #     boxed_image = myProcessor.draw_box_on_detection(highlight, c, r, area)

        # if boxed_image is not None and boxed_image.size > 300:
        #     cv2.imshow('Boxed Image', boxed_image)

        cv2.waitKey(5)
        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    myCam.terminate
    myMiniArm.terminate()