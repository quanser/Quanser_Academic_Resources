## imageNet example
# This example reads an RGB image from the CSI cameras 
# on the robot and runs it through an imageNet 
# to classify what appears on the image.

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# imports
from pit.jetson.nets import ImageNet
from pal.utilities.vision import Camera2D
import time
import time

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0 # runs at 30 fps
sampleTime = 1/sampleRate
simulationTime = 60.0 # runs for 1 minute
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
imageWidth = 640
imageHeight = 480

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Camera and model/network initialization

#cameraID # 0 for right camera, 1 for back, 2 for front, 3 for left 
cameraID = str(2)
input = Camera2D(cameraId=cameraID,
                 frameWidth=imageWidth, 
                 frameHeight=imageHeight, 
                 frameRate=sampleRate)

# model
myModel=ImageNet(network = 'googlenet',
                imageWidth=imageWidth,
                imageHeight=imageHeight, 
                threshold = 0.1, 
                showImage = True, 
                outputURI = "", 
                verbose=True)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Main Loop
try:
    while elapsed_time() < simulationTime:
        
        # Start timing this iteration
        start = time.time()

        # Read the camera
        newData = input.read() # if using csi cameras
        
        if newData is False:
           continue
        
        #pre process the image to use in the predictor
        img=myModel.pre_process(input.imageData) 

        predictions=myModel.predict(img, 
                                    topK=2,
                                    textOnImage=True)
        
        myModel.render() 

        # End timing this iteration
        end = time.time()

        # Calculate the computation time, 
        # and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )

        if sleepTime <= 0:
             time.sleep(0.0002)
        else:
             time.sleep(sleepTime)
    

except KeyboardInterrupt:
    print("User interrupted!")

finally:    
    print('closeCam')
    # Terminate the camera object
    input.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
