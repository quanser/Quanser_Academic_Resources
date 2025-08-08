#-----------------------------------------------------------------------------#
#------------------Skills Progression 3 - Pick and Place----------------------#
#-----------------------------------------------------------------------------#
#---------------------Lab 4 - Vision - Visual Servoing------------------------#
#-----------------------------------------------------------------------------#

# imports
from pal.products.qarm_mini import QArmMini
from hal.content.qarm_mini import QArmMiniFunctions
from pal.utilities.timing import QTimer
import cv2
import numpy as np
from hal.content.qarm_mini import QArmMiniImageProcessing as IP
from pal.utilities.vision import Camera2D
from pal.utilities.keyboard import QKeyboard
from pal.utilities.math import Integrator

## Section A - Initialization
myMiniArm   = QArmMini(hardware=1, id=8)
timer       = QTimer(sampleRate=10.0, totalTime=300.0)
kbd         = QKeyboard()
myArmMath   = QArmMiniFunctions()
myProcessor = IP()
boxed_image = None
myCam = Camera2D("0", frameWidth=640, frameHeight=360, frameRate=30)

joint_0 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
joint_1 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
joint_2 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
joint_3 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
mode    = 0 # mode = 1 (2 joints mode); mode = 2 (All joints mode) 

try:
    while timer.check():
        
        ## Section B - QArm Mini hardware I/O
        myMiniArm.read_write_std(joints=myMiniArm.HOME_POSE)

        ## Section C - Image Processing
        myCam.read()
        blur        = myProcessor.guassian_blur(myCam.imageData)
        hsv         = myProcessor.convert(blur, cv2.COLOR_BGR2HSV)
        colorThresh = myProcessor.threshold_color(hsv,(80, 180, 150), (50, 40, 70))
        mask_opened = myProcessor.open(colorThresh, 7, 5)
        mask_closed = myProcessor.close(mask_opened, 7, 5)
        grayscale   = myProcessor.convert(blur, cv2.COLOR_BGR2GRAY)
        highlight   = myProcessor.highlight(blur, colorThresh)
        c, r, area  = myProcessor.find_objects(mask_closed, 8, 500, 5000)
        if c is not None and r is not None:
            boxed_image = myProcessor.draw_box_on_detection(highlight, c, r, area)
        
        # cv2.imshow('Camera Feed', myCam.imageData)

        ## Section D - Visual Servoing
        # Check if a valid detection exists and visual servoing mode is set to 2 joints
        if boxed_image is not None and boxed_image.size > 300 and r is not None and c is not None and mode == 1:
            cv2.imshow('Boxed Image', boxed_image)

            # Define error in pixels
            err_y = r - 360 // 2 # vertical offset (image height)
            err_x = c - 640 // 2 # horizontal offset (image width)

            # Convert to rad/s (positive err_x = move right, err_y = move down)
            val_base  = -(np.pi / 6) / 320 * err_x   # base should respond to left/right
            val_elbow = -(np.pi / 6) / 180 * err_y   # elbow should respond to up/down

            # Scale and package into joint command array
            output = np.array([val_base, 0, val_elbow, 0], dtype=np.float64) * 0.5
            
            # Integrate joint velocities
            joint_0.integrate(output[0], timer.get_sample_time())
            joint_2.integrate(output[2], timer.get_sample_time())
            
            # Compute new joint positions and move the arm
            integrated_joints = np.array([joint_0.integrand, 0, joint_2.integrand, 0], dtype=np.float64)
            myMiniArm.read_write_std(joints=myMiniArm.HOME_POSE + integrated_joints)
        #----------------------------------------------------------------------------------------------------------------------#
        
        # Check if a valid detection exists and visual servoing mode is set to all joints
        elif boxed_image is not None and boxed_image.size > 300 and r is not None and c is not None and mode == 2:
            cv2.imshow('Boxed Image', boxed_image)
            
            # Calculate pixel error from image center
            err_x = 360 // 2 - r # vertical offset (image height)
            err_y = 640 // 2 - c # horizontal offset (image width)
            
            # Convert to rad/s (positive err_x = move right, err_y = move down)
            x_dir = 0.2 * (np.pi / 6) / 180 * err_x  # forward/backward motion
            y_dir = -0.2 * (np.pi / 6) / 320 * err_y # left/right motion
            z_dir = 0

            # Desired EE velocity vector in end-effector frame
            EE_velocity = np.array([
                [x_dir],
                [y_dir],
                [z_dir],
            ])

            # Get current pose, rotation matrix, and Jacobian
            pose, rotationMatrix, gamma = myArmMath.forward_kinematics(myMiniArm.positionMeasured)
            J, c, r, J_inv = myArmMath.differential_kinematics(myMiniArm.positionMeasured)

            # Transform velocity to base frame and add zero angular velocity
            _0_v_e = np.matmul(rotationMatrix, EE_velocity)
            _0_v_e = np.vstack((_0_v_e, [[0.0]]))  # adds a fourth row
            
            # Compute joint velocities using Jacobian inverse
            joint_velocities = np.matmul(J_inv, _0_v_e, dtype=np.float64)
            val0, val1, val2, val3 = joint_velocities.flatten()

            # Package joint velocities and integrate over time
            output = np.array([val0, val1, val2, val3], dtype=np.float64)
            joint_0.integrate(output[0], timer.get_sample_time())
            joint_1.integrate(output[1], timer.get_sample_time())
            joint_2.integrate(output[2], timer.get_sample_time())
            joint_3.integrate(output[3], timer.get_sample_time())

            # Command updated joint positions to the arm
            integrated_joints = np.array([joint_0.integrand, joint_1.integrand, joint_2.integrand, joint_3.integrand], dtype=np.float64)
            myMiniArm.read_write_std(joints=myMiniArm.HOME_POSE + integrated_joints)

        if r is None and c is None:
            joint_0 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
            joint_1 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
            joint_2 = Integrator(0, -2*np.pi/6, 2*np.pi/6)
            joint_3 = Integrator(0, -2*np.pi/6, 2*np.pi/6)

        cv2.waitKey(5)
        timer.sleep()

except KeyboardInterrupt:
    print('Received user terminate command.')

finally:
    myCam.terminate
    myMiniArm.terminate()