from qvl.qlabs import CommModularContainer
from qvl.character import QLabsCharacter
import math

import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsAnimal(QLabsCharacter):
    """ This class implements spawning and AI navigation of the environment for animals."""

    ID_ANIMAL = 10031
    
    FCN_ANIMAL_ENABLE_COLLISION = 20
    FCN_ANIMAL_ENABLE_COLLISION_ACK = 21
    FCN_ANIMAL_ADD_COLLISION_FILTER = 22
    FCN_ANIMAL_ADD_COLLISION_FILTER_ACK = 23
    FCN_ANIMAL_GET_COLLISION_COUNT = 24
    FCN_ANIMAL_GET_COLLISION_COUNT_RESPONSE = 25    

    GOAT = 0
    """ Configuration constant. """
    SHEEP = 1
    """ Configuration constant. """
    COW = 2
    """ Configuration constant. """


    GOAT_STANDING = 0
    """ Speed constant for the move_to method. """
    GOAT_WALK = 0.8
    """ Speed constant for the move_to method. """
    GOAT_RUN = 4.0
    """ Speed constant for the move_to method. """

    SHEEP_STANDING = 0
    """ Speed constant for the move_to method. """
    SHEEP_WALK = 0.60
    """ Speed constant for the move_to method. """
    SHEEP_RUN = 3.0
    """ Speed constant for the move_to method. """

    COW_STANDING = 0
    """ Speed constant for the move_to method. """
    COW_WALK = 1.0
    """ Speed constant for the move_to method. """
    COW_RUN = 6.0
    """ Speed constant for the move_to method. """


    def __init__(self, qlabs, verbose=False):
       """ Constructor method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_ANIMAL
       return

    def enable_collsion(self, enable, waitForConfirmation=True):
        """Allows for the animal to respond and track the number of external collisions. Note that at least one collision filter must also be added.

        :param enable: Enable or disable the collision response.
        :param waitForConfirmation: (Optional) Wait for confirmation of the before proceeding. This makes the method a blocking operation.
        :type enable: boolean
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise.
        :rtype: boolean
        """
        c = CommModularContainer()
        c.classID = self.ID_ANIMAL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_ANIMAL_ENABLE_COLLISION
        c.payload = bytearray(struct.pack(">B", enable))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_ANIMAL, self.actorNumber, self.FCN_ANIMAL_ENABLE_COLLISION_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False
        
        
    def add_collision_filter(self, class_id, waitForConfirmation=True):
        """When collisions are enabled, the animal will respond to hits from any actor of this class. This function may be called multiple times to add multiple classes.

        :param class_id: The actor class number to which the person should respond to.
        :param waitForConfirmation: (Optional) Wait for confirmation of the before proceeding. This makes the method a blocking operation.
        :type enable: int32
        :type waitForConfirmation: boolean
        :return: `True` if successful, `False` otherwise.
        :rtype: boolean
        """
        c = CommModularContainer()
        c.classID = self.ID_ANIMAL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_ANIMAL_ADD_COLLISION_FILTER
        c.payload = bytearray(struct.pack(">I", class_id))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_ANIMAL, self.actorNumber, self.FCN_ANIMAL_ADD_COLLISION_FILTER_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False        
            
            
    def get_collision_count(self):
        """Get the total number of collsions this actor has experienced. Note that collisions must be enabled and at least one collision filter set for this count to be active.

        :return:
            - **status** - True if successful or False otherwise
            - **count** - Number of hits the actor has registered
        :rtype: boolean, int32
        """
        c = CommModularContainer()
        c.classID = self.ID_ANIMAL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_ANIMAL_GET_COLLISION_COUNT
        c.payload = bytearray()
        
        count = -1

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
              c = self._qlabs.wait_for_container(self.ID_ANIMAL, self.actorNumber, self.FCN_ANIMAL_GET_COLLISION_COUNT_RESPONSE)
              if (c == None):
                     return False, count
              else:
                   if (len(c.payload) == 4):
                       count,  = struct.unpack(">I", c.payload)
                       return True, count
                   else:
                       return False, count


        else:
              return False, count

