from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsAutoclave:

    ID_AUTOCLAVE = 140
    FCN_AUTOCLAVE_SET_DRAWER = 10
    FCN_AUTOCLAVE_SET_DRAWER_ACK = 11

    RED = 0
    GREEN = 1
    BLUE = 2


    # Initilize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_AUTOCLAVE, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, configuration, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_AUTOCLAVE, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, configuration, waitForConfirmation)

    def set_drawer(self, qlabs, actorNumber, open_drawer, waitForConfirmation=True):
        c = CommModularContainer()
        c.classID = self.ID_AUTOCLAVE
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_AUTOCLAVE_SET_DRAWER
        c.payload = bytearray(struct.pack(">B", open_drawer ))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            qlabs.flush_receive()

        if (qlabs.send_container(c)):
            if waitForConfirmation:
                c = qlabs.wait_for_container(self.ID_AUTOCLAVE, actorNumber, self.FCN_AUTOCLAVE_SET_DRAWER_ACK)
                return c

            return True
        else:
            return False
