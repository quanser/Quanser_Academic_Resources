from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import math
import struct
import cv2
import numpy as np


######################### MODULAR CONTAINER CLASS #########################

class QLabsQCar(QLabsActor):
    """This class is for spawning QCars."""


    ID_QCAR = 160
    """ Class ID """
    FCN_QCAR_SET_VELOCITY_AND_REQUEST_STATE = 10
    FCN_QCAR_VELOCITY_STATE_RESPONSE = 11
    FCN_QCAR_SET_TRANSFORM_AND_REQUEST_STATE = 12
    FCN_QCAR_TRANSFORM_STATE_RESPONSE = 13
    FCN_QCAR_POSSESS = 20
    FCN_QCAR_POSSESS_ACK = 21
    FCN_QCAR_GHOST_MODE = 22
    FCN_QCAR_GHOST_MODE_ACK = 23
    FCN_QCAR_CAMERA_DATA_REQUEST = 100
    FCN_QCAR_CAMERA_DATA_RESPONSE = 101
    FCN_QCAR_LIDAR_DATA_REQUEST = 110
    FCN_QCAR_LIDAR_DATA_RESPONSE = 111


    CAMERA_CSI_RIGHT = 0
    #Image capture resolution: 820x410
    CAMERA_CSI_BACK = 1
    #Image capture resolution: 820x410
    CAMERA_CSI_LEFT = 2
    #Image capture resolution: 820x410
    CAMERA_CSI_FRONT = 3
    #Image capture resolution: 820x410
    CAMERA_RGB = 4
    #Image capture resolution: 640x480
    CAMERA_DEPTH = 5
    #Image capture resolution: 640x480
    CAMERA_OVERHEAD = 6
    CAMERA_TRAILING = 7
    #Note: The mouse scroll wheel can be used to zoom in and out in this mode. """

    _sensor_scaling = 1


    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_QCAR
       return

    def spawn_id(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new QCar actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 unknown error, -1 communications error
        :rtype: int32

        """

        self._sensor_scaling = scale[0]
        return super().spawn_id(actorNumber, location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn_id_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new QCar actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 unknown error, -1 communications error
        :rtype: int32

        """
        
        self._sensor_scaling = scale[0]
        return super().spawn_id_degrees(actorNumber, location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new QCar actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred. Note that if this is False, the returned actor number will be invalid.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 3 unknown error, -1 communications error.
            - **actorNumber** - An actor number to use for future references.
        :rtype: int32, int32

        """   

        self._sensor_scaling = scale[0]
        return super().spawn(location, rotation, scale, configuration, waitForConfirmation)
               
    def spawn_degrees(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new QCar actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred. Note that if this is False, the returned actor number will be invalid.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 3 unknown error, -1 communications error.
            - **actorNumber** - An actor number to use for future references.
        :rtype: int32, int32

        """
        self._sensor_scaling = scale[0]
        return super().spawn_degrees(location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn_id_and_parent_with_relative_transform(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new QCar actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 cannot find the parent actor, 4 unknown error, -1 communications error
        :rtype: int32

        """

        self._sensor_scaling = scale[0]
        return super().spawn_id_and_parent_with_relative_transform(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)

    def spawn_id_and_parent_with_relative_transform_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new QCar actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 cannot find the parent actor, 4 unknown error, -1 communications error
        :rtype: int32

        """

        self._sensor_scaling = scale[0]
        return super().spawn_id_and_parent_with_relative_transform_degrees(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)

    def set_transform_and_request_state(self, location, rotation, enableDynamics, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal, waitForConfirmation=True):
        """Sets the location, rotation, and other car properties. Note that setting the location ignores collisions so ensure that the location is free of obstacles that may trap the actor if it is subsequently used in a dynamic mode. This transform can also be used to "playback" previously recorded position data without the need for a full dynamic model.

        :param location: An array of floats for x, y and z coordinates in full-scale units. Multiply physical QCar locations by 10 to get full scale locations.
        :param rotation: An array of floats for the roll, pitch, and yaw in radians
        :param enableDynamics: (default True) Enables or disables gravity for set transform requests.
        :param headlights: Enable the headlights
        :param leftTurnSignal: Enable the left turn signal
        :param rightTurnSignal: Enable the right turn signal
        :param brakeSignal: Enable the brake lights (does not affect the motion of the vehicle)
        :param reverseSignal: Play a honking sound
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation. NOTE: Return data will only be valid if waitForConfirmation is True.
        :type location: float array[3]
        :type rotation: float array[3]
        :type enableDynamics: boolean
        :type headlights: boolean
        :type leftTurnSignal: boolean
        :type rightTurnSignal: boolean
        :type brakeSignal: boolean
        :type reverseSignal: boolean
        :type waitForConfirmation: boolean
        :return:
            - **status** - True if successful or False otherwise
            - **location** - in full scale
            - **rotation** - in radians
            - **forward vector** - unit scale vector
            - **up vector** - unit scale vector
            - **front bumper hit** - True if in contact with a collision object, False otherwise
            - **rear bumper hit** - True if in contact with a collision object, False otherwise
        :rtype: boolean, float array[3], float array[3], float array[3], float array[3], boolean, boolean

        """
        if (not self._is_actor_number_valid()):
            return False, [0,0,0], [0,0,0], [0,0,0], [0,0,0], False, False

        c = CommModularContainer()
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_SET_TRANSFORM_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ffffffBBBBBB", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], enableDynamics, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)


        location = [0,0,0]
        rotation = [0,0,0]
        forward_vector = [0,0,0]
        up_vector = [0,0,0]
        frontHit = False
        rearHit = False

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_TRANSFORM_STATE_RESPONSE)

                if (c == None):
                    return False, location, rotation, forward_vector, up_vector, frontHit, rearHit

                if len(c.payload) == 50:

                    location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], forward_vector[0], forward_vector[1], forward_vector[2], up_vector[0], up_vector[1], up_vector[2], frontHit, rearHit, = struct.unpack(">ffffffffffff??", c.payload[0:50])
                    return True, location, rotation, forward_vector, up_vector, frontHit, rearHit
                else:
                    return False, location, rotation, forward_vector, up_vector, frontHit, rearHit
            else:
                return True, location, rotation, forward_vector, up_vector, frontHit, rearHit
        else:
            return False, location, rotation, forward_vector, up_vector, frontHit, rearHit

    def set_transform_and_request_state_degrees(self, location, rotation, enableDynamics, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal, waitForConfirmation=True):
        """Sets the location, rotation, and other car properties. Note that setting the location ignores collisions so ensure that the location is free of obstacles that may trap the actor if it is subsequently used in a dynamic mode. This transform can also be used to "playback" previously recorded position data without the need for a full dynamic model.

        :param location: An array of floats for x, y and z coordinates in full-scale units. Multiply physical QCar locations by 10 to get full scale locations.
        :param rotation: An array of floats for the roll, pitch, and yaw in degrees.
        :param enableDynamics: (default True) Enables or disables gravity for set transform requests.
        :param headlights: Enable the headlights.
        :param leftTurnSignal: Enable the left turn signal.
        :param rightTurnSignal: Enable the right turn signal.
        :param brakeSignal: Enable the brake lights (does not affect the motion of the vehicle).
        :param reverseSignal: Enable the reverse lights.
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation. NOTE: Return data will only be valid if waitForConfirmation is True.
        :type location: float array[3]
        :type rotation: float array[3]
        :type enableDynamics: boolean
        :type headlights: boolean
        :type leftTurnSignal: boolean
        :type rightTurnSignal: boolean
        :type brakeSignal: boolean
        :type reverseSignal: boolean
        :type waitForConfirmation: boolean
        :return:
            - **status** - True if successful or False otherwise
            - **location** - in full scale
            - **rotation** - in radians
            - **forward vector** - unit scale vector
            - **up vector** - unit scale vector
            - **front bumper hit** - True if in contact with a collision object, False otherwise
            - **rear bumper hit** - True if in contact with a collision object, False otherwise
        :rtype: boolean, float array[3], float array[3], float array[3], float array[3], boolean, boolean

        """
        success, location, rotation, forward_vector, up_vector, frontHit, rearHit = self.set_transform_and_request_state(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], enableDynamics, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal, waitForConfirmation)
        rotation_deg = [rotation[0]/math.pi*180, rotation[1]/math.pi*180, rotation[2]/math.pi*180]

        return success, location, rotation_deg, forward_vector, up_vector, frontHit, rearHit

    def set_velocity_and_request_state(self, forward, turn, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal):
        """Sets the velocity, turn angle in radians, and other car properties.

        :param forward: Speed in m/s of a full-scale car. Multiply physical QCar speeds by 10 to get full scale speeds.
        :param turn: Turn angle in radians. Positive values turn right.
        :param headlights: Enable the headlights.
        :param leftTurnSignal: Enable the left turn signal.
        :param rightTurnSignal: Enable the right turn signal.
        :param brakeSignal: Enable the brake lights (does not affect the motion of the vehicle).
        :param reverseSignal: Enable the reverse lights.
        :type forward: float
        :type turn: float
        :type headlights: boolean
        :type leftTurnSignal: boolean
        :type rightTurnSignal: boolean
        :type brakeSignal: boolean
        :type reverseSignal: boolean
        :return:
            - **status** - True if successful, False otherwise
            - **location**
            - **rotation** - in radians
            - **front bumper hit** - True if in contact with a collision object, False otherwise
            - **rear bumper hit** - True if in contact with a collision object, False otherwise
        :rtype: boolean, float array[3], float array[3], boolean, boolean


        """

        if (not self._is_actor_number_valid()):
            return False, [0,0,0], [0,0,0], False, False

        c = CommModularContainer()
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_SET_VELOCITY_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ffBBBBB", forward, turn, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        location = [0,0,0]
        rotation = [0,0,0]
        frontHit = False
        rearHit = False


        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_VELOCITY_STATE_RESPONSE)

            if (c == None):
                return False, location, rotation, frontHit, rearHit

            if len(c.payload) == 26:
                location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], frontHit, rearHit, = struct.unpack(">ffffff??", c.payload[0:26])
                return True, location, rotation, frontHit, rearHit
            else:
                return False, location, rotation, frontHit, rearHit
        else:
            return False, location, rotation, frontHit, rearHit

    def set_velocity_and_request_state_degrees(self, forward, turn, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal):
        """Sets the velocity, turn angle in degrees, and other car properties.

        :param forward: Speed in m/s of a full-scale car. Multiply physical QCar speeds by 10 to get full scale speeds.
        :param turn: Turn angle in degrees. Positive values turn right.
        :param headlights: Enable the headlights.
        :param leftTurnSignal: Enable the left turn signal.
        :param rightTurnSignal: Enable the right turn signal.
        :param brakeSignal: Enable the brake lights (does not affect the motion of the vehicle).
        :param reverseSignal: Enable the reverse lights.
        :type forward: float
        :type turn: float
        :type headlights: boolean
        :type leftTurnSignal: boolean
        :type rightTurnSignal: boolean
        :type brakeSignal: boolean
        :type reverseSignal: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
            - **location**
            - **rotation** - in radians
            - **front bumper hit** - `True` if in contact with a collision object, `False` otherwise
            - **rear bumper hit** - `True` if in contact with a collision object, `False` otherwise
        :rtype: boolean, float array[3], float array[3], boolean, boolean


        """
        success, location, rotation, frontHit, rearHit = self.set_velocity_and_request_state(forward, turn/180*math.pi, headlights, leftTurnSignal, rightTurnSignal, brakeSignal, reverseSignal)

        rotation_deg = [rotation[0]/math.pi*180, rotation[1]/math.pi*180, rotation[2]/math.pi*180]
        return success, location, rotation_deg, frontHit, rearHit

    def possess(self, camera=CAMERA_TRAILING):
        """
        Possess (take control of) a QCar in QLabs with the selected camera.

        :param camera: Pre-defined camera constant. See CAMERA constants for available options. Default is the trailing camera.
        :type camera: uint32
        :return:
            - **status** - `True` if possessing the camera was successful, `False` otherwise
        :rtype: boolean

        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_POSSESS
        c.payload = bytearray(struct.pack(">B", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_POSSESS_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def ghost_mode(self, enable=True, color=[0,1,0]):
        """
        Ghost mode changes the selected QCar actor into a transparent colored version. This can be useful as a reference actor or indicating a change in state.

        :param enable: Set the QCar to the defined transparent color, otherwise revert to the solid color scheme.
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :type camera: uint32
        :type enable: boolean
        :type color: float array[3]
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean

        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_GHOST_MODE
        c.payload = bytearray(struct.pack(">Bfff", enable, color[0], color[1], color[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_GHOST_MODE_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def get_image(self, camera):
        """
        Request a JPG image from one of the QCar cameras.

        :param camera: Pre-defined camera constant. See CAMERA constants for available options. Trailing and Overhead cameras cannot be selected.
        :type camera: uint32
        :return:
            - **status** - `True` and image data if successful, `False` and empty otherwise
            - **imageData** - Image in a JPG format
        :rtype: boolean, byte array with jpg data

        """

        if (not self._is_actor_number_valid()):
            return False, None

        c = CommModularContainer()
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_CAMERA_DATA_REQUEST
        c.payload = bytearray(struct.pack(">I", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_CAMERA_DATA_RESPONSE)

            if (c == None):
                return False, None


            jpg_buffer = cv2.imdecode(np.frombuffer(bytearray(c.payload[8:len(c.payload)]), dtype=np.uint8, count=-1, offset=0), 1)


            return True, jpg_buffer
        else:
            return False, None

    def get_lidar(self, samplePoints=400):
        """
        Request LIDAR data from a QCar.

        :param samplePoints: (Optional) Change the number of points per revolution of the LIDAR.
        :type samplePoints: uint32
        :return: `True`, angles in radians, and distances in m if successful, `False`, none, and none otherwise
        :rtype: boolean, float array, float array

        """

        if (not self._is_actor_number_valid()):
            return False, None, None

        LIDAR_SAMPLES = 4096
        LIDAR_RANGE = 80*self._sensor_scaling

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
        c.classID = self.ID_QCAR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QCAR_LIDAR_DATA_REQUEST
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QCAR, self.actorNumber, self.FCN_QCAR_LIDAR_DATA_RESPONSE)

            if (c == None):
                return False, None, None

            if ((len(c.payload)-4)/2 != LIDAR_SAMPLES):
                #print("Received {} bytes, expected {}".format(len(c.payload), LIDAR_SAMPLES*2))
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
            return False, None, None


