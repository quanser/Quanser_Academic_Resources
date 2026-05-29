function Container = QBot2eMakeSetTransformStateContainer(DeviceNumber, Forward, Right) %#codegen

%skip size for now

Container = flip(typecast(int32(20), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(10)]; %Device function
Container = [Container flip(typecast(single(Forward), 'uint8'))];
Container = [Container flip(typecast(single(Right), 'uint8'))];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';