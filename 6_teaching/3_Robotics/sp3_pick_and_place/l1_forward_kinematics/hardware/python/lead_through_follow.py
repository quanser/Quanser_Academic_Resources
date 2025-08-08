#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#--------------Lab 1 - Forward Kinematics - Lead Through: Follow--------------#
#-----------------------------------------------------------------------------#

# imports
import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniFunctions, DataIO, PlotData
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing import QTimer

## Section A - Setup
gainBase        = 0.25
gainShoulder    = 0.40
gainElbow       = 0.25
gainWrist       = 0.25
poseDataCmd, poseDataMeas, jointDataCmd, jointDataMeas, timeData  = \
                                    [], [], [], [], []

## Section B - Initialization
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware = 1, id = 8)
myArmMath   = QArmMiniFunctions()
timer       = QTimer(sampleRate=30.0, totalTime=300.0)

## Section C - read saved Data
dataHandler = DataIO(filename='end_effector_data.csv')
data, numRows = dataHandler.read()
counter = 0

try:
    # main loop
    while timer.check():
        kbd.update()
        ## Section D - QArm Mini writes
        myMiniArm.read_write_std(np.array(data[counter], dtype=np.float64))

        ## Section E - Record data for plotting
        poseC, _, _ = myArmMath.forward_kinematics(data[counter])
        poseM, _, _ = myArmMath.forward_kinematics(myMiniArm.positionMeasured)
        poseDataCmd  .append(poseC)
        jointDataCmd .append(data[counter])
        poseDataMeas .append(poseM)
        jointDataMeas.append(myMiniArm.positionMeasured)
        timeData     .append(timer.get_current_time())

        # continue repeating command curves
        if counter == numRows:
            counter = -1
        counter = counter + 1

        # break if user taps space bar
        if kbd.states[kbd.K_SPACE]:
            break

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section F - Plot data
    plotter = PlotData()
    plotter.plot3D2Curves(poseDataCmd, poseDataMeas)
    plotter.plot2D2JointCurves(jointDataCmd, jointDataMeas, timeData)

    # terminate devices
    myMiniArm.terminate()
