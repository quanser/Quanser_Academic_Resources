function Container = QCar2MakeCommandVelocityStateContainer(DeviceNumber, Forward_And_Steering, Lights) %#codegen

%skip size for now

Container = flip(typecast(int32(161), 'uint8')); %Device ID
Container = [Container flip(typecast(int32(DeviceNumber), 'uint8'))];
Container = [Container uint8(10)]; %Device function
Container = [Container flip(typecast(single(Forward_And_Steering(2)), 'uint8'))];
Container = [Container flip(typecast(single(Forward_And_Steering(1)), 'uint8'))];


% 1 - L Outside Brake
% 2 - L Inside Brake
% 3 - R Inside Brake
% 4 - R Outside Brake
% 
% 5 - L Reverse
% 6 - R Reverse
% 
% 7 - BL Turn Signal
% 8 - BR Turn Signal
% 
% 9 - L Outside Headlight
% 10 - L Middle Headlight
% 11 - L Inside Headlight
% 12 - R Outside Headlight
% 13 - R Middle Headlight
% 14 - R Inside Headlight
% 
% 15 - FL Turn Signal
% 16 - FR Turn Signal

% Headlights
LightByte = Lights(9);
LightByte = bitor(LightByte, bitshift(Lights(10), 1));
LightByte = bitor(LightByte, bitshift(Lights(11), 2));
LightByte = bitor(LightByte, bitshift(Lights(12), 3));
LightByte = bitor(LightByte, bitshift(Lights(13), 4));
LightByte = bitor(LightByte, bitshift(Lights(14), 5));
Container = [Container LightByte];

% Left Turn
LightByte = Lights(15);
LightByte = bitor(LightByte, bitshift(Lights(7), 1));
Container = [Container LightByte];

% Right Turn
LightByte = Lights(16);
LightByte = bitor(LightByte, bitshift(Lights(8), 1));
Container = [Container LightByte];

% Brake
LightByte = Lights(1);
LightByte = bitor(LightByte, bitshift(Lights(2), 1));
LightByte = bitor(LightByte, bitshift(Lights(3), 2));
LightByte = bitor(LightByte, bitshift(Lights(4), 3));
Container = [Container LightByte];

% Reverse
LightByte = Lights(5);
LightByte = bitor(LightByte, bitshift(Lights(6), 1));
Container = [Container LightByte];

%Prepend container size
Container = [flip(typecast(int32(length(Container) + 4), 'uint8')) Container]';

