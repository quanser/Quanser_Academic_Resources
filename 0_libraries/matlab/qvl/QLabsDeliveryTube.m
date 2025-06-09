classdef QLabsDeliveryTube < QLabsActor
    properties (Constant)
        ID_DELIVERY_TUBE = 80

        FCN_DELIVERY_TUBE_SPAWN_BLOCK = 10
        FCN_DELIVERY_TUBE_SPAWN_BLOCK_ACK = 11
        FCN_DELIVERY_TUBE_SET_HEIGHT = 12
        FCN_DELIVERY_TUBE_SET_HEIGHT_ACK = 13
    
        BLOCK_CUBE = 0
        BLOCK_CYLINDER = 1
        BLOCK_SPHERE = 2
        BLOCK_GEOSPHERE = 3
    
        CONFIG_HOVER = 0
        CONFIG_NO_HOVER = 1
    end
    methods
        function obj = QLabsDeliveryTube(qlabs, verbose)
            arguments
                qlabs QuanserInteractiveLabs
                verbose logical = false
            end
            obj = obj@QLabsActor(qlabs, verbose);
    
            obj.classID = obj.ID_DELIVERY_TUBE;
        end

        function success = spawn_block(obj, blockType, mass, yawRotation, color)
            arguments
                obj QLabsDeliveryTube
                blockType int32
                mass single
                yawRotation single
                color (1,3) single
            end
            success = false;

            obj.c.classID = obj.ID_DELIVERY_TUBE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_DELIVERY_TUBE_SPAWN_BLOCK;
            obj.c.payload = [flip(typecast(int32(blockType), 'uint8')) ...
                             flip(typecast(single(mass), 'uint8')) ...
                             flip(typecast(single(yawRotation), 'uint8')) ...
                             flip(typecast(single(color(1)), 'uint8')) ...
                             flip(typecast(single(color(2)), 'uint8')) ...
                             flip(typecast(single(color(3)), 'uint8'))];
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_DELIVERY_TUBE, obj.actorNumber, obj.FCN_DELIVERY_TUBE_SPAWN_BLOCK_ACK);

                success = true;
                return
            else
                return
            end
        end

        function success = set_height(obj, height)
            arguments
                obj QLabsDeliveryTube
                height single
            end

            obj.c.classID = obj.ID_DELIVERY_TUBE;
            obj.c.actorNumber = obj.actorNumber;
            obj.c.actorFunction = obj.FCN_DELIVERY_TUBE_SET_HEIGHT;
            obj.c.payload = flip(typecast(single(height), 'uint8'));
            obj.c.containerSize = obj.c.BASE_CONTAINER_SIZE + length(obj.c.payload);

            obj.qlabs.flush_receive();

            if (obj.qlabs.send_container(obj.c))
                rc = obj.qlabs.wait_for_container(obj.ID_DELIVERY_TUBE, obj.actorNumber, obj.FCN_DELIVERY_TUBE_SET_HEIGHT_ACK);

                success = true;
                return
            else
                return
            end
        end
    end
end