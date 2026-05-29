function [LidarData] = QCarDecodeLidarContainer(Payload, StartIndex, NumSamples, LidarRange) %#codegen

NumBytes = typecast(uint8(flip(Payload(StartIndex:StartIndex+3))), 'int32');

LidarData = linspace(0,LidarRange, NumSamples);



if (NumBytes/2 ~= NumSamples)
     return
end

LidarAngle = linspace(-pi/4,pi/4, NumSamples/4);

for count = 1:NumSamples
    %LidarData(count) = ((double(Payload(StartIndex+(count-1)*2+4))*256 + double(Payload(StartIndex+(count-1)*2 + 5)))/65535*LidarRange)/cos(LidarAngle(mod(count,NumSamples/4)));
    dist = ((double(Payload(StartIndex+(count-1)*2+4))*256 + double(Payload(StartIndex+(count-1)*2 + 5)))/65535*LidarRange);
    
    LidarData(count) = dist;
end

