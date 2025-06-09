from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsTrafficCone(QLabsActor):
    """This class is for spawning traffic cones."""

    ID_TRAFFIC_CONE = 10000
    """Class ID"""
    
    FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES = 10
    FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES_ACK = 11
    FCN_TRAFFIC_CONE_GET_MATERIAL_PROPERTIES = 12
    FCN_TRAFFIC_CONE_GET_MATERIAL_PROPERTIES_RESPONSE = 13
    

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_TRAFFIC_CONE
       return
       
    def set_material_properties(self, materialSlot=0, color=[0,0,0], roughness=0.4, metallic=False, waitForConfirmation=True):
        """Sets the visual surface properties of the cone. The default colors are orange for material slot 0, and black for slot 1.

        :param materialSlot: Material index to be modified.  Setting an index for an unsupported slot will be ignored.
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param roughness: A value between 0.0 (completely smooth and reflective) to 1.0 (completely rough and diffuse). Note that reflections are rendered using screen space reflections. Only objects visible in the camera view will be rendered in the reflection of the object.
        :param metallic: Metallic (True) or non-metallic (False)
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type color: byte
        :type color: float array[3]
        :type roughness: float
        :type metallic: boolean
        :type waitForConfirmation: boolean
        :return: True if successful, False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_TRAFFIC_CONE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES
        c.payload = bytearray(struct.pack(">BffffB", materialSlot, color[0], color[1], color[2], roughness, metallic))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_TRAFFIC_CONE, self.actorNumber, self.FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False
            
   