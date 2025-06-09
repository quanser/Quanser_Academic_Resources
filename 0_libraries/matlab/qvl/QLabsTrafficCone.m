classdef QLabsTrafficCone < QLabsActor
    properties
        ID_TRAFFIC_CONE = 10000;

        FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES = 10;
        FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES_ACK = 11;
        FCN_TRAFFIC_CONE_GET_MATERIAL_PROPERTIES = 12;
        FCN_TRAFFIC_CONE_GET_MATERIAL_PROPERTIES_RESPONSE = 13;
    end
    methods
        function obj = QLabsTrafficCone(qlabs, verbose)

            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end

            obj = obj@QLabsActor(qlabs, verbose);

            obj.classID = obj.ID_TRAFFIC_CONE;


        end

        function success = set_material_properties(obj, materialSlot, color, roughness, metallic, waitForConfirmation)
            arguments
                obj QLabsTrafficCone
                materialSlot single = 0
                color (1,3) single = [0 0 0]
                roughness single = 0.4
                metallic logical = false
                waitForConfirmation logical = true
            end

            success = false;

            if (not(obj.is_actor_number_valid()) )
                return;
            end
    
            obj.c.classID = obj.ID_TRAFFIC_CONE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES;
            obj.c.payload = [uint8(materialSlot) ...
                             flip(typecast(single(color(1)), 'uint8')) ...
                             flip(typecast(single(color(2)), 'uint8')) ...
                             flip(typecast(single(color(3)), 'uint8')) ...
                             flip(typecast(single(roughness), 'uint8')) ...
                             uint8(metallic)];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);


            if (obj.qlabs.send_container(obj.c))
                if waitForConfirmation
                    rc = obj.qlabs.wait_for_container(obj.ID_TRAFFIC_CONE, obj.actorNumber, obj.FCN_TRAFFIC_CONE_SET_MATERIAL_PROPERTIES_ACK);

                    if isempty(rc)
                        return
                    else
                        success = true;
                    end
                else
                    success = true;
                end
            else
                success = false;
            end

        end

    end
end