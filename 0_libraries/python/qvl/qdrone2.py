from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import cv2
import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQDrone2(QLabsActor):
    """This class is for spawning a QDrone 2."""

    ID_QDRONE2 = 231

    FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE = 10
    FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE_RESPONSE = 11
    FCN_QDRONE2_SET_WORLD_TRANSFORM = 12
    FCN_QDRONE2_SET_WORLD_TRANSFORM_ACK = 13
    FCN_QDRONE2_POSSESS = 20
    FCN_QDRONE2_POSSESS_ACK = 21
    FCN_QDRONE2_IMAGE_REQUEST = 100
    FCN_QDRONE2_IMAGE_RESPONSE = 101
    FCN_QDRONE2_SET_CAMERA_RESOLUTION = 102
    FCN_QDRONE2_SET_CAMERA_RESOLUTION_RESPONSE = 103
    

    VIEWPOINT_CSI_LEFT = 0
    VIEWPOINT_CSI_BACK = 1
    VIEWPOINT_CSI_RIGHT = 2
    VIEWPOINT_RGB = 3
    VIEWPOINT_DEPTH = 4
    VIEWPOINT_DOWNWARD = 5
    VIEWPOINT_OPTICAL_FLOW = 6
    VIEWPOINT_OVERHEAD = 7
    VIEWPOINT_TRAILING = 8
 
    CAMERA_CSI_LEFT = 0
    CAMERA_CSI_BACK = 1
    CAMERA_CSI_RIGHT = 2
    CAMERA_RGB = 3
    CAMERA_DEPTH = 4
    CAMERA_DOWNWARD = 5
    CAMERA_OPTICAL_FLOW = 6
    

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_QDRONE2
       return

    def possess(self, camera=VIEWPOINT_TRAILING):
        """
        Possess (take control of) a QDrone in QLabs with the selected camera.

        :param camera: Pre-defined camera constant. See CAMERA constants for available options. Default is the trailing camera.
        :type camera: uint32
        :return:
            - **status** - `True` if possessing the camera was successful, `False` otherwise
        :rtype: boolean

        """
        
        if (not self._is_actor_number_valid()):
            return False
        
        c = CommModularContainer()
        c.classID = self.ID_QDRONE2
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QDRONE2_POSSESS
        c.payload = bytearray(struct.pack(">I", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QDRONE2, self.actorNumber, self.FCN_QDRONE2_POSSESS_ACK)
            if (c == None):
                if self._verbose:
                    print("QDrone 2 possess: No data returned from QLabs possibly due to a communcations timeout.")
                return False
            else:
                return True
        else:
            if self._verbose:
                print("QDrone 2 possess: Communications failure.")
            return False

    def set_velocity_and_request_state(self, motorsEnabled=False, velocity=[0,0,0], orientation=[0,0,0]):
        """Sets the velocity, turn angle in radians, and other properties.

        :param motorsEnabled: Enable the motors. Disabled by default immediately after spawning.
        :param velocity: The linear velocity in m/s in the body frame.
        :param orientation: The orientation in radians expressed in roll-pitch-yaw Euler angles.
        
        :type motorsEnabled: boolean
        :type velocity: float array[3]
        :type orientation: float array[3]

        :return:
            - **status** - `True` if successful, `False` otherwise. Other returned values are invalid if status is `False`.
            - **location** - World location in m
            - **orientation** - World orientation in radians (roll, pitch, yaw)
            - **quaternion** - World orientation in a quaternion vector
            - **velocity** - World linear velocity in m/s
            - **TOF distance** - Time of flight distance sensor. Returns 0 when outside the range of the sensor (too close or too far).
            - **collision** - The QDrone is currently colliding with another object or the environment.
            - **collision location** - Body frame location. Invalid if collision is False.
            - **collision force vector** - The vector along which the collision force is occuring. Invalid if collision is False.
            
        :rtype: boolean, float array[3], float array[3], float array[4], float array[3], float, boolean, float array[3], float array[3]


        """
        if (not self._is_actor_number_valid()):
            return False, [0,0,0], [0,0,0], [0,0,0,0], [0,0,0], 0.0, False, [0,0,0], [0,0,0]
        
        c = CommModularContainer()
        c.classID = self.ID_QDRONE2
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ffffffB", velocity[0], velocity[1], velocity[2], orientation[0], orientation[1], orientation[2], motorsEnabled))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)
        
        location = [0,0,0]
        orientation = [0,0,0]
        quaternion = [0,0,0,0]
        velocity = [0,0,0]
        TOFDistance = 0
        collision = False
        collisionLocation = [0,0,0]
        collisionForce = [0,0,0]  


        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QDRONE2, self.actorNumber, self.FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE_RESPONSE)

            if (c == None):
                if self._verbose:
                    print("QDrone 2 command_velocity_and_request_state: Received no data from QLabs possibly due to a communcations timeout.")
                return False, location, orientation, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce

            if len(c.payload) == 81:
                location[0], location[1], location[2], orientation[0], orientation[1], orientation[2], quaternion[0], quaternion[1], quaternion[2], quaternion[3], velocity[0], velocity[1], velocity[2], TOFDistance, collision, collisionLocation[0], collisionLocation[1], collisionLocation[2], collisionForce[0], collisionForce[1], collisionForce[2], = struct.unpack(">ffffffffffffff?ffffff", c.payload[0:81])
                return True, location, orientation, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce
            else:
                if self._verbose:
                    print("QDrone 2 command_velocity_and_request_state: Response packet was not the expected length ({} bytes).".format(len(c.payload)))
                return False, location, orientation, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce

        else:
            if self._verbose:
                print("QDrone 2 command_velocity_and_request_state: Communications failure.")
            return False, location, orientation, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce

    def set_velocity_and_request_state_degrees(self, motorsEnabled=False, velocity=[0,0,0], orientation=[0,0,0]):
        """Sets the velocity, turn angle in radians, and other properties.

        :param motorsEnabled: Enable the motors. Disabled by default immediately after spawning.
        :param velocity: The linear velocity in m/s in the body frame.
        :param orientation: The orientation in degrees expressed in roll-pitch-yaw Euler angles.
        
        :type motorsEnabled: boolean
        :type velocity: float array[3]
        :type orientation: float array[3]

        :return:
            - **status** - `True` if successful, `False` otherwise. Other returned values are invalid if status is `False`.
            - **location** - World location in m
            - **orientation** - World orientation in degrees (roll, pitch, yaw)
            - **quaternion** - World orientation in a quaternion vector
            - **velocity** - World linear velocity in m/s
            - **TOF distance** - Time of flight distance sensor. Returns 0 when outside the range of the sensor (too close or too far).
            - **collision** - The QDrone is currently colliding with another object or the environment.
            - **collision location** - Body frame location. Invalid if collision is False.
            - **collision force vector** - The vector along which the collision force is occuring. Invalid if collision is False.
            
        :rtype: boolean, float array[3], float array[3], float array[4], float array[3], float, boolean, float array[3], float array[3]


        """   

        success, location, orientation_r, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce = self.set_velocity_and_request_state(motorsEnabled, velocity, [orientation[0]/180*math.pi, orientation[1]/180*math.pi, orientation[2]/180*math.pi])
        
        orientation_d = [orientation_r[0]/math.pi*180, orientation_r[1]/math.pi*180, orientation_r[2]/math.pi*180]
        
        return success, location, orientation_d, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce

    def set_transform_and_dynamics(self, location, rotation, enableDynamics, waitForConfirmation=True):
        """Sets the location, rotation, and other properties. Note that setting the location ignores collisions so ensure that the location is free of obstacles that may trap the actor if it is subsequently used in a dynamic mode. This transform can also be used to "playback" previously recorded position data without the need for a full dynamic model.

        :param location: An array of floats for x, y and z coordinates in full-scale units. 
        :param rotation: An array of floats for the roll, pitch, and yaw in radians
        :param enableDynamics: Enables or disables dynamics. The velocity commands will have no effect when the dynamics are disabled.
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation.
        :type location: float array[3]
        :type rotation: float array[3]
        :type enableDynamics: boolean
        :type waitForConfirmation: boolean
        :return:
            - **status** - True if successful or False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_QDRONE2
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QDRONE2_SET_WORLD_TRANSFORM
        c.payload = bytearray(struct.pack(">ffffffB", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], enableDynamics))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)


        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_QDRONE2, self.actorNumber, self.FCN_QDRONE2_SET_WORLD_TRANSFORM_ACK)

                if (c == None):
                    return False

                
            return True
        else:
            return False

    def get_image(self, camera):
        """
        Request a JPG image from the QDrone camera.

        :param camera: Camera number to view from. Use the CAMERA constants.
        
        :type camera: int32

        :return:
            - **status** - `True` and image data if successful, `False` and empty otherwise
            - **cameraNumber** - The number of the camera currently being read
            - **imageData** - Image in a JPG format
        :rtype: boolean, int32, byte array with jpg data

        """

        if (not self._is_actor_number_valid()):
            return False, -1, None

        c = CommModularContainer()
        c.classID = self.ID_QDRONE2
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QDRONE2_IMAGE_REQUEST
        c.payload = bytearray(struct.pack(">I", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QDRONE2, self.actorNumber, self.FCN_QDRONE2_IMAGE_RESPONSE)

            if (c == None):
                if self._verbose:
                    print("QDrone 2 get_image: No data returned from QLabs possibly due to a communcations timeout.")
                return False, -1, None

            if len(c.payload) >= 8:
                camera_number, image_size, = struct.unpack(">II", c.payload[0:8])

                if (camera_number >= 0) and (len(c.payload) > 8):
                    imageData = cv2.imdecode(np.frombuffer(bytearray(c.payload[8:len(c.payload)]), dtype=np.uint8, count=-1, offset=0), 1)
                    
                    if (imageData is None) and self._verbose:
                        print("QDrone 2 get_image: Error decoding image data.")   
                    return True, camera_number, imageData
                else:
                    if self._verbose:
                        if (camera_number >= 0):
                            print("QDrone 2 get_image: Camera number was invalid.")
                        else:
                            print("Camera number was valid, but no image data was returned. Check that the image size is valid.")
                    return False, -1, None                    
            else:
                if self._verbose:
                    print("QDrone 2 get_image: Returned data was not in the expected format.")
                return False, -1, None
        else:
            if self._verbose:
                print("QDrone 2 get_image: Communications failure.")
            return False, -1, None

    def set_image_capture_resolution(self, width=640, height=480):
        """Change the default width and height of image resolution for capture

        :param width: Must be an even number. Default 640
        :param height: Must be an even number. Default 480
        :type width: uint32
        :type height: uint32
        :return: `True` if spawn was successful, `False` otherwise
        :rtype: boolean
        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_FREE_CAMERA
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION
        c.payload = bytearray(struct.pack(">II", width, height))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_FREE_CAMERA, self.actorNumber, self.FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION_RESPONSE)
            if (c == None):
                return False
            else:
                return True
        else:
            return False