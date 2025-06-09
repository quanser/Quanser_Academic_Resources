classdef QLabsStopSign < QLabsActor
    properties
        ID_STOP_SIGN = 10020;
    end
    methods
        function obj = QLabsStopSign(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_STOP_SIGN;

            return
        end
    end
end