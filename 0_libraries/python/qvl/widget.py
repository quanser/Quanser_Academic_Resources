from qvl.qlabs import QuanserInteractiveLabs, CommModularContainer
import math
import struct

######################### MODULAR CONTAINER CLASS #########################

class QLabsWidget:
    """ This class is for the spawning of widgets."""

    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS = 18
    FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS_ACK = 19
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET = 20
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET_ACK = 21
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE = 50
    FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE_ACK = 51
    FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION = 100
    FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION_ACK = 101


    CUBE = 0
    """See configurations"""
    CYLINDER = 1
    """See configurations"""
    SPHERE = 2
    """See configurations"""
    AUTOCLAVE_CAGE = 3
    PLASTIC_BOTTLE = 4
    """See configurations"""
    METAL_CAN = 5
    """See configurations"""

    _qlabs = None
    _verbose = False

    # Initialize class
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

    def spawn(self, location, rotation, scale, configuration, color=[1,1,1], measuredMass=0, IDTag=0, properties="", waitForConfirmation=True):
        """Spawns a widget in an instance of QLabs at a specific location and rotation using radians.

        :param location: An array of floats for x, y and z coordinates.
        :param rotation: An array of floats for the roll, pitch, and yaw in radians.
        :param scale: An array of floats for the scale in the x, y, and z directions.
        :param configuration: See configuration options
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param measuredMass: A float value for use with mass sensor instrumented actors. This does not alter the dynamic properties.
        :param IDTag: An integer value for use with IDTag sensor instrumented actors.
        :param properties: A string for use with properties sensor instrumented actors. This can contain any string that is available for use to parse out user-customized parameters.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type color: float array[3]
        :type measuredMass: float
        :type IDTag: uint8
        :type properties: string
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean

        """
        c = CommModularContainer()
        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = 0
        c.actorFunction = self.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET
        c.payload = bytearray(struct.pack(">IfffffffffffffBI", configuration, location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2], color[0], color[1], color[2], measuredMass, IDTag, len(properties)))
        c.payload = c.payload + bytearray(properties.encode('utf-8'))

        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):

            if waitForConfirmation:
                c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, 0, self.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def spawn_degrees(self, location, rotation, scale, configuration, color=[1,1,1], measuredMass=0, IDTag=0, properties="", waitForConfirmation=True):
        """Spawns a widget in an instance of QLabs at a specific location and rotation using degrees.

        :param location: An array of floats for x, y and z coordinates.
        :param rotation: An array of floats for the roll, pitch, and yaw in degrees.
        :param scale: An array of floats for the scale in the x, y, and z directions.
        :param configuration: See configuration options.
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param measuredMass: A float value for use with mass sensor instrumented actors. This does not alter the dynamic properties.
        :param IDTag: An integer value for use with IDTag sensor instrumented actors.
        :param properties: A string for use with properties sensor instrumented actors. This can contain any string that is available for use to parse out user-customized parameters.
        :param waitForConfirmation: (Optional) Make this operation blocking until confirmation of the spawn has occurred.
        :type location: float array[3]
        :type rotation: float array[3]
        :type scale: float array[3]
        :type configuration: uint32
        :type color: float array[3]
        :type measuredMass: float
        :type IDTag: uint8
        :type properties: string
        :type waitForConfirmation: boolean
        :return:
            - **status** - `True` if successful, `False` otherwise
        :rtype: boolean

        """
        return self.spawn(location, [rotation[0]/180*math.pi, rotation[1]/180*math.pi, rotation[2]/180*math.pi], scale, configuration, color, measuredMass, IDTag, properties, waitForConfirmation)

    def destroy_all_spawned_widgets(self):
        """Destroys all spawned widgets, but does not destroy actors.

        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """
        actorNumber = 0
        c = CommModularContainer()

        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS
        c.payload = bytearray()
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, actorNumber, self.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS_ACK)
            if (c == None):
                return False
            else:
                return True

        else:
            return False

    def widget_spawn_shadow(self, enableShadow=True):
        """If spawning a large number of widgets causes performance degradation, you can try disabling the widget shadows. This function must be called in advance of widget spawning and all subsequence widgets will be spawned with the specified shadow setting.

        :param enableShadow: (Optional) Show (`True`) or hide (`False`) widget shadows.
        :type enableShadow: boolean
        :return: `True` if successful, `False` otherwise
        :rtype: boolean

        """
        actorNumber = 0
        c = CommModularContainer()

        c.classID = CommModularContainer.ID_GENERIC_ACTOR_SPAWNER
        c.actorNumber = actorNumber
        c.actorFunction = self.FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION
        c.payload = bytearray(struct.pack(">B", enableShadow))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if (self._qlabs.send_container(c)):
            c = self._qlabs.wait_for_container(CommModularContainer.ID_GENERIC_ACTOR_SPAWNER, actorNumber, self.FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION_ACK)
            if (c == None):
                return False
            else:
                return True

        else:
            return False

