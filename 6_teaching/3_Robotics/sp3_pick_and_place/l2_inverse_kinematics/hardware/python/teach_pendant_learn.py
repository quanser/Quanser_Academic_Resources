#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#--------------Lab 2 - Inverse Kinematics - Teach Pendant: Learn--------------#
#-----------------------------------------------------------------------------#

# imports
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, QArmMiniFunctions, \
                                   DataIO, PlotData
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer
import numpy as np

## Section A - Setup
jointData, poseData, timeData        = [], [], []

## Section B - Initialization
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware=1, id=3)
kbdNav      = QArmMiniKeyboardNavigator(kbd, initialPose=myMiniArm.HOME_POSE)
timer       = QTimer(sampleRate=10.0, totalTime=300.0)
myArmMath   = QArmMiniFunctions()
prev        = 0

try:
    prevTime = timer.get_current_time()
    while timer.check():
        kbd.update()

        # To move one cartesian axis or gamma at a time w/ x, y, z, g
        myMiniArm.read_write_std(
            kbdNav.move_ee_with_keyboard(timer.get_current_time() - prevTime))
        prevTime =  timer.get_current_time()

        ## Section D - Record data for plotting
        pose, rotationMatrix, gamma = myArmMath.forward_kinematics(myMiniArm.positionMeasured)

        if not prev and kbd.states[kbd.K_SPACE]:
            poseData .append(np.array(np.append(pose, gamma), dtype=np.float64))
            jointData.append(myMiniArm.positionMeasured)
            timeData .append(timer.get_current_time())
        prev = kbd.states[kbd.K_SPACE]

        print('position (x, y, z):', pose)

        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section E - Plot data
    plotter = PlotData()
    plotter.plot2DJointCurves(jointData, timeData)

    # Section F - Save data
    dataHandler = DataIO(filename='end_effector_data.csv')
    dataHandler.write(poseData, mode='end-effector-pose')

    myMiniArm.terminate()

