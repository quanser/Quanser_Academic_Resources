import time
import numpy as np
from qvl.multi_agent import MultiAgent, readRobots
from qvl.qlabs import QuanserInteractiveLabs
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape
import numpy as np 

# testing multiagent: making sure all spawns happen and that all keys work. 
# Need to check in PC if all rt models started automatically


# Initialize an empty list (not a dictionary, because dictionaries are key-value pairs)
testArray = []

# Adding a new robot to the list

testArray.append({
    "RobotType": "QA", 
    "Location": [0.2, 0, 0], 
    "Radians": True,
    "Rotation": [0, 0, np.pi/5], 
    "Scale": 1
})

testArray.append({
    "RobotType": "QA", 
    "Location": [-.2, 0, 0], 
    "Radians": True,
    "Rotation": [0, 0, np.pi/5], 
    "Scale": 1
})


# testArray.append({
#     "RobotType": "QCar2", 
#     "Location": [-.5, 0, 0], 
#     "Rotation": [0, 0, 90], 
#     "Scale": .1,
#     "ActorNumber" : 5
# })


# testArray.append({
#     "RobotType": "QD2", 
#     "Location": [1, 0.5, 0], 
#     "Rotation": [0, 0, 90], 
#     "Scale": 1
# })

# testArray.append({
#     "RobotType": "QBP", 
#     "Location": [-1, .5, -0], 
#     "Rotation": [0, 0, 90], 
# })


mySpawns = MultiAgent(testArray)

actors = mySpawns.robotActors

print(actors)
print(actors[0].actorNumber)
print(actors[0].classID)

actors = mySpawns.robotsDict
print(actors)

robotsDir = readRobots()

print(robotsDir["QA_0"]["hilPort"])

mySpawns.qlabs.close()



