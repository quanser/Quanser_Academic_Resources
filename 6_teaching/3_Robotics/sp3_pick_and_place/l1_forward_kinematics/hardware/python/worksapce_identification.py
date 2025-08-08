#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#-----------Lab 1 - Forward Kinematics - Workspace Identification-------------#
#-----------------------------------------------------------------------------#

# imports
import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, \
                                   QArmMiniFunctions, DataIO, PlotData
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing import QTimer

## Section A - Setup
poseData, jointData, timeData  = [], [], []
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware=1, id=8)
kbdNav      = QArmMiniKeyboardNavigator(keyboard=kbd, initialPose=myMiniArm.HOME_POSE)
myArmMath   = QArmMiniFunctions()
timer       = QTimer(sampleRate=30.0, totalTime=300.0)

try:
    # main loop
    while timer.check():
        kbd.update()

        ## Section C - QArm Mini hardware I/O
        myMiniArm.read_write_std(
            kbdNav.move_joints_with_keyboard(timer.get_sample_time(), speed=np.pi/4))

        ## Section D - Record data for plotting
        pose, rotationMatrix, gamma = myArmMath.forward_kinematics(myMiniArm.positionMeasured)

        if kbd.states[kbd.K_SPACE]:
            poseData .append(pose)
            jointData.append(myMiniArm.positionMeasured)
            timeData .append(timer.get_current_time())

        timer.sleep(verbose=False)

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section E - Plot data
    plotter = PlotData()
    plotter.plot3D1Curve(poseData)
    plotter.plot2DJointCurves(jointData, timeData)

    # Section F - Save data
    dataHandler = DataIO(filename='end_effector_data.csv')
    dataHandler.write(poseData, mode='end-effector-pose')

    # terminate devices
    myMiniArm.terminate()