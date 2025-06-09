from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import cv2
import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQBot3(QLabsActor):


    ID_QBOT3 = 22

    FCN_QBOT3_COMMAND_AND_REQUEST_STATE = 10
    FCN_QBOT3_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
    FCN_QBOT3_POSSESS = 20
    FCN_QBOT3_POSSESS_ACK = 21
    FCN_QBOT3_RGB_REQUEST = 100
    FCN_QBOT3_RGB_RESPONSE = 101
    FCN_QBOT3_DEPTH_REQUEST = 110
    FCN_QBOT3_DEPTH_RESPONSE = 111


    VIEWPOINT_RGB = 0
    VIEWPOINT_DEPTH = 1
    VIEWPOINT_TRAILING = 2

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_QBOT3
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
        c.classID = self.ID_QBOT3
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT3_POSSESS
        c.payload = bytearray(struct.pack(">B", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT3, self.actorNumber, self.FCN_QBOT3_POSSESS_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def command_and_request_state(self, rightWheelSpeed, leftWheelSpeed):
        """Sets the velocity, turn angle in radians, and other car properties.

        :param forward: Speed in m/s of a full-scale car. Multiply physical QCar speeds by 10 to get full scale speeds.
        :param turn: Turn angle in radians. Positive values turn right.

        :type actorNumber: float
        :type turn: float

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
        c.classID = self.ID_QBOT3
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT3_COMMAND_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ff", rightWheelSpeed, leftWheelSpeed))
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
            c = self._qlabs.wait_for_container(self.ID_QBOT3, self.actorNumber, self.FCN_QBOT3_COMMAND_AND_REQUEST_STATE_RESPONSE)

            if (c == None):
                return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight

            if len(c.payload) == 55:
                location[0], location[1], location[2], forward[0], forward[1], forward[2], up[0], up[1], up[2], frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight, = struct.unpack(">fffffffff???ffII", c.payload[0:55])
                return True, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight
            else:
                return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight
        else:
            return False, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight

    def get_image_rgb(self):
        """
        Request a JPG image from the QBot camera.

        :return:
            - **status** - `True` and image data if successful, `False` and empty otherwise
            - **imageData** - Image in a JPG format
        :rtype: boolean, byte array with jpg data

        """

        if (not self._is_actor_number_valid()):
            return False, None

        c = CommModularContainer()
        c.classID = self.ID_QBOT3
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT3_RGB_REQUEST
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT3, self.actorNumber, self.FCN_QBOT3_RGB_RESPONSE)

            if (c == None):
                return False, None


            jpg_buffer = cv2.imdecode(np.frombuffer(bytearray(c.payload[4:len(c.payload)]), dtype=np.uint8, count=-1, offset=0), 1)


            return True, jpg_buffer
        else:
            return False, None

    def get_image_depth(self):
        """
        Request a JPG image from the QBot camera.

        :return:
            - **status** - `True` and image data if successful, `False` and empty otherwise
            - **imageData** - Image in a JPG format
        :rtype: boolean, byte array with jpg data

        """

        if (not self._is_actor_number_valid()):
            return False, None

        c = CommModularContainer()
        c.classID = self.ID_QBOT3
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT3_DEPTH_REQUEST
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT3, self.actorNumber, self.FCN_QBOT3_DEPTH_RESPONSE)

            if (c == None):
                return False, None


            jpg_buffer = cv2.imdecode(np.frombuffer(bytearray(c.payload[4:len(c.payload)]), dtype=np.uint8, count=-1, offset=0), 1)


            return True, jpg_buffer
        else:
            return False, None