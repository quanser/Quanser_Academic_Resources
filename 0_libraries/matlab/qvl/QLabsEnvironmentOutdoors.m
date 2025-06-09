classdef QLabsEnvironmentOutdoors < handle
    properties
        c = [];

        qlabs = [];
        verbose = false;
        classID = 0;
    end

    properties (Constant)
        %  This class modifies QLabs open worlds with outdoor environments.

        ID_ENVIRONMENT_OUTDOORS = 1100
        %  Class ID
    
        FCN_SET_TIME_OF_DAY = 10
        FCN_SET_TIME_OF_DAY_ACK = 11
        FCN_OVERRIDE_OUTDOOR_LIGHTING = 12
        FCN_OVERRIDE_OUTDOOR_LIGHTING_ACK = 13
        FCN_SET_WEATHER_PRESET = 14
        FCN_SET_WEATHER_PRESET_ACK = 15
    
        CLEAR_SKIES = 0
        PARTLY_CLOUDY = 1
        CLOUDY = 2
        OVERCAST = 3
        FOGGY = 4
        LIGHT_RAIN = 5
        RAIN = 6
        THUNDERSTORM = 7
        LIGHT_SNOW = 8
        SNOW = 9
        BLIZZARD = 10
        
    end

    methods
        function obj = QLabsEnvironmentOutdoors(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end            

            obj = obj@handle();

            obj.qlabs = qlabs;
            obj.verbose = verbose;
            obj.c = CommModularContainer();
        end

        function success = set_time_of_day(obj, time)
            arguments
                obj QLabsEnvironmentOutdoors
                time single = 12
            end
            success = false;

%             Set the time of day for an outdoor environment.

            obj.c.classID = obj.ID_ENVIRONMENT_OUTDOORS;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_SET_TIME_OF_DAY;
            obj.c.payload = [flip(typecast(single(time), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

           if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_ENVIRONMENT_OUTDOORS, 0, obj.FCN_SET_TIME_OF_DAY_ACK);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end
                success = true;
                return
            end
        end

        function success = set_outdoor_lighting(obj, state)
            arguments
                obj QLabsEnvironmentOutdoors
                state single
            end
            success = false;

%             Overrides the outdoor lighting set by other environment functions

            obj.c.classID = obj.ID_ENVIRONMENT_OUTDOORS;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_OVERRIDE_OUTDOOR_LIGHTING;
            obj.c.payload = [flip(typecast(int32(state), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_ENVIRONMENT_OUTDOORS, 0, obj.FCN_OVERRIDE_OUTDOOR_LIGHTING_ACK);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end
            end
            success = true;
            return
        end

        function success = set_weather_preset(obj, weather_preset)
            arguments
                obj QLabsEnvironmentOutdoors
                weather_preset single
            end
            success = false;

%             Set the weather conditions for an outdoor environment with a preset value
            
            obj.c.classID = obj.ID_ENVIRONMENT_OUTDOORS;
            obj.c.actorNumber = 0;
            obj.c.actorFunction = obj.FCN_SET_WEATHER_PRESET;
            obj.c.payload = [flip(typecast(int32(weather_preset), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_ENVIRONMENT_OUTDOORS, 0, obj.FCN_SET_WEATHER_PRESET_ACK);
                if isempty(rc)
                    if (obj.verbose == true)
                        fprintf('Timeout waiting for response.\n')
                    end
                    return
                end
                success = true;
                return
            end
        end
    end
end