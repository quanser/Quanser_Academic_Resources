import time
import math
import struct

from quanser.communications import Stream
import urllib.request, sys
from urllib.error import HTTPError, URLError
from socket import timeout

#Send the formatted request
def sendreq(url):
    #Format the HTTP get request with a timeout of 1s to account for async tasks that will not return

    response = "Call complete!"
    try:
        response = urllib.request.urlopen(url, timeout=1).read().decode('utf-8')
    #If the URL is not correct
    except (HTTPError, URLError) as error:
        response = "Error endpoint not found at " + url
    #If the request was not expected to return the call it complete, otherwise flag a timeout
    except timeout:
        if url.find("timed") == -1:
            response = "Call timed out"
        else:
            response = "Async call complete"

    return response


from qvl.qlabs import QuanserInteractiveLabs
from qvl.traffic_light import QLabsTrafficLight

# creates a server connection with Quanser Interactive Labs and manages the communications
qlabs = QuanserInteractiveLabs()

print("Connecting to QLabs...")
# trying to connect to QLabs and open the instance we have created - program will end if this fails
try:
    qlabs.open("localhost")
except:
    print("Unable to connect to QLabs")

# traffic light
TrafficLight0 = QLabsTrafficLight(qlabs)
TrafficLight0.spawn_degrees([-2.5, -5.5, 0], [0, 0, 90], scale=[1, 1, 1], configuration=0, waitForConfirmation=True)
TrafficLight0.set_color(QLabsTrafficLight.COLOR_GREEN)
TrafficLight1 = QLabsTrafficLight(qlabs)
TrafficLight1.spawn_degrees([8, -12.7, 0], [0, 0, 270], scale=[1, 1, 1], configuration=0, waitForConfirmation=True)
TrafficLight1.set_color(QLabsTrafficLight.COLOR_RED)

stream = Stream()
stream.connect("tcpip://localhost:12000", False, 64, 64)
buffer = bytearray(8)

i = 0
while (True):
    i=i+1
    print (i)
    bytes_read = stream.receive(buffer, 8)
    x, = struct.unpack("d", buffer)
    if x == 1:
        #QLabsTrafficLightSingle().setState(qlabs, 0, QLabsTrafficLightSingle().STATE_GREEN)
        #QLabsTrafficLightSingle().setState(qlabs, 1, QLabsTrafficLightSingle().STATE_RED) 
        #QLabsFreeCamera().possess(qlabs, deviceNumber=0)
        #os.system("CommandLight.py 192.168.1.20 immediate 0 0 1")
        print(sendreq("http://192.168.2.20:5000/immediate/green"))
        print(sendreq("http://192.168.2.21:5000/immediate/red"))
        TrafficLight0.set_color(QLabsTrafficLight.COLOR_GREEN)
        TrafficLight1.set_color(QLabsTrafficLight.COLOR_RED)

    else:
        #QLabsTrafficLightSingle().setState(qlabs, 0, QLabsTrafficLightSingle().STATE_RED)  
        #QLabsTrafficLightSingle().setState(qlabs, 1, QLabsTrafficLightSingle().STATE_GREEN)
        #QLabsFreeCamera().possess(qlabs, deviceNumber=1)
        #os.system("CommandLight.py 192.168.1.20 immediate 1 0 0")
        print(sendreq("http://192.168.2.20:5000/immediate/red"))
        print(sendreq("http://192.168.2.21:5000/immediate/green"))
        TrafficLight0.set_color(QLabsTrafficLight.COLOR_RED)
        TrafficLight1.set_color(QLabsTrafficLight.COLOR_GREEN)

stream.shutdown()
stream.close()

qlabs.close()
print("Done!")  
