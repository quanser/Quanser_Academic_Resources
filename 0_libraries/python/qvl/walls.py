from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsWalls(QLabsActor):
    """ This class is for spawning both static and dynamic walls."""

    ID_WALL = 10080
    """Class ID"""

    WALL_FOAM_BOARD = 0

    COMBINE_AVERAGE = 0
    COMBINE_MIN = 1
    COMBINE_MULTIPLY = 2
    COMBINE_MAX = 3

    FCN_WALLS_ENABLE_DYNAMICS = 14
    FCN_WALLS_ENABLE_DYNAMICS_ACK = 15
    FCN_WALLS_SET_TRANSFORM = 16
    FCN_WALLS_SET_TRANSFORM_ACK = 17
    FCN_WALLS_ENABLE_COLLISIONS = 18
    FCN_WALLS_ENABLE_COLLISIONS_ACK = 19
    FCN_WALLS_SET_PHYSICS_PROPERTIES = 20
    FCN_WALLS_SET_PHYSICS_PROPERTIES_ACK = 21

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_WALL
       return

    def set_enable_dynamics(self, enableDynamics, waitForConfirmation=True):
        """Sets the physics properties of the wall.

        :param enableDynamics: Enable (True) or disable (False) the wall dynamics. A dynamic actor can be pushed with other static or dynamic actors.  A static actor will generate collisions, but will not be affected by interactions with other actors.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type enableDynamics: boolean
        :type waitForConfirmation: boolean
        :return: True if successful, False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_WALL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_WALLS_ENABLE_DYNAMICS
        c.payload = bytearray(struct.pack(">B", enableDynamics))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_WALL, self.actorNumber, self.FCN_WALLS_ENABLE_DYNAMICS_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_enable_collisions(self, enableCollisions, waitForConfirmation=True):
        """Enables and disables physics collisions. When disabled, other physics or velocity-based actors will be able to pass through.

        :param enableCollisions: Enable (True) or disable (False) the collision.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type enableCollisions: boolean
        :type waitForConfirmation: boolean
        :return: True if successful, False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_WALL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_WALLS_ENABLE_COLLISIONS
        c.payload = bytearray(struct.pack(">B", enableCollisions))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_WALL, self.actorNumber, self.FCN_WALLS_ENABLE_COLLISIONS_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_physics_properties(self, enableDynamics, mass=1.0, linearDamping=0.01, angularDamping=0.0, staticFriction=0.0, dynamicFriction=0.7, frictionCombineMode=COMBINE_AVERAGE, restitution=0.3, restitutionCombineMode=COMBINE_AVERAGE, waitForConfirmation=True):
        """Sets the dynamic properties of the wall.

        :param enableDynamics: Enable (True) or disable (False) the wall dynamics. A dynamic actor can be pushed with other static or dynamic actors.  A static actor will generate collisions, but will not be affected by interactions with other actors.
        :param mass: (Optional) Sets the mass of the actor in kilograms.
        :param linearDamping: (Optional) Sets the damping of the actor for linear motions.
        :param angularDamping: (Optional) Sets the damping of the actor for angular motions.
        :param staticFriction: (Optional) Sets the coefficient of friction when the actor is at rest. A value of 0.0 is frictionless.
        :param dynamicFriction: (Optional) Sets the coefficient of friction when the actor is moving relative to the surface it is on. A value of 0.0 is frictionless.
        :param frictionCombineMode: (Optional) Defines how the friction between two surfaces with different coefficients should be calculated (see COMBINE constants).
        :param restitution: (Optional) The coefficient of restitution defines how plastic or elastic a collision is. A value of 0.0 is plastic and will absorb all energy. A value of 1.0 is elastic and will bounce forever. A value greater than 1.0 will add energy with each collision.
        :param restitutionCombineMode: (Optional) Defines how the restitution between two surfaces with different coefficients should be calculated (see COMBINE constants).
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.

        :type enableDynamics: boolean
        :type mass: float
        :type linearDamping: float
        :type angularDamping: float
        :type staticFriction: float
        :type dynamicFriction: float
        :type frictionCombineMode: byte
        :type restitution: float
        :type restitutionCombineMode: byte
        :type waitForConfirmation: boolean
        :return: True if successful, False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_WALL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_WALLS_SET_PHYSICS_PROPERTIES
        c.payload = bytearray(struct.pack(">BfffffBfB", enableDynamics, mass, linearDamping, angularDamping, staticFriction, dynamicFriction, frictionCombineMode, restitution, restitutionCombineMode))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_WALL, self.actorNumber, self.FCN_WALLS_SET_PHYSICS_PROPERTIES_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_transform(self, location, rotation, scale, waitForConfirmation=True):
        """Sets the location, rotation in radians, and scale. If a wall is parented to another actor then the location, rotation, and scale are relative to the parent actor.

        :param location: An array of floats for x, y and z coordinates in full-scale units. Multiply physical QCar locations by 10 to get full scale locations.
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
        c.classID = self.ID_WALL
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_WALLS_SET_TRANSFORM
        c.payload = bytearray(struct.pack(">fffffffff", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_WALL, self.actorNumber, self.FCN_WALLS_SET_TRANSFORM_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_transform_degrees(self, location, rotation, scale, waitForConfirmation=True):
        """Sets the location, rotation in degrees, and scale. If a wall is parented to another actor then the location, rotation, and scale are relative to the parent actor.

        :param location: An array of floats for x, y and z coordinates in full-scale units. Multiply physical QCar locations by 10 to get full scale locations.
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

