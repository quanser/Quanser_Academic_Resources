""" MultiAgent QBot Platform - QDrone 2 Leader Follower Example
-----------------------------------------------------------------------------

    Make sure you have Quanser Interactive Labs open in Open World/Warehouse
    environment before running this example.
    MAKE SURE TO ALWAYS RUN THIS FILE BEFORE STARTING THE MISSION SERVER.

    First run this file to set up the environment, robots, and necessary background files.
    Follow the instructions in the MS_QD2_QBPlat*.slx to run the example and start the drone controller. 

    """


import time
import numpy as np
import sys
from qvl.multi_agent import MultiAgent, readRobots
from qvl.qlabs import QuanserInteractiveLabs
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape

from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from pal.utilities.stream import BasicStream

try:
    from quanser.common import Timeout
except:
    from quanser.communications import Timeout


qlabs = QuanserInteractiveLabs()

print("Connecting to QLabs...")
if (not qlabs.open("localhost")):
    print("Unable to connect to QLabs") 
    sys.exit()  

print("Connected")  

QLabsRealTime().terminate_all_real_time_models()
time.sleep(1)
qlabs.destroy_all_spawned_actors()

# create a camera in this qlabs instance
camera = QLabsFreeCamera(qlabs)
camera.spawn_degrees(location=[-0.017, -3.068, 1.51], rotation=[-0, 19.575, 91.273])
# to switch our view from our current camera to the new camera we just initialized
camera.possess()

floor = QLabsBasicShape(qlabs)
floor.spawn(location=[0,0,0], scale=[2,2,0.001])

qlabs.close()

print("Disconnected from camera spawn")

time.sleep(1)

Robots = []

Robots.append({
    "RobotType": "QDrone2",
    "Location": [.75, 0, 0.1],
    "Rotation": [0, 0, 90],
})

Robots.append({
    "RobotType": "QBP",
    "Location": [-.75, 0, 0.1],
    "Rotation": [0, 0, 90],
})

mySpawns = MultiAgent(Robots)

actors = mySpawns.robotActors


#create server to send QBP location to the mission server
myServer = BasicStream('tcpip://localhost:18050', agent='S', sendBufferSize=2048, nonBlocking=False)
prev_con = False
error = 0
try:
    while True:
        # get qbot platform location
        status, location, rotation, scale = actors[1].get_world_transform()

        # First check if the server was connected.
        if not myServer.connected:
            myServer.checkConnection(timeout=Timeout(seconds=0, nanoseconds=1))

        # If a server accepted the connection, let the user know and proceed.
        if myServer.connected and not prev_con:
            print('Connection to Client was successful.')
            print('Streaming QBot Platform position on port 18050')
            prev_con = myServer.connected
            continue

        # Server is connected, so execute code within this section.
        if myServer.connected:
            output = [location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], int(status)]
            toNumpy = np.array(output, dtype=np.dtype('d'))
            bytesSent = myServer.send(toNumpy)
            #print('Bytes sent:', bytesSent)
            if bytesSent == -1:
                error = error + 1
            else:
                error = 0

            if error > 10:
                break

finally:
    print('Client Disconnected. Stopping Server.')
    QLabsRealTime().terminate_all_real_time_models()
    QLabsRealTime().terminate_all_real_time_models()
    mySpawns.qlabs.close()





