""" 
MultiVehicle QCar 2 example. 

Make sure you have Quanser Interactive Labs open in Self Driving Car Studio/Cityscape or Cityscape lite
environment before running this example.  

The run.bat file will run all the necessary parts. If you want to run it separate, 
run initCars.py first to spawn the cars in the space. 
Then using two different terminals run vehicle_control.py and vehicle_control2.py to control the vehicles.
Both will ask what type of car you are using, for both, write 2 and click enter. (it is a QCar 2). 
 """
import sys
import time
import numpy as np
from qvl.multi_agent import MultiAgent, readRobots
from qvl.qlabs import QuanserInteractiveLabs
from qvl.real_time import QLabsRealTime
from qvl.free_camera import QLabsFreeCamera

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
camera.spawn_degrees(location=[28.003, -11.688, 33.17], rotation=[0, 51.415, 141.502])
# to switch our view from our current camera to the new camera we just initialized
camera.possess()

qlabs.close()

print("Disconnected from camera qlabs session") 

QCars = []


QCars.append({
    "RobotType": "QCar2", 
    "Location": [-12.8205, -04.5991, 0], 
    "Rotation": [0, 0, -0.7330382858376184], 
    'Radians': True,
    "Scale": 1,
})

QCars.append({
    "RobotType": "QC2", 
    "Location": [22.5478, 00.814, 0], 
    "Rotation": [0, 0, 1.5707963267948966], 
    'Radians': True,
    "Scale": 1
})

mySpawns = MultiAgent(QCars)


mySpawns.qlabs.close()



