#-----------------------------------------------------------------------------#
#---------------------Quick Start Guide - QArm Mini --------------------------#
#-----------------------------------------------------------------------------#
#-----------------------------------------------------------------------------#

# imports
import numpy as np
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, \
                                   QArmMiniFunctions
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer

## Section A - Setup
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware=1, id=7)
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

        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:

    # terminate devices
    myMiniArm.terminate()