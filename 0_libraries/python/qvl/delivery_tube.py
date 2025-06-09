from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
from qvl.actor import QLabsActor
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsDeliveryTube(QLabsActor):


    ID_DELIVERY_TUBE = 80

    FCN_DELIVERY_TUBE_SPAWN_BLOCK = 10
    FCN_DELIVERY_TUBE_SPAWN_BLOCK_ACK = 11
    FCN_DELIVERY_TUBE_SET_HEIGHT = 12
    FCN_DELIVERY_TUBE_SET_HEIGHT_ACK = 13

    BLOCK_CUBE = 0
    BLOCK_CYLINDER = 1
    BLOCK_SPHERE = 2
    BLOCK_GEOSPHERE = 3

    CONFIG_HOVER = 0
    CONFIG_NO_HOVER = 1

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
        self.classID = self.ID_DELIVERY_TUBE
        return

    def spawn_block(self, blockType, mass, yawRotation, color):
        c = CommModularContainer()
        c.classID = self.ID_DELIVERY_TUBE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_DELIVERY_TUBE_SPAWN_BLOCK
        c.payload = bytearray(struct.pack(">Ifffff", blockType, mass, yawRotation, color[0], color[1], color[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_DELIVERY_TUBE, self.actorNumber, self.FCN_DELIVERY_TUBE_SPAWN_BLOCK_ACK)

            return True
        else:
            return False

    def set_height(self, height):
        c = CommModularContainer()
        c.classID = self.ID_DELIVERY_TUBE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_DELIVERY_TUBE_SET_HEIGHT
        c.payload = bytearray(struct.pack(">f", height))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_DELIVERY_TUBE, self.actorNumber, self.FCN_DELIVERY_TUBE_SET_HEIGHT_ACK)

            return True
        else:
            return False


class QLabsDeliveryTubeBottles(QLabsActor):


    ID_DELIVERY_TUBE_BOTTLES = 81

    FCN_DELIVERY_TUBE_SPAWN_CONTAINER = 10
    FCN_DELIVERY_TUBE_SPAWN_CONTAINER_ACK = 11
    FCN_DELIVERY_TUBE_SET_HEIGHT = 12
    FCN_DELIVERY_TUBE_SET_HEIGHT_ACK = 13

    PLASTIC_BOTTLE = 4
    METAL_CAN = 5

    CONFIG_HOVER = 0
    CONFIG_NO_HOVER = 1

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
        self.classID = self.ID_DELIVERY_TUBE_BOTTLES
        return

    def spawn_container(self, metallic, color, mass, propertyString="", height = 0.1, diameter = 0.65, roughness = 0.65):
        c = CommModularContainer()
        c.classID = self.ID_DELIVERY_TUBE_BOTTLES
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_DELIVERY_TUBE_SPAWN_CONTAINER
        c.payload = bytearray(struct.pack(">ffBffffffI", height, diameter, metallic, color[0], color[1], color[2], 1.0, roughness, mass, len(propertyString)))
        c.payload = c.payload + bytearray(propertyString.encode('utf-8'))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_DELIVERY_TUBE_BOTTLES, self.actorNumber, self.FCN_DELIVERY_TUBE_SPAWN_CONTAINER_ACK)

            return True
        else:
            return False

    def set_height(self, height):
        c = CommModularContainer()
        c.classID = self.ID_DELIVERY_TUBE_BOTTLES
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_DELIVERY_TUBE_SET_HEIGHT
        c.payload = bytearray(struct.pack(">f", height))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_DELIVERY_TUBE_BOTTLES, self.actorNumber, self.FCN_DELIVERY_TUBE_SET_HEIGHT_ACK)

            return True
        else:
            return False

