from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsGenericSensor(QLabsActor):
    """ This class is for spawning both generic distance sensing sensors."""

    ID_GENERIC_SENSOR = 220
    """Class ID"""

   
    FCN_GENERIC_SENSOR_SHOW_SENSOR = 10
    FCN_GENERIC_SENSOR_SHOW_SENSOR_ACK = 11
    FCN_GENERIC_SENSOR_SET_BEAM_SIZE = 12
    FCN_GENERIC_SENSOR_SET_BEAM_SIZE_ACK = 13
    FCN_GENERIC_SENSOR_TEST_BEAM_HIT = 14
    FCN_GENERIC_SENSOR_TEST_BEAM_HIT_RESPONSE = 15
    FCN_GENERIC_SENSOR_SET_TRANSFORM = 16
    FCN_GENERIC_SENSOR_SET_TRANSFORM_ACK = 17
    FCN_GENERIC_SENSOR_TEST_BEAM_HIT_WIDGET = 18
    FCN_GENERIC_SENSOR_TEST_BEAM_HIT_WIDGET_RESPONSE = 19
    

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_GENERIC_SENSOR
       return

    def set_transform(self, location, rotation, scale, waitForConfirmation=True):
        """Sets the location, rotation in radians, and scale. If a sensor is parented to another actor then the location, rotation, and scale are relative to the parent actor.

        :param location: An array of floats for x, y and z coordinates in full-scale units. 
        :param rotation: An array of floats for the roll, pitch, and yaw in radians
        :param scale: An array of floats for the scale in the x, y, and z directions.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type waitForConfirmation: boolean
        :return: True if successful or False otherwise
        :rtype: boolean
        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_GENERIC_SENSOR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_GENERIC_SENSOR_SET_TRANSFORM
        c.payload = bytearray(struct.pack(">fffffffff", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_GENERIC_SENSOR, self.actorNumber, self.FCN_GENERIC_SENSOR_SET_TRANSFORM_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_transform_degrees(self, location, rotation, scale, waitForConfirmation=True):
        """Sets the location, rotation in degrees, and scale. If a shape is parented to another actor then the location, rotation, and scale are relative to the parent actor.

        :param location: An array of floats for x, y and z coordinates in full-scale units. 
        :param rotation: An array of floats for the roll, pitch, and yaw in degrees
        :param scale: An array of floats for the scale in the x, y, and z directions.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type waitForConfirmation: boolean
        :return: True if successful or False otherwise
        :rtype: boolean
        """

        return self.set_transform(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, waitForConfirmation)

    def show_sensor(self, showBeam=True, showOriginIcon=True, iconScale=0.1, waitForConfirmation=True):
        """Displays the beam and sensor location for debugging purposes.

        :param showBeam: Make the beam shape visible. Note this will be visible to all cameras and may affect depth sensors.
        :param showOriginIcon: Display a cone representing the projecting location of the beam.
        :param iconScale: A scale factor for the cone icon. A value of one will make a cone 1m x 1m.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type showBeam: boolean
        :type showOriginIcon: boolean
        :type iconScale: float
        :type waitForConfirmation: boolean
        :return: True if successful or False otherwise
        :rtype: boolean
        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_GENERIC_SENSOR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_GENERIC_SENSOR_SHOW_SENSOR
        c.payload = bytearray(struct.pack(">??f", showBeam, showOriginIcon, iconScale))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_GENERIC_SENSOR, self.actorNumber, self.FCN_GENERIC_SENSOR_SHOW_SENSOR_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_beam_size(self, startDistance=0.0, endDistance=1.0, heightOrRadius=0.1, width=0.1, waitForConfirmation=True):
        """Adjusts the beam shape parameters

        :param startDistance: Forward distance from the beam origin to start sensing
        :param endDistance: Maximum distance from the beam origin to end sensing
        :param heightOrRadius: For rectangular beam shapes the height. For round beam shapes, the radius. 
        :param width: For rectangular beam shapes the width. Ignored for round beam shapes.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type startDistance: float
        :type endDistance: float
        :type heightOrRadius: float
        :type width: float
        :type waitForConfirmation: boolean
        :return: True if successful or False otherwise
        :rtype: boolean
        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_GENERIC_SENSOR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_GENERIC_SENSOR_SET_BEAM_SIZE
        c.payload = bytearray(struct.pack(">ffff", startDistance, endDistance, heightOrRadius, width))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_GENERIC_SENSOR, self.actorNumber, self.FCN_GENERIC_SENSOR_SET_BEAM_SIZE_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def test_beam_hit(self):
        """Queries the beam to test if it hits something in its path.

        :return:
            - **status** - `True` communication was successful, `False` otherwise
            - **hit** - `True` if a hit occurred, `False` otherwise
            - **actorClass** - ID of the actor class.  If the value is 0 this indicates an actor which cannot be queried further or an environmental object.
            - **actorNumber** - If the actor is a valid actor class that can be queried, this will return the actor ID.
            - **distance** - Distance to the hit surface.
        :rtype: boolean, boolean, int32, int32, float
        """

        hit = False
        actorClass = 0
        actorNumber = 0
        distance = 0.0

        if (not self._is_actor_number_valid()):
            return False, hit, actorClass, actorNumber

        c = CommModularContainer()
        c.classID = self.ID_GENERIC_SENSOR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_GENERIC_SENSOR_TEST_BEAM_HIT
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
        
            c = self._qlabs.wait_for_container(self.ID_GENERIC_SENSOR, self.actorNumber, self.FCN_GENERIC_SENSOR_TEST_BEAM_HIT_RESPONSE)
            if (c == None):
                pass
            else:
                hit, actorClass, actorNumber, distance, = struct.unpack(">?IIf", c.payload[0:13])

                return True, hit, actorClass, actorNumber, distance

        
        
        return False, hit, actorClass, actorNumber, distance
           
    def test_beam_hit_widget(self):
        """Queries the beam to test if it hits a widget and if so returns the widget properties

        :return:
            - **status** - `True` communication was successful, `False` otherwise
            - **hit** - `True` if a hit occurred on a widget, `False` otherwise including non-widget actors
            - **distance** - Distance to the hit surface.
            - **IDTag** - User assigned byte identifier
            - **mass** - User assigned mass value
            - **properties** - User assigned custom property string
        :rtype: boolean, boolean, float, byte, float, string
        """

        hit = False
        distance = 0.0
        IDTag = 0
        mass = 0.0
        properties = ""
        

        if (not self._is_actor_number_valid()):
            return False, hit, distance, IDTag, mass, properties

        c = CommModularContainer()
        c.classID = self.ID_GENERIC_SENSOR
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_GENERIC_SENSOR_TEST_BEAM_HIT_WIDGET
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
        
            c = self._qlabs.wait_for_container(self.ID_GENERIC_SENSOR, self.actorNumber, self.FCN_GENERIC_SENSOR_TEST_BEAM_HIT_WIDGET_RESPONSE)
            if (c == None):
                pass
            else:
                if (len(c.payload) >= 14):
                    hit, distance, IDTag, mass, properties_length, = struct.unpack(">?fBfI", c.payload[0:14])
                    
                    if properties_length > 0:
                        if (len(c.payload) == (14 + properties_length)):
                            properties = c.payload[14:(14+properties_length)].decode('utf-8')


                    return True, hit, distance, IDTag, mass, properties

        
        
        return False, hit, distance, IDTag, mass, properties