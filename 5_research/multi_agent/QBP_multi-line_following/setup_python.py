""" MultiAgent QBot Platform Example
----------------------------------

    Make sure you have Quanser Interactive Labs open in Open World/Warehouse
    environment before running this example.  
    First run this file to set up the environment. Then use
    line_folowing.slx and a joystick to control the QBots Line following. 

    """


import sys
import time
import numpy as np
from qvl.multi_agent import MultiAgent, readRobots
from qvl.qlabs import QuanserInteractiveLabs
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape
from qvl.qbot_platform_flooring import QLabsQBotPlatformFlooring

from qvl.qlabs import QuanserInteractiveLabs
from qvl.free_camera import QLabsFreeCamera
from qvl.system import QLabsSystem


qlabs = QuanserInteractiveLabs()
    
print("Connecting to QLabs...")
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
camera.spawn_degrees(location=[-1.771, 0.293, 1.169], rotation=[0, 39.681, -18.909])
# to switch our view from our current camera to the new camera we just initialized
camera.possess()

floor = QLabsQBotPlatformFlooring(qlabs)
floor.spawn(location = [ 0, 1.2,   0],rotation = [0,0,-np.pi/2])
floor.spawn(location = [ 0, 0,   0],rotation = [0,0,-np.pi/2], configuration=1)
floor.spawn(location = [ 0, -2.4,   0],rotation = [0,0,0], configuration=3)
floor.spawn(location = [ -1.2, 0,   0],rotation = [0,0,0])
floor.spawn(location = [ -1.2, 0,   0],rotation = [0,0,-np.pi/2], configuration=1)
floor.spawn(location = [ -1.2, -2.4,   0],rotation = [0,0,0], configuration=3)

coverup = QLabsBasicShape(qlabs)
coverup.spawn(location=[0.6,-0.6,0], scale=[0.59,0.7,0.007])
coverup.set_material_properties(color=[0,0,0], roughness=0.6)
coverup.spawn(location=[0.01,-0.6,0], scale=[0.55,0.7,0.007])
coverup.set_material_properties(color=[0,0,0], roughness=0.6)

coverup.spawn(location=[-0.6,-0.6,0], scale=[0.59,0.7,0.007])
coverup.set_material_properties(color=[0,0,0], roughness=0.6)
coverup.spawn(location=[-1.21,-0.6,0], scale=[0.59,0.7,0.007])
coverup.set_material_properties(color=[0,0,0], roughness=0.6)

qlabs.close()

print("Disconnected from camera/mats spawn") 

time.sleep(1)

# Initialize an empty list (not a dictionary, because dictionaries are key-value pairs)
QBots = []

QBots.append({
    "RobotType": "QBP", 
    "Location": [.26, -.5, -0], 
    "Rotation": [0, 0, -90], 
})

QBots.append({
    "RobotType": "QBP",
    "Location": [0, 0.89, -0], 
    "Rotation": [0, 0, 180], 
})

QBots.append({
    "RobotType": "QBP", 
    "Location": [-0.9, -1.1, -0], 
    "Rotation": [0, 0, -90], 
})

mySpawns = MultiAgent(QBots)

# # actors = mySpawns.robotActors

# # print(actors)

# # # robotsDir = readRobots()

mySpawns.qlabs.close()



