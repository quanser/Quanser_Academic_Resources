classdef QLabsFreeCamera < QLabsActor
    properties

        ID_FREE_CAMERA = 170;
    
        FCN_FREE_CAMERA_POSSESS = 10;
        FCN_FREE_CAMERA_POSSESS_ACK = 11;
        FCN_FREE_CAMERA_SET_CAMERA_PROPERTIES = 12;
        FCN_FREE_CAMERA_SET_CAMERA_PROPERTIES_ACK = 13;
        FCN_FREE_CAMERA_SET_TRANSFORM = 14;
        FCN_FREE_CAMERA_SET_TRANSFORM_ACK = 15;
        FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION = 90;
        FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION_RESPONSE = 91;
        FCN_FREE_CAMERA_REQUEST_IMAGE = 100;
        FCN_FREE_CAMERA_RESPONSE_IMAGE = 101;
    end
    methods
        %%
        function obj = QLabsFreeCamera(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_FREE_CAMERA;
        end

        %%
        function success = possess(obj)
            success = false;

            if (not(is_actor_number_valid(obj)))
                return
            end

            obj.c.classID = obj.ID_FREE_CAMERA;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_FREE_CAMERA_POSSESS;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_FREE_CAMERA, obj.actorNumber, obj.FCN_FREE_CAMERA_POSSESS_ACK);
                
                if isempty(rc)
                    if (obj.verbose)
                        fprintf('possess: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                    end
                    return
                end     
                
                success = true;
            else
                if (obj.verbose)
                    fprintf('possess: Communication failure (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                end
            end
        end

        %%
        function success = set_transform(obj, location, rotation)
            
            arguments
                obj QLabsActor
                location (1,3) double = [0 0 0]
                rotation (1,3) double = [0 0 0]
            end
            
            
            success = false;
    
    
            if (not(is_actor_number_valid(obj)))
                return
            end
    
            obj.c.classID = obj.ID_FREE_CAMERA;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_FREE_CAMERA_SET_TRANSFORM;
            obj.c.payload = [flip(typecast(single(location(1)), 'uint8')) ...
                         flip(typecast(single(location(2)), 'uint8')) ...
                         flip(typecast(single(location(3)), 'uint8')) ...
                         flip(typecast(single(rotation(1)), 'uint8')) ...
                         flip(typecast(single(rotation(2)), 'uint8')) ...
                         flip(typecast(single(rotation(3)), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);
    
    
            obj.qlabs.flush_receive()
    
            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_FREE_CAMERA, obj.actorNumber, obj.FCN_FREE_CAMERA_SET_TRANSFORM_ACK);
                if isempty(rc)
                    if (obj.verbose)
                            fprintf('possess: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                    end
                    return
                else
                    success = true;
                    return
                end
            else
                if (obj.verbose)
                        fprintf('possess: Communication failure (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                end
                return 
            end
            
        end
        
        %%
        function success = set_transform_degrees(obj, location, rotation)
            
            arguments
                obj QLabsActor
                location (1,3) double = [0 0 0]
                rotation (1,3) double = [0 0 0]
            end
            
            
            success = set_transform(obj, location, rotation/180*pi);
            
        end    
    

        %%
        function success = set_camera_properties(obj, fieldOfView, depthOfField, aperture, focusDistance)
%             Sets the camera properties. When depthOfField is enabled, the camera will produce more realistic (and cinematic) results by adding some blur to the view at distances closer and further away from a given focal distance. For more blur, use a large aperture (small value) and a narrow field of view.

            success = false;

            if (not(obj.is_actor_number_valid))
                return
            end

            obj.c.classID = obj.ID_FREE_CAMERA;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_FREE_CAMERA_SET_CAMERA_PROPERTIES;
            obj.c.payload = [flip(typecast(single(fieldOfView), 'uint8')) ...
                         uint8(depthOfField) ...
                         flip(typecast(single(aperture), 'uint8')) ...
                         flip(typecast(single(focusDistance), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_FREE_CAMERA, obj.actorNumber, obj.FCN_FREE_CAMERA_SET_CAMERA_PROPERTIES_ACK);
                if isempty(rc)
                    if (obj.verbose)
                            fprintf('possess: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                    end
                    return
                else
                    success = true;
                    return
                end
            end
        end

        %%
        function success = set_image_capture_resolution(obj, width, height)
            %"""Change the default width and height of image resolution for capture """
        
            arguments
                obj QLabsActor
                width int32 = 640
                height int32 = 480
            end

            success = false;

            if (not(obj.is_actor_number_valid))
                return
            end

            obj.c.classID = obj.ID_FREE_CAMERA;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION;
            obj.c.payload = [flip(typecast(int32(width), 'uint8')) ...
                             flip(typecast(int32(height), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);


            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_FREE_CAMERA, obj.actorNumber, obj.FCN_FREE_CAMERA_SET_IMAGE_RESOLUTION_RESPONSE);
                if isempty(rc)
                    if (obj.verbose)
                        fprintf('set_image_capture_resolution: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                    end
                    return
                else
                    success = true;
                    return
                end
            end
        end


        %%
        function [success, data] = get_image(obj)
            %Request an image from the camera actor. Note, set_image_capture_resolution must be set once per camera otherwise this method will fail.
    
            success = false;
            data = [];

            if (not(obj.is_actor_number_valid))
                return
            end
        
            obj.c.classID = obj.ID_FREE_CAMERA;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_FREE_CAMERA_REQUEST_IMAGE;
            obj.c.payload = [];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);


            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_FREE_CAMERA, obj.actorNumber, obj.FCN_FREE_CAMERA_RESPONSE_IMAGE);
                if isempty(rc)
                    if (obj.verbose)
                        fprintf('get_image: Communication timeout (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                    end
                    return
                else
                    if length(rc.payload) >= 4
                        image_size = typecast(flip(rc.payload(1:4)), 'int32');

                        if (image_size <= 0)
                            if (obj.verbose)
                                fprintf('get_image: jpg size invalid (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                            end
                            return
                        end
                        
                        [data, ~] = qc_jpeg_decompress(rc.payload(5:end));

                        success = true;
                    else
                        if (obj.verbose)
                            fprintf('get_image: Payload size smaller than expected (classID %u, actorNumber %u).\n', obj.classID, obj.actorNumber);
                        end
                    end
                    return
                end
            end
        end



    

    end % methods
end % class