import numpy as np
import numpy.linalg as npla
from scipy.interpolate import CubicSpline

from pal.products.qarm_mini import QArmMini
from pal.utilities.math import Calculus

#TODO: this code currently has not been tested.

class QArmMiniFunctions():
    """This class contains the functions for the QArm Mini such as Forward/Inverse Differential Drive Kinematics etc. """

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
        Calculates the forward kinematic pose given values of the joints.

        Parameters:
            theta(): Alternate joint angles vector 4 x 1

        Returns:
            - **posEndEffector** (): End-effector frame {e} position vector expressed in base frame {0}
            - **rotMatrix05**(): rotation matrix from end-effector frame {e} to base frame {0}
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

        alpha = theta[1] + theta[2] + theta[3] - np.pi/2

        #return the position of the end effector and the rotation matrix
        return posEndEffector, rotMatrix05, alpha

    def inverse_kinematics(self, posEndEffector, gamma, theta_prev):
        """
        Calculates the inverse kinematic joint values from pose.

        Parameters:

        posEndEffector (): end-effector position vector expressed in base frame {0}
        gamma (): wrist rotation angle gamma
        theta_prev (): previous theta values

        Return:
            - **thetaOptimal** *()* - Best solution depending on theta_prev
            - **theta** *()* - All 4 inverse kinematics solutions as a 4x4 matrix. Each col is a solution.
        """

        # Initialization
        theta = np.zeros((4, 4), dtype=np.float64)

        thetaOpt = np.zeros((4, 1), dtype=np.float64)
        d1_flag = 0
        d2_flag = 0
        numSolutions = 0
        indices = np.ones((4,1), dtype=np.float64)

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
            # closest solution to theta_prev. That happens later.

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

        # def solve_case_C_joint2(joint3, A, B, D, H):
        #     M = A + B*np.cos(joint3)
        #     N = B*np.sin(joint3)
        #     cos_term = (D*M + H*N)/(M**2 + N**2)
        #     sin_term = (H - N*cos_term)/(M)
        #     joint2 = np.arctan2(sin_term, cos_term)
        #     return joint2

        def check_joint_limits(theta):
            flag = 0

            if (theta[0] > 225.0*np.pi/180 or theta[0] <  -90.0*np.pi/180 or
                theta[1] > 180.0*np.pi/180 or theta[1] <    0.0*np.pi/180 or
                theta[2] >   0.0*np.pi/180 or theta[2] < -135.0*np.pi/180 or
                theta[3] > 157.5*np.pi/180 or theta[3] <    0.0*np.pi/180    ):
                flag = 1

            return flag

        A, B, H, D1, D2, F1, F2, numSolutions, d1_flag, d2_flag = inv_kin_setup(posEndEffector, gamma)

        if d1_flag:
            # there are 2 possible values for theta(3) based on the + or - sqrt.
            theta[2,0] = 2*np.arctan2(np.sqrt(B**2 - F1**2), B+F1)
            theta[2,1] = 2*np.arctan2(-np.sqrt(B**2 - F1**2), B+F1)

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

        if d2_flag:
            # check if the 2 solutions below are solutions (1 & 2) or (3 & 4) based
            # on whether numSolutions was set to 4 or not. If you are here, it was
            # definitely 4 or 2.

            indexModifier = 2 if numSolutions == 4 else 0

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

            theta[1,0 + indexModifier] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,0 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0 + indexModifier] + theta[2,0 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,0 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,0 + indexModifier] + theta[2,0 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)))

            theta[1,1 + indexModifier] = np.arctan2(posEndEffector[1]/(self.LAMBDA_2 * np.cos(theta[1,1 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1 + indexModifier] + theta[2,1 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)) ,
                                    posEndEffector[0]/(self.LAMBDA_2 * np.cos(theta[1,1 + indexModifier]) +
                                                       self.LAMBDA_3 * np.cos(theta[1,1 + indexModifier] + theta[2,1 + indexModifier]) +self.LAMBDA_4*np.cos(gamma)))

        # joint angle 3
        theta[3,:] = gamma + np.pi/2 - theta[1, :] - theta[2, :]

        #Joint checks and final modifications
        numSolutionsMod = 0
        for x in range(numSolutions):
            if check_joint_limits(theta[:,x]):
                indices[x] = 0
                numSolutionsMod = numSolutionsMod + 1

        numSolutions = numSolutions + numSolutionsMod

        # find the solution from thetas that is closest to thetaPrev
        closestSolution = theta[:,1]
        mark = 1

        for x in range(1,4):
            if indices[x]:
                if npla.norm(theta[:,x]-theta_prev, 2) < npla.norm(closestSolution - theta_prev , 2):
                    closestSolution = theta[:,x]
                    mark = x

        indices[mark] = 2
        thetaOpt = theta[:, mark]

        return theta, indices, numSolutions, thetaOpt

    def differential_kinematics(self, theta):
        """Implements the jacobian matrix using theta for the QArm Mini

        Parameters:

        theta (): Alternate joint angle vector 4 x 1

        Return:
            - **J** *()* - Best solution depending on theta_prev
            - **c** *()* - condition number of the jacobian matrix
            - **r** *()* - rank of the jacobian matrix
            - **J_inv** *()* - inverse of the jacobian matrix
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

    def trajectory_generator_cubic_splines(self, x, y, axis=0, bc_type='not-a-knot', extrapolate=None):

        cubic_spline = CubicSpline(x,y,axis,bc_type, extrapolate)

        return cubic_spline

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

    def __init__(self, keyboardDriver, initialPose=QArmMini.HOME_POSE):

        self.kbd = keyboardDriver #instance of KeyboardDriver from pal.utilities.keyboard
        mathFunc = Calculus()
        self.armMath = QArmMiniFunctions()
        self.joint_0_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=initialPose[0])
        self.joint_1_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=initialPose[1])
        self.joint_2_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=initialPose[2])
        self.joint_3_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=initialPose[3])

        ee_position, ee_rotation, gamma = self.armMath.forward_kinematics(theta=initialPose)

        self.x_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=ee_position[0])
        self.y_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=ee_position[1])
        self.z_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=ee_position[2])
        self.g_integrator = mathFunc.integrator_variable(dt=1.0/self.kbd.rate, integrand=gamma)

        self.j0Delta = next(self.joint_0_integrator)
        self.j1Delta = next(self.joint_1_integrator)
        self.j2Delta = next(self.joint_2_integrator)
        self.j3Delta = next(self.joint_3_integrator)

        self.xDelta = next(self.x_integrator)
        self.yDelta = next(self.y_integrator)
        self.zDelta = next(self.z_integrator)
        self.gDelta = next(self.g_integrator)

        self.current_joint_pose = initialPose
        self.current_ee_pose = ee_position
        self.current_gamma = gamma

        self.active_joint = None
        pass

    def activate_joint(self, mode='joint'):

        if mode=='joint':
            if self.kbd.k_1:
                self.active_joint = 0 # joint 1 base yaw
            elif self.kbd.k_2:
                self.active_joint = 1 # joint 2 shoulder pitch
            elif self.kbd.k_3:
                self.active_joint = 2 # joint 3 elbow pitch
            elif self.kbd.k_4:
                self.active_joint = 3 # joint 4 wrist pitch
        elif mode=='task':
            if self.kbd.k_x:
                self.active_joint = 4 # base frame x
            elif self.kbd.k_y:
                self.active_joint = 5 # base frame y
            elif self.kbd.k_z:
                self.active_joint = 6 # base frame z
            elif self.kbd.k_g:
                self.active_joint = 7 # base frame z
        else:
            self.active_joint = None

    def move_joints_with_keyboard(self, timestep, speed=np.pi/12):
        '''Tap the keyboard 1 through 4 keys to select a joint. Then use the
        UP and DOWN arrows to increase or decrease the joint's cmd
        respectively.'''

        if self.kbd.k_up:
            cmd = speed
        elif self.kbd.k_down:
            cmd = -1*speed
        else:
            cmd = 0
        self.activate_joint(mode='joint')

        if self.active_joint==0:
            self.j0Delta = self.joint_0_integrator.send((cmd, timestep))
        elif self.active_joint==1:
            self.j1Delta = self.joint_1_integrator.send((cmd, timestep))
        elif self.active_joint==2:
            self.j2Delta = self.joint_2_integrator.send((cmd, timestep))
        elif self.active_joint==3:
            self.j3Delta = self.joint_3_integrator.send((cmd, timestep))

        self.current_joint_pose = np.array([self.j0Delta, self.j1Delta, self.j2Delta, self.j3Delta], dtype=np.float64)

        return self.current_joint_pose

    def move_ee_with_keyboard(self, timestep, speed=0.02):
        '''Tap the keyboard x, y, z or g keys to select a cartesian x, y, z axis
        or the end-effector orientation angle gamma. Then use the
        UP and DOWN arrows to increase or decrease the corresponding cmd value.
        Note, the speed is multiplied by a factor of 10 for the end-effector
        angle Gamma.'''

        if self.kbd.k_up:
            cmd = speed
        elif self.kbd.k_down:
            cmd = -1*speed
        else:
            cmd = 0
        self.activate_joint(mode='task')

        if self.active_joint==4:
            self.xDelta = self.x_integrator.send((cmd, timestep))
        elif self.active_joint==5:
            self.yDelta = self.y_integrator.send((cmd, timestep))
        elif self.active_joint==6:
            self.zDelta = self.z_integrator.send((cmd, timestep))
        elif self.active_joint==7:
            self.gDelta = self.g_integrator.send((10*cmd, timestep))

        a, b, numSol, theta = self.armMath.inverse_kinematics(np.array([self.xDelta, self.yDelta, self.zDelta], dtype=np.float64), self.gDelta, self.current_joint_pose)
        if numSol > 0:
            self.current_joint_pose = theta

        return self.current_joint_pose