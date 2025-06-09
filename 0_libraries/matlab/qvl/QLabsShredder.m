classdef QLabsShredder < QLabsActor
    properties (Constant)
        ID_SHREDDER = 190

        RED = 0
        GREEN = 1
        BLUE = 2
        WHITE = 3
    end
    methods
        function obj = QLabsShredder(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_SHREDDER;
        end
    end
end