classdef QLabsCharacter < QLabsActor
    properties
        % This base class implements spawning and AI navigation of the environment for characters.
    
        FCN_CHARACTER_MOVE_TO = 10;
        FCN_CHARACTER_MOVE_TO_ACK = 11;
    end
    methods

        function obj = QLabsCharacter(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end

            obj = obj@QLabsActor(qlabs, verbose);



        end

%%
        function success = move_to(obj, location, speed, waitForConfirmation)

            arguments
                obj QLabsActor
                location (1,3) double = [0 0 0]
                speed double = 0
                waitForConfirmation logical = true
            end

            success = false;

            if (not(obj.is_actor_number_valid()))
                return
            end
    
            obj.c.classID = obj.classID;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_CHARACTER_MOVE_TO;
            obj.c.payload = [flip(typecast(single(location(1)), 'uint8')) ...
                         flip(typecast(single(location(2)), 'uint8')) ...
                         flip(typecast(single(location(3)), 'uint8')) ...
                         flip(typecast(single(speed), 'uint8'))];            
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);
    
            if waitForConfirmation
                obj.qlabs.flush_receive()
            end
    
            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.classID, obj.actorNumber, obj.FCN_CHARACTER_MOVE_TO_ACK);
                    if isempty(rc)
                        if (obj.verbose)
                                fprintf('possess: Communication timeout (classID %u), actorNumber %u).\n', obj.classID, obj.actorNumber);
                        end
                        return
                    else
                        success = true;
                        return
                    end
                end
            else
                if (obj.verbose)
                        fprintf('possess: Communication failure (classID %u), actorNumber %u).\n', obj.classID, obj.actorNumber);
                end
                return 
            end
        end
    end
end