# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
'''
setup_chessboard_move_camera.py 

High-level summary of the python file with a description of which PDFs 
accompany the python example.      
'''
import numpy as np
from qvl.qlabs import QuanserInteractiveLabs
from qvl.basic_shape import QLabsBasicShape
from qvl.reference_frame import QLabsReferenceFrame
from qvl.free_camera import QLabsFreeCamera
import qlabs_setup
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Setup

#=================== Virtual Env Setup ===================
# Connecting to Quanser Interactive Labs
qlabs = QuanserInteractiveLabs()
print("Connecting to QLabs...")

try:
    qlabs.open("localhost")
    print("Connected to QLabs")
except:
    print("Unable to connect to QLabs")
    quit()

clearEnv = input("Do you want to reset the virtual environment?(y/n): ")

if clearEnv == "y":
    # Destroy all spawned actors to reset the scene
    print("Deleting current spawned actors...")
    qlabs_setup.setup(initialPosition=[1.066, -6.218,0])

# Determine checkerboard height and width. 
# Actual dimensions will be larger to include the border
text = "Please specify the side length (number of cells) for a square chess board (integer): "
dimension = int(input(text))
text = "Please specify the size of each cell used for camera calibration (floating point): "
boxSize = float(input(text))

# Setup QLabs camera for camera calibration scene
freeCamera = QLabsFreeCamera(qlabs)
freeCamera.spawn([0, -20, 3], [0,-0.2,-3*np.pi/2])
freeCamera.possess()

# Spawn ref frame to aid with identifying how to move chessboard:
windowRefFrame = QLabsReferenceFrame(qlabs)
windowRefFrame.spawn_id( 
                        actorNumber = 2, 
                        location = [-5,-5,0], 
                        rotation = [0,0,0], 
                        scale = [2,2,2], 
                        configuration = 2, 
                        waitForConfirmation=False) 
                        
# Based on board dimensions add a white border, so grid size is always [L+2,W+2]
heightOfCenter = (dimension+2)/2-boxSize/2
initLocationBoard = [0,20, heightOfCenter+boxSize*1]
initRotation = [0,0,0]

# Create Spiral Around first object: 
rowSteps    = dimension/2
colSteps = dimension/2
colorBox    = [0,0,0]

# Already spawned object 1
objectCount = 1
shapeIndex = 1

def spawnBox(spawnLocation, shapeNumber, parentInfo, border = False): 
    spawnBox = QLabsBasicShape(qlabs) 
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
box1 = QLabsBasicShape(qlabs)
box1RefFrame = QLabsReferenceFrame(qlabs)

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
                        configuration = 2, 
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

spiral(dimension,dimension)

windowRefFrame = QLabsReferenceFrame(qlabs)
windowRefFrame.spawn_id( 
                        actorNumber = 2, 
                        location = [-5,0,0], 
                        rotation = [0,0,0], 
                        scale = [2,2,2], 
                        configuration = 2, 
                        waitForConfirmation=False)

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main Loop

# =================== Region: Student Input =================== 
# Runs a command line prompt to set the pose [x,y,z, roll, pitch, yaw] 
# of the spawned checkered board.
MAXSPACE = 1000 #m
try: 
    while True:
        text = "Enter location of checkerboard in space X,Y,Z,Roll,Pitch,Yaw. All values should be floating points, separated by a comma, and angles in radians:.. "
        checkerBoardPose = input(text)
        userDefinedLocation = np.array(checkerBoardPose.split(","), dtype= np.float32)
        numLocations = len(userDefinedLocation)
        print("your input is: ",userDefinedLocation )
        try: 
            if userDefinedLocation[2] < 0:
                print("Board bellow ground, setting height to 0")
                userDefinedLocation[2] = 0
            if np.absolute(userDefinedLocation[0]) > MAXSPACE or np.absolute(userDefinedLocation[1]) > MAXSPACE :
                text = "cannot spawn object outside of workspace. Setting spawn location to origin."
                print(text)
                userDefinedLocation[0] = 0
                userDefinedLocation[1] = 0
                
        except numLocations > 6 or numLocations < 6:
            text ="Invalid locations entries! setting spawn point to origin with zero orientations"
            print(text)
            userDefinedLocation = np.zeros((1,6), dtype= np.float32)


        chessBoardLocation    = userDefinedLocation[0:3]
        chessBoardOrientation = userDefinedLocation[3:6]
        chessBoardScale       = [1, 0.05, 1]

        box1RefFrame.set_transform(location = chessBoardLocation, 
                                rotation = chessBoardOrientation, 
                                scale    =  [1,1,1], 
                                waitForConfirmation = True)

        box1.set_transform(location = chessBoardLocation, 
                                rotation = chessBoardOrientation, 
                                scale    =  chessBoardScale, 
                                waitForConfirmation = True)
    
except KeyboardInterrupt: 
    qlabs.close()
    print("Done!")  
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
