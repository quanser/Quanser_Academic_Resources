function Container = QCarMakeSetTransformContainer(DeviceNumber, Location_v3, Rotation_v3, EnableDynamics, Headlights, LeftTurn, RightTurn, BrakeLight, Honk) %#codegen

%skip size for now

Container = flip(typecast(int32(160), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(12)]; %Device function
Container = [Container flip(typecast(single(Location_v3(1)), 'uint8'))];
Container = [Container flip(typecast(single(Location_v3(2)), 'uint8'))];
Container = [Container flip(typecast(single(Location_v3(3)), 'uint8'))];

Container = [Container flip(typecast(single(Rotation_v3(1)), 'uint8'))];
Container = [Container flip(typecast(single(Rotation_v3(2)), 'uint8'))];
Container = [Container flip(typecast(single(Rotation_v3(3)), 'uint8'))];

Container = [Container uint8(EnableDynamics)];
Container = [Container uint8(Headlights)];
Container = [Container uint8(LeftTurn)];
Container = [Container uint8(RightTurn)];
Container = [Container uint8(BrakeLight)];
Container = [Container uint8(Honk)];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';