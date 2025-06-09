classdef QLabsTrafficLight < QLabsActor
    properties  (Constant)
        ID_TRAFFIC_LIGHT = 10051;

        FCN_TRAFFIC_LIGHT_SET_STATE = 10
        FCN_TRAFFIC_LIGHT_SET_STATE_ACK = 11
        FCN_TRAFFIC_LIGHT_SET_COLOR = 12
        FCN_TRAFFIC_LIGHT_SET_COLOR_ACK = 13
        FCN_TRAFFIC_LIGHT_GET_COLOR = 14
        FCN_TRAFFIC_LIGHT_GET_COLOR_RESPONSE = 15        

        STATE_RED = 0
        % State constant for red light
        STATE_GREEN = 1
        % State constant for green light
        STATE_YELLOW = 2
        % State constant for yellow light

        COLOR_NONE = 0
        % Color constant for all lights off
        COLOR_RED = 1
        % Color constant for red light
        COLOR_YELLOW = 2
        % Color constant for yellow light
        COLOR_GREEN = 3
        % Color constant for green light

    end

    properties
        deprecation_warned = false;
    end


    methods
        function obj = QLabsTrafficLight(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_TRAFFIC_LIGHT;
        end

        function success = set_state(obj, state, waitForConfirmation)
            arguments
                obj QLabsTrafficLight
                state single
                waitForConfirmation logical = true
            end
            % DEPRECATED. Please use set_color instead. This method sets the light state (red/yellow/green) of a traffic light actor

            success = false;

            if obj.deprecation_warned == false
                disp("The set_state method and the STATE member constants have been deprecated and will be removed in a future version of the API. Please use set_color with the COLOR member constants instead.")
                obj.deprecation_warned = true;
            end       

            if (not(obj.is_actor_number_valid()))
               return 
            end
            
            obj.c.classID = obj.ID_TRAFFIC_LIGHT;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_TRAFFIC_LIGHT_SET_STATE;
            obj.c.payload = [uint8(state)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            
            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_TRAFFIC_LIGHT, obj.actorNumber, obj.FCN_TRAFFIC_LIGHT_SET_STATE_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                    end
                end

                success = true;
            end
        end


        function success = set_color(obj, color, waitForConfirmation)
            arguments
                obj QLabsTrafficLight
                color single
                waitForConfirmation logical = true
            end
            % Set the light color index of a traffic light actor

            success = false;

            if (not(obj.is_actor_number_valid()))
               return 
            end
            
            obj.c.classID = obj.ID_TRAFFIC_LIGHT;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_TRAFFIC_LIGHT_SET_COLOR;
            obj.c.payload = [uint8(color)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            
            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_TRAFFIC_LIGHT, obj.actorNumber, obj.FCN_TRAFFIC_LIGHT_SET_COLOR_ACK);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                    end
                end

                success = true;
            end
        end


        function [success, color] = get_color(obj)
            arguments
                obj QLabsTrafficLight
            end
            % Get the light color index of a traffic light actor

            success = false;
            color = 0;

            if (not(obj.is_actor_number_valid()))
               return 
            end
            
            obj.c.classID = obj.ID_TRAFFIC_LIGHT;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_TRAFFIC_LIGHT_GET_COLOR;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            
            if (obj.qlabs.send_container(obj.c))
                
                rc = obj.qlabs.wait_for_container(obj.ID_TRAFFIC_LIGHT, obj.actorNumber, obj.FCN_TRAFFIC_LIGHT_GET_COLOR_RESPONSE);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end

                if (length(rc.payload) ~= 1)
                    if (obj.verbose == true)
                        fprintf('Packet payload incorrect size.\n')
                    end
                    return
                end
            
                color = rc.payload(1);
                success = true;
            end
        end

    end
end