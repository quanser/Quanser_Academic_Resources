close all; warning off;
t = mission_server_data(1,:);

Plot_command = [1;... % P.1 - Monitoring Plots
                1];   % P.2 - Position Tracking Plots

%% Safety log (2:13) [12]

% Desired Position 
des_x               = mission_server_data(2,:);
des_y               = mission_server_data(3,:);
des_z               = mission_server_data(4,:);
des_yaw             = mission_server_data(5,:);

% Measured Position
meas_x              = mission_server_data(6,:);
meas_y              = mission_server_data(7,:);
meas_z              = mission_server_data(8,:);

% Measured Orientation
meas_roll           = mission_server_data(9,:);
meas_pitch          = mission_server_data(10,:);
meas_yaw            = mission_server_data(11,:);

% Tracking information
istracking          = mission_server_data(12,:);

% Loopback
loopback_time       = mission_server_data(13,:);

% Communication Watchdog 
comm_issue          = mission_server_data(14,:);

% Triggers
arm                 = mission_server_data(15,:);
takeoff             = mission_server_data(16,:);
e_stop              = mission_server_data(17,:);

%% P.1 (1 plot) - Monitoring Plots 

if Plot_command(1)
    figure;
    subplot(2,3,1)
        plot(t, arm)
        grid on; grid minor; 
        title('Arm Command');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,3,2)
        plot(t, takeoff)
        grid on; grid minor; 
        title('Take off Command');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,3,3)
        plot(t, e_stop)
        grid on; grid minor; 
        title('Emergency Stop');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,3,4)
        plot(t, istracking)
        grid on; grid minor; 
        title('Tracking signal from Optitrack');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,3,5)
        plot(t, loopback_time)
        grid on; grid minor; 
        title('Loopback Time');
        xlabel('Time (s)');
        ylabel('s');
    subplot(2,3,6)
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

