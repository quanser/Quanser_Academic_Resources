classdef QLabsWalls < QLabsActor
    properties (Constant)
        % This class is for spawning both static and dynamic walls.
        
        ID_WALL = 10080
        % Class ID
    
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
    end
    
    methods
        function obj = QLabsWalls(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_WALL;
        end

        function success = set_enable_dynamics(obj, enableDynamics, waitForConfirmation)
            arguments
                obj QLabsWalls
                enableDynamics logical
                waitForConfirmation logical = true
            end
            success = false;
%             Sets the physics properties of the wall.
               
            if ~obj.is_actor_number_valid()
                return
            end

            obj.c.classID = obj.ID_WALL;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_WALLS_ENABLE_DYNAMICS;
            %obj.c.payload = flip(typecast(single(enableDynamics), 'uint8'));
            obj.c.payload = uint8(enableDynamics);
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_WALL, obj.actorNumber, obj.FCN_WALLS_ENABLE_DYNAMICS_ACK);

                    if isempty(rc)
                        return
                    else
                        success = true;
                        return
                    end
                end
                success = true;
                return
            else
                return
            end
        end

        function success = set_enable_collisions(obj, enableCollisions, waitForConfirmation)
            arguments
                obj QLabsWalls
                enableCollisions logical
                waitForConfirmation logical = true
            end
            success = true;

%             Enables and disables physics collisions. When disabled, other physics or velocity-based actors will be able to pass through.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_WALL;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_WALLS_ENABLE_COLLISIONS;
            obj.c.payload = flip(typecast(single(enableCollisions), 'uint8'));
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_WALL, obj.actorNumber, obj.FCN_WALLS_ENABLE_COLLISIONS_ACK);

                    if isempty(rc)
                        return
                    else
                        success = true;
                        return
                    end
                end
                success = true;
                return
            else
                return
            end
        end

        function success = set_physics_properties(obj, enableDynamics, mass, linearDamping, angularDamping, staticFriction, dynamicFriction, frictionCombineMode, restitution, restitutionCombineMode, waitForConfirmation)
            arguments
                obj QLabsWalls
                enableDynamics logical
                mass single = 1.0
                linearDamping single = 0.01
                angularDamping single = 0.0
                staticFriction single = 0.0
                dynamicFriction single = 0.7
                frictionCombineMode uint8 = obj.COMBINE_AVERAGE
                restitution single = 0.3
                restitutionCombineMode uint8 = obj.COMBINE_AVERAGE
                waitForConfirmation logical = true
            end
            success = false;
%             Sets the dynamic properties of the wall.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_WALL;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_WALLS_SET_PHYSICS_PROPERTIES;
            obj.c.payload = [flip(typecast(single(enableDynamics), 'uint8')) ...
                             flip(typecast(single(mass), 'uint8')) ...
                             flip(typecast(single(linearDamping), 'uint8')) ...
                             flip(typecast(single(angularDamping), 'uint8')) ...
                             flip(typecast(single(staticFriction), 'uint8')) ...
                             flip(typecast(single(dynamicFriction), 'uint8')) ...
                             flip(typecast(single(frictionCombineMode), 'uint8')) ...
                             flip(typecast(single(restitution), 'uint8')) ...
                             flip(typecast(single(restitutionCombineMode), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_WALL, obj.actorNumber, obj.FCN_WALLS_SET_PHYSICS_PROPERTIES_ACK);

                    if isempty(rc)
                        return
                    else
                        success = true;
                        return
                    end
                end
                success = true;
                return
            else
                return
            end
        end

        function success = set_transform(obj, location, rotation, scale, waitForConfirmation)
            arguments
                obj QLabsWalls
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                waitForConfirmation logical = true
            end
            success = false;

%             Sets the location, rotation in radians, and scale. If a wall is parented to another actor then the location, rotation, and scale are relative to the parent actor.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_WALL;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_WALLS_SET_TRANSFORM;
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

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_WALL, obj.actorNumber, obj.FCN_WALLS_SET_TRANSFORM_ACK);

                    if isempty(rc)
                        return
                    else
                        success = true;
                        return
                    end
                end
                success = true;
                return
            else
                return
            end
        end

        function success = set_transform_degrees(obj, location, rotation, scale, waitForConfirmation)
            arguments
                obj QLabsWalls
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                waitForConfirmation logical = true
            end

%             Sets the location, rotation in degrees, and scale. If a wall is parented to another actor then the location, rotation, and scale are relative to the parent actor.

            success = obj.set_transform(location, rotation/180*pi, scale, waitForConfirmation);
        end
    end
end