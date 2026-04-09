import numpy as np
import cv2

from pal.products.qbot_platform import QBotPlatformDriver
from pal.utilities.math import Calculus
from scipy.ndimage import median_filter
from pal.utilities.math import Calculus
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
