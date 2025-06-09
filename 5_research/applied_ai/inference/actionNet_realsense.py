## actionNet example
# This example reads an RGB image  from the RealSense
# camera on the robot and runs it through an actionNet 
# to classify the action in the video.

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# imports
from pit.jetson.nets import ActionNet
from pal.utilities.vision import Camera3D
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
input = Camera3D(mode='rgb',
                 frameWidthRGB=imageWidth, 
                 frameHeightRGB=imageHeight, 
                 frameRateRGB=sampleRate)


# model
myModel=ActionNet(network = 'resnet-18',
                imageWidth=imageWidth,
                imageHeight=imageHeight, 
                threshold = 0.1, 
                skipFrames = 1, 
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
        newData = input.read_RGB()

        if newData == -1:
            continue
        
        # pre process the image to use in the predictor
        img=myModel.pre_process(input.imageBufferRGB)

        predictions=myModel.predict(img, 
                                    textOnImage = True)
        
        myModel.render(printPerformance=False) 

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
