classdef QLabsQDrone2 < QLabsActor
    properties (Constant)
        %This class is for spawning QBotPlatforms.

    ID_QDRONE2 = 231

    FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE = 10
    FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE_RESPONSE = 11
    FCN_QDRONE2_SET_WORLD_TRANSFORM = 12
    FCN_QDRONE2_SET_WORLD_TRANSFORM_ACK = 13
    FCN_QDRONE2_POSSESS = 20
    FCN_QDRONE2_POSSESS_ACK = 21
    FCN_QDRONE2_IMAGE_REQUEST = 100
    FCN_QDRONE2_IMAGE_RESPONSE = 101
    FCN_QDRONE2_SET_CAMERA_RESOLUTION = 102
    FCN_QDRONE2_SET_CAMERA_RESOLUTION_RESPONSE = 103
    

    VIEWPOINT_CSI_LEFT = 0
    VIEWPOINT_CSI_BACK = 1
    VIEWPOINT_CSI_RIGHT = 2
    VIEWPOINT_RGB = 3
    VIEWPOINT_DEPTH = 4
    VIEWPOINT_DOWNWARD = 5
    VIEWPOINT_OPTICAL_FLOW = 6
    VIEWPOINT_OVERHEAD = 7
    VIEWPOINT_TRAILING = 8
 
    CAMERA_CSI_LEFT = 0
    CAMERA_CSI_BACK = 1
    CAMERA_CSI_RIGHT = 2
    CAMERA_RGB = 3
    CAMERA_DEPTH = 4
    CAMERA_DOWNWARD = 5
    CAMERA_OPTICAL_FLOW = 6
	
    end
    methods
        function obj = QLabsQDrone2(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_QDRONE2;
        end
        
        function success = possess(obj, camera)
            arguments
                obj QLabsQDrone2
                camera single
            end
            success = false;
%             Possess (take control of) a QDrone in QLabs with the selected camera.
            
            if isempty(obj.is_actor_number_valid)
                return
            end

            obj.c.classID = obj.ID_QDRONE2;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QDRONE2_POSSESS;
            obj.c.payload = flip(typecast(int32(camera), 'uint8'));          
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QDRONE2, obj.actorNumber, obj.FCN_QDRONE2_POSSESS_ACK);
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

        function [success, location, orientation, quaternion, velocity, TOFDistance, collision, collisionLocation, collisionForce] = set_velocity_and_request_state(obj, motorsEnabled, velocity, orientation)
            arguments
                obj QLabsQDrone2
                motorsEnabled single
                velocity (1,3) single = [0 0 0]
                orientation (1,3) single = [0 0 0]
            end
            success = false;
			% Sets the velocity, turn angle in radians, and other properties.

            if isempty(obj.is_actor_number_valid)
                return
            end            

            obj.c.classID = obj.ID_QDRONE2;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE;
            obj.c.payload = [flip(typecast(single(velocity(1)), 'uint8')) ...
                             flip(typecast(single(velocity(2)), 'uint8')) ...
							 flip(typecast(single(velocity(3)), 'uint8')) ...
							 flip(typecast(single(orientation(1)), 'uint8')) ...
                             flip(typecast(single(orientation(2)), 'uint8')) ...
							 flip(typecast(single(orientation(3)), 'uint8')) ...
							 uint8(motorsEnabled)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

			location = [0,0,0];
			orientation = [0,0,0];
			quaternion = [0,0,0,0];
			velocity = [0,0,0];
			TOFDistance = 0;
			collision = false;
			collisionLocation = [0,0,0];
			collisionForce = [0,0,0];

            obj.qlabs.flush_receive()

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QDRONE2, obj.actorNumber, obj.FCN_QDRONE2_COMMAND_VELOCITY_AND_REQUEST_STATE_RESPONSE);

                if isempty(rc)
                    return
                end

                if length(obj.c.payload) == 81
					location(1) = typecast(flip(rc.payload(1:4)), 'single');
					location(2) = typecast(flip(rc.payload(5:8)), 'single');
					location(3) = typecast(flip(rc.payload(9:12)), 'single');
					orientation(1) = typecast(flip(rc.payload(13:16)), 'single');
					orientation(2) = typecast(flip(rc.payload(17:20)), 'single');
					orientation(3) = typecast(flip(rc.payload(21:24)), 'single');
					quaternion(1) = typecast(flip(rc.payload(25:28)), 'single');
					quaternion(2) = typecast(flip(rc.payload(29:32)), 'single');
					quaternion(3) = typecast(flip(rc.payload(33:36)), 'single');
					quaternion(4) = typecast(flip(rc.payload(37:40)), 'single');
					velocity(1) = typecast(flip(rc.payload(41:44)), 'single');
					velocity(2) = typecast(flip(rc.payload(45:48)), 'single');
					velocity(3) = typecast(flip(rc.payload(49:52)), 'single');
					TOFDistance = typecast(flip(rc.payload(53:56)), 'single');
					collision = typecast(rc.payload(57), 'logical');
					collisionLocation(1) = typecast(flip(rc.payload(58:61)), 'single');
					collisionLocation(2) = typecast(flip(rc.payload(62:65)), 'single');
					collisionLocation(3) = typecast(flip(rc.payload(66:69)), 'single');
					collisionForce(1) = typecast(flip(rc.payload(70:73)), 'single');
					collisionForce(2) = typecast(flip(rc.payload(74:77)), 'single');
					collisionForce(3) = typecast(flip(rc.payload(78:81)), 'single');
					
                    success = true;
                    return
                else
                    return
                end
            else
                return
            end
        end

        function [success, cameraNumber, imageData] = get_image(obj, camera)
            arguments
                obj QLabsQDrone2
                camera single
            end
            success = false;
			cameraNumber = -1;
            imageData = [];
		
			%Request a JPG image from the QDrone camera.	

            if isempty(obj.is_actor_number_valid())
                return
            end

            obj.c.classID = obj.ID_QDRONE2;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QDRONE2_IMAGE_REQUEST;
            obj.c.payload = uint8(camera);
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QDRONE2, obj.actorNumber, obj.FCN_QDRONE2_IMAGE_RESPONSE);

                if isempty(rc)
                    return
                end

				cameraNumber = typecast(flip(rc.payload(1:4)), 'int32');
                [imageData, ~] = qc_jpeg_decompress(rc.payload(9:end));
                
                success = true;
                return
                
            else
                return
            end
        end

        
    end
end