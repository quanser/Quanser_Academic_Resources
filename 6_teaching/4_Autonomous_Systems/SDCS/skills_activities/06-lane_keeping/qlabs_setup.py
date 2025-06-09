# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : File Description and Imports

"""
qlab_setup.py

Simulation setup code for lane keeping lab guide.
Please review the accompanying "Lab Guide - Lane Keeping" PDF
"""

from qvl.qcar2 import QLabsQCar2
from qvl.qlabs import QuanserInteractiveLabs
from qvl.basic_shape import QLabsBasicShape
from qvl.reference_frame import QLabsReferenceFrame
from qvl.real_time import QLabsRealTime
from qvl.free_camera import QLabsFreeCamera
import pal.resources.rtmodels as rtmodels
import numpy as np
import time
import random
#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Experiment Configuration 

# ===== Timing Parameters
# - start_at_curved: Set the starting configuration of the QCar. If true,
#   QCar starts at curved road with no NPC cars, else starts at stright 
#   road with NPC cars 
start_at_curved = False
#endregion


# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
#region : Utility Functions and Simulation Setup

class NPC_cars():
    def __init__(self,Qlab):
        color=[1,0,0]
        self.cars=[]
        self.speeds=[]
        self.lane_center = [-6.15,-2.5,-10.25]
        self.num_cars = random.randint(11,13)
        self.spacing = 30
        self.start_loc = 30
        print('Spawning',self.num_cars,'cars.' )
        
        for _ in range(self.num_cars):
            self.cars.append(QLabsQCar2(Qlab))
            self.speeds.append(random.random()*1+6)

        
        row_num=0
        # for i, car in enumerate(self.cars):
        count = 0
        while count < self.num_cars-1:
            car_per_row=random.randint(1,2)
            lane_pos=random.sample(self.lane_center,car_per_row)
            for y in lane_pos:
                car=self.cars[count]
                car.spawn(location=[self.start_loc+self.spacing*row_num,y,1],
                          scale=[1, 1, 1])
                car.set_led_strip_uniform(color=color,waitForConfirmation=False)
                count+=1
            row_num+=1

    def start(self):
        for i,car in enumerate(self.cars):
            v = self.speeds[i]
            car.set_velocity_and_request_state(v,0,0,0,0,0,0)

# initialize qlab
qlab=QuanserInteractiveLabs()
print("Connecting to QLabs...")
try:
    qlab.open("localhost")
    print("Connected to QLabs")
except:
    print("Unable to connect to QLabs")
    quit()

# Delete any previous QCar instances and stop any running spawn models
qlab.destroy_all_spawned_actors()
QLabsRealTime().terminate_all_real_time_models()


def spawnBox(spawnLocation, shapeNumber, parentInfo, border = False): 
    spawnBox = QLabsBasicShape(qlab) 
    spawnBox.spawn_id_and_parent_with_relative_transform( 
                                                actorNumber = shapeNumber, 
                                                location = spawnLocation, 
                                                rotation = [0,0,0], 
                                                scale    = [1, 1, 1], 
                                                configuration = spawnBox.SHAPE_CUBE, 
                                                parentClassID = parentInfo.ID_BASIC_SHAPE, 
                                                parentActorNumber = parentInfo.actorNumber, 
                                                parentComponent   = 0, 
                                                waitForConfirmation = False)

    if shapeNumber%2 == 0 or border == True:
        spawnBox.set_material_properties(
                                        color     = [1, 1, 1], 
                                        roughness = 10.0,
                                        metallic  = False,
                                        waitForConfirmation = False)

    else:
        spawnBox.set_material_properties(  
                                                color     = [0, 0,0], 
                                                roughness = 10.0,
                                                metallic  = False,
                                                waitForConfirmation = False)
    
#ID for object inside of spiral
box1 = QLabsBasicShape(qlab)
box1RefFrame = QLabsReferenceFrame(qlab)
initLocationBoard = [800,-6.5,1.115]
initRotation = [np.pi/2,0,np.pi/2]
boxSize = 0.8
def spiral(Col, Row):
    '''    
    Function used to spawn the boxes used by the chessboard grid. 
    Chessboard is created using a spiral from the center of the chessboard. 
    '''
    currentCol = currentRow = 0
    deltaCol = 0
    deltaRow = -1

    for i in range(max(Col+2, Row+2)**2):
        if (-(Col/2+1) < currentCol <= (Col/2+1)) and (-(Row/2+1) < currentRow <= (Row/2+1)):
            # print(i)
            if currentCol == 0 and currentRow == 0:
                # Spawn the master cube (this is the cube you will move around)                
                box1RefFrame.spawn_id( 
                        actorNumber = 1, 
                        location = initLocationBoard, 
                        rotation = initRotation, 
                        scale = [1,1,1], 
                        configuration = 0, 
                        waitForConfirmation=False)

                box1.spawn_id( 
                        actorNumber = 1, 
                        location = initLocationBoard, 
                        rotation = initRotation,
                        scale = [boxSize, 0.05, boxSize], 
                        configuration = box1.SHAPE_CUBE, 
                        waitForConfirmation=False)
                                
                box1.set_material_properties(   color     = [0, 0,0], 
                                                roughness = 10.0,
                                                metallic  = False,
                                                waitForConfirmation = False)
                
            elif  i >= max(Col, Row)**2 :
                boxLocation = [currentCol, 0 ,currentRow]
                spawnBox(boxLocation,i+1,box1, border= True)
            
            else:
                boxLocation = [currentCol, 0 ,currentRow]
                spawnBox(boxLocation,i+1,box1)

        if (currentCol == currentRow) or (currentCol < 0 and currentCol == -currentRow) or (currentCol > 0 and currentCol == 1-currentRow):
            deltaCol, deltaRow = -deltaRow, deltaCol
        currentCol, currentRow = currentCol+deltaCol, currentRow+deltaRow

spiral(12,1)

if start_at_curved:
    start_pos=[[3235,-4520,51],
            [0,0,-np.pi/3]]
else:
    start_pos=[[-50,-10.25,1],
            [0,0,0]]  
qcar_driver=QLabsQCar2(qlab)
qcar_driver.spawn_id(
        actorNumber=0,
        location=start_pos[0],
        rotation=start_pos[1],
        scale=[1, 1, 1],
        waitForConfirmation=True
    )
# Create a new camera view and attach it to the QCar
camera = QLabsFreeCamera(qlab)
camera.spawn()
qcar_driver.possess()

# Start spawn model
QLabsRealTime().start_real_time_model(rtmodels.QCAR2)

### virtual environment setup parameters
if not start_at_curved:
    NPC_cars=NPC_cars(qlab)
delta_x=0
notStarted = True
_,init_location,__,___=qcar_driver.get_world_transform()
msg = ''
while delta_x<850 and msg=='':
    _,new_location,__,___=qcar_driver.get_world_transform()
    if notStarted:
        diff=np.array(new_location)-np.array(init_location)
        if np.linalg.norm(diff)>2:
            if not start_at_curved:
                NPC_cars.start()
            start_time = time.time()
            print('Timer started')
            notStarted = False
    delta_x=new_location[0]-init_location[0]
    _,_,_,msg=qcar_driver.get_custom_properties()
    if msg:
        print('lane_keeping.py terminated on QCar2')

message = 'Task completed in '+str(round(time.time()-start_time,2))+\
        ' seconds, press any keys to continue'
input(message)
#endregion
