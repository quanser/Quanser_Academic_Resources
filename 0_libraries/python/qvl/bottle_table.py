from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
from qvl.widget import QLabsWidget
from quanser.common import GenericError
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsBottleTableAttachment:


    ID_BOTTLE_TABLE_ATTACHMENT = 101

    FCN_BOTTLE_TABLE_ATTACHMENT_REQUEST_LOAD_MASS = 91
    FCN_BOTTLE_TABLE_ATTACHMENT_RESPONSE_LOAD_MASS = 92

    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_ATTACHMENT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_ATTACHMENT, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, waitForConfirmation)

    def spawn_and_parent_with_relative_transform(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):
        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_ATTACHMENT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def get_measured_mass(self, qlabs, actorNumber):
        c = CommModularContainer()
        c.classID = self.ID_BOTTLE_TABLE_ATTACHMENT
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_BOTTLE_TABLE_ATTACHMENT_REQUEST_LOAD_MASS
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        if (qlabs.send_container(c)):
            c = qlabs.wait_for_container(self.ID_BOTTLE_TABLE_ATTACHMENT, actorNumber, self.FCN_BOTTLE_TABLE_ATTACHMENT_RESPONSE_LOAD_MASS)

            if (len(c.payload) == 4):
                mass,  = struct.unpack(">f", c.payload)
                return mass
            else:
                return -1.0

        else:
            return -1.0

class QLabsBottleTableSupport:


    ID_BOTTLE_TABLE_SUPPORT = 102



    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SUPPORT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SUPPORT, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, waitForConfirmation)

    def spawn_and_parent_with_relative_transform(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):
        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_SUPPORT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

class QLabsBottleTableSensorTowerShort:


    ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT = 103

    FCN_BOTTLE_TABLE_SENSOR_TOWER_SHORT_REQUEST_PROXIMITY = 17
    FCN_BOTTLE_TABLE_SENSOR_TOWER_SHORT_RESPONSE_PROXIMITY = 18

    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, waitForConfirmation)

    def spawn_and_parent_with_relative_transform(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):
        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def spawn_and_parent_with_relative_transform_degrees(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):

        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def get_proximity(self, qlabs, actorNumber):
        c = CommModularContainer()
        c.classID = self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_BOTTLE_TABLE_SENSOR_TOWER_SHORT_REQUEST_PROXIMITY
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        relative_x = 0.0
        relative_y = 0.0
        relative_z = 0.0
        properties = ""
        properties_size = 0

        if (qlabs.send_container(c)):
            c = qlabs.wait_for_container(self.ID_BOTTLE_TABLE_SENSOR_TOWER_SHORT, actorNumber, self.FCN_BOTTLE_TABLE_SENSOR_TOWER_SHORT_RESPONSE_PROXIMITY)

            if (len(c.payload) >= 16):
                relative_x, relative_y, relative_z, properties_size, = struct.unpack(">fffI", c.payload[0:16])

                if (properties_size > 0):
                    properties = c.payload[16:(16+properties_size)].decode("utf-8")

        return [relative_x, relative_y, relative_z], properties

class QLabsBottleTableSensorTowerTall:


    ID_BOTTLE_TABLE_SENSOR_TOWER_TALL = 104

    FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_REQUEST_TOF = 15
    FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_RESPONSE_TOF = 16
    FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_REQUEST_PROXIMITY = 19
    FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_RESPONSE_PROXIMITY = 20


    # Initialize class
    def __init__(self):

       return

    def spawn(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):
        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, waitForConfirmation)

    def spawn_degrees(self, qlabs, actorNumber, location, rotation, waitForConfirmation=True):

        return qlabs.spawn(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, waitForConfirmation)

    def spawn_and_parent_with_relative_transform(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):
        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def spawn_and_parent_with_relative_transform_degrees(self, qlabs, actorNumber, location, rotation, parentClass, parentActorNumber, parentComponent, waitForConfirmation=True):

        return qlabs.spawn_and_parent_with_relative_transform(actorNumber, self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, location[0], location[1], location[2], rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi, 1, 1, 1, 0, parentClass, parentActorNumber, parentComponent, waitForConfirmation)

    def get_proximity(self, qlabs, actorNumber):
        c = CommModularContainer()
        c.classID = self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_REQUEST_PROXIMITY
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        relative_x = 0.0
        relative_y = 0.0
        relative_z = 0.0
        properties = ""
        properties_size = 0

        if (qlabs.send_container(c)):
            c = qlabs.wait_for_container(self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, actorNumber, self.FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_RESPONSE_PROXIMITY)

            if (len(c.payload) >= 16):
                relative_x, relative_y, relative_z, properties_size, = struct.unpack(">fffI", c.payload[0:16])

                if (properties_size > 0):
                    properties = c.payload[16:(16+properties_size)].decode("utf-8")

        return [relative_x, relative_y, relative_z], properties



    def get_tof(self, qlabs, actorNumber):
        c = CommModularContainer()
        c.classID = self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_REQUEST_TOF
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        qlabs.flush_receive()

        tof_distance = 0.0

        if (qlabs.send_container(c)):
            c = qlabs.wait_for_container(self.ID_BOTTLE_TABLE_SENSOR_TOWER_TALL, actorNumber, self.FCN_BOTTLE_TABLE_SENSOR_TOWER_TALL_RESPONSE_TOF)

            if (len(c.payload) == 4):
                tof_distance, = struct.unpack(">f", c.payload[0:4])


        return tof_distance
