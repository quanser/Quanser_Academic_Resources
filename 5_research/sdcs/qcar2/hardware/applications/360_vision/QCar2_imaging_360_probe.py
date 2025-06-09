## imaging_360.py
# This example demonstrates how to read all 4 csi cameras and display in a single openCV window. If you encounter any errors, 
# use the hardware_test_csi_camera_single.py script to find out which camera is giving you trouble. 

from pal.utilities.vision import Camera2D
from pal.utilities.probe import Probe
import time
import struct
import numpy as np 

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Timing Parameters and methods 
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate     = 30.0
sampleTime     = 1/sampleRate
simulationTime = 60.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# Additional parameters
ipHost, ipDriver = '192.168.3.10', 'localhost'
counter = 0
imageWidth = 640
imageHeight = 480
imageBuffer360 = np.zeros((imageHeight + 40, 4*imageWidth + 120, 3), dtype=np.uint8) # 20 px padding between pieces  
        
# Stitch images together with black padding
horizontalBlank     = np.zeros((20, 4*imageWidth+120, 3), dtype=np.uint8)
verticalBlank       = np.zeros((imageHeight, 20, 3), dtype=np.uint8)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Initialize the CSI cameras and probe
myCam1 = Camera2D(cameraId="0", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam2 = Camera2D(cameraId="1", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam3 = Camera2D(cameraId="3", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
myCam4 = Camera2D(cameraId="2", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)
probe = Probe(ip = ipHost)
probe.add_display(imageSize = [imageHeight + 40, 4*imageWidth + 120, 3], scaling = True,
                            scalingFactor= 2, name="360 CSI")

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
## Main Loop
try:
    while elapsed_time() < simulationTime:
        start = time.time()
        if not probe.connected:
            probe.check_connection()
        if probe.connected:
        # Start timing this iteration

            # Capture RGB Image from CSI
            flag1=myCam1.read()
            flag2=myCam2.read()
            flag3=myCam3.read()
            flag4=myCam4.read()

            imageBuffer360 = np.concatenate(
                                            (horizontalBlank, 
                                                np.concatenate((    verticalBlank, 
                                                                    myCam2.imageData[:,320:640], 
                                                                    verticalBlank, 
                                                                    myCam3.imageData, 
                                                                    verticalBlank, 
                                                                    myCam4.imageData, 
                                                                    verticalBlank, 
                                                                    myCam1.imageData, 
                                                                    verticalBlank, 
                                                                    myCam2.imageData[:,0:320], 
                                                                    verticalBlank), 
                                                                    axis = 1), 
                                                horizontalBlank
                                                ), 
                                                axis=0
                                            )

            if all([flag1,flag2,flag3,flag4]): counter += 1
            if counter % 4 == 0:
                sending = probe.send(name="360 CSI",
                                    imageData=imageBuffer360)

        # End timing this iteration
        end = time.time()

        # Calculate the computation time, and the time that the thread should pause/sleep for
        computationTime = end - start
        sleepTime = sampleTime - ( computationTime % sampleTime )
        
        # Pause/sleep for sleepTime in milliseconds
        if sleepTime <= 0:
            sleepTime = 0 
        time.sleep(sleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate all webcam objects    
    probe.terminate()
    myCam1.terminate()
    myCam2.terminate()
    myCam3.terminate()
    myCam4.terminate()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 