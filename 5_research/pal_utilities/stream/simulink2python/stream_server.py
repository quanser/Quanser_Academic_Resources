## stream_example_server
# This example initializes a stream server that receives an image from the client. You do not need any
# additional hardware to run this example. If running this on a QCar, QBot etc. you will have to modify
# IP addresses accordingly at the client side.
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

# imports
from pal.utilities.stream import BasicStream
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout
import time
import numpy as np
import cv2

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Image Parameters
imageWidth = 640
imageHeight = 480
imageChannels = 3
bufferSize = imageHeight*imageWidth*imageChannels 
imageData = np.zeros((imageHeight, imageWidth, imageChannels), dtype=np.uint8)
sizeInBytes = imageData.tobytes()
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Create a BasicStream object configured as a Server agent, with buffer sizes enough to send/receive the image above.
# Note that this is setup to be non-blocking. The server tries to receive data as fast as possible.
myServer = BasicStream('tcpip://localhost:18001', agent='S', sendBufferSize=bufferSize, recvBufferSize=bufferSize, receiveBuffer=imageData, nonBlocking=False, reshapeOrder='F')
timeout=Timeout(seconds=0, nanoseconds=1)
prev_con = False

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 30.0
sampleTime = 1/sampleRate
simulationTime = 30.0
print('Sample Time: ', sampleTime)
counter = 0
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
# Main Loop
try:
    while elapsed_time() < simulationTime:

        # First check if a client connected successfully.
        if not myServer.connected:
            myServer.checkConnection(timeout=timeout)

        # If a client has just connected, let the user know and proceed.
        if myServer.connected and not prev_con:
            print('Connection to Client was successful.')
        prev_con = myServer.connected

        # Client is connected, execute the code within this section.
        if myServer.connected:

            # Start timing this iteration
            start = time.time()

            # Receive data from client
            recvFlag, bytesReceived = myServer.receive(iterations=2, timeout=timeout)
            print('Bytes received:', bytesReceived)
            if not recvFlag:
                counter += 1
                if counter > 10:
                    print('Client stopped sending data over.')
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
            newImg = cv2.cvtColor(myServer.receiveBuffer, cv2.COLOR_BGR2RGB) 
            cv2.imshow('Server Image Received', newImg)
            cv2.waitKey(msSleepTime)

except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Terminate Server
    myServer.terminate()
    print('All the right turns in all the right places.')