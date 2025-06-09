classdef QuanserInteractiveLabs < handle
    properties
        qlabs_stream = []

        BUFFER_SIZE = 100000

        read_buffer = [];
        send_buffer = [];

        receive_packet_buffer = [];
        receive_packet_size = 0;
        receive_packet_container_index = 0;

		wait_for_container_timeout = 5;

        c = [];
    end

    methods
%%
        function obj = QuanserInteractiveLabs()
            obj = obj@handle();

            obj.c = CommModularContainer();
        end
%%
        function success = open(obj, hostname, timeout)

            arguments
                obj QuanserInteractiveLabs
                hostname char = 'localhost'
                timeout double = 10
            end

            defaultTimeout = timeout;

            % create a client connection
            [obj.qlabs_stream, would_block] = quanser.communications.stream.connect(['tcpip://' hostname ':18000'], true);

            satisfied = false;
            would_block = true;

            try
                if would_block
                    while ((satisfied == false) && (defaultTimeout > 0))
                        satisfied = obj.qlabs_stream.poll(1, 'connect');
                        defaultTimeout = defaultTimeout - 1;

                        if any(satisfied)
                            break;
                        end
                    end
                else
                    satisfied = true;
                end

            catch me
                %fprintf(2, 'Exception occurred. %s\n', me.message);
            end

            success = satisfied;

        end
%%
        function close(obj)
            if ~isempty(obj.qlabs_stream)
                %stream_shutdown(obj.qlabs_stream);
                obj.qlabs_stream.close();
                obj.qlabs_stream = [];
            end
        end
%%
        function delete(obj)
            obj.close()
        end

%%
        function success = send_container(obj, container)

            byte_data = [typecast(int32(container.containerSize+1), 'uint8') ...
                         uint8(123) ...
                         flip(typecast(int32(container.containerSize), 'uint8')) ...
                         flip(typecast(int32(container.classID), 'uint8')) ...
                         flip(typecast(int32(container.actorNumber), 'uint8')) ...
                         uint8(container.actorFunction) ...
                         container.payload];

            [is_sent, ~] = obj.qlabs_stream.send_uint8_array(byte_data);
            obj.qlabs_stream.flush();
            success = is_sent;
        end


%%
        function new_data = receive_new_data(obj)
            new_data = false;

            debug = false;

            [data, ~] = obj.qlabs_stream.receive_uint8s(obj.BUFFER_SIZE);
            bytes_read = length(data);

            if (debug && (bytes_read > 0))
                fprintf("New received data size: %u\n", bytes_read)
            end

            while bytes_read > 0

                obj.receive_packet_buffer = [obj.receive_packet_buffer; data];


                [data, ~] = obj.qlabs_stream.receive_uint8s(obj.BUFFER_SIZE);
                bytes_read = length(data);

                if (debug && (bytes_read > 0))
                    fprintf("Subsequent data received size: %u\n", bytes_read)
                end

            end


            if length(obj.receive_packet_buffer) > 5
                if (obj.receive_packet_buffer(5) == 123)

                    obj.receive_packet_size = typecast(uint8(obj.receive_packet_buffer(1:4)), 'int32');
                    obj.receive_packet_size = obj.receive_packet_size + 4;

                    if (debug)
                        fprintf("Expected packet size: %u\n", obj.receive_packet_size);
                        fprintf("Current buffer size: %u\n", length(obj.receive_packet_buffer));
                    end

                    if length(obj.receive_packet_buffer) >= obj.receive_packet_size

                        obj.receive_packet_container_index = 6;
                        new_data = true;
                    end

                else
                    %print("Error parsing multiple packets in receive buffer.  Clearing internal buffers.")
                    obj.receive_packet_buffer = [];
                end

            end
        end
%%
        function [c, is_more_containers] = get_next_container(obj)
            c = CommModularContainer();
            is_more_containers = false;

            if (obj.receive_packet_container_index > 0)

                c.containerSize  = typecast(uint8(flip(obj.receive_packet_buffer(obj.receive_packet_container_index+0:obj.receive_packet_container_index+3))), 'int32');
                c.classID        = typecast(uint8(flip(obj.receive_packet_buffer(obj.receive_packet_container_index+4:obj.receive_packet_container_index+7))), 'int32');
                c.actorNumber   = typecast(uint8(flip(obj.receive_packet_buffer(obj.receive_packet_container_index+8:obj.receive_packet_container_index+11))), 'int32');
                c.actorFunction = uint8(obj.receive_packet_buffer(obj.receive_packet_container_index+12));

                PayloadStart = obj.receive_packet_container_index+13;
                PayloadEnd = obj.receive_packet_container_index + c.containerSize - 1;

                c.payload = obj.receive_packet_buffer(PayloadStart:PayloadEnd);

                obj.receive_packet_container_index = obj.receive_packet_container_index + c.containerSize;

                if (obj.receive_packet_container_index >= obj.receive_packet_size)

                    is_more_containers = false;

                    if length(obj.receive_packet_buffer) == obj.receive_packet_size
                        % The data buffer contains only the one packet.  Clear the buffer.
                        obj.receive_packet_buffer = [];
                    else
                        % Remove the packet from the data buffer.  There is another packet in the buffer already.
                        obj.receive_packet_buffer = obj.receive_packet_buffer((obj.receive_packet_container_index):(length(obj.receive_packet_buffer)));
                    end

                    obj.receive_packet_container_index = 0;

                else
                    is_more_containers = true;
                end


            end
        end

%%
		function set_wait_for_container_timeout(obj, timeout)

			if (timeout < 0)
				timeout = 0;
			end

			obj.wait_for_container_timeout = timeout;

		end

%%
		function container = wait_for_container(obj, classID, actorNumber, actorFunction)
            container = [];

			tic

            while(true)
                while (obj.receive_new_data() == false)

					if toc > obj.wait_for_container_timeout
						return
					end

                end

                more_containers = true;

                while (more_containers)
                    [current_container, more_containers] = obj.get_next_container();

                    if current_container.classID == classID
                        if current_container.actorNumber == actorNumber
                            if current_container.actorFunction == actorFunction
                                container = current_container;
                                return;
                            end
                        end
                    end
                end
            end
        end


%%
        function flush_receive(obj)
            % get any data still in the receive buffer out

            [data, ~] = obj.qlabs_stream.receive_uint8s(obj.BUFFER_SIZE);
            bytes_read = length(data);

            obj.receive_packet_container_index = 0;
            obj.receive_packet_buffer = [];
        end

%%
        function num_destroyed = destroy_all_spawned_actors(obj)
            % Find and destroy all spawned actors and widgets. This is a blocking operation.
            num_destroyed = 0;
            device_num = 0;

            obj.c.classID = obj.c.ID_GENERIC_ACTOR_SPAWNER;
            obj.c.actorNumber = device_num;
            obj.c.actorFunction = obj.c.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS;
            obj.c.payload = [];
            obj.c.containerSize = 13 + length(obj.c.payload);


            if (send_container(obj, obj.c))
                rc = wait_for_container(obj, obj.c.ID_GENERIC_ACTOR_SPAWNER, device_num, obj.c.FCN_GENERIC_ACTOR_SPAWNER_DESTROY_ALL_SPAWNED_ACTORS_ACK);

                if isempty(rc)
                    fprintf('destroy_all_spawned_actors: Communication timeout.\n');
                    return
                end

                num_destroyed = typecast(flip(rc.payload), 'int32');
            else
                fprintf('destroy_all_spawned_actors: Communication failure).\n');
            end

        end
    end
end