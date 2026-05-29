function Container = QCarMakeCameraRequestContainer(DeviceNumber, CameraNumber) %#codegen

%skip size for now

Container = flip(typecast(int32(160), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(100)]; %Device function
Container = [Container flip(typecast(int32(CameraNumber), 'uint8'))];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';

% Container = [flip(typecast(int32(14), 'uint8')) ...
%              flip(typecast(int32(160), 'uint8')) ...
%              uint8(DeviceNumber) ...
%              uint8(100) ...
%              flip(typecast(int32(length(CameraNumber) + 4), 'uint8'))]';