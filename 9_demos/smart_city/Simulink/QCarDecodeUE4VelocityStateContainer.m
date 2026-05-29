function [Location, Rotation, BumpForward, BumpRear] = QCarDecodeUE4VelocityStateContainer(Payload, StartIndex) %#codegen

Location = [single(0); single(0); single(0)];
Rotation = [single(0); single(0); single(0)];
BumpForward = uint8(0);
BumpRear = uint8(0);

Location(1) = typecast(uint8(flip(Payload(StartIndex:StartIndex+3))), 'single');
Location(2) = typecast(uint8(flip(Payload(StartIndex+4:StartIndex+7))), 'single');
Location(3) = typecast(uint8(flip(Payload(StartIndex+8:StartIndex+11))), 'single');

Rotation(1) = typecast(uint8(flip(Payload(StartIndex+12:StartIndex+15))), 'single');
Rotation(2) = typecast(uint8(flip(Payload(StartIndex+16:StartIndex+19))), 'single');
Rotation(3) = typecast(uint8(flip(Payload(StartIndex+20:StartIndex+23))), 'single');

BumpForward = uint8(Payload(StartIndex+24));
BumpRear = uint8(Payload(StartIndex+25));
