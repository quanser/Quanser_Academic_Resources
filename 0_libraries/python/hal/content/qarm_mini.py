import numpy as np
import cv2
import numpy.linalg as npla
import csv
import matplotlib.pyplot as plt
from pal.products.qarm_mini import QArmMini
from pal.utilities.math import Integrator
from pal.utilities.keyboard import QKeyboard
#TODO: this code currently has not been tested.

class QArmMiniFunctions():
    """This class contains kinematic functions for the QArm Mini such as
    Forward/Inverse Position/Differential Kinematics etc. """

    # Manipulator parameters
    # The following variables are the length measurements of the links:
    L_1 = 0.1300
    L_2 = 0.1240
    L_3 = 0.0230
    L_4 = 0.1240
    L_5 = 0.1320

    # Lambda variables are the distances between joints:
    LAMBDA_1 = L_1
    LAMBDA_2 = np.sqrt(L_2**2 + L_3**2)
    LAMBDA_3 = L_4
    LAMBDA_4 = L_5

    def forward_kinematics(self, theta):
        """
        Implements the forward position kinematics for the QArm Mini.

        Parameters
        ----------
        theta : array_like
            A 4x1 array containing the joint angles.

        Returns
        -------
        posEndEffector : array_like
            A 3x1 array containing the end-effector position 0_p_0e
        rotMatrix05 : matrix
            The rotation matrix from base frame {0} to the end-effector frame {e}.
        gamma: float
            the end-effector orientation angle with respect to the horizontal plane.
        """

        # Transformation matrices for all frames:

        # transMatrix{i-1}{i} = quanser_DH(          a,    alpha,             d,     theta )
        transMatrix01 = self.quanser_DH(             0,  np.pi/2, self.LAMBDA_1,  theta[0] )
        transMatrix12 = self.quanser_DH( self.LAMBDA_2,        0,             0,  theta[1] )
        transMatrix23 = self.quanser_DH( self.LAMBDA_3,        0,             0,  theta[2] )
        transMatrix34 = self.quanser_DH(             0,  np.pi/2,             0,  theta[3] )
        transMatrix45 = self.quanser_DH(             0,        0, self.LAMBDA_4,         0 )

        # Tranformation matrix from
        transMatrix02 = transMatrix01@transMatrix12
        transMatrix03 = transMatrix02@transMatrix23
        transMatrix04 = transMatrix03@transMatrix34
        transMatrix05 = transMatrix04@transMatrix45

        # Position of end-effector Transformation

        # Extract the Position vector
        # p1   = T01[1:3,4]
        # p2   = T02[1:3,4]
        # p3   = T03[1:3,4]
        # p4   = T04[1:3,4]
        posEndEffector   = transMatrix05[0:3,3]

        # Extract the Rotation matrix
        # rotMatrix01 = transMatrix01[1:3,1:3]
        # rotMatrix02 = transMatrix02[1:3,1:3]
        # rotMatrix03 = transMatrix03[1:3,1:3]
        # rotMatrix04 = transMatrix04[1:3,1:3]
        rotMatrix05 = transMatrix05[0:3,0:3]

        gamma = theta[1] + theta[2] + theta[3] - np.pi/2

        #return the position of the end effector and the rotation matrix
        return posEndEffector, rotMatrix05, gamma

    def inverse_kinematics(self, posEndEffector, gamma, thetaPrevious):
        """
        Implements the inverse position kinematics for the QArm Mini.

        Parameters
        ----------
        posEndEffector : array_like
            A 3x1 array containing the end-effector position 0_p_0e
        gamma: float
            The end-effector orientation angle with respect to the horizontal plane.
        thetaPrevious : array_like
            The last measured joint angles of the manipulator.

        Returns
        -------
        theta : array_like
            A 4x4 array containing upto 4 possible solutions
        indices : array_like
            A 4x1 array contained validity indices. 1 represents a solution in
            the corresponding column of the theta output. 2 represents the
            optimal solution in the corresponding column of the theta output.
        numSolutions : array_like
            Total number of solutions found, anywhere from 0 to 4.
        thetaOpt : array_like
            The optimal solution closests to thetaPrevious.
        """

        # Initialization
        theta = np.zeros((4, 4), dtype=np.float64)

        thetaOpt = np.zeros((4, 1), dtype=np.float64)
        d1_flag = 0
        d2_flag = 0
        numSolutions = 0
        indices = np.zeros((4,1), dtype=np.float64)

        # Equations:
        # LAMBDA_2 cos(theta2) + (-LAMBDA_3) sin(theta2 + theta3) = sqrt(x^2 + y^2)
        #   A     cos( 2    ) +     C      sin(   2   +    3  ) =    D

        # LAMBDA_2 sin(theta2) - (-LAMBDA_3) cos(theta2 + theta3) = LAMBDA_1 - z
        #   A     sin( 2    ) -     C      cos(   2   +    3  ) =    H

        # Solution:
        def inv_kin_setup(posEndEffector, gamma):

            A = self.LAMBDA_2
            B = self.LAMBDA_3
            D1 = np.sqrt(posEndEffector[0]**2 + posEndEffector[1]**2) - self.LAMBDA_4*np.cos(gamma)
            D2 = -np.sqrt(posEndEffector[0]**2 + posEndEffector[1]**2) - self.LAMBDA_4*np.cos(gamma)
            H =  posEndEffector[2] - self.LAMBDA_1 - self.LAMBDA_4*np.sin(gamma)

            A_2 = A**2
            B_2 = B**2
            F1 = (D1**2 + H**2 - A_2 - B_2)/(2*A)
            F2 = (D2**2 + H**2 - A_2 - B_2)/(2*A)

            # Evaluate the total number of solutions. The solution for joint 3
            # requires us to calculate the square root of B^2 - F^2. For this, the
            # F1 and F2 terms cannot be larger than B in magnitude. Determining
            # which ones violate this condition will help us narrow down solutions
            # from 4 to 2 to 0. Note that this check does not eliminate solutions that
            # are not feasible due to joint limits, neither does it check for the
            # closest solution to thetaPrevious. That happens later.

            F1_2 = F1**2
            F2_2 = F2**2

             # Initialize flags
            d1_flag = 0
            d2_flag = 0
            numSolutions = 0

            if B_2 < F1_2 and B_2 < F2_2:
                # Both conditions are violated, so no solutions exist
                numSolutions = 0
            elif B_2 < F1_2 and B_2 >= F2_2:
                # F1 is a problem, F2 is not, 2 solutions exist
                numSolutions = 2
                d2_flag = 1
            elif B_2 < F2_2 and B_2 >= F1_2:
                # F2 is a problem, F1 is not, 2 solutions exist
                numSolutions = 2
                d1_flag = 1
            else:
                # 4 solutions exist theoretically!
                numSolutions = 4
                d1_flag = 1
                d2_flag = 1

            return A, B, H, D1, D2, F1, F2, numSolutions, d1_flag, d2_flag

        def check_joint_limits(theta):
            flag = 0

            if (theta[0] > QArmMini.LIMITS_MAX[0] or theta[0] < QArmMini.LIMITS_MIN[0] or
                theta[1] > QArmMini.LIMITS_MAX[1] or theta[1] < QArmMini.LIMITS_MIN[1] or
                theta[2] > QArmMini.LIMITS_MAX[2] or theta[2] < QArmMini.LIMITS_MIN[2] or
                theta[3] > QArmMini.LIMITS_MAX[3] or theta[3] < QArmMini.LIMITS_MIN[3]    ):
                flag = 1

            return flag

        A, B, H, D1, D2, F1, F2, numSolutions, d1_flag, d2_flag = inv_kin_setup(posEndEffector, gamma)

        if d1_flag:
            # there are 2 possible values for theta(3) based on the + or - sqrt.
            theta[2,0] = 2*np.arctan2(np.sqrt(B**2 - F1**2), B+F1)
            theta[2,1] = 2*np.arctan2(-np.sqrt(B**2 - F1**2), B+F1)

            indices[0] = 1
            indices[1] = 1
            # solve the 2 possible theta(1) values based on the theta(2) ones
            # that were just found.

            # theta(1,0) from theta(2,0)
            M =  B*np.cos(theta[2,0])
            N = B*np.sin(theta[2,0])
            cos_term = (D1*A + D1*M + H*N)/((A + M)**2 + N**2)
            sin_term = (H*A + H*M - D1*N)/((A + M)**2 + N**2)
            theta[1,0] = np.arctan2(sin_term, cos_term)

            # theta(1,1) from theta(2,1)
            M = B*np.cos(theta[2,1])
            N = B*np.sin(theta[2,1])
            cos_term = (D1*A + D1*M + H*N)/((A + M)**2 + N**2)
            sin_term = (H*A + H*M - D1*N)/((A + M)**2 + N**2)
            theta[1,1] = np.arctan2(sin_term, cos_term)

            # Find the two corresponding theta(1) solutions using theta(1) and theta(2)
            theta[0,0] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,0]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0] + theta[2,0]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,0]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0] + theta[2,0]) +self.LAMBDA_4*np.cos(gamma)))

            theta[0,1] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,1]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1] + theta[2,1]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,1]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1] + theta[2,1]) +self.LAMBDA_4*np.cos(gamma)))
            theta[3,0] = gamma + np.pi/2 - theta[1, 0] - theta[2, 0]
            theta[3,1] = gamma + np.pi/2 - theta[1, 1] - theta[2, 1]

        if d2_flag:
            # check if the 2 solutions below are solutions (1 & 2) or (3 & 4) based
            # on whether numSolutions was set to 4 or not. If you are here, it was
            # definitely 4 or 2.

            indexModifier = 2 if numSolutions == 4 else 0

            indices[0 + indexModifier] = 1
            indices[1 + indexModifier] = 1

            # there are 2 possible values for theta(2) based on the + or - sqrt.
            theta[2,0+indexModifier] = 2*np.arctan2(np.sqrt(B**2 - F2**2), B+F2)
            theta[2,1+indexModifier] = 2*np.arctan2(-np.sqrt(B**2 - F2**2), B+F2)

            # solve the 2 possible theta(1) values based on the theta(2) ones
            # that were just found.
            M = B*np.cos(theta[2,0 + indexModifier])
            N = B*np.sin(theta[2,0 + indexModifier])
            cos_term = (D2*A + D2*M + H*N)/((A + M)**2 + N**2)
            sin_term = (H*A + H*M - D2*N)/((A + M)**2 + N**2)
            theta[1,0+indexModifier] = np.arctan2(sin_term, cos_term)

            # theta(1,1) from theta(2,1)
            M = B*np.cos(theta[2,1 + indexModifier])
            N = B*np.sin(theta[2,1 + indexModifier])
            cos_term = (D2*A + D2*M + H*N)/((A + M)**2 + N**2)
            sin_term = (H*A + H*M - D2*N)/((A + M)**2 + N**2)
            theta[1,0+indexModifier] = np.arctan2(sin_term, cos_term)

            # Find the two corresponding theta(1) solutions using theta(1) and theta(2)

            theta[0,0 + indexModifier] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,0 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0 + indexModifier] + theta[2,0 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,0 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0 + indexModifier] + theta[2,0 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)))

            theta[0,1 + indexModifier] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,1 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1 + indexModifier] + theta[2,1 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,1 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1 + indexModifier] + theta[2,1 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)))

            # joint angle 3
            theta[3,0 + indexModifier] = gamma + np.pi/2 - theta[1, 0 + indexModifier] - theta[2, 0 + indexModifier]
            theta[3,1 + indexModifier] = gamma + np.pi/2 - theta[1, 1 + indexModifier] - theta[2, 1 + indexModifier]

        #Joint checks and final modifications
        numSolutionsMod = 0
        for x in range(numSolutions):
            if check_joint_limits(theta[:,x]):

                indices[x] = 0
                numSolutionsMod = numSolutionsMod - 1
        numSolutions = numSolutions + numSolutionsMod

        # find the solution from thetas that is closest to thetaPrev
        closestSolution = theta[:,1]
        mark = 1

        for x in range(1,4):
            if indices[x]:
                if npla.norm(theta[:,x]-thetaPrevious, 2) < npla.norm(closestSolution - thetaPrevious , 2):
                    closestSolution = theta[:,x]
                    mark = x

        indices[mark] = 2
        thetaOpt = theta[:, mark]

        return theta, indices, numSolutions, thetaOpt

    def differential_kinematics(self, theta):
        """
        Implements the differential kinematics for the QArm Mini.

        Parameters
        ----------
        theta : array_like
            A 4x1 array containing the joint angles.

        Returns
        -------
        J : matrix
            A 4x4  Jacobian matrix
        c : float
            The condition number of the Jacobian (inf at singularity).
        r : int
            The rank of the Jacobian ().
        J_inv : matrix
            The 4x4 inverse of the Jacobian.
        """
        # jacobian for the qarm mini

        J = np.identity(4)

        J[0,0] = -self.LAMBDA_2*np.sin(theta[0])*np.cos(theta[1]) - self.LAMBDA_3*np.sin(theta[0])*np.cos(theta[1] + theta[2]) - self.LAMBDA_4*np.sin(theta[0])*np.sin(theta[1] + theta[2] + theta[3])
        J[0,1] = -self.LAMBDA_2*np.cos(theta[0])*np.sin(theta[1]) - self.LAMBDA_3*np.cos(theta[0])*np.sin(theta[1] + theta[2]) + self.LAMBDA_4*np.cos(theta[0])*np.cos(theta[1] + theta[2] + theta[3])
        J[0,2] = -self.LAMBDA_3*np.cos(theta[0])*np.sin(theta[1] + theta[2]) + self.LAMBDA_4*np.cos(theta[0])*np.cos(theta[1] + theta[2] + theta[3])
        J[0,3] = self.LAMBDA_4*np.cos(theta[0])*np.cos(theta[1] + theta[2] + theta[3])

        J[1,0] = self.LAMBDA_2*np.cos(theta[0])*np.cos(theta[1]) + self.LAMBDA_3*np.cos(theta[0])*np.cos(theta[1]+theta[2]) + self.LAMBDA_4*np.cos(theta[0])*np.sin(theta[1] + theta[2] + theta[3])
        J[1,1] = -self.LAMBDA_2*np.sin(theta[0])*np.sin(theta[1]) - self.LAMBDA_3*np.sin(theta[0])*np.sin(theta[1]+theta[2]) + self.LAMBDA_4*np.sin(theta[0])*np.sin(theta[1] + theta[2] + theta[3])
        J[1,2] = -self.LAMBDA_3*np.sin(theta[0])*np.sin(theta[1] + theta[2]) + self.LAMBDA_4*np.sin(theta[0])*np.sin(theta[1] + theta[2] + theta[3])
        J[1,3] = self.LAMBDA_4*np.sin(theta[0])*np.sin(theta[1] + theta[2] + theta[3])

        J[2,0] = 0
        J[2,1] = self.LAMBDA_2*np.cos(theta[1]) + self.LAMBDA_3*np.cos(theta[1] + theta[2]) + self.LAMBDA_4*np.sin(theta[1] + theta[2] + theta[3])
        J[2,2] = self.LAMBDA_3*np.cos(theta[1] + theta[2]) + self.LAMBDA_4*np.sin(theta[1] + theta[2] + theta[3])
        J[2,3] = self.LAMBDA_4*np.sin(theta[1] + theta[2] + theta[3])

        J[3,0] = 0
        J[3,1] = 1
        J[3,2] = 1
        J[3,3] = 1

        c = npla.cond(J) #condition number for the Jacobian
        r = npla.matrix_rank(J) # rank number for the jacobian
        J_inv = npla.inv(J) # inverse of the jacobian matrix

        return J, c, r, J_inv
    
    def cubic_spline(self, T, Pf, Pi):
        """
        Generate cubic spline coefficients for X, Y, Z.
        
        Parameters:
            T  : Duration of the segment
            Pf : Final position (4D: x, y, z, gamma)
            Pi : Initial position (4D: x, y, z, gamma)

        Returns:
            coefficients : 3x4 matrix of spline coefficients for x, y, z
        """
        a0 = Pi[0:3]
        a1 = np.zeros(3)
        a2 = 3 * (Pf[0:3] - Pi[0:3]) / (T ** 2)
        a3 = -2 * (Pf[0:3] - Pi[0:3]) / (T ** 3)

        coefficients = np.column_stack((a0, a1, a2, a3))  # Shape: 3x4
        return coefficients
    
    def waypoint_navigator(self, duration, waypoints, total_time, current_position):
        """
        Parameters:
            duration         : Time in seconds between each waypoint transition
            waypoints        : 4xN matrix of waypoints
            dt               : Time step (sample time)
            total_time       : Current time from timer (in seconds)
            current_position : Current measured position of the robot (4D)
        
        Returns:
            Pf               : Final target pose for current segment
            Pi               : Initial pose (starting from current_position)
            time_vector      : [1, t, t^2, t^3] used for spline generation
            waypoint_number  : Current waypoint index
        """
        num_waypoints = waypoints.shape[1]

        # Get current segment index and time within the segment
        t_mod = total_time % duration
        segment_index = int(total_time // duration)

        # Loop the index when it exceeds the number of waypoints
        next_index = segment_index % num_waypoints

        # Final and initial positions
        Pf = waypoints[:, next_index]
        Pi = current_position
        time_vector = np.array([1, t_mod, t_mod**2, t_mod**3])
        waypoint_number = next_index

        return Pf, Pi, time_vector, waypoint_number

    def quanser_DH(self, a, alpha, d, theta):

        """
        QUANSER_DH
        v 1.0 - 26th March 2019
        REFERENCE:
        Chapter 3. Forward and Inverse Kinematics
        Robot Modeling and Control
        Spong, Hutchinson, Vidyasagar
        2006
        (Using standard DH parameters)

        :param a: translation along x_{i} from z_{i-1} to z_{i}
        :param alpha: rotation about x_{i} from z_{i-1} to z_{i}
        :param d: translation along z_{i-1} from x_{i-1} to x_{i}
        :param theta: rotation about z_{i-1} from x_{i-1} to x_{i}

        :return:
            -**T**: transformation from {i} to {i-1}
        """

        # Rotation Transformation about z axis by theta
        rotTFMatrixAboutZByTheta = np.array([[np.cos(theta), -np.sin(theta), 0, 0],
                                            [np.sin(theta), np.cos(theta), 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 0, 0, 1]], dtype=np.float64)

        # Translation Transformation along z axis by d
        transTFMatrixAlongZByD = np.array([[1, 0, 0, 0],
                                            [0, 1, 0, 0],
                                            [0, 0, 1, d],
                                            [0, 0, 0, 1]], dtype=np.float64)

        # Translation Transformation along x axis by a
        transTFMatrixAlongXByA = np.array([[1, 0, 0, a],
                                            [0, 1, 0, 0],
                                            [0, 0, 1, 0],
                                            [0, 0, 0, 1]], dtype=np.float64)

        # Rotation Transformation about x axis by alpha
        rotTFMatrixAlongXByAlpha = np.array([[1, 0, 0, 0],
                                            [0, np.cos(alpha), -np.sin(alpha), 0],
                                            [0, np.sin(alpha), np.cos(alpha), 0],
                                            [0, 0, 0, 1]], dtype=np.float64)

        # For a transformation FROM frame {i} TO frame {i-1}: A
        transMatrix = rotTFMatrixAboutZByTheta@transTFMatrixAlongZByD@transTFMatrixAlongXByA@rotTFMatrixAlongXByAlpha

        return transMatrix

class QArmMiniKeyboardNavigator():

    '''This class provides a range of methods that let you drive the QArm Mini
    manipulator using a KeyboardDriver class.

    Use the move_joints_with_keyboard method to control the manipulator one
    joint at a time (selected with keys 1 through 4) using the UP and DOWN
    arrow keys.

    Use the move_ee_with_keyboard method to control the manipulator's
    end-effector one cartesian axis or gamma at a time (selected with keys x,
    y, z, or g) using the UP and DOWN arrow keys. '''

    def __init__(self, keyboard, initialPose=QArmMini.HOME_POSE):

        self.kbd = keyboard #instance of KeyboardDriver from pal.utilities.keyboard
        self.armMath = QArmMiniFunctions()

        ee_position, ee_rotation, gamma = self.armMath.forward_kinematics(theta=initialPose)

        self.joint_0_integrator = Integrator(integrand=initialPose[0],
                                        minSaturation=QArmMini.LIMITS_MIN[0],
                                        maxSaturation=QArmMini.LIMITS_MAX[0])
        self.joint_1_integrator = Integrator(integrand=initialPose[1],
                                        minSaturation=QArmMini.LIMITS_MIN[1],
                                        maxSaturation=QArmMini.LIMITS_MAX[1])
        self.joint_2_integrator = Integrator(integrand=initialPose[2],
                                        minSaturation=QArmMini.LIMITS_MIN[2],
                                        maxSaturation=QArmMini.LIMITS_MAX[2])
        self.joint_3_integrator = Integrator(integrand=initialPose[3],
                                        minSaturation=QArmMini.LIMITS_MIN[3],
                                        maxSaturation=QArmMini.LIMITS_MAX[3])

        self.x_integrator = Integrator(integrand=ee_position[0])
        self.y_integrator = Integrator(integrand=ee_position[1])
        self.z_integrator = Integrator(integrand=ee_position[2])
        self.g_integrator = Integrator(integrand=gamma,
                                       minSaturation=-np.pi/2,
                                       maxSaturation=np.pi/2)

        self.j0Delta = self.joint_0_integrator.integrand
        self.j1Delta = self.joint_1_integrator.integrand
        self.j2Delta = self.joint_2_integrator.integrand
        self.j3Delta = self.joint_3_integrator.integrand

        self.xDelta = self.x_integrator.integrand
        self.yDelta = self.y_integrator.integrand
        self.zDelta = self.z_integrator.integrand
        self.gDelta = self.g_integrator.integrand

        self.current_joint_pose = initialPose
        self.current_ee_pose = ee_position
        self.current_gamma = gamma

        self.active_joint = None
        pass

    def activate_joint(self, mode='joint'):

        if mode=='joint':
            if self.kbd.states[self.kbd.K_1]:
                self.active_joint = 0 # joint 1 base yaw
            elif self.kbd.states[self.kbd.K_2]:
                self.active_joint = 1 # joint 2 shoulder pitch
            elif self.kbd.states[self.kbd.K_3]:
                self.active_joint = 2 # joint 3 elbow pitch
            elif self.kbd.states[self.kbd.K_4]:
                self.active_joint = 3 # joint 4 wrist pitch
        elif mode=='task':
            if self.kbd.states[self.kbd.K_X]:
                self.active_joint = 4 # base frame x
            elif self.kbd.states[self.kbd.K_Y]:
                self.active_joint = 5 # base frame y
            elif self.kbd.states[self.kbd.K_Z]:
                self.active_joint = 6 # base frame z
            elif self.kbd.states[self.kbd.K_G]:
                self.active_joint = 7 # base frame z
        else:
            self.active_joint = None

    def move_joints_with_keyboard(self, timestep, speed=np.pi/12):
        '''Tap the keyboard 1 through 4 keys to select a joint. Then use the
        UP and DOWN arrows to increase or decrease the joint's cmd
        respectively.'''

        if self.kbd.states[self.kbd.K_UP]:
            cmd = speed
        elif self.kbd.states[self.kbd.K_DOWN]:
            cmd = -1*speed
        else:
            cmd = 0
        self.activate_joint(mode='joint')

        if self.active_joint==0:
            self.j0Delta = self.joint_0_integrator.integrate(cmd, timestep)
        elif self.active_joint==1:
            self.j1Delta = self.joint_1_integrator.integrate(cmd, timestep)
        elif self.active_joint==2:
            self.j2Delta = self.joint_2_integrator.integrate(cmd, timestep)
        elif self.active_joint==3:
            self.j3Delta = self.joint_3_integrator.integrate(cmd, timestep)

        self.current_joint_pose = np.array([self.j0Delta, self.j1Delta, self.j2Delta, self.j3Delta], dtype=np.float64)

        return self.current_joint_pose

    def move_ee_with_keyboard(self, timestep, speed=0.05):
        '''Tap the keyboard x, y, z or g keys to select a cartesian x, y, z axis
        or the end-effector orientation angle gamma. Then use the
        UP and DOWN arrows to increase or decrease the corresponding cmd value.
        Note, the speed is multiplied by a factor of 10 for the end-effector
        angle Gamma.'''

        if self.kbd.states[self.kbd.K_UP]:
            cmd = speed
        elif self.kbd.states[self.kbd.K_DOWN]:
            cmd = -1*speed
        else:
            cmd = 0
        self.activate_joint(mode='task')

        xDelta = self.xDelta
        yDelta = self.yDelta
        zDelta = self.zDelta
        gDelta = self.gDelta

        if self.active_joint==4:
            xDelta = self.x_integrator.integrate(cmd, timestep)
        elif self.active_joint==5:
            yDelta = self.y_integrator.integrate(cmd, timestep)
        elif self.active_joint==6:
            zDelta = self.z_integrator.integrate(cmd, timestep)
        elif self.active_joint==7:
            gDelta = self.g_integrator.integrate(10*cmd, timestep)

        a, b, numSol, theta = self.armMath.inverse_kinematics(np.array([xDelta, yDelta, zDelta], dtype=np.float64), gDelta, self.current_joint_pose)
        if numSol > 0:
            self.current_joint_pose = theta
            self.xDelta = xDelta
            self.yDelta = yDelta
            self.zDelta = zDelta
            self.gDelta = gDelta
        else:
            self.x_integrator.reset(self.xDelta)
            self.y_integrator.reset(self.yDelta)
            self.z_integrator.reset(self.zDelta)
            self.g_integrator.reset(self.gDelta)

        return self.current_joint_pose

class DataIO():
    '''
    Writes/reads manipulator data to/from a csv file.

    Parameters
    ----------
    filename : string
        Filename used for read/write operations.
    newLine : string
        newline parameter to be used, '' or '\\n'
    '''
    def __init__(self, filename='data.csv', newLine=''):
        self.filename = filename
        self.newLine = newLine
        pass

    def write(self, data, mode='joints'):
        '''
        Writes manipulator data to a csv file.

        Parameters
        ----------
        data : list of lists
            Input data to be recorded. Provide a list of n datapoints, with
            each data points being a list of 3 end-effector-pose XYZ parameters
            or a list of 4 joint parameters.
        mode : string
            set to either 'end-effector-pose' or 'joints' as per data values
        '''
        with open(self.filename, 'w', newline=self.newLine) as csvFile:
            writer = csv.writer(csvFile)
            if mode == 'joints':
                writer.writerow(['Theta0', 'Theta1', 'Theta2', 'Theta3'])
            elif mode == 'end-effector-pose':
                writer.writerow(['X', 'Y', 'Z'])
            writer.writerows(data)

    def read(self):
        '''
        Reads manipulator data from a csv file.

        Returns
        -------
        data : list of lists
            Provides a list of n datapoints, with each data points being a list
            of 3 end-effector-pose XYZ parameters or a list of 4 joint
            parameters based on the data read.
        numRows : int
            The number of data points read (not including a titles)
        '''

        data = []
        f = open(self.filename, newline=self.newLine)
        reader = csv.reader(f)
        counter = 0
        firstRowFlag = False
        for row in reader:
            if counter == 0:
                try:
                    for idx, val in enumerate(row):
                        row[idx] = float(val)
                    data.append(row)
                    firstRowFlag = True
                except:
                    pass
            if counter > 0:
                for idx, val in enumerate(row):
                    row[idx] = float(val)
                data.append(row)
            counter = counter + 1

        if firstRowFlag: numRows = counter - 1 # first row wasn't text but data
        else: numRows = counter - 2 # don't count first row as it was text

        counter = 0           # reset counter

        return data, numRows

class PlotData():
    '''
    Plotter based on Matplotlib's pyplot specifically for QArm Mini Labs.
    '''
    @staticmethod
    def plot3D1Curve(data):
        '''
        Plots a single 3D X/Y/Z curve. No time data required.
        '''
        if not data:
            print('Plot 1x 3D curve: no data recorded.')
            return
        fig = plt.figure()
        ax = plt.axes(projection = '3d')
        plotData = np.asarray(data)
        plotData = plotData.transpose()
        ax.plot3D(plotData[0], plotData[1], plotData[2], 'blue')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    @staticmethod
    def plot3D2Curves(dataCmd, dataMeas):
        '''
        Plots a pair of 3D X/Y/Z curves. No time data required. Use to compare
        commands vs measured end-effector data.
        '''
        if not dataCmd or not dataMeas:
            print('Plot 2x 3D curves: no data recorded.')
            return
        fig = plt.figure()
        ax = plt.axes(projection = '3d')
        plotDataA = np.asarray(dataCmd)
        plotDataA = plotDataA.transpose()
        ax.plot3D(plotDataA[0], plotDataA[1], plotDataA[2], 'blue', label='Command')
        plotDataB = np.asarray(dataMeas)
        plotDataB = plotDataB.transpose()
        ax.plot3D(plotDataB[0], plotDataB[1], plotDataB[2], 'red', label='Measured')
        ax.legend(), ax.set_xlabel('X'), ax.set_ylabel('Y'), ax.set_zlabel('Z')
        plt.show()

    @staticmethod
    def plot2DJointCurves(data, timeData):
        '''
        Plots joint data on a time axis.
        '''
        if not data or not timeData:
            print('Plot 2D curves: no data recorded.')
            return
        fig, axs = plt.subplots(4, 1, layout='constrained')
        plotData = np.asarray(data)
        plotData = plotData.transpose()
        axs[0].plot(timeData, plotData[0], 'blue', label='J1')
        axs[1].plot(timeData, plotData[1], 'blue', label='J2')
        axs[2].plot(timeData, plotData[2], 'blue', label='J3')
        axs[3].plot(timeData, plotData[3], 'blue', label='J4')
        axs[0].set_xlabel('time (s)'), axs[0].set_ylabel('J1 (rad)')
        axs[1].set_xlabel('time (s)'), axs[1].set_ylabel('J2 (rad)')
        axs[2].set_xlabel('time (s)'), axs[2].set_ylabel('J3 (rad)')
        axs[3].set_xlabel('time (s)'), axs[3].set_ylabel('J4 (rad)')
        axs[0].legend(), axs[1].legend(), axs[2].legend(), axs[3].legend()
        axs[0].grid(True), axs[1].grid(True), axs[2].grid(True), axs[3].grid(True)
        plt.show()

    @staticmethod
    def plot2D2JointCurves(dataCmd, dataMeas, timeData):
        '''
        Plots a pair of joint data curves on a time axis. Use to compare
        commands vs measured joint data.
        '''
        if not dataCmd or not dataMeas or not timeData:
            print('Plot 2x 2D curves: no data recorded.')
            return
        fig, axs = plt.subplots(4, 1, layout='constrained')
        plotDataA = np.asarray(dataCmd)
        plotDataA = plotDataA.transpose()
        plotDataB = np.asarray(dataMeas)
        plotDataB = plotDataB.transpose()

        axs[0].plot(timeData, plotDataA[0], label='J1 Cmd')
        axs[1].plot(timeData, plotDataA[1], label='J2 Cmd')
        axs[2].plot(timeData, plotDataA[2], label='J3 Cmd')
        axs[3].plot(timeData, plotDataA[3], label='J4 Cmd')
        axs[0].plot(timeData, plotDataB[0], label='J1 Meas')
        axs[1].plot(timeData, plotDataB[1], label='J2 Meas')
        axs[2].plot(timeData, plotDataB[2], label='J3 Meas')
        axs[3].plot(timeData, plotDataB[3], label='J4 Meas')
        axs[0].set_xlabel('time (s)'), axs[0].set_ylabel('J1 (rad)')
        axs[1].set_xlabel('time (s)'), axs[1].set_ylabel('J2 (rad)')
        axs[2].set_xlabel('time (s)'), axs[2].set_ylabel('J3 (rad)')
        axs[3].set_xlabel('time (s)'), axs[3].set_ylabel('J4 (rad)')
        axs[0].legend(), axs[1].legend(), axs[2].legend(), axs[3].legend()
        axs[0].grid(True), axs[1].grid(True), axs[2].grid(True), axs[3].grid(True)
        plt.show()

class QArmMiniImageProcessing():
    def __init__(self, resolution=(640,360,3)):
        self.width = resolution[0]
        self.height = resolution[1]
        self.channels = resolution[2]
        pass

    def guassian_blur(self, img, kernelSize=5, stdDev=1):
        # return the image passed through Guassian Blur
        return cv2.GaussianBlur(img, (kernelSize, kernelSize), stdDev)

    def convert(self, img, code=cv2.COLOR_BGR2HSV):
        # return the image converted as needed
        return cv2.cvtColor(img, code=code)

    def threshold_grayscale(self, img, upper, lower, code=cv2.THRESH_BINARY):
        # return a thresholded grayscale image
        _, imgOutput = cv2.threshold(img, lower, upper, code)
        return imgOutput

    def threshold_color(self, img, upper, lower):
        # return a thresholded color image
        return cv2.inRange(img, lower, upper)

    def close(self, img, kernel, iterations=1):
        # return a closed image (dilated and eroded in that order)
        kernel = np.ones((kernel, kernel), np.uint8)
        clean = img
        for _ in range(iterations):
            dilated = cv2.dilate(clean, kernel, iterations=1)
            clean   = cv2.erode(dilated, kernel, iterations=1)
        return clean

    def open(self, img, kernel, iterations=1):
        # return a opened image (eroded and dilated in that order)
        kernel = np.ones((kernel, kernel), np.uint8)
        clean = img
        for _ in range(iterations):
            eroded   = cv2.erode(clean, kernel, iterations=1)
            clean = cv2.dilate(eroded, kernel, iterations=1)
        return clean

    def highlight(self, imgRGB, mask):
        # take everything that's 0 in mask and turn it gray...
        allGray = cv2.bitwise_and(cv2.cvtColor(
                                        imgRGB,
                                        cv2.COLOR_RGB2GRAY),
                                  cv2.bitwise_not(mask))
        # take everything that's 1 in mask and keep it RGB
        allColor = cv2.bitwise_and(imgRGB, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR))


        # combine allGray and allColor
        return cv2.bitwise_or(allColor, cv2.cvtColor(allGray, cv2.COLOR_GRAY2BGR))

    def find_objects(self, image, connectivity, minArea, maxArea):
        col = 0
        row = 0
        area = 0
        # run connected component analysis
        analysis = cv2.connectedComponentsWithStats(image, connectivity=connectivity, ltype=cv2.CV_32S)
        (labels, ids, values, centroids) = analysis

        # find the results that best match min & max area
        for idx, val in enumerate(values):
            if val[4]>minArea and val[4] < maxArea:
                value = val
                centroid = centroids[idx]
                col = centroid[0]
                row = centroid[1]
                area = value[4]
                break
            else:
                col = None
                row = None
                area = None
        return col, row, area
    
    def draw_lines(self, img_in, color, pts):
        """
        Draw lines connecting the points using the provided color
        
        Args:
            img_in: Input image (grayscale or RGB)
            color: RGB color values as tuple/list (R, G, B) with values 0-255
            pts: Bounding box coordinates [x_min, y_min, x_max, y_max]
        
        Returns:
            img_out: Output image with the bounding box drawn
        """
        
        # Convert grayscale to RGB if needed
        if len(img_in.shape) == 2:
            img_out = cv2.cvtColor(img_in, cv2.COLOR_GRAY2RGB)
        else:
            img_out = img_in.copy()
        
        # Extract box coordinates
        box = pts
        x_min, y_min, x_max, y_max = box[0], box[1], box[2], box[3]
        
        # Define rectangle corners in order to draw closed box
        # Format: [x, y] pairs for each corner
        rectangle_pts = np.array([
            [x_min, y_min],  # top-left
            [x_min, y_max],  # bottom-left  
            [x_max, y_max],  # bottom-right
            [x_max, y_min],  # top-right
            [x_min, y_min]   # back to top-left to close the box
        ], dtype=np.int32)
        
        # Draw lines between consecutive points
        for i in range(len(rectangle_pts) - 1):
            pt1 = rectangle_pts[i]
            pt2 = rectangle_pts[i + 1]
            
            # Calculate number of iterations needed
            itr = max(abs(pt2[0] - pt1[0]), abs(pt2[1] - pt1[1]))
            
            if itr > 0:
                # Generate linear interpolation between points
                x_vec = np.round(np.linspace(pt1[0], pt2[0], itr)).astype(int)
                y_vec = np.round(np.linspace(pt1[1], pt2[1], itr)).astype(int)
                
                # Draw pixels along the line
                for j in range(itr):
                    x, y = x_vec[j], y_vec[j]
                    if 0 <= y < img_out.shape[0] and 0 <= x < img_out.shape[1]:
                        img_out[y, x, 0] = color[0]  # R
                        img_out[y, x, 1] = color[1]  # G
                        img_out[y, x, 2] = color[2]  # B
        
        return img_out

    def draw_box_on_detection(self, image, col, row, area):
        """
        Helper function to draw bounding box based on find_objects results
        Assumes the bounding box can be derived from connected components stats
        """
        # Example: create a square box around the centroid
        box_size = int(np.sqrt(area) / 2)  # Half the square root of area
        
        x_min = int(col - box_size)
        y_min = int(row - box_size) 
        x_max = int(col + box_size)
        y_max = int(row + box_size)
        
        # Ensure bounds are within image
        h, w = image.shape[:2]
        x_min = max(0, x_min)
        y_min = max(0, y_min)
        x_max = min(w-1, x_max)
        y_max = min(h-1, y_max)
        
        pts = [x_min, y_min, x_max, y_max]
        color = (0, 0, 255)  # Red box
        
        return self.draw_lines(image, color, pts)