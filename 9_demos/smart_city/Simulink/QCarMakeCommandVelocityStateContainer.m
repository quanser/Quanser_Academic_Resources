function Container = QCarMakeCommandVelocityStateContainer(DeviceNumber, Forward_And_Steering, Lights) %#codegen

%skip size for now

Container = flip(typecast(int32(160), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(10)]; %Device function
Container = [Container flip(typecast(single(Forward_And_Steering(1)), 'uint8'))];
Container = [Container flip(typecast(single(Forward_And_Steering(2)), 'uint8'))];
Container = [Container Lights(1)];
Container = [Container Lights(2)];
Container = [Container Lights(3)];
Container = [Container Lights(4)];
Container = [Container Lights(5)];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';