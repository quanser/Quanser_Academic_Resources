from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsTrafficLight(QLabsActor):


    ID_TRAFFIC_LIGHT = 10051
    """Class ID"""

    FCN_TRAFFIC_LIGHT_SET_STATE = 10
    FCN_TRAFFIC_LIGHT_SET_STATE_ACK = 11
    FCN_TRAFFIC_LIGHT_SET_COLOR = 12
    FCN_TRAFFIC_LIGHT_SET_COLOR_ACK = 13
    FCN_TRAFFIC_LIGHT_GET_COLOR = 14
    FCN_TRAFFIC_LIGHT_GET_COLOR_RESPONSE = 15



    STATE_RED = 0
    """State constant for red light"""
    STATE_GREEN = 1
    """State constant for green light"""
    STATE_YELLOW = 2
    """State constant for yellow light"""

    deprecation_warned = False


    COLOR_NONE = 0
    """Color constant for all lights off"""

    COLOR_RED = 1
    """Color constant for red light"""

    COLOR_YELLOW = 2
    """Color constant for yellow light"""

    COLOR_GREEN = 3
    """Color constant for green light"""



    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_TRAFFIC_LIGHT
       return

    def set_state(self, state, waitForConfirmation=True):
        """DEPRECATED. Please use set_color instead. This method sets the light state (red/yellow/green) of a traffic light actor.

        :param state: An integer constant corresponding to a light state (see class constants)
        :param waitForConfirmation: (Optional) Wait for confirmation of the state change before proceeding. This makes the method a blocking operation.
        :type state: uint32
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False
        
        if self.deprecation_warned == False:
            print("The set_state method and the STATE member constants have been deprecated and will be removed in a future version of the API. Please use set_color with the COLOR member constants instead.")



    def set_color(self, color, waitForConfirmation=True):
        """Set the light color index of a traffic light actor

        :param color: An integer constant corresponding to a light color index (see class constants)
        :param waitForConfirmation: (Optional) Wait for confirmation of the color change before proceeding. This makes the method a blocking operation.
        :type color: uint32
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_TRAFFIC_LIGHT
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_TRAFFIC_LIGHT_SET_COLOR
        c.payload = bytearray(struct.pack(">B", color))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_TRAFFIC_LIGHT, self.actorNumber, self.FCN_TRAFFIC_LIGHT_SET_COLOR_ACK)
                if (c == None):
                    return False

            return True
        else:
            return False        
        
    def get_color(self):
        """Get the light color index of a traffic light actor

        :return:
            - **status** - `True` if successful, `False` otherwise
            - **color** - Color index. The color index is only valid if status is true.

        :rtype: boolean, uint32        

        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_TRAFFIC_LIGHT
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_TRAFFIC_LIGHT_GET_COLOR
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(self.ID_TRAFFIC_LIGHT, self.actorNumber, self.FCN_TRAFFIC_LIGHT_GET_COLOR_RESPONSE)
            if (c == None):
              return False, 0
            
            if len(c.payload) == 1:
                return True, c.payload[0]
            else:
                return False, 0

        else:
            return False, 0

