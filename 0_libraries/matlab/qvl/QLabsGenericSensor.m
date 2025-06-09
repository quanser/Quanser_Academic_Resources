classdef QLabsGenericSensor < QLabsActor
    properties
%         This class is for spawning both generic distance sensing sensors.

        ID_GENERIC_SENSOR = 220
%         Class ID
       
        FCN_GENERIC_SENSOR_SHOW_SENSOR = 10
        FCN_GENERIC_SENSOR_SHOW_SENSOR_ACK = 11
        FCN_GENERIC_SENSOR_SET_BEAM_SIZE = 12
        FCN_GENERIC_SENSOR_SET_BEAM_SIZE_ACK = 13
        FCN_GENERIC_SENSOR_TEST_BEAM_HIT = 14
        FCN_GENERIC_SENSOR_TEST_BEAM_HIT_RESPONSE = 15
        FCN_GENERIC_SENSOR_SET_TRANSFORM = 16
        FCN_GENERIC_SENSOR_SET_TRANSFORM_ACK = 17
    end
    methods
        function obj = QLabsGenericSensor(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_GENERIC_SENSOR;
        end

        function success = set_transform(obj, location, rotation, scale, waitForConfirmation)
            arguments
                obj QLabsGenericSensor
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                waitForConfirmation logical = true
            end
            success = false;

%             Sets the location, rotation in radians, and scale. If a sensor is parented to another actor then the location, rotation, and scale are relative to the parent actor.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_GENERIC_SENSOR;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_SENSOR_SET_TRANSFORM;
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
                    rc = obj.qlabs.wait_for_container(obj.ID_GENERIC_SENSOR, obj.actorNumber, obj.FCN_GENERIC_SENSOR_SET_TRANSFORM_ACK);

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
                obj QLabsGenericSensor
                location (1,3) single
                rotation (1,3) single
                scale (1,3) single
                waitForConfirmation logical = true
            end
            
%             Sets the location, rotation in degrees, and scale. If a shape is parented to another actor then the location, rotation, and scale are relative to the parent actor.

            success = obj.set_transform(location, rotation/180*pi, scale, waitForConfirmation);
            return
        end

        function success = show_sensor(obj, showBeam, showOriginIcon, iconScale, waitForConfirmation)
            arguments
                obj QLabsGenericSensor
                showBeam logical = true
                showOriginIcon logical = true
                iconScale single = 0.1
                waitForConfirmation logical = true
            end
            success = false;

%             Displays the beam and sensor location for debugging purposes.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_GENERIC_SENSOR;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_SENSOR_SHOW_SENSOR;
            obj.c.payload = [uint8(showBeam) ...
                             uint8(showOriginIcon) ...
                             flip(typecast(single(iconScale), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if(obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_GENERIC_SENSOR, obj.actorNumber, obj.FCN_GENERIC_SENSOR_SHOW_SENSOR_ACK);
                    
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

        function success = set_beam_size(obj, startDistance, endDistance, heightOrRadius, width, waitForConfirmation)
            arguments
                obj QLabsGenericSensor
                startDistance single = 0.0
                endDistance single = 1.0
                heightOrRadius single = 0.1
                width single = 0.1
                waitForConfirmation logical = true
            end
            success = false;

%             Adjusts the beam shape parameters

            if isempty(obj.is_actor_number_valid)
                return
            end

            obj.c.classID = obj.ID_GENERIC_SENSOR;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_SENSOR_SET_BEAM_SIZE;
            obj.c.payload = [flip(typecast(single(startDistance), 'uint8')) ...
                             flip(typecast(single(endDistance), 'uint8')) ...
                             flip(typecast(single(heightOrRadius), 'uint8')) ...
                             flip(typecast(single(width), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_GENERIC_SENSOR, obj.actorNumber, obj.FCN_GENERIC_SENSOR_SET_BEAM_SIZE_ACK);

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

        function [success, hit, actorClass, actorNumber, distance] = test_beam_hit(obj)
            arguments
               obj QLabsGenericSensor 
            end
            success = false;
            hit = false;
            actorClass = 0;
            actorNumber = 0;
            distance = 0.0;

%             Queries the beam to test if it hits another actor.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_GENERIC_SENSOR;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_GENERIC_SENSOR_TEST_BEAM_HIT;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_GENERIC_SENSOR, obj.actorNumber, obj.FCN_GENERIC_SENSOR_TEST_BEAM_HIT_RESPONSE);
                if isempty(rc)
                    
                else
                    hit = rc.payload(1) ~= 0;
                    actorClass = typecast(flip(rc.payload(2:5)), 'int32');
                    actorNumber = typecast(flip(rc.payload(6:9)), 'int32');
                    distance = typecast(flip(rc.payload(10:13)), 'single');

                    success = true;
                    return
                end
            end
            return
        end
    end
end