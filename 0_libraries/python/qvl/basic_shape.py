from qvl.qlabs import CommModularContainer
from qvl.actor import QLabsActor

import numpy as np
import math
import struct


######################### MODULAR CONTAINER CLASS #########################

class QLabsBasicShape(QLabsActor):
    """ This class is for spawning both static and dynamic basic shapes."""

    ID_BASIC_SHAPE = 200
    """Class ID"""

    SHAPE_CUBE = 0
    """See configurations"""
    SHAPE_CYLINDER = 1
    """See configurations"""
    SHAPE_SPHERE = 2
    """See configurations"""
    SHAPE_CONE = 3
    """See configurations"""

    COMBINE_AVERAGE = 0
    COMBINE_MIN = 1
    COMBINE_MULTIPLY = 2
    COMBINE_MAX = 3


    FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES = 10
    FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES_ACK = 11
    FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES = 30
    FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES_RESPONSE = 31
    
    FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES = 20
    FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES_ACK = 21
    
    FCN_BASIC_SHAPE_ENABLE_DYNAMICS = 14
    FCN_BASIC_SHAPE_ENABLE_DYNAMICS_ACK = 15
    FCN_BASIC_SHAPE_SET_TRANSFORM = 16
    FCN_BASIC_SHAPE_SET_TRANSFORM_ACK = 17
    FCN_BASIC_SHAPE_ENABLE_COLLISIONS = 18
    FCN_BASIC_SHAPE_ENABLE_COLLISIONS_ACK = 19

    def __init__(self, qlabs, verbose=False):
       """ Constructor Method

       :param qlabs: A QuanserInteractiveLabs object
       :param verbose: (Optional) Print error information to the console.
       :type qlabs: object
       :type verbose: boolean
       """

       self._qlabs = qlabs
       self._verbose = verbose
       self.classID = self.ID_BASIC_SHAPE
       return

    def set_material_properties(self, color, roughness=0.4, metallic=False, waitForConfirmation=True):
        """Sets the visual surface properties of the shape.

        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param roughness: A value between 0.0 (completely smooth and reflective) to 1.0 (completely rough and diffuse). Note that reflections are rendered using screen space reflections. Only objects visible in the camera view will be rendered in the reflection of the object.
        :param metallic: Metallic (True) or non-metallic (False)
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
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
        c.classID = self.ID_BASIC_SHAPE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES
        c.payload = bytearray(struct.pack(">ffffB", color[0], color[1], color[2], roughness, metallic))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False
            
    def get_material_properties(self):
        """Gets the visual surface properties of the shape.

        :return:
            - **status** - True if successful or False otherwise
            - **color** - Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
            - **roughness** - A value between 0.0 (completely smooth and reflective) to 1.0 (completely rough and diffuse). 
            - **metallic** - Metallic (True) or non-metallic (False)
        :rtype: boolean, float array[3], float, boolean

        """
        color = [0,0,0]
        roughness = 0
        metallic = False
        
        if (self._is_actor_number_valid()):
            
            c = CommModularContainer()
            c.classID = self.ID_BASIC_SHAPE
            c.actorNumber = self.actorNumber
            c.actorFunction = self.FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES
            c.payload = bytearray()
            c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

            self._qlabs.flush_receive()

            if (self._qlabs.send_container(c)):

                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES_RESPONSE)
                if (c == None):
                    pass
                    
                elif len(c.payload) == 17:
                    color[0], color[1], color[2], roughness, metallic, = struct.unpack(">ffff?", c.payload[0:17])
                    return True, color, roughness, metallic          
        

        return False, color, roughness, metallic          

    def set_enable_dynamics(self, enableDynamics, waitForConfirmation=True):
        """Sets the visual surface properties of the shape.

        :param enableDynamics: Enable (True) or disable (False) the shape dynamics. A dynamic actor can be pushed with other static or dynamic actors.  A static actor will generate collisions, but will not be affected by interactions with other actors.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type enableDynamics: boolean
        :type waitForConfirmation: boolean
        :return: True if successful, False otherwise
        :rtype: boolean

        """
        if (not self._is_actor_number_valid()):
            return False

        c = CommModularContainer()
        c.classID = self.ID_BASIC_SHAPE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_BASIC_SHAPE_ENABLE_DYNAMICS
        c.payload = bytearray(struct.pack(">B", enableDynamics))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_ENABLE_DYNAMICS_ACK)
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
        c.classID = self.ID_BASIC_SHAPE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_BASIC_SHAPE_ENABLE_COLLISIONS
        c.payload = bytearray(struct.pack(">B", enableCollisions))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_ENABLE_COLLISIONS_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_physics_properties(self, enableDynamics, mass=1.0, linearDamping=0.01, angularDamping=0.0, staticFriction=0.0, dynamicFriction=0.7, frictionCombineMode=COMBINE_AVERAGE, restitution=0.3, restitutionCombineMode=COMBINE_AVERAGE, waitForConfirmation=True):
        """Sets the dynamic properties of the shape.

        :param enableDynamics: Enable (True) or disable (False) the shape dynamics. A dynamic actor can be pushed with other static or dynamic actors.  A static actor will generate collisions, but will not be affected by interactions with other actors.
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
        c.classID = self.ID_BASIC_SHAPE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES
        c.payload = bytearray(struct.pack(">BfffffBfB", enableDynamics, mass, linearDamping, angularDamping, staticFriction, dynamicFriction, frictionCombineMode, restitution, restitutionCombineMode))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES_ACK)
                if (c == None):
                    return False
                else:
                    return True

            return True
        else:
            return False

    def set_transform(self, location, rotation, scale, waitForConfirmation=True):
        """Sets the location, rotation in radians, and scale. If a shape is parented to another actor then the location, rotation, and scale are relative to the parent actor.

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
        c.classID = self.ID_BASIC_SHAPE
        c.actorNumber = self.actorNumber
        c.actorFunction = self.FCN_BASIC_SHAPE_SET_TRANSFORM
        c.payload = bytearray(struct.pack(">fffffffff", location[0], location[1], location[2], rotation[0], rotation[1], rotation[2], scale[0], scale[1], scale[2]))
        c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload)

        if waitForConfirmation:
            self._qlabs.flush_receive()

        if (self._qlabs.send_container(c)):
            if waitForConfirmation:
                c = self._qlabs.wait_for_container(self.ID_BASIC_SHAPE, self.actorNumber, self.FCN_BASIC_SHAPE_SET_TRANSFORM_ACK)
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

    def _rotate_vector_2d_degrees(self, vector, angle):
        """Internal helper function to rotate a vector on the z plane.

        :param vector: Vector to rotate
        :param angle: Rotation angle in radians
        :type vector: float array[3]
        :type angle: float
        :return: Rotated vector
        :rtype: float array[3]
        """

        result = [0,0,vector[2]]

        result[0] = math.cos(angle)*vector[0] - math.sin(angle)*vector[1]
        result[1] = math.sin(angle)*vector[0] + math.cos(angle)*vector[1]

        return result

    def spawn_id_box_walls_from_end_points(self, actorNumber, startLocation, endLocation, height, thickness, color=[1,1,1], waitForConfirmation=True):
        """Given a start and end point, this helper method calculates the position, rotation, and scale required to place a box on top of this line.

        :param actorNumber: User defined unique identifier for the class actor in QLabs
        :param startLocation: An array of floats for x, y and z coordinates.
        :param endLocation: An array of floats for x, y and z coordinates.
        :param height: The height of the wall.
        :param thickness: The width or thickness of the wall.
        :param color: Red, Green, Blue components of the RGB color on a 0.0 to 1.0 scale.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.
        :type actorNumber: uint32
        :type startLocation: float array[3]
        :type endLocation: float array[3]
        :type height: float
        :type thickness: float
        :type color: float array[3]
        :type waitForConfirmation: boolean
        :return: True if successful or False otherwise
        :rtype: boolean
        """


        length = math.sqrt(pow(startLocation[0] - endLocation[0],2) + pow(startLocation[1] - endLocation[1],2) + pow(startLocation[2] - endLocation[2],2))
        location = [(startLocation[0] + endLocation[0])/2, (startLocation[1] + endLocation[1])/2, (startLocation[2] + endLocation[2])/2]

        yRotation = -math.asin( (endLocation[2] - startLocation[2])/(length) )
        zRotation = math.atan2( (endLocation[1] - startLocation[1]), (endLocation[0] - startLocation[0]))

        shiftedLocation = [location[0]+math.sin(yRotation)*math.cos(zRotation)*height/2, location[1]+math.sin(yRotation)*math.sin(zRotation)*height/2, location[2]+math.cos(yRotation)*height/2]

        if (0 == self.spawn_id(actorNumber, shiftedLocation, [0, yRotation, zRotation], [length, thickness, height], self.SHAPE_CUBE, waitForConfirmation)):
            if (True == self.set_material_properties(color, 1, False, waitForConfirmation)):
                return True
            else:
                return False

        else:
            return False

    def spawn_id_box_walls_from_center(self, actorNumbers, centerLocation, yaw, xSize, ySize, zHeight, wallThickness, floorThickness=0, wallColor=[1,1,1], floorColor=[1,1,1], waitForConfirmation=True):
        """Creates a container-like box with 4 walls and an optional floor.

        :param actorNumbers: An array of 5 user defined unique identifiers for the class actors in QLabs.
        :param centerLocation: An array of floats for x, y and z coordinates.
        :param yaw: Rotation about the z axis in radians.
        :param xSize: Size of the box in the x direction.
        :param ySize: Size of the box in the y direction.
        :param zSize: Size of the box in the z direction.
        :param wallThickness: The thickness of the walls.
        :param floorThickness: (Optional) The thickness of the floor. Setting this to 0 will spawn a box without a floor.
        :param wallColor: (Optional) Red, Green, Blue components of the wall color on a 0.0 to 1.0 scale.
        :param floorColor: (Optional) Red, Green, Blue components of the floor color on a 0.0 to 1.0 scale.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.

        :type actorNumbers: uint32 array[5]
        :type centerLocation: float array[3]
        :type yaw: float
        :type xSize: float
        :type ySize: float
        :type zSize: float
        :type wallThickness: float
        :type floorThickness: float
        :type wallColor: float array[3]
        :type floorColor: float array[3]
        :type waitForConfirmation: boolean

        :return: True if successful or False otherwise
        :rtype: boolean
        """
        origin = [centerLocation[0],  centerLocation[1], centerLocation[2] + zHeight/2 + floorThickness]

        location = np.add(origin, self._rotate_vector_2d_degrees([xSize/2 + wallThickness/2, 0, 0], yaw) )
        if (0 != self.spawn_id(actorNumbers[0], location, [0, 0, yaw], [wallThickness, ySize, zHeight], self.SHAPE_CUBE, waitForConfirmation)):
            return False
        if (True != self.set_material_properties(wallColor, 1, False, waitForConfirmation)):
            return False

        location = np.add(origin, self._rotate_vector_2d_degrees([ - xSize/2 - wallThickness/2, 0, 0], yaw) )
        if (0 != self.spawn_id(actorNumbers[1], location, [0, 0, yaw], [wallThickness, ySize, zHeight], self.SHAPE_CUBE, waitForConfirmation)):
            return False
        if (True != self.set_material_properties(wallColor, 1, False, waitForConfirmation)):
            return False


        location = np.add(origin, self._rotate_vector_2d_degrees([0, ySize/2 + wallThickness/2, 0], yaw) )
        if (0 != self.spawn_id(actorNumbers[2], location, [0, 0, yaw], [xSize + wallThickness*2, wallThickness, zHeight], self.SHAPE_CUBE, waitForConfirmation)):
            return False
        if (True != self.set_material_properties(wallColor, 1, False, waitForConfirmation)):
            return False


        location = np.add(origin, self._rotate_vector_2d_degrees([0, - ySize/2 - wallThickness/2, 0], yaw) )
        if (0 != self.spawn_id(actorNumbers[3], location, [0, 0, yaw], [xSize + wallThickness*2, wallThickness, zHeight], self.SHAPE_CUBE, waitForConfirmation)):
            return False
        if (True != self.set_material_properties(wallColor, 1, False, waitForConfirmation)):
            return False

        if (floorThickness > 0):
            if (0 != self.spawn_id(actorNumbers[4], [centerLocation[0], centerLocation[1], centerLocation[2]+ floorThickness/2], [0, 0, yaw], [xSize+wallThickness*2, ySize+wallThickness*2, floorThickness], self.SHAPE_CUBE, waitForConfirmation)):
                return False
            if (True != self.set_material_properties(floorColor, 1, False, waitForConfirmation)):
                return False

        return True

    def spawn_id_box_walls_from_center_degrees(self, actorNumbers, centerLocation, yaw, xSize, ySize, zHeight, wallThickness, floorThickness=0, wallColor=[1,1,1], floorColor=[1,1,1], waitForConfirmation=True):
        """Creates a container-like box with 4 walls and an optional floor.

        :param actorNumbers: An array of 5 user defined unique identifiers for the class actors in QLabs.
        :param centerLocation: An array of floats for x, y and z coordinates.
        :param yaw: Rotation about the z axis in degrees.
        :param xSize: Size of the box in the x direction.
        :param ySize: Size of the box in the y direction.
        :param zSize: Size of the box in the z direction.
        :param wallThickness: The thickness of the walls.
        :param floorThickness: (Optional) The thickness of the floor. Setting this to 0 will spawn a box without a floor.
        :param wallColor: (Optional) Red, Green, Blue components of the wall color on a 0.0 to 1.0 scale.
        :param floorColor: (Optional) Red, Green, Blue components of the floor color on a 0.0 to 1.0 scale.
        :param waitForConfirmation: (Optional) Wait for confirmation of the operation before proceeding. This makes the method a blocking operation.

        :type actorNumbers: uint32 array[5]
        :type centerLocation: float array[3]
        :type yaw: float
        :type xSize: float
        :type ySize: float
        :type zSize: float
        :type wallThickness: float
        :type floorThickness: float
        :type wallColor: float array[3]
        :type floorColor: float array[3]
        :type waitForConfirmation: boolean

        :return: True if successful or False otherwise
        :rtype: boolean
        """
        return self.spawn_id_box_walls_from_center(actorNumbers, centerLocation, yaw/180*math.pi, xSize, ySize, zHeight, wallThickness, floorThickness, wallColor, floorColor, waitForConfirmation)

