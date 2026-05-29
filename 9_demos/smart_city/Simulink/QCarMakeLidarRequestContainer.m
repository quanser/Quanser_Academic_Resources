function Container = QCarMakeLidarRequestContainer(DeviceNumber) %#codegen

%skip size for now

Container = flip(typecast(int32(160), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(110)]; %Device function

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';


% Container = [flip(typecast(int32(10), 'uint8')) ...
%              flip(typecast(int32(160), 'uint8')) ...
%              uint8(DeviceNumber) ...
%              uint8(110)]';