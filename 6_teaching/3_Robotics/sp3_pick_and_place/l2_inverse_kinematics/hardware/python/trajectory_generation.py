#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#--------------Lab 2 - Inverse Kinematics - Trajectory Generation-------------#
#-----------------------------------------------------------------------------#

# imports
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniKeyboardNavigator, QArmMiniFunctions, \
                                   DataIO, PlotData
from pal.utilities.keyboard import QKeyboard
from pal.utilities.timing   import QTimer
import numpy as np

## Section A - Setup
poseDataCmd, poseDataMeas = [], []

## Section B - Initialization
kbd         = QKeyboard()
myMiniArm   = QArmMini(hardware=1, id=8)
kbdNav      = QArmMiniKeyboardNavigator(kbd, initialPose=myMiniArm.HOME_POSE)
timer       = QTimer(sampleRate=30.0, totalTime=300.0)
myArmMath   = QArmMiniFunctions()

# Define individual positions (as column vectors)
home = np.array([0.256, 0, 0.256, 0])
A = np.array([0.12, -0.08, 0.05, -np.pi/2])
B = np.array([0.12,  0.08, 0.05, -np.pi/2])
C = np.array([0.18,  0.08, 0.05, -np.pi/2])
D = np.array([0.18, -0.08, 0.05, -np.pi/2])
rest = np.array([0.12, -0.08, 0.10, -np.pi/2])

# Stack waypoints horizontally and transpose (4xN matrix)
waypoints = np.array([rest, A, B, C, D, A]).T

try:
    # Initialize previous joint angles to home pose (used for inverse kinematics continuity)
    thetaPrev = myMiniArm.HOME_POSE
    while timer.check():
        # Forward kinematics: calculate current end-effector position from measured joint angles
        pose, rotationMatrix, gamma = myArmMath.forward_kinematics(myMiniArm.positionMeasured)
        # Get next waypoint info for trajectory generation
        Pf, Pi, time_vector, waypoint_number = myArmMath.waypoint_navigator(
            3.0,                            # Duration to move between each waypoint
            waypoints,                      # 4xN list of waypoints
            timer.get_current_time(),       # Current elapsed time since start
            pose                            # Current end-effector pose as initial position
        )

        # Generate cubic spline coefficients for smooth interpolation between Pi and Pf
        coefficients = myArmMath.cubic_spline(3.0, Pf, Pi)
        # Ensure time_vector is a column vector (4, 1)
        time_vector = time_vector.reshape((4, 1))

        # Multiply coefficients (3x4) by time_vector (4x1) → result is (3x1): [x, y, z]
        position = np.matmul(coefficients, time_vector)

        # flatten to get it as a 1D array [x, y, z]
        position = position.flatten()

        # Inverse kinematics: compute joint angles for commanded end-effector position
        theta, indices, numSolutions, thetaOpt = myArmMath.inverse_kinematics(position, -np.pi/2, thetaPrev)

        ## Section D - QArm Mini writes
        myMiniArm.read_write_std(thetaOpt)
  
        ## Section E - Record data for plotting
        poseDataCmd .append(position)
        poseDataMeas.append(pose)

        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    # Section F - Plot data
    plotter = PlotData()
    plotter.plot3D2Curves(poseDataCmd, poseDataMeas)

    myMiniArm.terminate()

