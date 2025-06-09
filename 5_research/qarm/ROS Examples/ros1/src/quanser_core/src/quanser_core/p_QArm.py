import numpy as np
import time

from quanser.hardware import HIL, HILError, PWMMode, MAX_STRING_LENGTH
from .q_misc import Utilities
saturate = Utilities.saturate

class QArm():
    '''QArm class for initialization, I/O and termination'''
    #region: Channel and Buffer definitions
    # Other Writes 
    write_other_channels = np.array([1000, 1001, 1002, 1003, 1004, 11000, 11001, 11002, 11003, 11005, 11006, 11007], dtype=np.int32)
    write_other_buffer = np.zeros(12, dtype=np.float64)
    write_LED_channels = np.array([11005, 11006, 11007], dtype=np.int32)
    write_LED_buffer = np.array([1,0,0], dtype=np.float64)

    # Other Reads
    read_other_channels = np.array([1000, 1001, 1002, 1003, 1004, 3000, 3001, 3002, 3003, 3004, 10000, 10001, 10002, 10003, 10004, 11000, 11001, 11002, 11003, 11004], dtype=np.int32)
    read_other_buffer = np.zeros(20, dtype=np.float64)
    
    # User LEDs Write Only - Other channel 11004:11007 are User LEDs
    read_analog_channels = np.array([5, 6, 7, 8, 9], dtype=np.int32)
    read_analog_buffer = np.zeros(5, dtype=np.float64)

    measJointCurrent = np.zeros(5, dtype=np.float64)
    measJointPosition = np.zeros(5, dtype=np.float64)
    measJointSpeed = np.zeros(5, dtype=np.float64)
    measJointPWM= np.zeros(5, dtype=np.float64)
    measJointTemperature = np.zeros(5, dtype=np.float64)    
    status = False
    #endregion

    def __init__(self):
        ''' This function configures the QArm in Position (0) or PWM (1) mode based on the input, and returns a handle to the card. Use the handle for other read/write methods. .'''
        
        self.mode = 0 # Only Position Mode is tested and available in Python
        self.hardware = 1 # Only Hardware support is enabled.
        self.card = HIL()
        if self.hardware:
            board_identifier = "0"
        else:
            board_identifier = "0@tcpip://localhost:18900?nagle='off'"

        board_specific_options = f"j0_mode={int(self.mode)};j1_mode={int(self.mode)};j2_mode={int(self.mode)};j3_mode={int(self.mode)};gripper_mode=0;j0_profile_config=0;j0_profile_velocity=1.5708;j0_profile_acceleration=1.0472;j1_profile_config=0;j1_profile_velocity=1.5708;j1_profile_acceleration=1.0472;j2_profile_config=0;j2_profile_velocity=1.5708;j2_profile_acceleration=1.0472;j3_profile_config=0;j3_profile_velocity=1.5708;j3_profile_acceleration=1.0472;"
        

        try:
            # Open the Card
            self.card.open("qarm_usb", board_identifier)
            if self.card.is_valid():
                self.card.set_card_specific_options(board_specific_options, MAX_STRING_LENGTH)
                self.status = True
                if self.mode:
                    print('QArm configured in PWM Mode.')
                else:
                    print('QArm configured in Position Mode.')
        
        except HILError as h:
            print(h.get_error_message())  


    def terminate(self):
        ''' This function terminates the QArm card after setting final values for home position and 0 pwm.'''
        
        # Other channel 1000 is steering, 11008:11011 are 4x indicators, and 11000:11003 are 4x lamps  
        self.write_other_buffer = np.zeros(12, dtype=np.float64)
        
        try:    
            # self.card.write(None, 0, None, 0, None, 0, self.write_other_channels, 12, 
            #                     None, None, None, self.write_other_buffer)
            self.card.close()
            print('QArm terminated successfully.')
            
        except HILError as h:
            print(h.get_error_message())

    def read_write_std(self, phiCMD=np.zeros(4, dtype=np.float64), grpCMD=np.zeros(1, dtype=np.float64), baseLED=np.array([1, 0, 0], dtype=np.float64)):
        '''Use this to write motor and LED commands, and read the battery voltage, motor current and encoder counts \n

        INPUTS:
        phiCMD - angular position of joints 1 to 4 as a 4x1 numpy array (active in Position mode only)
        grpCMD - gripper position 1x1 numpy array 
        baseLED - base RGB LED state as a 3x1 numpy array 

        OUTPUTS:
        None, use the self variables - measJointCurrent, measJointPosition, measJointSpeed, measJointPWM and measJointTemperature'''
        self.write_other_buffer[4] = saturate(grpCMD,0.9,0.1) # Saturate gripper between 0.1 (open) and 0.9 (close)
        self.write_other_buffer[9:12] = baseLED

        if self.mode:
            self.write_other_buffer[5:9] = np.zeros(4, dtype=np.float64)
        else:
            self.write_other_buffer[0:4] = phiCMD
        
        # IO
        try:
            if True:
                #Writes: Analog Channel, Num Analog Channel, PWM Channel, Num PWM Channel, Digital Channel, Num Digital Channel, Other Channel, Num Other Channel, Analog Buffer, PWM Buffer, Digital Buffer, Other Buffer           
                self.card.write(None, 0, None, 0, None, 0, self.write_other_channels, 12, 
                                None, None, None, self.write_other_buffer)

                #Reads: Analog Channel, Num Analog Channel, PWM Channel, Num PWM Channel, Digital Channel, Num Digital Channel, Other Channel, Num Other Channel, Analog Buffer, PWM Buffer, Digital Buffer, Other Buffer
                self.card.read(self.read_analog_channels, 5, None, 0, None, 0, self.read_other_channels, 20, 
                                self.read_analog_buffer, None, None, self.read_other_buffer)

                self.measJointCurrent = self.read_analog_buffer
                self.measJointPosition = self.read_other_buffer[0:5]
                self.measJointSpeed = self.read_other_buffer[5:10]
                self.measJointPWM = self.read_other_buffer[15:20]
                self.measJointTemperature = self.read_other_buffer[10:15]    

        except HILError as h:
            print(h.get_error_message())

        finally:
            pass

    def read_std(self):
        '''Use this to read the battery voltage, motor current and encoder counts \n

        OUTPUTS:
        Use the class variables - measJointCurrent, measJointPosition, measJointSpeed, measJointPWM and measJointTemperature'''
        
        # IO
        try:
            if True:
                #Reads: Analog Channel, Num Analog Channel, PWM Channel, Num PWM Channel, Digital Channel, Num Digital Channel, Other Channel, Num Other Channel, Analog Buffer, PWM Buffer, Digital Buffer, Other Buffer
                self.card.read(self.read_analog_channels, 5, None, 0, None, 0, self.read_other_channels, 20, 
                                self.read_analog_buffer, None, None, self.read_other_buffer)

                self.measJointCurrent = self.read_analog_buffer
                self.measJointPosition = self.read_other_buffer[0:5]
                self.measJointSpeed = self.read_other_buffer[5:10]
                self.measJointPWM = self.read_other_buffer[15:20]
                self.measJointTemperature = self.read_other_buffer[10:15]    

        except HILError as h:
            print(h.get_error_message())

        finally:
            pass

    def write_LEDs(self, baseLED=np.array([1, 0, 0], dtype=np.float64)):
        '''Use this to write LED commands (eg. to verify functionality HIL Card access) \n

        INPUTS:
        baseLED - base RGB LED state as a 3x1 numpy array '''
        self.write_LED_buffer = baseLED
       
        # IO
        try:
            if True:
                #Writes: Analog Channel, Num Analog Channel, PWM Channel, Num PWM Channel, Digital Channel, Num Digital Channel, Other Channel, Num Other Channel, Analog Buffer, PWM Buffer, Digital Buffer, Other Buffer           
                self.card.write(None, 0, None, 0, None, 0, self.write_LED_channels, 3, 
                                None, None, None, self.write_LED_buffer)  

        except HILError as h:
            print(h.get_error_message())

        finally:
            pass

class QArmUtilities():
    '''QArm utilities, such as Forward/Inverse Kinematics, Differential Kinematics etc.'''
    #region: QArm Parameters
    
    L1 = 0.1400
    L2 = 0.3500
    L3 = 0.0500
    L4 = 0.2500
    L5 = 0.1500
    beta = np.arctan(L3/L2)

    lambda1 = L1
    lambda2 = np.sqrt(L2**2 + L3**2)
    lambda3 = L4 + L5
    #endregion

    @staticmethod
    def take_user_input_joint_space():
        '''Use this method to take a user input for joint commands. Note that this method pauses execution until it returns. This is elegantly useful with the Position Mode on the QArm, which uses low level trajectory generation.'''
        stringCmd = input("Where should the arm go? Enter floating point values separated by commas for the base, shoulder, elbow, wrist, and gripper.\nAll joints are floats, gripper is boolean. Type Ctrl+C to exit)\n")
        try:
            stringCmd = stringCmd.split(',')
            result = np.array([float(stringCmd[i]) for i in range(len(stringCmd))])
        except:
            print("Invalid entry. Going HOME instead. Please try again.")
            result = np.array([0, 0, 0, 0, 0])
        finally:
            return result 

    @staticmethod
    def take_user_input_task_space():
        '''Use this method to take a user input for end-effector position commands. Note that this method pauses execution until it returns. Note that this uses joint level trajectory generation, so the end-effector path will not be linear.'''
        stringCmd = input("Where should the end-effector go? Enter floating point values separated by commas for the X, Y, Z, and gripper.\nAll values are floats, gripper is boolean. Type Ctrl+C to exit)\n")
        try:
            stringCmd = stringCmd.split(',')
            result = np.array([float(stringCmd[i]) for i in range(len(stringCmd))])
        except:
            print("Invalid entry. Going HOME instead. Please try again.")
            result = np.array([0.45, 0.00, 0.49, 0])
        finally:
            return result

    def qarm_forward_kinematics(self, phi):
        ''' QUANSER_ARM_FPK v 1.0 - 30th August 2020

        REFERENCE: 
        Chapter 3. Forward Kinematics
        Robot Dynamics and Control, Spong, Vidyasagar, 1989
        
        INPUTS:
        phi     : Alternate joint angles vector 4 x 1

        OUTPUTS:
        p4      : End-effector frame {4} position vector expressed in base frame {0}
        R04     : rotation matrix from end-effector frame {4} to base frame {0}'''

        # From phi space to theta space 
        theta = phi
        theta[0] = phi[0]
        theta[1] = phi[1] + self.beta - np.pi/2
        theta[2] = phi[2] - self.beta
        theta[3] = phi[3]

        # Transformation matrices for all frames:

        # T{i-1}{i} = quanser_arm_DH(  a, alpha,  d,     theta )
        T01 = self.quanser_arm_DH(            0, -np.pi/2, self.lambda1,  theta[0] )
        T12 = self.quanser_arm_DH( self.lambda2,        0,            0,  theta[1] )
        T23 = self.quanser_arm_DH(            0, -np.pi/2,            0,  theta[2] )
        T34 = self.quanser_arm_DH(            0,        0, self.lambda3,  theta[3] )

        T02 = T01@T12
        T03 = T02@T23
        T04 = T03@T34

        # Position of end-effector Transformation

        # Extract the Position vector 
        # p1   = T01(1:3,4);
        # p2   = T02(1:3,4);
        # p3   = T03(1:3,4);
        p4   = T04[0:3,3]

        # Extract the Rotation matrix
        # R01 = T01(1:3,1:3);
        # R02 = T02(1:3,1:3);
        # R03 = T03(1:3,1:3);
        R04 = T04[0:3,0:3]

        return p4, R04
    
    def qarm_inverse_kinematics(self, p, gamma, phi_prev):
        '''QUANSER_ARM_IPK v 1.0 - 31st August 2020

        REFERENCE: 
        Chapter 4. Inverse Kinematics
        Robot Dynamics and Control, Spong, Vidyasagar, 1989

        INPUTS:
        p        : end-effector position vector expressed in base frame {0}
        gamma    : wrist rotation angle gamma

        OUTPUTS:
        phi_optimal : Best solution depending on phi_prev
        phi         : All four Inverse Kinematics solutions as a 4x4 matrix. 
                      Each col is a solution.'''

        # Initialization
        theta   = np.zeros((4, 4), dtype=np.float64)
        phi = np.zeros((4, 4), dtype=np.float64)
 
        # Equations:
        # lambda2 cos(theta2) + (-lambda3) sin(theta2 + theta3) = sqrt(x^2 + y^2)
        #   A     cos( 2    ) +     C      sin(   2   +    3  ) =    D
            
        # lambda2 sin(theta2) - (-lambda3) cos(theta2 + theta3) = lambda1 - z
        #   A     sin( 2    ) -     C      cos(   2   +    3  ) =    H
        
        # Solution:
        def inv_kin_setup(p):
            A = self.lambda2
            C = -self.lambda3
            H =  self.lambda1 - p[2]
            D1 = -np.sqrt(p[0]**2 + p[1]**2)
            D2 =  np.sqrt(p[0]**2 + p[1]**2)
            F = (D1**2 + H**2 - A**2 - C**2)/(2*A)
            return A, C, H, D1, D2, F

        def solve_case_C_j2(j3, A, C, D, H):
            M = A + C*np.sin(j3)
            N = -C*np.cos(j3)
            cos_term = (D*M + H*N)/(M**2 + N**2)
            sin_term = (H - N*cos_term)/(M)
            j2 = np.arctan2(sin_term, cos_term)
            return j2

        A, C, H, D1, D2, F = inv_kin_setup(p)
        
        # Joint 3 solution:
        theta[2,0] = 2*np.arctan2( C + np.sqrt(C**2 - F**2) , F )
        theta[2,1] = 2*np.arctan2( C - np.sqrt(C**2 - F**2) , F )
        theta[2,2] = 2*np.arctan2( C + np.sqrt(C**2 - F**2) , F )
        theta[2,3] = 2*np.arctan2( C - np.sqrt(C**2 - F**2) , F )
        
        # Joint 2 solution:
        theta[1,0] = solve_case_C_j2(theta[2,0], A, C, D1, H)
        theta[1,1] = solve_case_C_j2(theta[2,1], A, C, D1, H)
        theta[1,2] = solve_case_C_j2(theta[2,2], A, C, D2, H)
        theta[1,3] = solve_case_C_j2(theta[2,3], A, C, D2, H)
        
        # Joint 1 solution:
        theta[0,0] = np.arctan2( p[1]/( self.lambda2 * np.cos( theta[1,0] ) - self.lambda3 * np.sin( theta[1,0] + theta[2,0] ) ) ,
                                 p[0]/( self.lambda2 * np.cos( theta[1,0] ) - self.lambda3 * np.sin( theta[1,0] + theta[2,0] )  ) )
        theta[0,1] = np.arctan2( p[1]/( self.lambda2 * np.cos( theta[1,1] ) - self.lambda3 * np.sin( theta[1,1] + theta[2,1] ) ) ,
                                 p[0]/( self.lambda2 * np.cos( theta[1,1] ) - self.lambda3 * np.sin( theta[1,1] + theta[2,1] )  ) )
        theta[0,2] = np.arctan2( p[1]/( self.lambda2 * np.cos( theta[1,2] ) - self.lambda3 * np.sin( theta[1,2] + theta[2,2] ) ) ,
                                 p[0]/( self.lambda2 * np.cos( theta[1,2] ) - self.lambda3 * np.sin( theta[1,2] + theta[2,2] )  ) )
        theta[0,3] = np.arctan2( p[1]/( self.lambda2 * np.cos( theta[1,3] ) - self.lambda3 * np.sin( theta[1,3] + theta[2,3] ) ) ,
                                 p[0]/( self.lambda2 * np.cos( theta[1,3] ) - self.lambda3 * np.sin( theta[1,3] + theta[2,3] )  ) )
            
        # Remap theta back to phi
        phi[0,:] = theta[0,:]
        phi[1,:] = theta[1,:] - self.beta + np.pi/2
        phi[2,:] = theta[2,:] + self.beta
        phi[3,:] = gamma*np.ones((4))

        phi = np.mod(phi + np.pi, 2*np.pi) - np.pi
        
        phi_optimal = phi[:,0]
        if np.linalg.norm(phi_optimal - phi_prev) > np.linalg.norm(phi[:,1] - phi_prev):
            phi_optimal = phi[:,1]
        if np.linalg.norm(phi_optimal - phi_prev) > np.linalg.norm(phi[:,2] - phi_prev):
            phi_optimal = phi[:,2]
        if np.linalg.norm(phi_optimal - phi_prev) > np.linalg.norm(phi[:,3] - phi_prev):
            phi_optimal = phi[:,3]

        return phi, phi_optimal

    def quanser_arm_DH(self, a, alpha, d, theta):

        ''' QUANSER_ARM_DH
        v 1.0 - 26th March 2019

        REFERENCE: 
        Chapter 3. Forward and Inverse Kinematics
        Robot Modeling and Control 
        Spong, Hutchinson, Vidyasagar
        2006

        INPUTS:
        a       :   translation  : along : x_{i}   : from : z_{i-1} : to : z_{i}
        alpha   :      rotation  : about : x_{i}   : from : z_{i-1} : to : z_{i}
        d       :   translation  : along : z_{i-1} : from : x_{i-1} : to : x_{i}
        theta   :      rotation  : about : z_{i-1} : from : x_{i-1} : to : x_{i}
        (Standard DH Parameters are being used here)

        OUTPUTS:
        T       : transformation                   : from :     {i} : to : {i-1}'''

        # Rotation Transformation about z axis by theta
        T_R_z = np.array([[np.cos(theta), -np.sin(theta), 0, 0], [np.sin(theta), np.cos(theta), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float64)
            
        # Translation Transformation along z axis by d
        T_T_z = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, d], [0, 0, 0, 1]], dtype=np.float64)

        # Translation Transformation along x axis by a
        T_T_x = np.array([[1, 0, 0, a], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float64)

        # Rotation Transformation about x axis by alpha
        T_R_x = np.array([[1, 0, 0, 0], [0, np.cos(alpha), -np.sin(alpha), 0], [0, np.sin(alpha), np.cos(alpha), 0], [0, 0, 0, 1]], dtype=np.float64)

        # For a transformation FROM frame {i} TO frame {i-1}: A
        T = T_R_z@T_T_z@T_T_x@T_R_x
        
        return T

    # def qarm_move_to_position(self, location):