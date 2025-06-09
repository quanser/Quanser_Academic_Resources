from qvl.qlabs import CommModularContainer
from quanser.common import GenericError
import math
import os
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsEnvironmentOutdoors:
    """ This class modifies QLabs open worlds with outdoor environments."""

    ID_ENVIRONMENT_OUTDOORS = 1100
    """Class ID"""

    FCN_SET_TIME_OF_DAY = 10
    FCN_SET_TIME_OF_DAY_ACK = 11
    FCN_OVERRIDE_OUTDOOR_LIGHTING = 12
    FCN_OVERRIDE_OUTDOOR_LIGHTING_ACK = 13
    FCN_SET_WEATHER_PRESET = 14
    FCN_SET_WEATHER_PRESET_ACK = 15

    CLEAR_SKIES = 0
    PARTLY_CLOUDY = 1
    CLOUDY = 2
    OVERCAST = 3
    FOGGY = 4
    LIGHT_RAIN = 5
    RAIN = 6
    THUNDERSTORM = 7
    LIGHT_SNOW = 8
    SNOW = 9
    BLIZZARD = 10


    _qlabs = None
    _verbose = False

    def __init__(self, qlabs, verbose=False):
       """ Constructor method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       return

    def set_time_of_day(self, time):
        """
        Set the time of day for an outdoor environment.

        :param time: A value from 0 to 24. Midnight is a value 0 or 24. Noon is a value of 12.
        :type time: float
        :return: `True` if setting the time was successful, `False` otherwise
        :rtype: boolean

        """
        c = CommModularContainer()
        c.classID = self.ID_ENVIRONMENT_OUTDOORS
        c.actorNumber = 0
        c.actorFunction = self.FCN_SET_TIME_OF_DAY
        c.payload = bytearray(struct.pack(">f", time))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_ENVIRONMENT_OUTDOORS, 0, self.FCN_SET_TIME_OF_DAY_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def set_outdoor_lighting(self, state):
        """
        Overrides the outdoor lighting set by other environment functions

        :param state: 0 force lights off, 1 force lights on
        :type time: int32
        :return: `True` if setting the time was successful, `False` otherwise
        :rtype: boolean

        """
        c = CommModularContainer()
        c.classID = self.ID_ENVIRONMENT_OUTDOORS
        c.actorNumber = 0
        c.actorFunction = self.FCN_OVERRIDE_OUTDOOR_LIGHTING
        c.payload = bytearray(struct.pack(">I", state))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_ENVIRONMENT_OUTDOORS, 0, self.FCN_OVERRIDE_OUTDOOR_LIGHTING_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False

    def set_weather_preset(self, weather_preset):
        """
        Set the weather conditions for an outdoor environment with a preset value

        :param weather_preset: A preset index (see defined constants for weather types)
        :type time: int32
        :return: `True` if setting the time was successful, `False` otherwise
        :rtype: boolean

        """
        c = CommModularContainer()
        c.classID = self.ID_ENVIRONMENT_OUTDOORS
        c.actorNumber = 0
        c.actorFunction = self.FCN_SET_WEATHER_PRESET
        c.payload = bytearray(struct.pack(">I", weather_preset))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_ENVIRONMENT_OUTDOORS, 0, self.FCN_SET_WEATHER_PRESET_ACK)
            if (c == None):
                return False
            else:
                return True
        else:
            return False