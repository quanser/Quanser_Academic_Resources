function Container = QCar2MakeSetLEDStripContainer(DeviceNumber, LEDStrip, Brightness) %#codegen

% Create an empty container in case the size checks fail
Container = uint8([]);

if size(LEDStrip, 1) ~= 3
    return
end

if size(LEDStrip, 2) ~= 33
    return
end

Container = flip(typecast(int32(161), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(32)]; %Device function
Container = [Container flip(typecast(flip(single(LEDStrip(:)*Brightness)), 'uint8'))'];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';

