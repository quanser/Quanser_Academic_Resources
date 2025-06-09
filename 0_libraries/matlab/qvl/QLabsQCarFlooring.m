classdef QLabsQCarFlooring < QLabsActor
    properties (Constant)
%         This class is for spawning static floors.

        ID_FLOORING = 10090
%         Class ID
    
        FLOORING_QCAR_MAP_LARGE = 0
        FLOORING_QCAR_MAP_SMALL = 1

    end
    methods
        function obj = QLabsQCarFlooring(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_FLOORING;
        end
    end
end