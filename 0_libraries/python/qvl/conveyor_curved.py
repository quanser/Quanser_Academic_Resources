from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
from qvl.actor import QLabsActor
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsConveyorCurved(QLabsActor):


    ID_CONVEYOR_CURVED = 211

    FCN_CONVEYOR_CURVED_SET_SPEED = 10
    FCN_CONVEYOR_CURVED_SET_SPEED_ACK = 11


    # Initialize class
    def __init__(self, qlabs, verbose=False):
        """ Constructor Method

        :param qlabs: A QuanserInteractiveLabs object
        :param verbose: (Optional) Print error information to the console.
        :type qlabs: object
        :type verbose: boolean
        """

        self._qlabs = qlabs
        self._verbose = verbose
        self.classID = self.ID_CONVEYOR_CURVED
        return

    def set_speed(self, speed):
        c = CommModularContainer()
        c.classID = self.ID_CONVEYOR_CURVED
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_CONVEYOR_CURVED_SET_SPEED
        c.payload = bytearray(struct.pack(">f", speed))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_CONVEYOR_CURVED, self.actorNumber, self.FCN_CONVEYOR_CURVED_SET_SPEED_ACK)

            return True
        else:
            return False