from qvl.actor import QLabsActor

import math
import struct

class QLabsCrosswalk(QLabsActor):
    """This class is for spawning crosswalks."""

    ID_CROSSWALK = 10010
    """Class ID"""

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_CROSSWALK
       return


    def spawn_id(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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
        scale = [scale[2], scale[1], scale[0]]
        return super().spawn_id(actorNumber, location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn_id_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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
        scale = [scale[2], scale[1], scale[0]]
        return super().spawn_id_degrees(actorNumber, location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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
        
        scale = [scale[2], scale[1], scale[0]]
        return super().spawn(location, rotation, scale, configuration, waitForConfirmation)
               
    def spawn_degrees(self, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor with the next available actor number within this class.

        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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

        scale = [scale[2], scale[1], scale[0]]
        return super().spawn_degrees(location, rotation, scale, configuration, waitForConfirmation)
        
    def spawn_id_and_parent_with_relative_transform(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in radians
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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
        scale = [scale[2], scale[1], scale[0]]
        return super().spawn_id_and_parent_with_relative_transform(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)

    def spawn_id_and_parent_with_relative_transform_degrees(self, actorNumber, location=[0,0,0], rotation=[0,0,0], scale=[1,1,1], configuration=0, parentClassID=0, parentActorNumber=0, parentComponent=0, waitForConfirmation=True):
        """Spawns a new crosswalk actor relative to an existing actor and creates a kinematic relationship.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param location: (Optional) An array of floats for x, y and z coordinates
        :param rotation: (Optional) An array of floats for the roll, pitch, and yaw in degrees
        :param scale: (Optional) An array of floats for the scale in the x, y, and z directions. Scale values of 0.0 should not be used and only uniform scaling is recommended. Sensor scaling will be based on scale[0].
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
        scale = [scale[2], scale[1], scale[0]]
        return super().spawn_id_and_parent_with_relative_transform_degrees(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)
