from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

from quanser.common import GenericError
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQBot2e(QLabsActor):


    ID_QBOT2e = 20

    FCN_QBOT_COMMAND_AND_REQUEST_STATE = 10
    FCN_QBOT_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
    FCN_QBOT_POSSESS = 20
    FCN_QBOT_POSSESS_ACK = 21


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
       self.classID = self.ID_QBOT2e
       return


    def possess(self, qlabs, actorNumber, camera):
        c = CommModularContainer()
        c.classID = self.ID_QBOT2e
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_POSSESS
        c.payload = bytearray(struct.pack(">B", camera))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT2e, self.actorNumber, self.FCN_QBOT_POSSESS_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def command_and_request_state(self, rightWheelSpeed, leftWheelSpeed):
        c = CommModularContainer()
        c.classID = self.ID_QBOT2e
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_QBOT_COMMAND_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ff", rightWheelSpeed, leftWheelSpeed))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_QBOT2e, self.actorNumber, self.FCN_QBOT_COMMAND_AND_REQUEST_STATE_RESPONSE)

            return True
        else:
            return False

