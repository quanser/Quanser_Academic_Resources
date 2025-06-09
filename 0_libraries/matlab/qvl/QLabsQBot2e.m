classdef QLabsQBot2e < QLabsActor
    properties (Constant)
        ID_QBOT2e = 20

        FCN_QBOT_COMMAND_AND_REQUEST_STATE = 10
        FCN_QBOT_COMMAND_AND_REQUEST_STATE_RESPONSE = 11
        FCN_QBOT_POSSESS = 20
        FCN_QBOT_POSSESS_ACK = 21
    
    
        VIEWPOINT_RGB = 0
        VIEWPOINT_DEPTH = 1
        VIEWPOINT_TRAILING = 2
    end
    methods
        function obj = QLabsQBot2e(qlabs, verbose)
            arguments 
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_QBOT2e;
        end

        function success = possess(obj, camera)
            arguments
                obj qlabs_qbot
                camera single
            end
            success = false;

            obj.c.classID = obj.ID_QBOT2e;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_POSSESS;
            obj.c.payload = uint8(camera);
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = qlabs.wait_for_container(obj.ID_QBOT2e, obj.actorNumber, obj.FCN_QBOT_POSSESS_ACK);
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

        function success = command_and_request_state(obj, rightWheelSpeed, leftWheelSpeed)
            arguments
                obj QLabsQBot2e
                rightWheelSpeed single
                leftWheelSpeed single
            end
            success = false;

            obj.c.classID = obj.ID_QBOT2e;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_QBOT_COMMAND_AND_REQUEST_STATE;
            obj.c.payload = [flip(typecast(single(rightWheelSpeed), 'uint8')) ...
                             flip(typecast(single(leftWheelSpeed), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_QBOT2e, obj.actorNumber, obj.FCN_QBOT_COMMAND_AND_REQUEST_STATE_RESPONSE);

                success = true;
                return
            else
                return
            end
        end
    end
end