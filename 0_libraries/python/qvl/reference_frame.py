from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import math
import struct
import cv2
import numpy as np


######################### MODULAR CONTAINER CLASS #########################

class QLabsReferenceFrame(QLabsActor):
    """ This class supports the spawning of reference frame actors in the QLabs open worlds."""

    ID_REFERENCE_FRAME = 10040
    """Class ID"""
    FCN_REFERENCE_FRAME_SET_TRANSFORM = 10
    FCN_REFERENCE_FRAME_SET_TRANSFORM_ACK = 11
    FCN_REFERENCE_FRAME_SET_ICON_SCALE = 12
    FCN_REFERENCE_FRAME_SET_ICON_SCALE_ACK = 13


    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_REFERENCE_FRAME
       return

    def set_transform(self, location, rotation, scale, waitForConfirmation=True):
        """
        Change the location, rotation, and scale of a spawned reference frame in radians

        :param location: An array of floats for x, y and z coordinates
        :param rotation: An array of floats for the roll, pitch, yaw in radians
        :param scale: An array of floats for x, y and z coordinates
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the operation has occurred.
        :type location: array[3]
        :type rotation: array[3]
        :type scale: array[3]
        :type waitForConfirmation: boolean
        :return: `True` if spawn was successful, `False` otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_REFERENCE_FRAME
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_REFERENCE_FRAME_SET_TRANSFORM
        c.payload = bytearray(struct.pack(">fffffffff", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_REFERENCE_FRAME, self.actorNumber, self.FCN_REFERENCE_FRAME_SET_TRANSFORM_ACK)
                if (c == None):
                    return False
                else:
                    return True
            return True
        else:
            return False

    def set_transform_degrees(self, location, rotation, scale, waitForConfirmation=True):
        """
        Change the location and rotation of a spawned reference frame in degrees

        :param location: An array of floats for x, y and z coordinates
        :param rotation: An array of floats for the roll, pitch, yaw in degrees
        :param scale: An array of floats for x, y and z coordinates
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the operation has occurred.
        :type location: array[3]
        :type rotation: array[3]
        :type scale: array[3]
        :type waitForConfirmation: boolean
        :return: `True` if spawn was successful, `False` otherwise
        :rtype: boolean

        """
        return self.set_transform(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, waitForConfirmation)

    def set_icon_scale(self, scale, waitForConfirmation=True):
        """
        Change the scale of the axis icon only (if a visible configuration was selected) relative to the actor scale. This scale will not affect any child actors.

        :param scale: An array of floats for x, y and z coordinates
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the operation has occurred.
        :type scale: array[3]
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_REFERENCE_FRAME
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_REFERENCE_FRAME_SET_ICON_SCALE
        c.payload = bytearray(struct.pack(">fff", scale[0], scale[1], scale[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_REFERENCE_FRAME, self.actorNumber, self.FCN_REFERENCE_FRAME_SET_ICON_SCALE_ACK)
                if (c == None):
                    return False
                else:
                    return True
            return True
        else:
            return False

