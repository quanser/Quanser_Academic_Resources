#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#--------------Lab 1 - Forward Kinematics - Lead Through: Learn---------------#
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
jointData, poseData, timeData        = [], [], []

## Section B - Initialization
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware = 1, id = 8,
                       boardSpecificOptions = ('j0_mode=1;j1_mode=1;j2_mode=1;j3_mode=1;gripper_mode=1;'))
myArmMath   = QArmMiniFunctions()
timer       = QTimer(sampleRate=30.0, totalTime=300.0)

try:
    # main loop
    while timer.check():
        kbd.update()

        ## Section C - QArm Mini PWM logic
        # update joint data
        myMiniArm.read_outputs()

        # generate saturated PWM cmd proportional to the measured speed of the QArm Mini
        pwmCmd = np.clip([gainBase, gainShoulder, gainElbow, gainWrist] * myMiniArm.speedMeasured,
                            [-0.3, -0.4, -0.3, -0.3],
                            [0.3, 0.4, 0.3, 0.3])

        # write PWM cmd to the joints
        myMiniArm.write_joint_PWM(pwmCmd)

        ## Section D - Data recording
        if kbd.states[kbd.K_SPACE]:
            pose, _, _ = myArmMath.forward_kinematics(myMiniArm.positionMeasured)
            jointData.append(myMiniArm.positionMeasured)
            poseData.append(pose)
            timeData.append(timer.get_current_time())

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section E - Plot data
    plotter = PlotData()
    plotter.plot3D1Curve(poseData)
    plotter.plot2DJointCurves(jointData, timeData)

    ## Section F - Save data
    dataHandler = DataIO(filename='end_effector_data.csv')
    dataHandler.write(jointData, mode='joints')

    # terminate devices
    myMiniArm.terminate()