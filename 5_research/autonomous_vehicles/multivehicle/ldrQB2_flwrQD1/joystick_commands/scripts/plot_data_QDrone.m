close all;
t = QDrone_data(1,:);

Plot_command = [1;... % P.1 - Reference Commands
                1;... % P.2 - BF Attitude estimates 
                1;... % P.3 - BF Attitude rates estimates 
                1;... % P.4 - BF Attitude acceleration estimates 
                1;... % P.5 - BF MIU Accelerometer Measurements
                1];   % P.6 - QDrone Battery And Sensor Health  



%% Plant log (1:22) [22]

% Motor percentage commands 
Motor1_cmd          = QDrone_data(2,:);
Motor2_cmd          = QDrone_data(3,:);
Motor3_cmd          = QDrone_data(4,:);
Motor4_cmd          = QDrone_data(5,:);


% BF Attitude Estimates, all rates in rad, rad/s or rad/s/s
BF_est_roll         = QDrone_data(6,:);
BF_est_pitch        = QDrone_data(7,:);
BF_est__yaw         = QDrone_data(8,:);
BF_est_roll_rate    = QDrone_data(9,:);
BF_est_pitch_rate   = QDrone_data(10,:);
BF_est_yaw_rate     = QDrone_data(11,:);
BF_est_roll_accel   = QDrone_data(12,:);
BF_est_pitch_accel  = QDrone_data(13,:);
BF_est_yaw_accel    = QDrone_data(14,:);

% DAQ
gyro_x              = QDrone_data(15,:);
gyro_y              = QDrone_data(16,:);
gyro_z              = QDrone_data(17,:);
acc_x               = QDrone_data(18,:);
acc_y               = QDrone_data(19,:);
acc_z               = QDrone_data(20,:);
battery_level       = QDrone_data(21,:);
low_battery         = QDrone_data(22,:);
sensor_issue        = QDrone_data(23,:);


%% Signal conditioning for plots
% Attitude Estimates (rad)
BF_est_roll_deg    = (180/pi).*BF_est_roll;
BF_est_pitch_deg   = (180/pi).*BF_est_pitch;
BF_est_yaw_deg     = (180/pi).*BF_est__yaw;

% Attitude Rate Estimates (rad/s)(HARDWARE FILTERED GYROSCOPE)
BF_est_roll_rate_deg     = (180/pi).*gyro_x;
BF_est_pitch_rate_deg    = (180/pi).*gyro_y;
BF_est_yaw_rate_deg      = (180/pi).*gyro_z;

% Attitude acceleration (rad/s/s) Estimates
BF_est_roll_accel_deg    = (180/pi).*BF_est_roll_accel;
BF_est_pitch_accel_deg   = (180/pi).*BF_est_pitch_accel;
BF_est_yaw_accel_deg     = (180/pi).*BF_est_yaw_accel;

%% P.1 (1 plot) - Reference Commands 

if Plot_command(1)
     figure; title('Motor Commands (Percentage of battery voltage)');
    subplot(4,1,1); 
        plot(t, Motor1_cmd, 'b');
        grid on; grid minor; 
    ylabel('%'); xlabel('Time (s)'); title('Motor 1');

    subplot(4,1,2); 
        plot(t, Motor2_cmd, 'b');
        grid on; grid minor; 
    ylabel('%'); xlabel('Time (s)'); title('Motor 2');

    subplot(4,1,3); 
        plot(t, Motor3_cmd, 'b');
        grid on; grid minor; 
    ylabel('%'); xlabel('Time (s)'); title('Motor 3');

    subplot(4,1,4); 
        plot(t, Motor4_cmd, 'b');
        grid on; grid minor; 
    ylabel('%'); xlabel('Time (s)'); title('Motor 4');
end

%% P.2 (1 plots) - BF Attitude estimates 

if Plot_command(2)
% P.2 Attitude Angle
    figure;title('BF Attitude estimates');
    
    subplot(3,1,1);
        plot(t, BF_est_roll_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('deg');title('Roll Estimates');
    
    subplot(3,1,2);
        plot(t, BF_est_pitch_deg, 'r');
    grid on; grid minor;
    xlabel('Time (s)');ylabel('deg');title('Pitch Estimates'); 
    
    subplot(3,1,3);
        plot(t, BF_est_yaw_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)');ylabel('deg');title('Yaw Estimates');

end

%% P.3 (1 plots) - BF Attitude rate estimates (Gyroscope)

if Plot_command(3)
% P.2 Attitude Angle
    figure;
    title('BF Attitude rate estimates (Gyroscope)');
    
    subplot(3,1,1);
        plot(t, BF_est_roll_rate_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)');ylabel('deg/s');title('Roll Rate Estimates');
    
    subplot(3,1,2);
        plot(t, BF_est_pitch_rate_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)');ylabel('deg/s');title('Pitch Rate Estimates');
    
    subplot(3,1,3);
        plot(t, BF_est_yaw_rate_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)');ylabel('deg/s');title('Yaw Rate Estimates');

end

%% P.4 (1 plots) - BF Attitude Acceleration estimates 

if Plot_command(4)
% P.2 Attitude Angle
    figure;
    title('BF Attitude Acceleration Estimates');
    
    subplot(3,1,1);
        plot(t, BF_est_roll_accel_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('deg/s/s'); title('Pitch Acceleration Estimates');
    
    subplot(3,1,2);
        plot(t, BF_est_pitch_accel_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('deg/s/s'); title('Roll Acceleration Estimates');
    
    subplot(3,1,3);
        plot(t, BF_est_yaw_accel_deg, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('deg/s/s'); title('Yaw Acceleration Estimates');

end

%% P.5 (1 plots) - IMU Accelerometer Measurements
if Plot_command(5)
% P.2 Attitude Angle
    figure;
    title('BF accelerometer measurements');
    subplot(3,1,1);
        plot(t, acc_x, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('m/s/s'); title('BF IMU x-Acceleration');
    
    subplot(3,1,2);
        plot(t, acc_y, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('m/s/s'); title('BF IMU y-Acceleration');
     
    subplot(3,1,3);
        plot(t, acc_z, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('m/s/s'); title('BF IMU z-Acceleration');

end

%% P.6 (2 plots) - QDrone Battery And Sensor Health 

if Plot_command(6)
% P.6.1 Battery Level During Flight
    figure;
        plot(t, battery_level, 'r');
    grid on; grid minor; 
    xlabel('Time (s)'); ylabel('V');title('QDrone Battery Level');
    
% P.6.2 Battery Issue or Sensor Issue
    
    figure;title('Sensor Issues');
        
    subplot(2,1,1);
        plot(t, low_battery, 'r');
    grid on; grid minor;
    ylabel('bool');xlabel('Time (s)');title('Low Battery Detection');
        
    subplot(2,1,2);
        plot(t, sensor_issue, 'r');
    grid on; grid minor; 
    ylabel('bool');xlabel('Time (s)');title('Sensor Health Monitor');
    
    
end
