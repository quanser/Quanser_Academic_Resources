clear all;

%% CHANGEABLE VARIABLES
% map_type = 1 -> Large SDCS Map
% map_type = 0 -> Small SDCS Map
map_type = 1;

% qcar_types = 3 -> VIRTUAL ONLY QCar2
% qcar_types = 2 -> Physical QCar 2's (+ virtual)
% qcar_types = 1 -> BOTH Physical QCar 1 and 2's (+ virtual)
% qcar_types = 0 -> Physical QCar 1's (+ virtual)
qcar_types = 1;


%% Setting Qcar Variables

% Various Timing Loops
CSI_Sample_Time = 1/60;
Controller_Sample_Time =CSI_Sample_Time/10;
RealSense_Sample_Time = CSI_Sample_Time*2;
NN_Sample_Time = RealSense_Sample_Time*1;
ImageDisplay_Sample_Time = CSI_Sample_Time*6;
LiDAR_Sample_Time = CSI_Sample_Time*3;
Audio_Sample_Time = 0.3;
Initialization_Time = 5; %5 seconds to make sure all systems are good
cameraStepSize = 3e-2;

% Size of lidar capture
SPR_qcar2 = 1000; %Scans per revolution for the LiDAR scan (Long Mode)
SPR_qcar1 = 384; %Scans per revolution for the LiDAR scan (Long Mode)


% define where the calibration was taken from (2 options)
if map_type == 1
    cal_pos = [0, 2, 0] % large map calibration spot
else
    cal_pos = [0, 0, 0] % small map calibration spot
end

% load car sounds
load QCar_Sounds.mat;

%% Gyro KF
GyroKF_sampleTime = 0.001;

GyroKF_X0 = [0;0];
GyroKF_P0 = eye(2);

GyroKF_Q = diag([0.01, 0.001]);
GyroKF_R = 0.01;


%% QCar EKF
QCarEKF_sampleTime = GyroKF_sampleTime;

QCarEKF_L = 0.24;

QcarKF_X0 = [0; 0; 0];
QCarEKF_P0 = eye(3);

QCarEKF_Q = diag([0.00001, 0.00001, 0.00001]);

QCarEKF_R_heading = diag(0.1);
QCarEKF_R_combined = diag([0.1, 0.1, 0.01]);

%% Load Calibration Files

% lidar to map frame rotations
qcar2_lidar_to_map_rotation = 0; % qcar 2 lidar already aligned to map frame
qcar1_lidar_to_map_rotation = pi/2; % qcar 2 lidar already aligned to map frame


% distance and angles need to be loaded from a file based on types of qcars
% reminder: 0 = qcar1, 1 = both, 2 = qcar2
switch qcar_types

    case 0
        % load in dist + angles of lidar
        load distance_new_qcar1.mat;
        load angles_new_qcar1.mat;
        range_qcar1 = distance_new_qcar1(2: length (distance_new_qcar1), width (distance_new_qcar1)-5);
        angles_qcar1 = angles_new_qcar1(2: length (angles_new_qcar1), width (angles_new_qcar1)-5);

        % remove 0's from calib scan (bad readings)
        range_indicies_qcar1 = find(range_qcar1 == 0);
        range_qcar1(range_indicies_qcar1) = [];
        angles_qcar1(range_indicies_qcar1) = [];

    case 1
        load distance_new_qcar1.mat;
        load angles_new_qcar1.mat;
        range_qcar1 = distance_new_qcar1(2: length (distance_new_qcar1), width (distance_new_qcar1)-5);
        angles_qcar1 = angles_new_qcar1(2: length (angles_new_qcar1), width (angles_new_qcar1)-5);
        range_indicies_qcar1 = find(range_qcar1 == 0);
        range_qcar1(range_indicies_qcar1) = [];
        angles_qcar1(range_indicies_qcar1) = [];

        load distance_new_qcar2.mat;
        load angles_new_qcar2.mat;
        range_qcar2 = distance_new_qcar2(2: length (distance_new_qcar2), width (distance_new_qcar2)-5);
        angles_qcar2 = angles_new_qcar2(2: length (angles_new_qcar2), width (angles_new_qcar2)-5);

        range_indicies_qcar2 = find(range_qcar2 == 0);
        range_qcar2(range_indicies_qcar2) = [];
        angles_qcar2(range_indicies_qcar2) = [];

    case 2

        load distance_new_qcar2.mat;
        load angles_new_qcar2.mat;
        range_qcar2 = distance_new_qcar2(2: length (distance_new_qcar2), width (distance_new_qcar2)-5);
        angles_qcar2 = angles_new_qcar2(2: length (angles_new_qcar2), width (angles_new_qcar2)-5);
        range_indicies_qcar2 = find(range_qcar2 == 0);
        range_qcar2(range_indicies_qcar2) = [];
        angles_qcar2(range_indicies_qcar2) = [];

end

%% Load and Plot Paths

% load pre-defined paths
load ("SDCS_Paths_7.mat");

% default map mask to all paths
map_mask = [1 1 1 1 1 1 0];
% if using the small map mask paths
if map_type == 0
    map_mask = [1 1 1 0 0 1 0];
end


% plot calibration scan and paths (calibration is the origin)
figure(1)
hold on;

% if only using qcar 1 plot qcar 1 calibration scan
if qcar_types == 0
    polar(-angles_qcar1-qcar1_lidar_to_map_rotation-1*pi/180, range_qcar1,'k.');

% if using only virtual QCars
elseif qcar_types == 3
    % don't add to the polar plot
    
%if using any qcar 2s, plot using qcar 2 calibration scan
else
    polar(-angles_qcar2-qcar2_lidar_to_map_rotation-1*pi/180, range_qcar2,'k.');

end

% plot all paths
plot (path_x - cal_pos(1), path_y - cal_pos(2));
plot (path_x2 - cal_pos(1), path_y2 - cal_pos(2));
plot (path_x3 - cal_pos(1), path_y3 - cal_pos(2));
plot (path_x4 - cal_pos(1), path_y4 - cal_pos(2));
plot (path_x5 - cal_pos(1), path_y5 - cal_pos(2));
plot (path_x6 - cal_pos(1), path_y6 - cal_pos(2));
plot (path_x7 - cal_pos(1), path_y7 - cal_pos(2));
hold off;
