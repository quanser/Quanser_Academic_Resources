from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsCharacter(QLabsActor):
    """ This base class implements spawning and AI navigation of the environment for characters."""

    FCN_CHARACTER_MOVE_TO = 10
    FCN_CHARACTER_MOVE_TO_ACK = 11


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

    def move_to(self, location, speed, waitForConfirmation=True):
        """Commands an actor to move from the present location to a new target location by using AI path navigation.

        :param location: A target destination as an array of floats for x, y and z coordinates in full-scale units.
        :param speed: The speed at which the person should walk to the destination (refer to the constants for recommended speeds)
        :param waitForConfirmation: (Optional) Wait for confirmation before proceeding. This makes the method a blocking operation, but only until the command is received. The time for the actor to traverse to the destination is always non-blocking.
        :type location: float array[3]
        :type speed: float
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean

        .. tip::

            Ensure the start and end locations are in valid navigation areas so the actor can find a path to the destination.

        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.classID
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_CHARACTER_MOVE_TO
        c.payload = bytearray(struct.pack(">ffff", location[0], location[1], location[2], speed))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.classID, self.actorNumber, self.FCN_CHARACTER_MOVE_TO_ACK)
                if (c == None):
                    return False
                else:
                    return True
            return True
        else:
            return False
