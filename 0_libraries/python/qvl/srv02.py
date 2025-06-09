from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
import math
import os

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsSRV02:


    ID_SRV02 = 40

    FCN_SRV02_COMMAND_AND_REQUEST_STATE = 10
    FCN_SRV02_COMMAND_AND_REQUEST_STATE_RESPONSE = 11


    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_SRV02, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1.0, 1.0, 1.0, configuration, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_SRV02, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1.0, 1.0, 1.0, configuration, waitForConfirmation)

    def command_and_request_state(self, qlabs, actorNumber, angle, waitForConfirmation=True):
        c = CommModularContainer()
        c.classID = self.ID_SRV02
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_SRV02_COMMAND_AND_REQUEST_STATE
        c.payload = bytearray(struct.pack(">ff", angle, 0))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        if (qlabs.send_container(c)):
            if (waitForConfirmation):
                c = qlabs.wait_for_container(self.ID_SRV02, actorNumber, self.FCN_SRV02_COMMAND_AND_REQUEST_STATE_RESPONSE)

            return True
        else:
            return False

    def command_and_request_state_degrees(self, qlabs, actorNumber, angle, waitForConfirmation=True):

        return self.command_and_request_state(qlabs, actorNumber, angle/180*math.pi, waitForConfirmation)
