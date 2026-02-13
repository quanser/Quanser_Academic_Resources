classdef QLabsQBotPlatform < QLabsActor
    properties (Constant)
        %This class is for spawning QBotPlatforms.

        ID_QBOT_PLATFORM = 23
    
        FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE = 10
        FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
        FCN_QBOT_PLATFORM_SET_TRANSFORM = 14
        FCN_QBOT_PLATFORM_SET_TRANSFORM_RESPONSE = 15
        FCN_QBOT_PLATFORM_POSSESS = 20
        FCN_QBOT_PLATFORM_POSSESS_ACK = 21
        FCN_QBOT_PLATFORM_IMAGE_REQUEST = 100
        FCN_QBOT_PLATFORM_IMAGE_RESPONSE = 101
        FCN_QBOT_PLATFORM_LIDAR_DATA_REQUEST = 120
        FCN_QBOT_PLATFORM_LIDAR_DATA_RESPONSE = 121
        
    
        VIEWPOINT_RGB = 0
        VIEWPOINT_DEPTH = 1
        VIEWPOINT_DOWNWARD = 2
        VIEWPOINT_TRAILING = 3
     
        CAMERA_RGB = 0
        CAMERA_DEPTH = 1
        CAMERA_DOWNWARD = 2
    
        sensor_scaling = 1
    end
    methods
        %% Constructor
        function obj = QLabsQBotPlatform(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_QBOT_PLATFORM;
        end

        %% Possess (take control of) a QBot in QLabs with the selected camera.
        function success = possess(obj, camera)
            arguments
                obj QLabsQBotPlatform
                camera single
            end
            success = false;

            obj.c.classID = obj.ID_QBOT_PLATFORM;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_PLATFORM_POSSESS;
            obj.c.payload = uint8(camera);            
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT_PLATFORM, obj.actorNumber, obj.FCN_QBOT_PLATFORM_POSSESS_ACK);
                if isempty(rc)
                    return
                else
                    success = true;
                    return
                end
            else
                return
            end
        end

        %% Sets the velocity, turn angle in radians, and other car properties.
        function [success, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight] = command_and_request_state(obj, rightWheelSpeed, leftWheelSpeed, leftLED, rightLED)
            arguments
                obj QLabsQBotPlatform
                rightWheelSpeed single
                leftWheelSpeed single
                leftLED (1,3) single = [1 0 0]
                rightLED (1,3) single = [1 0 0]
            end
            success = false;

            obj.c.classID = obj.ID_QBOT_PLATFORM;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE;
            obj.c.payload = [flip(typecast(single(rightWheelSpeed), 'uint8')) ...
                             flip(typecast(single(leftWheelSpeed), 'uint8')) ...
                             flip(typecast(single(leftLED(1)), 'uint8')) ...
                             flip(typecast(single(leftLED(2)), 'uint8')) ...
                             flip(typecast(single(leftLED(3)), 'uint8')) ...
                             flip(typecast(single(rightLED(1)), 'uint8')) ...
                             flip(typecast(single(rightLED(2)), 'uint8')) ...
                             flip(typecast(single(rightLED(3)), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            location = [0,0,0];
            forward = [0,0,0];
            up = [0,0,0];
            frontHit = false;
            leftHit = false;
            rightHit = false;
            gyro = 0;
            heading = 0;
            encoderLeft = 0;
            encoderRight = 0;

            obj.qlabs.flush_receive()

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT_PLATFORM, obj.actorNumber, obj.FCN_QBOT_PLATFORM_COMMAND_AND_REQUEST_STATE_RESPONSE);

                if isempty(rc)
                    return
                end

                if length(obj.c.payload) == 55
                    [typecast(flip(single(location(1)), 'uint8')) ...
                     typecast(flip(single(location(2)), 'uint8')) ...
                     typecast(flip(single(location(3)), 'uint8')) ...
                     typecast(flip(single(forward(1)), 'uint8')) ...
                     typecast(flip(single(forward(2)), 'uint8')) ...
                     typecast(flip(single(forward(3)), 'uint8')) ...
                     typecast(flip(single(up(1)), 'uint8')) ...
                     typecast(flip(single(up(2)), 'uint8')) ...
                     typecast(flip(single(up(3)), 'uint8')) ...
                     typecast(flip(single(frontHit), 'logical')) ...
                     typecast(flip(single(leftHit), 'logical')) ...
                     typecast(flip(single(rightHit), 'logical')) ...
                     typecast(flip(single(gyro), 'uint8')) ...
                     typecast(flip(single(heading), 'uint8')) ...
                     typecast(flip(single(encoderLeft), 'uint8')) ...
                     typecast(flip(single(encoderRight), 'uint8'))];
                    
                    success = true;
                    return
                else
                    return
                end
            else
                return
            end
        end

        %% Sets the transform, LED colors, and enabling/disabling of physics dynamics
        function [success, location, forward, up] = set_transform(obj, location, rotation, scale, leftLED, rightLED, enableDynamics, waitForConfirmation)
            arguments
                obj QLabsQBotPlatform
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [0 0 0]
                leftLED (1,3) single = [1 0 0]
                rightLED (1,3) single = [1 0 0]
                enableDynamics logical = true
                waitForConfirmation logical = true
            end 

            if (not(obj.is_actor_number_valid()) )
                return
            end

            obj.c.classID = obj.ID_QBOT_PLATFORM;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_PLATFORM_SET_TRANSFORM;
            obj.c.payload = [flip(typecast(single(location(1)), 'uint8')) ...
                     flip(typecast(single(location(2)), 'uint8')) ...
                     flip(typecast(single(location(3)), 'uint8')) ...
                     flip(typecast(single(rotation(1)), 'uint8')) ...
                     flip(typecast(single(rotation(2)), 'uint8')) ...
                     flip(typecast(single(rotation(3)), 'uint8')) ...
                     flip(typecast(single(scale(1)), 'uint8')) ...
                     flip(typecast(single(scale(2)), 'uint8')) ...
                     flip(typecast(single(scale(3)), 'uint8')) ...
                     flip(typecast(single(leftLED(1)), 'uint8')) ...
                     flip(typecast(single(leftLED(2)), 'uint8')) ...
                     flip(typecast(single(leftLED(3)), 'uint8')) ...
                     flip(typecast(single(rightLED(1)), 'uint8')) ...
                     flip(typecast(single(rightLED(2)), 'uint8')) ...
                     flip(typecast(single(rightLED(3)), 'uint8')) ...
                     enableDynamics];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if (waitForConfirmation)
                obj.qlabs.flush_receive();
            end

            success = false;
            location = [0,0,0];
            forward = [0,0,0];
            up = [0,0,0];

            
            if (obj.qlabs.send_container(obj.c))
                
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_QBOT_PLATFORM, obj.actorNumber, obj.FCN_QBOT_PLATFORM_SET_TRANSFORM_RESPONSE);
                    if isempty(rc)
                        if (obj.verbose == true)
                            fprintf('Timeout waiting for response.\n')
                        end
                        return
                    end

                    % THIS IS WRONG!  SHOULD BE USING RC and the assignment
                    % to the return variables is missing.
                    if length(obj.c.payload) == 36
                        [typecast(flip(single(location(1)), 'uint8')) ...
                         typecast(flip(single(location(2)), 'uint8')) ...
                         typecast(flip(single(location(3)), 'uint8')) ...
                         typecast(flip(single(forward(1)), 'uint8')) ...
                         typecast(flip(single(forward(2)), 'uint8')) ...
                         typecast(flip(single(forward(3)), 'uint8')) ...
                         typecast(flip(single(up(1)), 'uint8')) ...
                         typecast(flip(single(up(2)), 'uint8')) ...
                         typecast(flip(single(up(3)), 'uint8'))];
                        
                        success = true;
                    end   

                    return
                end

                success = true;
            end

            
        end

        %% Sets the transform, LED colors, and enabling/disabling of physics dynamics
        function [success, location, forward, up] = set_transform_degrees(obj, location, rotation, scale, leftLED, rightLED, enableDynamics, waitForConfirmation)
            arguments
                obj QLabsQBotPlatform
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [0 0 0]
                leftLED (1,3) single = [1 0 0]
                rightLED (1,3) single = [1 0 0]
                enableDynamics logical = true
                waitForConfirmation logical = true
            end 

            [success, location, forward, up] = obj.set_transform(location, rotation/180*pi, scale, leftLED, rightLED, enableDynamics, waitForConfirmation);

        end


        %% Request a JPG image from the QBot camera.
        function [success, imageData] = get_image(obj, camera)
            arguments
                obj QLabsQBotPlatform
                camera single
            end
            success = false;
            imageData = [];

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_QBOT_PLATFORM;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_PLATFORM_IMAGE_REQUEST;
            obj.c.payload = uint8(camera);
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT_PLATFORM, obj.actorNumber, obj.FCN_QBOT_PLATFORM_IMAGE_RESPONSE);

                if isempty(rc)
                    return
                end

                [imageData, ~] = qc_jpeg_decompress(rc.payload(5:end));
                
                success = true;
                return
                
            else
                return
            end
        end

        %% Request LIDAR data from a QbotPlatform.
        function [success, angle, distances] = get_lidar(obj, samplePoints)
            arguments
                obj QLabsQBotPlatform
                samplePoints single = 400
            end
            success = false;
            angle = [];
            distances = [];
            
            if isempty(obj.is_actor_number_valid())
                if (obj.verbose)
                    fprintf('actorNumber object variable empty. Use a spawn function to assign an actor or manually assign the actorNumber variable.')
                end
                return
            end

            LIDAR_SAMPLES = 4096;
            LIDAR_RANGE = 8*obj.sensor_scaling;

            % The LIDAR is simulated by using 4 orthogonal virtual cameras that are 1 pixel high. The
            % lens distortion of these cameras must be removed to accurately calculate the XY position
            % of the depth samples.

            quarter_angle = linspace(0, 45, int32(LIDAR_SAMPLES/8));
            lens_curve = -0.0077*quarter_angle.*quarter_angle + 1.3506*quarter_angle;
            lens_curve_rad = lens_curve/180*pi;

            angles = [pi*4/2-1*flip(lens_curve_rad) ...
                       lens_curve_rad ...
                       (pi/2 - 1*flip(lens_curve_rad)) ...
                       (pi/2 + lens_curve_rad) ...
                       (pi - 1*flip(lens_curve_rad)) ...
                       (pi + lens_curve_rad) ...
                       (pi*3/2 - 1*flip(lens_curve_rad)) ...
                       (pi*3/2 + lens_curve_rad)];

            obj.c.classID = obj.ID_QBOT_PLATFORM;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_PLATFORM_LIDAR_DATA_REQUEST;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT_PLATFORM, obj.actorNumber, obj.FCN_QBOT_PLATFORM_LIDAR_DATA_RESPONSE);

                if isempty(rc)
                    if (obj.verbose)
                        fprintf('Failed to receive return container.')
                    end
                    return
                end
                if ((length(rc.payload)-4)/2 ~= LIDAR_SAMPLES)
                    if (obj.verbose)
                        fprintf('Received %u bytes, expected %u\n', length(rc.payload), LIDAR_SAMPLES*2)
                    end
                    return
                end

                distance = zeros(1, LIDAR_SAMPLES);

                % Parse 16-bit samples from the returned payload. Payload layout: 4-byte header, then 2 bytes per sample
                for count = 1:LIDAR_SAMPLES
                    b1 = rc.payload(5 + (count-1)*2);
                    b2 = rc.payload(6 + (count-1)*2);
                    raw_value = mod(double(b1)*256 + double(b2), 65535);
                    distance(count) = (raw_value/65535)*LIDAR_RANGE;
                end

                % Resample the data using a linear radial distribution to the desired number of points
                % and realign the first index to be 0 (forward)
                sampled_angles = linspace(0, 2*pi, samplePoints+1);
                sampled_angles = sampled_angles(1:end-1);
                sampled_distance = zeros(1, samplePoints);

                % Start from the index closest to 0 radians to avoid hard-coded offsets
                [~, index_raw] = min(abs(angles - 0));

                for count = 1:samplePoints
                    while angles(index_raw) < sampled_angles(count)
                        index_raw = index_raw + 1;
                        if index_raw > LIDAR_SAMPLES
                            index_raw = 1;
                        end
                    end

                    prev_idx = index_raw - 1;
                    if prev_idx < 1
                        prev_idx = LIDAR_SAMPLES;
                    end

                    if (angles(index_raw) - angles(prev_idx)) == 0
                        sampled_distance(count) = distance(index_raw);
                    else
                        sampled_distance(count) = (distance(index_raw) - distance(prev_idx)) * ...
                        (sampled_angles(count) - angles(prev_idx)) / ...
                        (angles(index_raw) - angles(prev_idx)) + distance(prev_idx);
                    end
                end

                success = true;
                angle = sampled_angles;
                distances = sampled_distance;
                return
            else
                if (obj.verbose)
                    fprintf('Communications request for LIDAR data failed.')
                end
                return
            end
        end

    end
end