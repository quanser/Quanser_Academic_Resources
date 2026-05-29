function [SampledAngles, SampledDistance] = QCar2DecodeLidarContainer(Payload, StartIndex, NumSamples, LidarRange) %#codegen

RAW_LIDAR_IMAGE_SIZE = 4096;

% calculate the inverse of the lense curvature based on impirical values
quarter_angle = linspace(0, 45, RAW_LIDAR_IMAGE_SIZE/8);
lens_curve = -0.0077*quarter_angle.^2 + 1.3506*quarter_angle;
lens_curve_rad = lens_curve/180*pi;

% setup pre-calculated point distribution
RawLidarAngle = [pi*4/2-1*flip(lens_curve_rad) ...
                      lens_curve_rad ...
                  pi/2 - 1*flip(lens_curve_rad) ...
                  pi/2 + lens_curve_rad ...
                  pi - 1*flip(lens_curve_rad) ...
                  pi + lens_curve_rad ...
                  pi*3/2 - 1*flip(lens_curve_rad) ...
                  pi*3/2 + lens_curve_rad];

RawLidarDist = zeros(1,RAW_LIDAR_IMAGE_SIZE); 


SampledAngles = linspace(0,2*pi, NumSamples);
SampledDistance = linspace(0,0, NumSamples);

% Convert raw data to distances
NumBytes = typecast(uint8(flip(Payload(StartIndex:StartIndex+3))), 'int32');

if (NumBytes/2 ~= RAW_LIDAR_IMAGE_SIZE)
     return
end

for count = 1:RAW_LIDAR_IMAGE_SIZE
    RawLidarDist(count) = ((double(Payload(StartIndex+(count-1)*2+4))*256 + double(Payload(StartIndex+(count-1)*2 + 5)))/65535*LidarRange);
end

% Resample the data using a linear radial distribution to the desired number of points
% and realign the first index to be 0 (forward)

index_raw = 513;
for count = 1:NumSamples
    while (RawLidarAngle(index_raw) < SampledAngles(count))
        index_raw = mod((index_raw + 1), 4096);
    end
            
    if index_raw ~= 0
        if (RawLidarAngle(index_raw)-RawLidarAngle(index_raw-1)) == 0
            SampledDistance(count) = RawLidarDist(index_raw);
        else
            SampledDistance(count) = (RawLidarDist(index_raw)-RawLidarDist(index_raw-1))*(SampledAngles(count)-RawLidarAngle(index_raw-1))/(RawLidarAngle(index_raw)-RawLidarAngle(index_raw-1)) + RawLidarDist(index_raw-1);
        end 
        
    else
        SampledDistance(count) = RawLidarDist(index_raw);
    end
end    
