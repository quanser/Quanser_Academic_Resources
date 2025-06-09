classdef QLabsWidget < QLabsActor
    properties (Constant)
        FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS = 18
        FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS_ACK = 19
        FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET = 20
        FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET_ACK = 21
        FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE = 50
        FCN_GENERIC_ACTOR_SPAWNER_SPAWN_AND_PARENT_RELATIVE_ACK = 51
        FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION = 100
        FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION_ACK = 101
    
    
        CUBE = 0
        CYLINDER = 1
        SPHERE = 2
        AUTOCLAVE_CAGE = 3
        PLASTIC_BOTTLE = 4
        METAL_CAN = 5
    end

    methods
        
        function success = spawn(obj, location, rotation, scale, configuration, color, measuredMass, IDTag, properties, waitForConfirmation)
            arguments
                obj QLabsWidget
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                configuration single
                color (1,3) single = [1 1 1]
                measuredMass single = 0
                IDTag single = 0
                properties string = ""
                waitForConfirmation logical = true
            end
            success = false;
%             Spawns a widget in an instance of QLabs at a specific location and rotation using radians.

            obj.c.classID = obj.c.ID_GENERIC_ACTOR_SPAWNER;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET;         
            obj.c.payload = [flip(typecast(int32(configuration), 'uint8')) ...
                         flip(typecast(single(location(1)), 'uint8')) ...
                         flip(typecast(single(location(2)), 'uint8')) ...
                         flip(typecast(single(location(3)), 'uint8')) ...
                         flip(typecast(single(rotation(1)), 'uint8')) ...
                         flip(typecast(single(rotation(2)), 'uint8')) ...
                         flip(typecast(single(rotation(3)), 'uint8')) ...
                         flip(typecast(single(scale(1)), 'uint8')) ...
                         flip(typecast(single(scale(2)), 'uint8')) ...
                         flip(typecast(single(scale(3)), 'uint8')) ...
                         flip(typecast(single(color(1)), 'uint8')) ...
                         flip(typecast(single(color(2)), 'uint8')) ...
                         flip(typecast(single(color(3)), 'uint8')) ...
                         flip(typecast(single(measuredMass), 'uint8')) ...
                         uint8(IDTag) ...
                         flip(typecast(int32(length(char(properties))), 'uint8')) ...
                         uint8(char(properties))];
            
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.c.ID_GENERIC_ACTOR_SPAWNER, 0, obj.FCN_GENERIC_ACTOR_SPAWNER_SPAWN_WIDGET_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end
                end
                success = true;
                return
            end
        end

        function success = spawn_degrees(obj, location, rotation, scale, configuration, color, measuredMass, IDTag, properties, waitForConfirmation)
            arguments
                obj QLabsWidget
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                configuration single
                color (1,3) single = [1 1 1]
                measuredMass single = 0
                IDTag single = 0
                properties string = ""
                waitForConfirmation logical = true
            end
            
%             Spawns a widget in an instance of QLabs at a specific location and rotation using degrees.


            success = obj.spawn(location, [rotation(1)/180*pi, rotation(2)/180*pi, rotation(3)/180*pi], scale, configuration, color, measuredMass, IDTag, properties, waitForConfirmation);
            return
        end

        function success = destroy_all_spawned_widgets(obj)
            arguments
                obj QLabsWidget
            end
            success = false;
            
%             Destroys all spawned widgets, but does not destroy actors.
            
            actorNumber = 0;

            obj.c.classID = obj.c.ID_GENERIC_ACTOR_SPAWNER;
            obj.c.actorNumber = actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.c.ID_GENERIC_ACTOR_SPAWNER, actorNumber, obj.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_WIDGETS_ACK);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end
                success = true;
                return
            end
        end

        function success = widget_spawn_shadow(obj, enableShadow)
            arguments
                obj QLabsWidget
                enableShadow logical = true
            end
            success = false;

%             If spawning a large number of widgets causes performance degradation, you can try disabling the widget shadows. This function must be called in advance of widget spawning and all subsequence widgets will be spawned with the specified shadow setting.

            actorNumber = 0;
            
            obj.c.classID = obj.c.ID_GENERIC_ACTOR_SPAWNER;
            obj.c.actorNumber = actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION;
            obj.c.payload = [uint8(enableShadow)];      
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.c.ID_GENERIC_ACTOR_SPAWNER, actorNumber, obj.FCN_GENERIC_ACTOR_SPAWNER_WIDGET_SPAWN_CONFIGURATION_ACK);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end
                success = true;
                return
            end
        end
    end
end