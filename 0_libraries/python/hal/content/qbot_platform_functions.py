import numpy as np
import cv2

from pal.products.qbot_platform import QBotPlatformDriver
from pal.utilities.math import Calculus, wrap_to_pi
from scipy.ndimage import median_filter
from pal.utilities.stream import BasicStream
from quanser.common import Timeout
from quanser.image_processing import Lidar2DMatchScansGrid 

class QBPMovement():
    """ This class contains the functions for the QBot Platform such as
    Forward/Inverse Differential Drive Kinematics etc. """

    def __init__(self):
        self.WHEEL_RADIUS = QBotPlatformDriver.WHEEL_RADIUS      # radius of the wheel (meters)
        self.WHEEL_BASE = QBotPlatformDriver.WHEEL_BASE          # distance between wheel contact points on the ground (meters)
        self.WHEEL_WIDTH = QBotPlatformDriver.WHEEL_WIDTH        # thickness of the wheel (meters)
        self.ENCODER_COUNTS = QBotPlatformDriver.ENCODER_COUNTS  # encoder counts per channel
        self.ENCODER_MODE = QBotPlatformDriver.ENCODER_MODE      # multiplier for a quadrature encoder

    def diff_drive_inverse_velocity_kinematics(self, forSpd, turnSpd):
        """This function is for the differential drive inverse velocity
        kinematics for the QBot Platform. It converts provided body speeds
        (forward speed in m/s and turn speed in rad/s) into corresponding
        wheel speeds (rad/s)."""

        #------------Replace the following lines with your code---------------#
        wL = 0
        wR = 0
        #---------------------------------------------------------------------#
        return wL, wR

    def diff_drive_forward_velocity_kinematics(self, wL, wR):
        """This function is for the differential drive forward velocity
        kinematics for the QBot Platform. It converts provided wheel speeds
        (rad/s) into corresponding body speeds (forward speed in m/s and
        turn speed in rad/s)."""
        #------------Replace the following lines with your code---------------#
        forSpd = 0
        turnSpd = 0
        #---------------------------------------------------------------------#
        return forSpd, turnSpd

class QBPVision():
    def __init__(self):
        self.imageCriteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    def undistort_img(self,distImgs,cameraMatrix,distCoefficients):
        """
        This function undistorts a general camera, given the camera matrix and
        coefficients.
        """

        undist = cv2.undistort(distImgs,
                               cameraMatrix,
                               distCoefficients,
                               None,
                               cameraMatrix)
        return undist

    def df_camera_undistort(self, image):
        """
        This function undistorts the downward camera using the camera
        intrinsics and coefficients."""
        CSICamIntrinsics = np.array([[419.36179672, 0, 292.01381114],
                                     [0, 420.30767196, 201.61650657],
                                     [0, 0, 1]])
        CSIDistParam = np.array([-7.42983302e-01,
                                 9.24162996e-01,
                                 -2.39593372e-04,
                                 1.66230745e-02,
                                 -5.27787439e-01])
        undistortedImage = self.undistort_img(
                                                image,
                                                CSICamIntrinsics,
                                                CSIDistParam
                                                )
        return undistortedImage

    def subselect_and_threshold(self, image, rowStart, rowEnd, minThreshold, maxThreshold):
        """
        This function subselects a horizontal slice of the input image from
        rowStart to rowEnd for all columns, and then thresholds it based on the
        provided min and max thresholds. Returns the binary output from
        thresholding."""

        #------------Replace the following lines with your code---------------#
        subImage = None
        binary = None
        #---------------------------------------------------------------------#

        return binary

    def image_find_objects(self, image, connectivity, minArea, maxArea):
        """
        This function implements connected component labeling on the provided
        image with the desired connectivity. From the list of blobs detected,
        it returns the first blob that fits the desired area criteria based
        on minArea and maxArea provided. Returns the column and row location
        of the blob centroid, as well as the blob's area. """

        col = 0
        row = 0
        area = 0

        #------------Replace the following lines with your code---------------#

        (labels, ids, values, centroids) = None
        #---------------------------------------------------------------------#

        #-------------Uncomment the following 12 lines of code----------------#

        # for idx, val in enumerate(values):
        #     if val[4]>minArea and val[4] < maxArea:
        #         value = val
        #         centroid = centroids[idx]
        #         col = centroid[0]
        #         row = centroid[1]
        #         area = value[4]
        #         break
        #     else:
        #         col = None
        #         row = None
        #         area = None
        #---------------------------------------------------------------------#

        return col, row, area

    def line_to_speed_map(self, sampleRate, saturation):

        integrator   = Calculus().integrator(dt = sampleRate, saturation=saturation)
        derivative   = Calculus().differentiator(dt = sampleRate)
        next(integrator)
        next(derivative)
        forSpd, turnSpd = 0, 0
        offset = 0

        while True:
            col, kP, kD = yield forSpd, turnSpd

            if col is not None:
                #-----------Complete the following lines of code--------------#
                error = 0
                angle = np.arctan2(0, 0)
                turnSpd = 0 * angle + 0 * derivative.send(angle)
                forSpd = 0
                #-------------------------------------------------------------#
                offset = integrator.send(25*turnSpd)



class QBPRanging():
    def __init__(self):
        pass

    def adjust_and_subsample(self, ranges, angles,end=-1,step=4):

        # correct angles data
        angles_corrected = -1*angles + np.pi/2
        # return every 4th sample
        return ranges[0:end:step], angles_corrected[0:end:step]

    def correct_lidar(self, lidarPosition, ranges, angles):

        # Convert lidar data from polar into cartesian, and add lidar position
        # Then Convert back into polar coordinates

        #-------Replace the following line with your code---------#
        # Determine the start of the focus region 
        ranges_c=None
        angles_c=None
        #---------------------------------------------------------#

        return ranges_c, angles_c

    def detect_obstacle(self, ranges, angles, forSpd, forSpeedGain, turnSpd, turnSpeedGain, minThreshold, obstacleNumPoints):

        halfNumPoints = 205
        quarterNumPoints = round(halfNumPoints/2)

        # Grab the first half of ranges and angles representing 180 degrees
        frontRanges = ranges[0:halfNumPoints]
        frontAngles = angles[0:halfNumPoints]

        # Starting index in top half          1     West
        # Mid point in west quadrant         51     North-west
        # Center index in top half          102     North
        # Mid point in east quadrant     51+102     North-east
        # Ending index in top half          205     East

        ### Section 1 - Dynamic Focus Region ###
        
        #-------Replace the following line with your code---------#
        # Determine the start of the focus region 
        startingIndex = 0
        #---------------------------------------------------------#

        # Setting the upper and lower bound such that the starting index 
        # is always in the first quarant
        if startingIndex < 0:
            startingIndex = 0
        elif startingIndex > 102:
            startingIndex = 102

        # Pick quarterNumPoints in ranges and angles from the front half
        # this will be the region you monitor for obstacles
        monitorRanges = frontRanges[startingIndex:startingIndex+quarterNumPoints]
        monitorAngles = frontAngles[startingIndex:startingIndex+quarterNumPoints]

        ### Section 2 - Dynamic Stop Distance ###

        #-------Replace the following line with your code---------#
        # Determine safetyThreshold based on Forward Speed 
        safetyThreshold = 1
        
        #---------------------------------------------------------#

        
        # At angles corresponding to monitorAngles, pick uniform ranges based on
        # a safety threshold
        safetyAngles = monitorAngles
        safetyRanges = safetyThreshold*monitorRanges/monitorRanges

  
        ### Section 3 - Obstacle Detection ###

        
        #-------Replace the following line with your code---------#
        # Total number of obstacles detected between 
        # minThreshold & safetyThreshold
        # Then determine obstacleFlag based on obstacleNumPoints

        obstacleFlag = 0
        
        #---------------------------------------------------------#


        # Lidar Ranges and Angles for plotting (both scan & safety zone)
        plottingRanges = np.append(monitorRanges, safetyRanges)
        plottingAngles = np.append(monitorAngles, safetyAngles)

        return plottingRanges, plottingAngles, obstacleFlag
    

class QBPLocalization():
    """ This class contains the functions for the QBot Platform 
        for localization using lidar data """
    def __init__(self, resolution=20, max_range=5):
        self.lidarScanMatch = Lidar2DMatchScansGrid(resolution=resolution, max_range=max_range)
        self.pose = np.array([0.0,0.0,0.0],dtype=np.float32)
        self.score = np.array([0.0],dtype=np.float32)
        self.covariance = np.eye(3,dtype=np.float32)
        self.prevPose =  np.array([0.0,0.0,0.0],dtype=np.float32)

        self.refRanges = None
        self.refAngles = None
        self.refXY = None
        self.refSaved = False # flag for whether reference scan has been saved 
    
    def save_ref(self, rangesIn, anglesIn):
        """ This function saves input LiDAR data as a reference scan"""
        self.refSaved = False

        if rangesIn is not None and anglesIn is not None:
            
            # Modify the code below-------------------------------------------#
            # save reference scan
            # self.refRanges = 
            # self.refAngles = 
            # ----------------------------------------------------------------#

            # set flag 
            self.refSaved = True

            # initialize generator that converts each scan point to Cartesian  
            self.refXY = self.polar_to_cartesian(self.refRange, self.refAngles)

        return self.refSaved
        
    def polar_to_cartesian(self, rangesIn, anglesIn):
        """ This generator converts polar coordinates
            to Cartesian """
        idx = 0
        while True:
            yield [rangesIn[idx]*np.cos(anglesIn[idx]), 
                   rangesIn[idx]*np.sin(anglesIn[idx])]
            idx = (idx+4)%len(rangesIn) # plot every 4th point 

    def scan_match(self, ranges, angles, transRange=(3.0, 3.0), rotRange=2*np.pi):
        """ This function checks for a saved reference scan and then runs
            the match method to find the transformation between the current scan"""
        if not self.refSaved:
            return False
        else:
            # Modify the code below ------------------------------------------#
            newMatch = self.lidarScanMatch.match(ref_ranges=None, 
                                            ref_angles=None, 
                                            num_ref_points = None,
                                            ranges = None, 
                                            angles = None, 
                                            num_points = None,
                                            initial_pose = None, 
                                            translation_search_range = np.array(transRange, dtype=np.float32), 
                                            rotation_search_range = rotRange,
                                            pose=self.pose, 
                                            score=self.score, 
                                            covariance=self.covariance)
            
            # save pose estimate 
            # self.prevPose = 
            # ----------------------------------------------------------------#

            # iterate to the next point in the reference scan
            self.refX, self.refY = next(self.refXY)
    
    def terminate(self):
        self.lidarScanMatch.close()

class QBPFusion():
    def __init__(self):
        pass

    def complementary_filter(self, dt, x0=0):
        """Complementary filter combining a rate and a correction signal,
        applying a low-pass path to the rate signal and a high-pass path
        to the correction signal.

        Parameters
        ----------
        dt : float
            Sampling time (s).
        x0 : float
            Initial condition for the error-integral (bias) state.

        Receives
        --------
        tuple[float, float, float, float] : (rate, correction, k_p, k_i)
            rate : float
                Signal to be low-pass filtered (e.g., from a gyroscope
                or accelerometer).
            correction : float
                Signal to be high-pass filtered (e.g., from a camera or
                wheel odometry).
            k_p : float
                Proportional gain.
            k_i : float
                Integral gain.

        Yields
        ------
        float
            Filtered output signal (the estimate).
        """

        estimate = 0
        temp = 0
        integratedError = 0
        integratorRate = Calculus().integrator(dt, integrand=x0)
        integratorTuner = Calculus().integrator(dt, integrand=0)
        next(integratorRate)
        next(integratorTuner)
        while True:
            rate, correction, kP, kI = yield estimate
            error = estimate - correction
            integratedError = integratorTuner.send(error)
            # temp = rate - (kP*error)
            temp = rate - kP*error - kI*integratedError
            estimate = integratorRate.send(temp)

class QBPFusion():
    def __init__(self):
        pass

    def complementary_filter(self, dt, x0=0):
        """Complementary filter combining a rate and a correction signal,
        applying a low-pass path to the rate signal and a high-pass path
        to the correction signal.

        Parameters
        ----------
        dt : float
            Sampling time (s).
        x0 : float
            Initial condition for the error-integral (bias) state.

        Receives
        --------
        tuple[float, float, float, float] : (rate, correction, k_p, k_i)
            rate : float
                Signal to be low-pass filtered (e.g., from a gyroscope
                or accelerometer).
            correction : float
                Signal to be high-pass filtered (e.g., from a camera or
                wheel odometry).
            k_p : float
                Proportional gain.
            k_i : float
                Integral gain.

        Yields
        ------
        float
            Filtered output signal (the estimate).
        """

        estimate = 0
        temp = 0
        integratedError = 0
        integratorRate = Calculus().integrator(dt, integrand=x0)
        integratorTuner = Calculus().integrator(dt, integrand=0)
        next(integratorRate)
        next(integratorTuner)
        while True:
            rate, correction, kP, kI = yield estimate
            error = estimate - correction
            integratedError = integratorTuner.send(error)
            temp = rate - (kP*error)
            estimate = integratorRate.send(temp)

class QBotEKF:
    """An EKF designed to estimate the position and orientation of a QBot.

    This implementation follows the MATLAB-based approach for QBot differential drive
    robots, using a threshold-based switching between curved and straight-line motion
    models for improved accuracy at low angular velocities.

    Attributes:
        ekf (EKF): Extended Kalman filter for pose estimation [x, y, theta].
        omega_threshold (float): Threshold for switching between motion models (rad/s).
        x_hat (ndarray): State estimate vector [x; y; theta].
    """

    def __init__(
            self,
            x_0,
            omega_threshold=0.02,
            Q_ekf=None,
            R_ekf=None
        ):
        """Initialize QBotEKF with initial state and noise covariance matrices.

        Args:
            x_0 (ndarray): Initial state vector [x, y, theta].
            omega_threshold (float, optional): Angular velocity threshold for motion
                model switching. Below this, uses straight-line approximation.
                Default: 0.02 rad/s
            Q_ekf (ndarray, optional): EKF process noise covariance matrix (3x3).
                Default: 0.0075 * I(3)
            R_ekf (ndarray, optional): EKF measurement noise covariance matrix (3x3).
                Default: 0.001 * I(3)
        """

        # Set default noise covariances if not provided
        if Q_ekf is None:
            Q_ekf = 0.0075 * np.eye(3)
        if R_ekf is None:
            R_ekf = 0.001 * np.eye(3)

        x_0 = np.squeeze(x_0)

        # Initialize the EKF with full pose state [x, y, theta]
        self.ekf = EKF(
            x_0=x_0,
            P_0=0.01 * np.eye(3),
            Q=Q_ekf,
            R=R_ekf,
            f=self.f,
            J_f=self.J_f,
            h=self.h,
            J_h=self.J_h
        )

        self.omega_threshold = omega_threshold
        self.x_hat = self.ekf.x_hat

    def f(self, x, u, dt):
        """Motion model for the differential drive robot.

        Implements exact kinematic model with threshold-based switching between
        curved motion (omega > threshold) and straight-line approximation.

        Args:
            x (ndarray): State vector [x, y, theta] (3x1).
            u (ndarray): Control input vector [v, omega] (2x1).
                v: linear velocity (m/s)
                omega: angular velocity (rad/s)
            dt (float): Time step in seconds.

        Returns:
            ndarray: Updated state vector after applying motion model (3x1).
        """

        v = u[0, 0] if u.ndim > 1 else u[0]
        omega = u[1, 0] if u.ndim > 1 else u[1]
        theta_k = x[2, 0]

        if np.abs(omega) > self.omega_threshold:
            # Exact curved motion model
            # X(k+1) = X(k) - (v/omega)*sin(theta) + (v/omega)*sin(theta + omega*dt)
            # Y(k+1) = Y(k) + (v/omega)*cos(theta) - (v/omega)*cos(theta + omega*dt)
            # theta(k+1) = theta(k) + omega*dt

            theta_next = theta_k + omega * dt

            x_pred = x + np.array([
                [-(v / omega) * np.sin(theta_k) + (v / omega) * np.sin(theta_next)],
                [(v / omega) * np.cos(theta_k) - (v / omega) * np.cos(theta_next)],
                [omega * dt]
            ])
        else:
            # Straight-line approximation (avoids division by zero)
            # This is valid when omega ≈ 0
            x_pred = x + np.array([
                [v * np.cos(theta_k) * dt],
                [v * np.sin(theta_k) * dt],
                [omega * dt]
            ])

        # Normalize predicted heading to [-pi, pi]
        x_pred[2, 0] = wrap_to_pi(x_pred[2, 0])

        return x_pred

    def J_f(self, x, u, dt):
        """Jacobian matrix of the motion model.

        Computes the linearization of the motion model about the current state.
        Uses threshold-based switching for consistency with f().

        Args:
            x (ndarray): State vector [x, y, theta] (3x1).
            u (ndarray): Control input vector [v, omega] (2x1).
            dt (float): Time step in seconds.

        Returns:
            ndarray: Jacobian matrix (3x3).
        """

        v = u[0, 0] if u.ndim > 1 else u[0]
        omega = u[1, 0] if u.ndim > 1 else u[1]
        theta_k = x[2, 0]

        if np.abs(omega) > self.omega_threshold:
            # Jacobian for curved motion model
            theta_next = theta_k + omega * dt

            F = np.array([
                [1, 0, -(v / omega) * np.cos(theta_k) + (v / omega) * np.cos(theta_next)],
                [0, 1, -(v / omega) * np.sin(theta_k) + (v / omega) * np.sin(theta_next)],
                [0, 0, 1]
            ])
        else:
            # Jacobian for straight-line approximation
            F = np.array([
                [1, 0, -v * np.sin(theta_k) * dt],
                [0, 1, v * np.cos(theta_k) * dt],
                [0, 0, 1]
            ])

        return F

    def h(self, x, dt=None):
        """Measurement model (identity for direct state observation).

        Assumes direct measurement of position and heading from GPS/compass or
        localization algorithm.

        Args:
            x (ndarray): State vector [x, y, theta] (3x1).
            dt (float, optional): Time step (unused for linear measurement model).

        Returns:
            ndarray: Predicted measurement vector [x, y, theta] (3x1).
        """
        return x

    def J_h(self, x, dt=None):
        """Jacobian of the measurement model.

        Since measurement model is identity (direct observation), Jacobian is identity.

        Args:
            x (ndarray): State vector [x, y, theta] (3x1).
            dt (float, optional): Time step (unused).

        Returns:
            ndarray: Jacobian matrix (identity, 3x3).
        """
        return np.eye(3)

    def update(self, u=None, dt=None, lidar_pose=None):
        """Update the EKF state estimate using control input and LiDAR measurements.

        Orchestrates the predict and correct steps of the EKF. Supports scenarios
        with or without LiDAR localization measurements.

        Args:
            u (ndarray, optional): Control input vector [v, omega].
                v: linear velocity from odometry (m/s)
                omega: angular velocity from gyroscope or odometry (rad/s)
            dt (float, optional): Time step in seconds.
            lidar_pose (ndarray, optional): LiDAR scan-matched pose measurement [x, y, theta].
                If None, prediction-only update is performed.
        """

        # Prediction step
        if dt is not None and u is not None:
            self.ekf.predict(u, dt)
            self.ekf.x_hat[2, 0] = wrap_to_pi(self.ekf.x_hat[2, 0])

        # Correction step (measurement update)
        if lidar_pose is not None:
            lidar_pose = np.squeeze(lidar_pose)

            # Handle both 1D and 2D input
            if lidar_pose.ndim == 0:
                lidar_pose = lidar_pose.reshape((1, 1))
            elif lidar_pose.ndim == 1:
                lidar_pose = lidar_pose.reshape((len(lidar_pose), 1))

            # Normalize innovation for heading component to [-pi, pi]
            # This prevents "wrapping" errors when heading crosses -pi or pi
            z_pred = self.ekf.h(self.ekf.x_hat)
            innovation = lidar_pose - z_pred
            innovation[2, 0] = wrap_to_pi(innovation[2, 0])

            # Reconstruct measurement with normalized innovation
            lidar_pose_normalized = z_pred + innovation

            self.ekf.correct(lidar_pose_normalized, dt)
            self.ekf.x_hat[2, 0] = wrap_to_pi(self.ekf.x_hat[2, 0])

        # Update public state estimate
        self.x_hat = self.ekf.x_hat