classdef QLabsRoundaboutSign < QLabsActor
    properties
        ID_ROUNDABOUT_SIGN = 10060;
    end
    methods
        function obj = QLabsRoundaboutSign(qlabs, verbose) 

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            
            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_ROUNDABOUT_SIGN;
        end
    end
end