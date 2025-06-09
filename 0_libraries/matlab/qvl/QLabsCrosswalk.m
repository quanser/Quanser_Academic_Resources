classdef QLabsCrosswalk < QLabsActor
    properties
        ID_CROSSWALK = 10010;
    end
    methods
        function obj = QLabsCrosswalk(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_CROSSWALK;

        end            

        function success = spawn_id(obj, actorNumber, location, rotation, scale, configuration, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                actorNumber single
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                waitForConfirmation logical = true
            end
            
%           Spawns a new crosswalk actor.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            success = spawn_id@QLabsActor(obj, actorNumber, location, rotation, scale, configuration, waitForConfirmation);
            return
        end

        function success = spawn_id_degrees(obj, actorNumber, location, rotation, scale, configuration, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                actorNumber single
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                waitForConfirmation logical = true
            end

%           Spawns a new crosswalk actor.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            success = spawn_id_degrees@QLabsActor(obj, actorNumber, location, rotation, scale, configuration, waitForConfirmation);
            return
        end

        function [status, actorNumber] = spawn(obj, location, rotation, scale, configuration, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                waitForConfirmation logical = true
            end

%           Spawns a new crosswalk actor with the next available actor number within this class.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            [status, actorNumber] = spawn@QLabsActor(obj, location, rotation, scale, configuration, waitForConfirmation);
            return
        end

        function [status, actorNumber] = spawn_degrees(obj, location, rotation, scale, configuration, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                waitForConfirmation logical = true
            end

%           Spawns a new crosswalk actor with the next available actor number within this class.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            [status, actorNumber] = spawn_degrees@QLabsActor(obj, location, rotation, scale, configuration, waitForConfirmation);
            return
        end

        function success = spawn_id_and_parent_with_relative_transform(obj, actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                actorNumber single
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                parentClassID single = 0
                parentActorNumber single = 0
                parentComponent single = 0
                waitForConfirmation logical = true
            end

%           Spawns a new crosswalk actor relative to an existing actor and creates a kinematic relationship.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            success = spawn_id_and_parent_with_relative_transform(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation);
            return
        end

        function success = spawn_id_and_parent_with_relative_transform_degrees(obj, actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation)
            arguments
                obj QLabsCrosswalk
                actorNumber single
                location (1,3) single = [0 0 0]
                rotation (1,3) single = [0 0 0]
                scale (1,3) single = [1 1 1]
                configuration single = 0
                parentClassID single = 0
                parentActorNumber single = 0
                parentComponent = 0
                waitForConfirmation logical = true
            end

%           Spawns a new crosswalk actor relative to an existing actor and creates a kinematic relationship.
%           Scale reordering is required to deal with a graphics engine
%           limitation on decals.

            scale = [scale(3) scale(2) scale(1)];
            success = spawn_id_and_parent_with_relative_transform_degrees(actorNumber, location, rotation, scale, configuration, parentClassID, parentActorNumber, parentComponent, waitForConfirmation);
            return
        end


    end
end