#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#--------------Lab 2 - Inverse Kinematics - Teach Pendant: Follow-------------#
#-----------------------------------------------------------------------------#

# imports
import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniFunctions, DataIO, PlotData
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer

## Section A - Setup
poseDataCmd, poseDataMeas, timeData        = [], [], []

## Section B - Initialization
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware = 1, id = 8)
myArmMath   = QArmMiniFunctions()
timer       = QTimer(sampleRate=20.0, totalTime=300.0)
threshold   = 3

## Section C - read saved Data
dataHandler = DataIO(filename='end_effector_data.csv')
data, numRows = dataHandler.read()
counter = 0

try:
    thetaPrev = myMiniArm.HOME_POSE
    # main loop
    while timer.check():
        kbd.update()

        # Compute inverse kinematics
        theta, indices, numSolutions, thetaOpt = myArmMath.inverse_kinematics(data[counter][0:3], data[counter][3], thetaPrev)
            
        ## Section D - QArm Mini writes
        myMiniArm.read_write_std(thetaOpt)

        ## Section E - Record data for plotting
        poseC = data[counter]
        poseM, _, _ = myArmMath.forward_kinematics(myMiniArm.positionMeasured)
        poseDataCmd .append(poseC)
        poseDataMeas.append(poseM)
        timeData    .append(timer.get_current_time())    
        # continue repeating command curves
        if timer.get_current_time() > threshold:
            counter = counter +  1
            if counter == numRows:
                counter = 0
            threshold = timer.get_current_time() + 3

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section F - Plot data
    plotter = PlotData()
    plotter.plot3D2Curves(poseDataCmd, poseDataMeas)

    # terminate devices
    myMiniArm.terminate()