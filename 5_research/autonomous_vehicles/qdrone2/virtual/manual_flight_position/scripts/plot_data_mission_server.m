close all; warning off;

index = 1;

%t = mission_server_data(1,:);
nSize = 1;
t = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

Plot_command = [1;... % P.1 - Monitoring Plots
                1];   % P.2 - Position Tracking Plots

%% Safety log (2:18) [17]

% Desired Position 
%des_x               = mission_server_data(2,:);
nSize = 1;
des_x = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%des_y               = mission_server_data(3,:);
nSize = 1;
des_y = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%des_z               = mission_server_data(4,:);
nSize = 1;
des_z = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%des_yaw             = mission_server_data(5,:);
nSize = 1;
des_yaw = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

% Measured Position
%meas_x              = mission_server_data(6,:);
nSize = 1;
meas_x = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%meas_y              = mission_server_data(7,:);
nSize = 1;
meas_y = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%meas_z              = mission_server_data(8,:);
nSize = 1;
meas_z = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;


% Measured Orientation
%meas_roll           = mission_server_data(9,:);
nSize = 1;
meas_roll = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%meas_pitch          = mission_server_data(10,:);
nSize = 1;
meas_pitch = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%meas_yaw            = mission_server_data(11,:);
nSize = 1;
meas_yaw = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;


% Tracking information
%istracking          = mission_server_data(12,:);
nSize = 1;
is_tracking = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;


% Loopback
%loopback_time       = mission_server_data(13,:);
nSize = 1;
loopback_time = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;


% Communication Watchdog 
%comm_issue          = mission_server_data(14,:);
nSize = 1;
comm_issue = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;


% Triggers
%arm                 = mission_server_data(15,:);
nSize = 1;
arm = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%takeoff             = mission_server_data(16,:);
nSize = 1;
takeoff = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%e_stop              = mission_server_data(17,:);
nSize = 1;
e_stop = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%joystick_issue      = mission_server_data(18,:);
nSize = 1;
joystick_issue = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

% Flight Plan data
nSize = 1;
Flight_Plan = mission_server_data(index:(index+nSize-1),:);
index = index + nSize;

%% P.1 (2 plot) - Monitoring Plots 

if Plot_command(1)

    % Joystick and Mission Plan
    figure;
    subplot(1,2,1)
        plot(t, Flight_Plan)
        grid on; grid minor; 
        title('Flight Plan Status');
        xlabel('Time (s)');
        ylabel('State');
    subplot(1,2,2)
        plot(t, joystick_issue)
        grid on; grid minor; 
        title('Joystick Issue');
        xlabel('Time (s)');
        ylabel('bool');

    % Various Status
    figure;
    subplot(3,1,1)
        plot(t, is_tracking)
        grid on; grid minor; 
        title('Tracking signal from Optitrack');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(3,1,2)
        plot(t, loopback_time)
        grid on; grid minor; 
        title('Loopback Time');
        xlabel('Time (s)');
        ylabel('s');
    subplot(3,1,3)
        plot(t, comm_issue)
        grid on; grid minor; 
        title('Communication Issue');
        xlabel('Time (s)');
        ylabel('bool');
end

%% P.2 (1 plot) - Position Tracking Plots 

if Plot_command(2)
    figure; 
    subplot(2,2,1); hold on; 
        plot(t, des_x, 'b');
        plot(t, meas_x, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('X Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,2); hold on;
        plot(t, des_y, 'b');
        plot(t, meas_y, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('Y Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,3); hold on;
        plot(t, des_z, 'b');
        plot(t, meas_z, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('Z Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,4); hold on; 
        plot(t, des_yaw, 'b');
        plot(t, meas_yaw, 'r');
        hold off; grid on; grid minor;
    ylabel('rad'); xlabel('Time (s)'); title('Yaw - Research Studio Frame/Inertial Frame');    
    legend('desired','measured');
end

