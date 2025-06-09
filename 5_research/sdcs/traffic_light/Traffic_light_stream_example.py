## Traffic light example using stream
# This example initializes a stream client that sends the color array data 
# to the server on the Traffic Light.  
# Modify the light_ip variable to have the correct IP of the Traffic light.
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
# imports
from pal.utilities.stream import BasicStream
from pal.products.traffic_light import TrafficLight
try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout
import time
import numpy as np
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

## -- -- -TRAFFIC LIGHT IP- -- -- 
light_ip = '192.168.2.3'
# -- -- -- -- -- -- -- -- -- -- --

## Initialize the traffic light
trafficLight = TrafficLight(light_ip)
response = trafficLight.start_stream()
print('Starting Stream...')
print(response)
time.sleep(2)
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

# Create a BasicStream object configured as a Client agent, 
# with buffer sizes enough to send the traffic light colors.
# Note that this is set up to be blocking. 
# Thus, the client send returns when data is received.
networkAddress = 'tcpip://'+light_ip+':18020'

myClient = BasicStream(networkAddress, 
                       agent='C', 
                       receiveBuffer=np.zeros(3, dtype=np.uint8), 
                       sendBufferSize=1460, 
                       recvBufferSize=1460, 
                       nonBlocking=False)

timeout=Timeout(seconds=0, nanoseconds=1)
prev_con = False
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

## Timing Parameters and methods
startTime = time.time()
def elapsed_time():
    return time.time() - startTime

sampleRate = 10.0
sampleTime = 1/sampleRate
simulationTime = 20.0
print('Sample Time: ', sampleTime)
# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 

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

            # Send color data to server, a different color each second
            if np.floor(elapsed_time()) % 3 == 0:
                color = [1, 0, 0]
            elif np.floor(elapsed_time()) % 3 == 2:
                color = [0, 1, 0]
            else:
                color = [0, 0, 1]

            #color = [1, 0, 0] # for red
            #color = [0, 1, 0] # for yellow
            #color = [0, 0, 1] # for green
            bytesSent = myClient.send(np.array(color, dtype=np.uint8))

            if bytesSent == -1:
                print('Server application not receiving.')
                break

            # End timing this iteration
            end = time.time()

            # Calculate the computation time, and the sleep time for the thread
            computationTime = end - start
            sleepTime = sampleTime - ( computationTime % sampleTime )

            time.sleep(sleepTime)
            
except KeyboardInterrupt:
    print("User interrupted!")

finally:
    # Reset Traffic Light
    print('Reset Traffic Light LEDs')
    bytesSent = myClient.send(np.array([0, 0, 0], dtype=np.uint8))
    time.sleep(0.2)
    # Terminate Client
    myClient.terminate()
    print('Client terminated')
    # Terminate trafficLight
    trafficLight.stop_stream()
    print('Stopping Stream')


