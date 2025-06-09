classdef QLabsPerson < QLabsCharacter
    properties (Constant)
        % This class implements spawning and AI navigation of the environment for human pedestrians
    
        ID_PERSON = 10030
    
        STANDING = 0
        % Speed constant for the move_to method. 
        WALK = 1.2
        % Speed constant for the move_to method. 
        JOG = 3.6
        % Speed constant for the move_to method. 
        RUN = 6.0
        % Speed constant for the move_to method. 
    end
    methods
        function obj = QLabsPerson(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end

            obj = obj@QLabsCharacter(qlabs, verbose);

            obj.classID = obj.ID_PERSON;

        end
    end
end