from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from quanser.common import GenericError
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsQBotHopper:


    ID_QBOT_DUMPING_MECHANISM = 111

    FCN_QBOT_DUMPING_MECHANISM_COMMAND = 10
    FCN_QBOT_DUMPING_MECHANISM_COMMAND_ACK = 12


    VIEWPOINT_RGB = 0
    VIEWPOINT_DEPTH = 1
    VIEWPOINT_TRAILING = 2

    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_QBOT_DUMPING_MECHANISM, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1.0, 1.0, 1.0, configuration, waitForConfirmation)

    def spawn_and_parent_with_relative_transform(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):
        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_QBOT_DUMPING_MECHANISM, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1.0, 1.0, 1.0, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, configuration=0, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_QBOT_DUMPING_MECHANISM, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1.0, 1.0, 1.0, configuration, waitForConfirmation)

    def command(self, qlabs, actorNumber, angle):
        c = CommModularContainer()
        c.classID = self.ID_QBOT_DUMPING_MECHANISM
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_QBOT_DUMPING_MECHANISM_COMMAND
        c.payload = bytearray(struct.pack(">f", angle))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        if (qlabs.send_container(c)):
            c = qlabs.wait_for_container(self.ID_QBOT_DUMPING_MECHANISM, actorNumber, self.FCN_QBOT_DUMPING_MECHANISM_COMMAND_ACK)

            return True
        else:
            return False

    def command_degrees(self, qlabs, actorNumber, angle):
        self.command(qlabs, actorNumber, angle/180*math.pi)