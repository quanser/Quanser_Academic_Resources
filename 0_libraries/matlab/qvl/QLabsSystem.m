classdef QLabsSystem < handle
    properties
%         The System is a special class that allows you to modify elements of the user interface and application.

        ID_SYSTEM = 1000
%         Class ID.s
        FCN_SYSTEM_SET_TITLE_STRING = 10
        FCN_SYSTEM_SET_TITLE_STRING_ACK = 11
        FCN_SYSTEM_EXIT_APP = 100
        FCN_SYSTEM_EXIT_APP_ACK = 101        
    
        c = []
        qlabs = []
        verbose = false
    end
    methods
        function obj = QLabsSystem(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@handle();

            obj.qlabs = qlabs;
            obj.verbose = verbose;
            obj.c = CommModularContainer();
        end

        function success = set_title_string(obj, titleString, waitForConfirmation)
            arguments
                obj QLabsSystem
                titleString string
                waitForConfirmation logical = true
            end
            success = false;

%             Sets the title string in the upper left of the window to custom text. This can be useful when doing screen recordings or labeling experiment configurations.

            obj.c.classID = obj.ID_SYSTEM;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_SYSTEM_SET_TITLE_STRING;
            obj.c.payload = [flip(typecast(int32(length(char(titleString))), 'uint8')) ...
                             uint8(char(titleString))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_SYSTEM, 0, obj.FCN_SYSTEM_SET_TITLE_STRING_ACK);

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

        %%
        function success = exit_application(obj, delay, waitForConfirmation)
            arguments
                obj QLabsSystem
                delay single
                waitForConfirmation logical = true
            end
            success = false;

%             Sets the title string in the upper left of the window to custom text. This can be useful when doing screen recordings or labeling experiment configurations.

            obj.c.classID = obj.ID_SYSTEM;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_SYSTEM_EXIT_APP;
            obj.c.payload = [flip(typecast(single(delay), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            if waitForConfirmation
                obj.qlabs.flush_receive();
            end

            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_SYSTEM, 0, obj.FCN_SYSTEM_EXIT_APP_ACK);

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



    end
end