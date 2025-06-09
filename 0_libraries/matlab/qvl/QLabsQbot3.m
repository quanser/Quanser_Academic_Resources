classdef QLabsQbot3 < QLabsActor
    properties (Constant)
        ID_QBOT3 = 22

        FCN_QBOT3_COMMAND_AND_REQUEST_STATE = 10
        FCN_QBOT3_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
        FCN_QBOT3_POSSESS = 20
        FCN_QBOT3_POSSESS_ACK = 21
        FCN_QBOT3_RGB_REQUEST = 100
        FCN_QBOT3_RGB_RESPONSE = 101
        FCN_QBOT3_DEPTH_REQUEST = 110
        FCN_QBOT3_DEPTH_RESPONSE = 111
    
    
        VIEWPOINT_RGB = 0
        VIEWPOINT_DEPTH = 1
        VIEWPOINT_TRAILING = 2  
    end
    methods
        function obj = QLabsQbot3(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_QBOT3;
        end
        
        function success = possess(obj, camera)
            arguments
                obj QLabsQbot3
                camera single
            end
            success = false;
%             Possess (take control of) a QBot in QLabs with the selected camera.


            obj.c.classID = obj.ID_QBOT3;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT3_POSSESS;
            obj.c.payload = uint8(camera);            
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT3, obj.actorNumber, obj.FCN_QBOT3_POSSESS_ACK);

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

        function [success, location, forward, up, frontHit, leftHit, rightHit, gyro, heading, encoderLeft, encoderRight] = command_and_request_state(obj, rightWheelSpeed, leftWheelSpeed)
            arguments
                obj QLabsQbot3
                rightWheelSpeed single
                leftWheelSpeed single
            end
            success = false;

%             Sets the velocity, turn angle in radians, and other car properties.

            obj.c.classID = obj.ID_QBOT3;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT3_COMMAND_AND_REQUEST_STATE;
            obj.c.payload = [flip(typecast(single(rightWheelSpeed), 'uint8')) ...
                             flip(typecast(single(leftWheelSpeed), 'uint8'))];
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

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT3, obj.actorNumber, obj.FCN_QBOT3_COMMAND_AND_REQUEST_STATE_RESPONSE);

                if isempty(rc)
                    return
                end

                if length(obj.c.payload) == 55
					location(1) = typecast(flip(rc.payload(1:4)), 'single');
					location(2) = typecast(flip(rc.payload(5:8)), 'single');
					location(3) = typecast(flip(rc.payload(9:12)), 'single');
					forward(1) = typecast(flip(rc.payload(13:16)), 'single');
					forward(2) = typecast(flip(rc.payload(17:20)), 'single');
					forward(3) = typecast(flip(rc.payload(21:24)), 'single');
					up(1) = typecast(flip(rc.payload(25:28)), 'single');
					up(2) = typecast(flip(rc.payload(29:32)), 'single');
					up(3) = typecast(flip(rc.payload(33:36)), 'single');
					frontHit = typecast(rc.payload(37), 'logical');
					leftHit = typecast(rc.payload(38), 'logical');				
					rightHit = typecast(rc.payload(39), 'logical');				
					gyro = typecast(flip(rc.payload(40:43)), 'single');
					heading = typecast(flip(rc.payload(44:47)), 'single');
					encoderLeft = typecast(flip(rc.payload(48:51)), 'int32');
					encoderLeft = typecast(flip(rc.payload(52:55)), 'int32');

                    success = true;
                    return

                else
                    return
                end
            else
                return
            end
        end

        function [success, imageData] = get_image_rgb(obj)
            arguments
                obj QLabsQbot3
            end
            success = false;
            imageData = [];

%             Request a JPG image from the QBot camera.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_QBOT3;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT3_RGB_REQUEST;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT3, obj.actorNumber, obj.FCN_QBOT3_RGB_RESPONSE);

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

        function [success, imageData] = get_image_depth(obj)
            arguments
                obj QLabsQbot3
            end
            success = false;
            imageData = [];

%             Request a JPG image from the QBot camera.

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_QBOT3;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT3_DEPTH_REQUEST;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT3, obj.actorNumber, obj.FCN_QBOT3_DEPTH_RESPONSE);

                if isempty(rc)
                    return
                end

                [imageData, result] = qc_jpeg_decompress(rc.payload(5:end));

                success = true;
                return

            else
                return
            end
        end
    end
end