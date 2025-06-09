from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import cv2
import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQBotPlatform(QLabsActor):
    """This class is for spawning QBotPlatforms."""

    ID_QBOT_PLATFORM = 23

    FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE = 10
    FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
    FCN_QBOT_PLATFORM_SET_TRANSFORM = 14
    FCN_QBOT_PLATFORM_SET_TRANSFORM_RESPONSE = 15
    FCN_QBOT_PLATFORM_POSSESS = 20
    FCN_QBOT_PLATFORM_POSSESS_ACK = 21
    FCN_QBOT_PLATFORM_IMAGE_REQUEST = 100
    FCN_QBOT_PLATFORM_IMAGE_RESPONSE = 101
    FCN_QBOT_PLATFORM_LIDAR_DATA_REQUEST = 120
    FCN_QBOT_PLATFORM_LIDAR_DATA_RESPONSE = 121
    

    VIEWPOINT_RGB = 0
    VIEWPOINT_DEPTH = 1
    VIEWPOINT_DOWNWARD = 2
    VIEWPOINT_TRAILING = 3
 
    CAMERA_RGB = 0
    CAMERA_DEPTH = 1
    CAMERA_DOWNWARD = 2
    

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_QBOT_PLATFORM
       return

    def possess(self, camera):
        """
        Possess (take control of) a QBot in QLabs with the selected camera.

        :param camera: Pre-defined camera constant. See CAMERA constants for available options. Default is the trailing camera.
        :type camera: uint32
        :return:
            - **status** - `True` if possessing the camera was successful, `False` otherwise
        :rtype: boolean

        """
        c = CommModularContainer()
        c.classID = self.ID_QBOT_PLATFORM
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_PLATFORM_POSSESS
        c.payload = bytearray(struct.pack(">B", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_POSSESS_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def command_and_request_state(self, rightWheelSpeed, leftWheelSpeed, leftLED=[1,0,0], rightLED=[1,0,0]):
        """Sets the wheel speeds and LED colors.

        :param rightWheelSpeed: Speed in m/s
        :param leftWheelSpeed: Speed in m/s
        :param leftLED: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param rightLED: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        

        :type rightWheelSpeed: float
        :type leftWheelSpeed: float
        :type leftLED: float array[3]
        :type rightLED: float array[3]

        :return:
            - **status** - `True` if successful, `False` otherwise
            - **location** - world location in m
            - **forward vector** - unit scale vector
            - **up vector** - unit scale vector
            - **front bumper hit** - true if in contact with a collision object, False otherwise
            - **left bumper hit** - true if in contact with a collision object, False otherwise
            - **right bumper hit** - true if in contact with a collision object, False otherwise
            - **gyro** - turn rate in rad/s
            - **heading** - angle in rad
            - **encoder left** - in counts
            - **encoder right** - in counts

        :rtype: boolean, float array[3], float array[3], float array[3], boolean, boolean, boolean, float, float, uint32, uint32


        """
        c = CommModularContainer()
        c.classID = self.ID_QBOT_PLATFORM
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ffffffff", rightWheelSpeed, leftWheelSpeed, leftLED[0], leftLED[1], leftLED[2], rightLED[0], rightLED[1], rightLED[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        location = [0,0,0]
        forward = [0,0,0]
        up = [0,0,0]
        frontHit = False
        leftHit = False
        rightHit = False
        gyro = 0
        heading = 0
        encoderLeft = 0
        encoderRight = 0


        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE)

            if (c == None):
                return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight

            if len(c.payload) == 55:
                location[0], location[1], location[2], forward[0], forward[1], forward[2], up[0], up[1], up[2], frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight, = struct.unpack(">fffffffff???ffII", c.payload[0:55])
                return True, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight
            else:
                return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight
        else:
            return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight
               
    def set_transform(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], leftLED=[1,0,0], rightLED=[1,0,0], enableDynamics=True, waitForConfirmation=True):
        """Sets the transform, LED colors, and enabling/disabling of physics dynamics

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param leftLED: (Optional) Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param rightLED: (Optional) Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param enableDynamics: (default True) Enables or disables gravity for set transform requests.
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation. NOTE: Return data will only be valid if waitForConfirmation is True.
        
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type leftLED: float array[3]
        :type rightLED: float array[3
        :type enableDynamics: boolean
        :type waitForConfirmation: boolean

        :return:
            - **status** - True if successful or False otherwise
            - **location** - world location in m
            - **forward vector** - unit scale vector
            - **up vector** - unit scale vector

        :rtype: boolean, float array[3], float array[3], float array[3]


        """
        c = CommModularContainer()
        c.classID = self.ID_QBOT_PLATFORM
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_PLATFORM_SET_TRANSFORM
        c.payload = bytearray(struct.pack(">fffffffffffffffB", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], leftLED[0], leftLED[1], leftLED[2], rightLED[0], rightLED[1], rightLED[2], enableDynamics))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        location = [0,0,0]
        forward = [0,0,0]
        up = [0,0,0]
        

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_SET_TRANSFORM_RESPONSE)

                if (c == None):
                    return False, location, forward, up

                if len(c.payload) == 36:

                    location[0], location[1], location[2], forward[0], forward[1], forward[2], up[0], up[1], up[2], = struct.unpack(">fffffffff", c.payload[0:36])
                    return True, location, forward, up
                else:
                    return False, location, forward, up
            else:
                return True, location, forward, up
        else:
            return False, location, forward, up

    def set_transform_degrees(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], leftLED=[1,0,0], rightLED=[1,0,0], enableDynamics=True, waitForConfirmation=True):
        """Sets the transform, LED colors, and enabling/disabling of physics dynamics

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param leftLED: (Optional) Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param rightLED: (Optional) Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param enableDynamics: (default True) Enables or disables gravity for set transform requests.
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation. NOTE: Return data will only be valid if waitForConfirmation is True.
        
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type leftLED: float array[3]
        :type rightLED: float array[3
        :type enableDynamics: boolean
        :type waitForConfirmation: boolean

        :return:
            - **status** - True if successful or False otherwise
            - **location** - world location in m
            - **forward vector** - unit scale vector
            - **up vector** - unit scale vector

        :rtype: boolean, float array[3], float array[3], float array[3]


        """
        
        
        success, location, forward, up = self.set_transform(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, leftLED, rightLED, enableDynamics, waitForConfirmation)

        return success, location, forward, up
        
    def get_image(self, camera):
        """
        Request a JPG image from the QBot camera.

        :param camera: Camera number to view from.
        
        :type camera: byte

        :return:
            - **status** - `True` and image data if successful, `False` and empty otherwise
            - **imageData** - Image in a JPG format
        :rtype: boolean, byte array with jpg data

        """

        if (not self._is_actor_number_valid()):
            return False, None

        c = CommModularContainer()
        c.classID = self.ID_QBOT_PLATFORM
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_PLATFORM_IMAGE_REQUEST
        c.payload = bytearray(struct.pack(">B", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_IMAGE_RESPONSE)

            if (c == None):
                return False, None


            imageData = cv2.imdecode(np.frombuffer(bytearray(c.payload[8:len(c.payload)]), dtype=np.uint8, count=-1, offset=0), 1)


            return True, imageData
        else:
            return False, None

    def get_lidar(self, samplePoints=400):
        """
        Request LIDAR data from a QBotPlatform.

        :param samplePoints: (Optional) Change the number of points per revolution of the LIDAR.
        :type samplePoints: uint32
        :return: `True`, angles in radians, and distances in m if successful, `False`, none, and none otherwise
        :rtype: boolean, float array, float array

        """

        if (not self._is_actor_number_valid()):
            if (self._verbose):
                print('actorNumber object variable None. Use a spawn function to assign an actor or manually assign the actorNumber variable.')
            return False, None, None
            

        LIDAR_SAMPLES = 4096
        LIDAR_RANGE = 8

        # The LIDAR is simulated by using 4 orthogonal virtual cameras that are 1 pixel high. The
        # lens distortion of these cameras must be removed to accurately calculate the XY position
        # of the depth samples.
        quarter_angle = np.linspace(0, 45, int(LIDAR_SAMPLES/8))
        lens_curve = -0.0077*quarter_angle*quarter_angle + 1.3506*quarter_angle
        lens_curve_rad = lens_curve/180*np.pi

        angles = np.concatenate((np.pi*4/2-1*np.flip(lens_curve_rad), \
                                 lens_curve_rad, \
                                 (np.pi/2 - 1*np.flip(lens_curve_rad)), \
                                 (np.pi/2 + lens_curve_rad), \
                                 (np.pi - 1*np.flip(lens_curve_rad)), \
                                 (np.pi + lens_curve_rad), \
                                 (np.pi*3/2 - 1*np.flip(lens_curve_rad)), \
                                 (np.pi*3/2 + lens_curve_rad)))



        c = CommModularContainer()
        c.classID = self.ID_QBOT_PLATFORM
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_PLATFORM_LIDAR_DATA_REQUEST
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT_PLATFORM, self.actorNumber, self.FCN_QBOT_PLATFORM_LIDAR_DATA_RESPONSE)

            if (c == None):
                if (self._verbose):
                    print('Failed to receive return container.')
                return False, None, None

            if ((len(c.payload)-4)/2 != LIDAR_SAMPLES):
                
                if (self._verbose):
                    print("Received {} bytes, expected {}".format(len(c.payload), LIDAR_SAMPLES*2))

                return False, None, None

            distance = np.linspace(0,0,LIDAR_SAMPLES)

            for count in range(LIDAR_SAMPLES-1):
                # clamp any value at 65535 to 0
                raw_value = ((c.payload[4+count*2] * 256 + c.payload[5+count*2] )) %65535

                # scale to LIDAR range
                distance[count] = (raw_value/65535)*LIDAR_RANGE


            # Resample the data using a linear radial distribution to the desired number of points
            # and realign the first index to be 0 (forward)
            sampled_angles = np.linspace(0,2*np.pi, num=samplePoints, endpoint=False)
            sampled_distance = np.linspace(0,0, samplePoints)

            index_raw = 512
            for count in range(samplePoints):
                while (angles[index_raw] < sampled_angles[count]):
                    index_raw = (index_raw + 1) % 4096


                if index_raw != 0:
                    if (angles[index_raw]-angles[index_raw-1]) == 0:
                        sampled_distance[count] = distance[index_raw]
                    else:
                        sampled_distance[count] = (distance[index_raw]-distance[index_raw-1])*(sampled_angles[count]-angles[index_raw-1])/(angles[index_raw]-angles[index_raw-1]) + distance[index_raw-1]


                else:
                    sampled_distance[count] = distance[index_raw]


            return True, sampled_angles, sampled_distance
        else:
            if (self._verbose):
                print('Communications request for LIDAR data failed.')
            return False, None, None