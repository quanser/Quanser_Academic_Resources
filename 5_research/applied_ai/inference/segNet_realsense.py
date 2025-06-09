## SegNet example
# This example reads an RGB image from the RealSense
# camera on the robot and runs it through
# a SegNet to segment different areas on the input image.

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# imports
from pit.jetson.nets import SegNet
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
imageWidth = 640
imageHeight = 480

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Camera and model/network initialization
input = Camera3D(mode='rgb',
                 frameWidthRGB=imageWidth,
                 frameHeightRGB=imageHeight,
                 frameRateRGB=sampleRate)

# model
myModel=SegNet(network = 'fcn-resnet18-mhp', # 'fcn-resnet18-voc-320x320'
                imageWidth=imageWidth,
                imageHeight=imageHeight,
                visualize='overlay,mask',
                filter_mode = 'linear',
                alpha=120.0,
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
                                    ignore_class = "void")
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

except KeyboardInterrupt: print("User interrupted!")

finally:
    print('closeCam')
    # Terminate the camera object
    input.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
