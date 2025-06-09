classdef QLabsDeliveryTubeBottles < QLabsActor
    properties (Constant)
        ID_DELIVERY_TUBE_BOTTLES = 81

        FCN_DELIVERY_TUBE_SPAWN_CONTAINER = 10
        FCN_DELIVERY_TUBE_SPAWN_CONTAINER_ACK = 11
        FCN_DELIVERY_TUBE_SET_HEIGHT = 12
        FCN_DELIVERY_TUBE_SET_HEIGHT_ACK = 13
    
        PLASTIC_BOTTLE = 4
        METAL_CAN = 5
    
        CONFIG_HOVER = 0
        CONFIG_NO_HOVER = 1
    end
    methods
        function obj = QLabsDeliveryTubeBottles(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_DELIVERY_TUBE_BOTTLES;
        end

        function success = spawn_container(obj, metallic, color, mass, propertyString, height, diameter, roughness)
            arguments
                obj QLabsDeliveryTubeBottles
                metallic logical
                color (1,3) single
                mass single
                propertyString string = ""
                height single = 0.1
                diameter single = 0.65
                roughness single = 0.65
            end
            success = false;

            obj.c.classID = obj.ID_DELIVERY_TUBE_BOTTLES;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_DELIVERY_TUBE_SPAWN_CONTAINER;
            %obj.c.payload = bytearray(struct.pack(">ffBffffffI", height, diameter, metallic, color[0], color[1], color[2], 1.0, roughness, mass, len(propertyString)))
            obj.c.payload = [flip(typecast(single(height), 'uint8')) ...
                             flip(typecast(single(diameter), 'uint8')) ...
                             uint8(metallic) ...
                             flip(typecast(single(color(1)), 'uint8')) ...
                             flip(typecast(single(color(2)), 'uint8')) ...
                             flip(typecast(single(color(3)), 'uint8')) ...
                             flip(typecast(single(1), 'uint8')) ...
                             flip(typecast(single(roughness), 'uint8')) ...
                             flip(typecast(single(mass), 'uint8')) ...
                             flip(typecast(int32(length(char(propertyString))), 'uint8')) ...
                             uint8(char(propertyString))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_DELIVERY_TUBE_BOTTLES, obj.actorNumber, obj.FCN_DELIVERY_TUBE_SPAWN_CONTAINER_ACK);

                success = true;
                return
            else
                return
            end
        end

        function success = set_height(obj, height)
            arguments
                obj QLabsDeliveryTubeBottles
                height single
            end
            success = false;

            obj.c.classID = obj.ID_DELIVERY_TUBE_BOTTLES;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_DELIVERY_TUBE_SET_HEIGHT;
            obj.c.payload = flip(typecast(single(height), 'uint8'));
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_DELIVERY_TUBE_BOTTLES, obj.actorNumber, obj.FCN_DELIVERY_TUBE_SET_HEIGHT_ACK);

                success = true;
                return
            else
                return
            end
        end
    end
end