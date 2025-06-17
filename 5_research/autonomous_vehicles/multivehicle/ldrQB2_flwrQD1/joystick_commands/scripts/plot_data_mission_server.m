close all; warning off;
t = mission_server_data(1,:);

Plot_command = [1;... % P.1 - Monitoring Plots
                1];   % P.2 - Position Tracking Plots

%% Data log (2:31) [30]

% Triggers
arm                     = mission_server_data(2,:);
takeoff                 = mission_server_data(3,:);
e_stop                  = mission_server_data(4,:);
Joystick_Issue          = mission_server_data(5,:);

%
% Leader Data - QBot 2/2e
%
% Measured Position
meas_x_leader           = mission_server_data(6,:);
meas_y_leader           = mission_server_data(7,:);
meas_z_leader           = mission_server_data(8,:);

% Measured Orientation
meas_roll_leader        = mission_server_data(9,:);
meas_pitch_leader       = mission_server_data(10,:);
meas_yaw_leader         = mission_server_data(11,:);

% IsTracking?
isTracking_leader       = mission_server_data(12,:);

% Desired Position 
des_v_leader            = mission_server_data(13,:);
des_omega_leader        = mission_server_data(14,:);
des_LED2_leader         = mission_server_data(15,:);
des_dummy_leader        = mission_server_data(16,:);

% Loopback
loopback_time_leader    = mission_server_data(17,:);

% Communication Watchdog 
comm_issue_leader       = mission_server_data(18,:);

%
% Follower Data - QDrone
%
% Measured Position
meas_x_follower         = mission_server_data(19,:);
meas_y_follower         = mission_server_data(20,:);
meas_z_follower         = mission_server_data(21,:);

% Measured Orientation
meas_roll_follower      = mission_server_data(22,:);
meas_pitch_follower     = mission_server_data(23,:);
meas_yaw_follower       = mission_server_data(24,:);

% IsTracking?
isTracking_follower     = mission_server_data(25,:);

% Desired Position 
des_x_follower          = mission_server_data(26,:);
des_y_follower          = mission_server_data(27,:);
des_z_follower          = mission_server_data(28,:);
des_yaw_follower        = mission_server_data(29,:);

% Loopback
loopback_time_follower  = mission_server_data(30,:);

% Communication Watchdog 
comm_issue_follower     = mission_server_data(31,:);


%% P.1 (1 plot) - Monitoring Plots 

if Plot_command(1)
    figure;
    subplot(2,2,1)
        plot(t, arm)
        grid on; grid minor; 
        title('Arm Command');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,2,2)
        plot(t, takeoff)
        grid on; grid minor; 
        title('Take off Command');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,2,3)
        plot(t, e_stop)
        grid on; grid minor; 
        title('Emergency Stop');
        xlabel('Time (s)');
        ylabel('bool');
    subplot(2,2,4)
        plot(t, Joystick_Issue)
        grid on; grid minor; 
        title('Joystick Issue');
        xlabel('Time (s)');
        ylabel('bool');
end

if Plot_command(1)
    figure;
    subplot(3,2,1)
        plot(t, isTracking_leader)
        grid on; grid minor;
        title('isTracking - Leader')
        xlabel('Time(s)')
        ylabel('bool')
    subplot(3,2,2)
        plot(t, loopback_time_leader)
        grid on; grid minor;
        title('Loopback Time - Leader')
        xlabel('Time(s)')
        ylabel('seconds')
    subplot(3,2,3)
        plot(t, comm_issue_leader)
        grid on; grid minor;
        title('Communication Issue - Leader')
        xlabel('Time(s)')
        ylabel('bool')
    subplot(3,2,4)
        plot(t, isTracking_follower)
        grid on; grid minor;
        title('isTracking - Follower')
        xlabel('Time(s)')
        ylabel('bool')
    subplot(3,2,5)
        plot(t, loopback_time_follower)
        grid on; grid minor;
        title('Loopback Time - Follower')
        xlabel('Time(s)')
        ylabel('seconds')
    subplot(3,2,6)
        plot(t, comm_issue_follower)
        grid on; grid minor;
        title('Communication Issue - Follower')
        xlabel('Time(s)')
        ylabel('bool')
end


%% P.2 (1 plot) - Position Tracking Plots 

if Plot_command(2)
    figure; 
    subplot(3,1,1); hold on;
        plot(t, des_v_leader);
        hold off; grid on; grid minor;
        ylabel('m/s'); xlabel('Time (s)'); title('Leader (QBot 2e) Linear Speed Command');

    subplot(3,1,2); hold on;
        plot(t, des_omega_leader.*180/pi);
        hold off; grid on; grid minor;
        ylabel('deg/s'); xlabel('Time (s)'); title('Leader (QBot 2e) Angular Speed Command');

    subplot(3,1,3); hold on;
        plot(t, des_LED2_leader);
        hold off; grid on; grid minor;
        ylabel('0 = Green; 1 = Red'); xlabel('Time (s)'); title('Leader (QBot 2e) LED2 Command');

end

if Plot_command(2)
    figure; 
    subplot(2,2,1); hold on; 
        plot(t, des_x_follower, 'b');
        plot(t, meas_x_follower, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('Follower X Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,2); hold on;
        plot(t, des_y_follower, 'b');
        plot(t, meas_y_follower, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('Follower Y Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,3); hold on;
        plot(t, des_z_follower, 'b');
        plot(t, meas_z_follower, 'r');
        hold off; grid on; grid minor;
    ylabel('m'); xlabel('Time (s)'); title('Follower Z Position - Research Studio Frame/Inertial Frame');
    legend('desired','measured');

    subplot(2,2,4); hold on; 
        plot(t, des_yaw_follower, 'b');
        plot(t, meas_yaw_follower, 'r');
        hold off; grid on; grid minor;
    ylabel('rad'); xlabel('Time (s)'); title('Follower Yaw - Research Studio Frame/Inertial Frame');    
    legend('desired','measured');
end


