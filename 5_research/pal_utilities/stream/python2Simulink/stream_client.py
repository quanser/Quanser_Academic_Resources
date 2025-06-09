## stream_client
# This example initializes a stream client that sends an image to the server. You need a webcam to run
# this example connected via USB. If running this on a QCar, QBot etc. you do not need any additional
# hardware, but you will have to modify IP addresses accordingly at the client side.
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# imports
from pal.utilities.stream import BasicStream
from pal.utilities.vision import Camera2D
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout
import time
import cv2
import numpy as np
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Image parameters
imageWidth = 640
imageHeight = 480
imageChannels = 3
bufferSize = imageHeight*imageWidth*imageChannels 

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Create a BasicStream object configured as a Client agent, with buffer sizes enough to send the image above.
# Note that this is setup to be blocking. Thus, the client send returns when data is received.
myClient = BasicStream('tcpip://localhost:18001', agent='C', sendBufferSize=bufferSize, recvBufferSize=2048, nonBlocking=False)
timeout=Timeout(seconds=0, nanoseconds=1)
prev_con = False

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 20.0
print('Sample Time: ', sampleTime)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Initialize the CSI cameras
myCam1 = Camera2D(cameraId="1", frameWidth=imageWidth, frameHeight=imageHeight, frameRate=sampleRate)

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Main Loop
try:
    while elapsed_time() < simulationTime:

        # First check if the server was connected.
        if not myClient.connected:
            myClient.checkConnection(timeout=timeout)

        # If a server accepted the connection, let the user know and proceed.
        if myClient.connected and not prev_con:
            print('Connection to Server was successful.')
            prev_con = myClient.connected
            continue

        # Server is connected, so execute code within this section.
        if myClient.connected:

            # Start timing this iteration
            start = time.time()

            # Capture RGB Image from CSI
            myCam1.read()

            # Send data to server after converting image to float32 data type
            #bytesSent = myClient.send( np.array( myCam1.image_data, dtype=np.float32 )/255 )
            bytesSent = myClient.send(myCam1.imageData)# cv2.cvtColor(myCam1.imageData, cv2.COLOR_BGR2RGB)   )
            print('Bytes sent:', bytesSent)

            if bytesSent == -1:
                print('Server application not receiving.')
                break

            # End timing this iteration
            end = time.time()

            # Calculate the computation time, and the time that the thread should pause/sleep for
            computationTime = end - start
            sleepTime = sampleTime - ( computationTime % sampleTime )

            # Pause/sleep for sleepTime in milliseconds
            msSleepTime = int(1000*sleepTime)
            if msSleepTime <= 0:
                msSleepTime = 1 # this check prevents an indefinite sleep as cv2.waitKey waits indefinitely if input is 0

            cv2.imshow('Client Image Captured', myCam1.imageData)
            cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate Webcam
    myCam1.terminate()

    # Terminate Client
    myClient.terminate()

    print('All the right turns in all the right places.')

