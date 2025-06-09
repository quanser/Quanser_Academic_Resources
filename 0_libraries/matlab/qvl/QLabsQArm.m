classdef QLabsQArm < QLabsActor
    properties
        ID_QARM = 10  
    end
    methods
        function obj = QLabsQArm(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_QARM;
        end
    end
end