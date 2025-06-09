from qvl.qlabs import CommModularContainer

import math
import struct
import cv2
import numpy as np


######################### MODULAR CONTAINER CLASS #########################

class QLabsActor:
    """ This the base actor class."""

    FCN_UNKNOWN = 0
    """Function ID is not recognized."""
    FCN_REQUEST_PING = 1
    """Request a response from an actor to test if it is present."""
    FCN_RESPONSE_PING = 2
    """Response from an actor to confirming it is present."""
    FCN_REQUEST_WORLD_TRANSFORM = 3
    """Request a world transform from the actor to read its current location, rotation, and scale."""
    FCN_RESPONSE_WORLD_TRANSFORM = 4
    """Response from an actor with its current location, rotation, and scale."""
    FCN_SET_CUSTOM_PROPERTIES = 5
    """Set custom properties of measured mass, ID, and/or property string."""
    FCN_SET_CUSTOM_PROPERTIES_ACK = 6
    """Set custom properties acknowledgment"""
    FCN_REQUEST_CUSTOM_PROPERTIES = 7
    """Request the custom properties of measured mass, ID, and/or property string previously assigned to the actor."""
    FCN_RESPONSE_CUSTOM_PROPERTIES = 8
    """Response containing the custom properties of measured mass, ID, and/or property string previously assigned to the actor."""
    

    actorNumber = None
    """ The current actor number of this class to be addressed. This will be set by spawn methods and cleared by destroy methods. It will not be modified by the destroy all actors.  This can be manually altered at any time to use one object to address multiple actors. """
    _qlabs = None
    _verbose = False
    classID = 0

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       return

    def _is_actor_number_valid(self):
        if self.actorNumber == None:
            if (self._verbose):
                print('actorNumber object variable None. Use a spawn function to assign an actor or manually assign the actorNumber variable.')

            return False
        else:
            return True

    def destroy(self):
        """Find and destroy a specific actor. This is a blocking operation.

        :return:
            - **numActorsDestroyed** - The number of actors destroyed. -1 if failed.
        :rtype: int32

        """
        if (not self._is_actor_number_valid()):
            return -1

        c = CommModularContainer()

        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ACTOR
        c.payload = bytearray(struct.pack(">II", self.classID, self.actorNumber))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ACTOR_ACK)
            if (c == None):
                return -1

            if len(c.payload) == 4:
                numActorsDestroyed, = struct.unpack(">I", c.payload[0:4])
                self.actorNumber = None
                return numActorsDestroyed
            else:
                return -1
        else:
            return -1

    def destroy_all_actors_of_class(self):
        """Find and destroy all actors of this class. This is a blocking operation.

        :return:
            - **numActorsDestroyed** - The number of actors destroyed. -1 if failed.
        :rtype: int32

        """

        c = CommModularContainer()

        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_ACTORS_OF_CLASS
        c.payload = bytearray(struct.pack(">I", self.classID))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_ACTORS_OF_CLASS_ACK)
            if (c == None):
                return -1

            if len(c.payload) == 4:
                numActorsDestroyed, = struct.unpack(">I", c.payload[0:4])
                self.actorNumber = None
                return numActorsDestroyed
            else:
                return -1
        else:
            return -1

    def spawn_id(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 unknown error, -1 communications error
        :rtype: int32

        """

        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID
        c.payload = bytearray(struct.pack(">IIfffffffffI", self.classID, actorNumber, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], configuration))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)


        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_ID_ACK)
                if (c == None):
                    if (self._verbose):
                        print('spawn_id: Communication timeout (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
                    return -1
                if len(c.payload) == 1:
                    status, = struct.unpack(">B", c.payload[0:1])
                    if (status == 0):
                        self.actorNumber = actorNumber

                    elif (self._verbose):
                        if (status == 1):
                            print('spawn_id: Class not available (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
                        elif (status == 2):
                            print('spawn_id: Actor number not available or already in use (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
                        elif (status == -1):
                            print('spawn_id: Communication error (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
                        else:
                            print('spawn_id: Unknown error (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
                    return status
                else:
                    if (self._verbose):
                        print("spawn: Communication error (classID {}, actorNumber {}).".format(self.classID, actorNumber))
                    return -1

            self.actorNumber = actorNumber
            return 0
        else:
            if (self._verbose):
                print('spawn_id: Communication failed (classID {}, actorNumber {}).'.format(self.classID, actorNumber))
            return -1

    def spawn_id_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 unknown error, -1 communications error
        :rtype: int32

        """

        return self.spawn_id(actorNumber, location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, configuration, waitForConfirmation)

    def spawn(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred. Note that if this is False, the returned actor number will be invalid.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 3 unknown error, -1 communications error.
            - **actorNumber** - An actor number to use for future references.
        :rtype: int32, int32

        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN
        c.payload = bytearray(struct.pack(">IfffffffffI", self.classID, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], configuration))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_RESPONSE)
                if (c == None):
                    if (self._verbose):
                        print('spawn: Communication timeout (classID {}).'.format(self.classID))
                    return -1, -1
                if len(c.payload) == 5:
                    status, actorNumber, = struct.unpack(">BI", c.payload[0:5])
                    if (status == 0):
                        self.actorNumber = actorNumber

                    elif (self._verbose):
                        if (status == 1):
                            print('spawn: Class not available (classID {}).'.format(self.classID))
                        elif (status == -1):
                            print('spawn: Communication error (classID {}).'.format(self.classID))
                        else:
                            print('spawn: Unknown error (classID {}).'.format(self.classID))

                    return status, actorNumber
                else:
                    if (self._verbose):
                        print('spawn: Communication error (classID {}).'.format(self.classID))
                    return -1, -1

            return 0, -1
        else:
            if (self._verbose):
                print('spawn: Communication failed (classID {}).'.format(self.classID))
            return -1, -1

    def spawn_degrees(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred. Note that if this is False, the returned actor number will be invalid.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 3 unknown error, -1 communications error.
            - **actorNumber** - An actor number to use for future references.
        :rtype: int32, int32

        """
        return self.spawn(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, configuration, waitForConfirmation)

    def spawn_id_and_parent_with_relative_transform(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 cannot find the parent actor, 4 unknown error, -1 communications error
        :rtype: int32

        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE
        c.payload = bytearray(struct.pack(">IIfffffffffIIII", self.classID, actorNumber, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], configuration, parentClassID, parentActorNumber, parentComponent))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE_ACK)
                if (c == None):
                    if (self._verbose):
                        print("spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Communication timeout.".format(self.classID, actorNumber))
                    return -1

                if len(c.payload) == 1:
                    status, = struct.unpack(">B", c.payload[0:1])
                    if (status == 0):
                        self.actorNumber = actorNumber

                    elif (self._verbose):
                        if (status == 1):
                            print('spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Class not available.'.format(self.classID, actorNumber))
                        elif (status == 2):
                            print('spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Actor number not available or already in use.'.format(self.classID, actorNumber))
                        elif (status == 3):
                            print('spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Cannot find parent.'.format(self.classID, actorNumber))
                        elif (status == -1):
                            print('spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Communication error.'.format(self.classID, actorNumber))
                        else:
                            print('spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Unknown error.'.format(self.classID, actorNumber))

                    return status
                else:
                    if (self._verbose):
                        print("spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Communication error.".format(self.classID, actorNumber))
                    return -1

            self.actorNumber = actorNumber
            return 0
        else:
            if (self._verbose):
                print("spawn_id_and_parent_with_relative_transform (classID {}, actorNumber {}): Communication failed.".format(self.classID, actorNumber))
            return -1

    def spawn_id_and_parent_with_relative_transform_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param configuration: (Optional) Spawn configuration. See class library for configuration options.
        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type actorNumber: uint32
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 class not available, 2 actor number not available or already in use, 3 cannot find the parent actor, 4 unknown error, -1 communications error
        :rtype: int32

        """
        return self.spawn_id_and_parent_with_relative_transform(actorNumber, location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)

    def ping(self):
        """Checks if the actor is still present in the environment. Note that if you did not spawn
        the actor with one of the spawn functions, you may need to manually set the actorNumber member variable.


        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean
        """

        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.classID
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_REQUEST_PING
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            c = self._qlabs.wait_for_container(self.classID, self.actorNumber, self.FCN_RESPONSE_PING)
            if (c == None):
                return False

            if c.payload[0] > 0:
                return True
            else:
                return False
        else:
            if (self._verbose):
                print("ping: Communication failed.")
            return False

    def get_world_transform(self):
        """Get the location, rotation, and scale in world coordinates of the actor.

        :return:
            - **status** - True if successful, False otherwise
            - **location**
            - **rotation**
            - **scale**
        :rtype: boolean, float array[3], float array[3], float array[3]
        """

        if (not self._is_actor_number_valid()):
            return False, [0,0,0], [0,0,0], [0,0,0]

        c = CommModularContainer()
        c.classID = self.classID
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_REQUEST_WORLD_TRANSFORM
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        location = [0,0,0]
        rotation = [0,0,0]
        scale = [0,0,0]

        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            c = self._qlabs.wait_for_container(self.classID, self.actorNumber, self.FCN_RESPONSE_WORLD_TRANSFORM)
            if (c == None):
                return False, location, rotation, scale

            if len(c.payload) == 36:
                location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], = struct.unpack(">fffffffff", c.payload[0:36])
                return True, location, rotation, scale
            else:
                if (self._verbose):
                    print("get_world_transform: Communication error (classID {}, actorNumber {}).".format(self.classID, self.actorNumber))
                return False, location, rotation, scale
        else:
            if (self._verbose):
                print("get_world_transform: Communication failed (classID {}, actorNumber {}).".format(self.classID, self.actorNumber))
            return False, location, rotation, scale

    def get_world_transform_degrees(self):
        """Get the location, rotation, and scale in world coordinates of the actor.

        :return:
            - **status** - True if successful, False otherwise
            - **location**
            - **rotation**
            - **scale**
        :rtype: boolean, float array[3], float array[3], float array[3]
        """
        success, location, rotation, scale = self.get_world_transform()
        rotation_deg = [rotation[0]/math.pi*180, rotation[1]/math.pi*180, rotation[2]/math.pi*180]

        return  success, location, rotation_deg, scale

    def parent_with_relative_transform(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Parents one existing actor to another to create a kinematic relationship.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 cannot find this actor, 2 cannot find the parent actor, 3 unknown error, -1 communications error
        :rtype: int32

        """
        if (self.actorNumber == None):
            if (self._verbose):
                print("This actor object has no actor number defined. If used with the spawn methods, ensure wait for confirmation is true to get the actor number assigned to this object.")

            return 1
        

        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_RELATIVE
        c.payload = bytearray(struct.pack(">IIfffffffffIII", self.classID, self.actorNumber, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], parentClassID, parentActorNumber, parentComponent))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_RELATIVE_ACK)
                if (c == None):
                    if (self._verbose):
                        print("parent_with_relative_transform (classID {}, actorNumber {}): Communication timeout.".format(self.classID, self.actorNumber))
                    return -1

                if len(c.payload) == 1:
                    status, = struct.unpack(">B", c.payload[0:1])
                    if (status == 0):
                        pass

                    elif (self._verbose):
                        if (status == 1):
                            print('parent_with_relative_transform (classID {}, actorNumber {}): Cannot find this actor.'.format(self.classID, self.actorNumber))
                        elif (status == 2):
                            print('parent_with_relative_transform (classID {}, actorNumber {}): Cannot find parent (classID {}, actorNumber {}).'.format(self.classID, self.actorNumber, parentClassID, parentActorNumber))
                        elif (status == -1):
                            print('parent_with_relative_transform (classID {}, actorNumber {}): Communication error.'.format(self.classID, self.actorNumber))
                        else:
                            print('parent_with_relative_transform (classID {}, actorNumber {}): Unknown error.'.format(self.classID, self.actorNumber))

                    return status
                else:
                    if (self._verbose):
                        print("parent_with_relative_transform (classID {}, actorNumber {}): Communication error.".format(self.classID, self.actorNumber))
                    return -1

            return 0
        else:
            if (self._verbose):
                print("parent_with_relative_transform (classID {}, actorNumber {}): Communication failed.".format(self.classID, self.actorNumber))
            return -1

    def parent_with_relative_transform_degrees(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Parents one existing actor to another to create a kinematic relationship.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used.
        :param parentClassID: (Optional) See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: (Optional) User defined unique identifier for the class actor in QLabs
        :param parentComponent: (Optional) `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 cannot find this actor, 2 cannot find the parent actor, 3 unknown error, -1 communications error
        :rtype: int32

        """

        return self.parent_with_relative_transform(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)

    def parent_with_current_world_transform(self, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Parents one existing actor to another to create a kinematic relationship while preserving the current world transform of the child actor.

        :param parentClassID: See the ID variables in the respective library classes for the class identifier
        :param parentActorNumber: User defined unique identifier for the class actor in QLabs
        :param parentComponent: `0` for the origin of the parent actor, see the parent class for additional reference frame options
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type parentClassID: uint32
        :type parentActorNumber: uint32
        :type parentComponent: uint32
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 cannot find this actor, 2 cannot find the parent actor, 3 unknown error, -1 communications error
        :rtype: int32

        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_CURRENT_WORLD
        c.payload = bytearray(struct.pack(">IIIII", self.classID, self.actorNumber, parentClassID, parentActorNumber, parentComponent))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_CURRENT_WORLD_ACK)
                if (c == None):
                    if (self._verbose):
                        print("parent_with_current_world_transform (classID {}, actorNumber {}): Communication timeout.".format(self.classID, self.actorNumber))
                    return -1

                if len(c.payload) == 1:
                    status, = struct.unpack(">B", c.payload[0:1])
                    if (status == 0):
                        pass

                    elif (self._verbose):
                        if (status == 1):
                            print('parent_with_current_world_transform (classID {}, actorNumber {}): Cannot find this actor.'.format(self.classID, self.actorNumber))
                        elif (status == 2):
                            print('parent_with_current_world_transform (classID {}, actorNumber {}): Cannot find parent (classID {}, actorNumber {}).'.format(self.classID, self.actorNumber, parentClassID, parentActorNumber))
                        elif (status == -1):
                            print('parent_with_current_world_transform (classID {}, actorNumber {}): Communication error.'.format(self.classID, self.actorNumber))
                        else:
                            print('parent_with_current_world_transform (classID {}, actorNumber {}): Unknown error.'.format(self.classID, self.actorNumber))

                    return status
                else:
                    if (self._verbose):
                        print("parent_with_current_world_transform (classID {}, actorNumber {}): Communication error.".format(self.classID, self.actorNumber))
                    return -1

            return 0
        else:
            if (self._verbose):
                print("parent_with_current_world_transform (classID {}, actorNumber {}): Communication failed.".format(self.classID, self.actorNumber))
            return -1

    def parent_break(self, waitForConfirmation=True):
        """Breaks any relationship with a parent actor (if it exists) and preserves the current world transform

        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type waitForConfirmation: boolean
        :return:
            - **status** - 0 if successful, 1 cannot find this actor, -1 communications error
        :rtype: int32

        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_BREAK_WITH_CURRENT_WORLD
        c.payload = bytearray(struct.pack(">II", self.classID, self.actorNumber))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, CommModularContainer.FCN_GENERIC_ACTOR_SPAWNER_PARENT_BREAK_WITH_CURRENT_WORLD_ACK)
                if (c == None):
                    if (self._verbose):
                        print("parent_break (classID {}, actorNumber {}): Communication timeout.".format(self.classID, self.actorNumber))
                    return -1

                if len(c.payload) == 1:
                    status, = struct.unpack(">B", c.payload[0:1])
                    if (status == 0):
                        pass

                    elif (self._verbose):
                        if (status == 1):
                            print('parent_break (classID {}, actorNumber {}): Cannot find this actor.'.format(self.classID, self.actorNumber))
                        else:
                            print('parent_break (classID {}, actorNumber {}): Unknown error.'.format(self.classID, self.actorNumber))

                    return status
                else:
                    if (self._verbose):
                        print("parent_break (classID {}, actorNumber {}): Communication error.".format(self.classID, self.actorNumber))
                    return -1

            self.actorNumber = c.actorNumber
            return 0
        else:
            if (self._verbose):
                print("parent_break (classID {}, actorNumber {}): Communication failed.".format(self.classID, self.actorNumber))
            return -1

    def set_custom_properties(self, measuredMass=0, IDTag=0, properties="", waitForConfirmation=True):
        """Assigns custom properties to an actor.

        :param measuredMass: A float value for use with mass sensor instrumented actors. This does not alter the dynamic properties.
        :param IDTag: An integer value for use with IDTag sensor instrumented actors or for custom use.
        :param properties: A string for use with properties sensor instrumented actors. This can contain any string that is available for use to parse user-customized parameters.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type measuredMass: float
        :type IDTag: uint32
        :type properties: string
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.classID
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_SET_CUSTOM_PROPERTIES
        c.payload = bytearray(struct.pack(">fII", measuredMass, IDTag, len(properties)))
        c.payload = c.payload + bytearray(properties.encode('utf-8'))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.classID, self.actorNumber, self.FCN_SET_CUSTOM_PROPERTIES_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def get_custom_properties(self):
        """Gets previously assigned custom properties to an actor.

        :return:
            - **status** - `True` if successful, `False` otherwise
            - **measuredMass** - float value
            - **IDTag** - integer value
            - **properties** - UTF-8 string
        :rtype: boolean, float, int32, string

        """

        measuredMass = 0.0
        IDTag = 0
        properties = ""


        if (not self._is_actor_number_valid()):
            return False, measuredMass, IDTag, properties

        c = CommModularContainer()
        c.classID = self.classID
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_REQUEST_CUSTOM_PROPERTIES
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        
        self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            
            c = self._qlabs.wait_for_container(self.classID, self.actorNumber, self.FCN_RESPONSE_CUSTOM_PROPERTIES)
            if (c == None):
                pass
            else:

                if len(c.payload) >= 12:
                    measuredMass, IDTag, stringLength, = struct.unpack(">fII", c.payload[0:12])

                    if (stringLength > 0):

                        if (len(c.payload) == (12 + stringLength)):
                            properties = c.payload[12:(12+stringLength)].decode('utf-8')

                            return True, measuredMass, IDTag, properties
                    else:
                        return True, measuredMass, IDTag, properties
        
        return False, measuredMass, IDTag, properties