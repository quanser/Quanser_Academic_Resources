classdef QLabsYieldSign < QLabsActor
    properties
        ID_YIELD_SIGN = 10070
    end

    methods
        function obj = QLabsYieldSign(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_YIELD_SIGN;

            return
        end
    end
end