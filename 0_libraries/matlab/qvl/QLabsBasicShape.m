classdef QLabsBasicShape < QLabsActor
    properties (Constant)
        ID_BASIC_SHAPE = 200;

        SHAPE_CUBE = 0
        SHAPE_CYLINDER = 1
        SHAPE_SPHERE = 2
        SHAPE_CONE = 3

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
    end
    
    methods
        %% Constructor
        function obj = QLabsBasicShape(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_BASIC_SHAPE;
        end

        %% Sets the visual surface properties of the shape.
        function success = set_material_properties(obj, color, roughness, metallic, waitForConfirmation)

            
            arguments
                obj QLabsBasicShape
                color (1,3) single
                roughness double = 0.4
                metallic logical = false
                waitForConfirmation logical = true
            end 

            success = false;


            if (not(obj.is_actor_number_valid()))
                return
            end

            obj.c.classID = obj.ID_BASIC_SHAPE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES;

            obj.c.payload = [flip(typecast(single(color(1)), 'uint8')) ...
                         flip(typecast(single(color(2)), 'uint8')) ...
                         flip(typecast(single(color(3)), 'uint8')) ...
                         flip(typecast(single(roughness), 'uint8')) ...
                         uint32(metallic)];

            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive()
            end
            
            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_SET_MATERIAL_PROPERTIES_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end

                success = true;
            end
        end

        %% Gets the visual surface properties of the shape.
        function [success, color, roughness, metallic] = get_material_properties(obj)


            arguments
                obj QLabsBasicShape
            end

            color = [0,0,0];
            roughness = 0;
            metallic = false;
            success = false;

            if (obj.is_actor_number_valid())
                obj.c.classID = self.ID_BASIC_SHAPE;
                obj.c.actorNumber = self.actorNumber;
                obj.c.actorFunction = self.FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES;
                obj.c.payload = [];
                obj.c.containerSize = c.BASE_CONTAINER_SIZE + len(c.payload);

                obj.qlabs.flush_receive()

                if (obj.qlabs.send_container(obj.c))
                    
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_GET_MATERIAL_PROPERTIES_RESPONSE);
                    if isempty(rc)
                        if (obj.verbose == true)
                            disp('Timeout waiting for response.')
                        end
                    else
                        if length(rc.payload) == 17
                            color(1) = typecast(flip(rc.payload(1:4)), 'single');
                            color(2) = typecast(flip(rc.payload(5:8)), 'single');
                            color(3) = typecast(flip(rc.payload(9:12)), 'single');
                            roughness = typecast(flip(rc.payload(13:16)), 'single');
                            metallic = payload(17) > 0;
    
                            success = true;
                            return;
                        else
                            if (obj.verbose == true)
                                fprintf('Container payload does not match expected size.\n')
                            end                          
                            return
                        end
                        
                    end
                else
                    if (obj.verbose)
                        fprintf('spawn_id: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, actorNumber);
                    end
                end
            end
        end
        
        %% Sets the visual surface properties of the shape.
        function success = set_enable_dynamics(obj, enableDynamics, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                enableDynamics logical
                waitForConfirmation logical = true
            end
            
            success = false;

            
            if (not(obj.is_actor_number_valid()))
                return
            end
            
            obj.c.classID = obj.ID_BASIC_SHAPE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_BASIC_SHAPE_ENABLE_DYNAMICS;
            obj.c.payload = [uint8(enableDynamics)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_ENABLE_DYNAMICS_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end

                success = true;
            end
        end 

        %% Enables and disables physics collisions. When disabled, other physics or velocity-based actors will be able to pass through.
        function success = set_enable_collisions(obj, enableCollisions, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                enableCollisions logical
                waitForConfirmation logical = true
            end
            success = false;

            
            if (not(obj.is_actor_number_valid))
                return
            end

            obj.c.classID = obj.ID_BASIC_SHAPE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_BASIC_SHAPE_ENABLE_COLLISIONS;
            obj.c.payload = [uint8(enableCollisions)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_ENABLE_COLLISIONS_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end

                success = true;
            end
        end

        %% Sets the dynamic properties of the shape.
        function success = set_physics_properties(obj, enableDynamics, mass, linearDamping, angularDamping, staticFriction, dynamicFriction, frictionCombineMode, restitution, restitutionCombineMode, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                enableDynamics logical
                mass double = 1.0
                linearDamping double = 0.01
                angularDamping double = 0.0
                staticFriction double = 0.0
                dynamicFriction double = 0.7
                frictionCombineMode int32 = obj.COMBINE_AVERAGE
                restitution double = 0.3
                restitutionCombineMode int32 = obj.COMBINE_AVERAGE
                waitForConfirmation logical = true
                
            end
            success = false;
   

            if (not(obj.is_actor_number_valid()))
                return
            end

            obj.c.classID = obj.ID_BASIC_SHAPE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES;
            
            obj.c.payload = [uint32(enableDynamics) ...
                     flip(typecast(single(mass), 'uint8')) ...
                     flip(typecast(single(linearDamping), 'uint8')) ...
                     flip(typecast(single(angularDamping), 'uint8')) ...
                     flip(typecast(single(staticFriction), 'uint8')) ...
                     flip(typecast(single(dynamicFriction), 'uint8')) ...
                     uint32(frictionCombineMode) ...
                     flip(typecast(single(restitution), 'uint8')) ...
                     uint32(restitutionCombineMode)];

            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive();
            end
            
            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_SET_PHYSICS_PROPERTIES_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end

                success = true;
            end
        end

        %% Sets the location, rotation in radians, and scale. If a shape is parented to another actor then the location, rotation, and scale are relative to the parent actor.
        function success = set_transform(obj, location, rotation, scale, waitForConfirmation)


            arguments
                obj QLabsBasicShape
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [0 0 0]
                waitForConfirmation logical = true
            end 

            success = false;

            if (not(obj.is_actor_number_valid()))
                return
            end

            obj.c.classID = obj.ID_BASIC_SHAPE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_BASIC_SHAPE_SET_TRANSFORM;
            obj.c.payload = [flip(typecast(single(location(1)), 'uint8')) ...
                     flip(typecast(single(location(2)), 'uint8')) ...
                     flip(typecast(single(location(3)), 'uint8')) ...
                     flip(typecast(single(rotation(1)), 'uint8')) ...
                     flip(typecast(single(rotation(2)), 'uint8')) ...
                     flip(typecast(single(rotation(3)), 'uint8')) ...
                     flip(typecast(single(scale(1)), 'uint8')) ...
                     flip(typecast(single(scale(2)), 'uint8')) ...
                     flip(typecast(single(scale(3)), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_BASIC_SHAPE, obj.actorNumber, obj.FCN_BASIC_SHAPE_SET_TRANSFORM_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end

                success = true;
            end
        end

        %% Sets the location, rotation in degrees, and scale. If a shape is parented to another actor then the location, rotation, and scale are relative to the parent actor.
        function success = set_transform_degrees(obj, location, rotation, scale, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [0 0 0]
                waitForConfirmation logical = true
            end

            success = obj.set_transform(location, rotation/180*pi, scale, waitForConfirmation);
            
        end

        %% Internal helper function to rotate a vector on the z plane.
        function result = rotate_vector_2d_degrees(obj, vector, angle)
            arguments
                obj QLabsBasicShape
                vector (1,3) single
                angle double
            end

            result = [0,0,vector(3)];

            result(1) = cos(angle)*vector(1) - sin(angle)*vector(2);
            result(2) = sin(angle)*vector(1) + cos(angle)*vector(2);
            
            return
        end

        %% Given a start and end point, this helper method calculates the position, rotation, and scale required to place a box on top of this line.
        function success = spawn_id_box_walls_from_end_points(obj, actorNumber, startLocation, endLocation, height, thickness, color, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                actorNumber double
                startLocation (1,3) single
                endLocation (1,3) single
                height double
                thickness double
                color (1,3) single = [1 1 1]
                waitForConfirmation logical = true
            end
            success = false;

            length = sqrt(power(startLocation(1) - endLocation(1), 2) + power(startLocation(2) - endLocation(2), 2) + power(startLocation(3) - endLocation(3), 2));
            location = [(startLocation(1) + endLocation(1))/2, (startLocation(2) + endLocation(2))/2, (startLocation(3) + endLocation(3))/2];

            yRotation = asin( (endLocation(3) - startLocation(3))/(length) );
            zRotation = atan2( (endLocation(2) - startLocation(2)), (endLocation(1) - startLocation(1)) );

            shiftedLocation = [location(1)+sin(yRotation)*cos(zRotation)*height/2, location(2)+sin(yRotation)*sin(zRotation)*height/2, location(3)+cos(yRotation)*height/2];

            if (0 == obj.spawn_id(actorNumber, shiftedLocation, [0, yRotation, zRotation], [length, thickness, height], obj.SHAPE_CUBE, waitForConfirmation))
                if (true == obj.set_material_properties(color, 1, false, waitForConfirmation))
                    success = true;
                    return
                else
                    return
                end
                
                return
            end
        end

        %% Creates a container-like box with 4 walls and an optional floor.
        function success = spawn_id_box_walls_from_center(obj, actorNumbers, centerLocation, yaw, xSize, ySize, zHeight, wallThickness, floorThickness, wallColor, floorColor, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                actorNumbers (1,5) single
                centerLocation (1,3) single
                yaw single
                xSize single
                ySize single
                zHeight single
                wallThickness single
                floorThickness single = 0
                wallColor (1,3) single = [1 1 1]
                floorColor (1,3) single = [1 1 1]
                waitForConfirmation logical = true
            end
            success = false;


            
            origin = [centerLocation(1), centerLocation(2), centerLocation(3) + zHeight/2 + floorThickness];

            location = origin + obj.rotate_vector_2d_degrees([xSize/2 + wallThickness/2, 0, 0], yaw);
            if (0 ~= obj.spawn_id(actorNumbers(1), location, [0, 0, yaw], [wallThickness, ySize, zHeight], obj.SHAPE_CUBE, waitForConfirmation))
                return
            end
            if (true ~= obj.set_material_properties(wallColor, 1, false, waitForConfirmation))
                return
            end

            location = origin + obj.rotate_vector_2d_degrees([ - xSize/2 - wallThickness/2, 0, 0], yaw);
            if (0 ~= obj.spawn_id(actorNumbers(2), location, [0, 0, yaw], [wallThickness, ySize, zHeight], obj.SHAPE_CUBE, waitForConfirmation))
                return
            end
            if (true ~= obj.set_material_properties(wallColor, 1, false, waitForConfirmation))
                return
            end

            location = origin + obj.rotate_vector_2d_degrees([0, ySize/2 + wallThickness/2, 0], yaw);
            if (0 ~= obj.spawn_id(actorNumbers(3), location, [0, 0, yaw], [xSize + wallThickness*2, wallThickness, zHeight], obj.SHAPE_CUBE, waitForConfirmation))
                return
            end
            if (true ~= obj.set_material_properties(wallColor, 1, false, waitForConfirmation))
                return
            end

            location = origin + obj.rotate_vector_2d_degrees([0, - ySize/2 - wallThickness/2, 0], yaw);
            if (0 ~= obj.spawn_id(actorNumbers(4), location, [0, 0, yaw], [xSize + wallThickness*2, wallThickness, zHeight], obj.SHAPE_CUBE, waitForConfirmation))
                return
            end
            if (true ~= obj.set_material_properties(wallColor, 1, false, waitForConfirmation))
                return
            end

            if (floorThickness > 0)
                if (0 ~= obj.spawn_id(actorNumbers(5), [centerLocation(1), centerLocation(2), centerLocation(3)+ floorThickness/2], [0, 0, yaw], [xSize+wallThickness*2, ySize+wallThickness*2, floorThickness], obj.SHAPE_CUBE, waitForConfirmation))
                    return
                end
                if (true ~= obj.set_material_properties(floorColor, 1, false, waitForConfirmation))
                    return
                end
            end

            success = true;
            return

        end

        %% Creates a container-like box with 4 walls and an optional floor.
        function success = spawn_id_box_walls_from_center_degrees(obj, actorNumbers, centerLocation, yaw, xSize, ySize, zHeight, wallThickness, floorThickness, wallColor, floorColor, waitForConfirmation)
            arguments
                obj QLabsBasicShape
                actorNumbers (1,5) single
                centerLocation (1,3) single
                yaw single
                xSize single
                ySize single
                zHeight single
                wallThickness single
                floorThickness single = 0
                wallColor (1,3) single = [1 1 1]
                floorColor (1,3) single = [1 1 1]
                waitForConfirmation logical = true
            end

            success = obj.spawn_id_box_walls_from_center(actorNumbers, centerLocation, yaw/180*pi, xSize, ySize, zHeight, wallThickness, floorThickness, wallColor, floorColor, waitForConfirmation);
            return 

        end
    end
end