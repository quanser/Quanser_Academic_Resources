close all;
time = mission_server_data(1,:);

Plot_command = [1;... % P.1 - Reference Commands
                1];   % P.2 - Monitoring

%% Safety log (2:13) [12]

% Emergency Abort Command
arm                 = mission_server_data(2,:);
takeoff_land        = mission_server_data(3,:); % not used in manual flight
emergency_abort     = mission_server_data(4,:);
joystick_issue      = mission_server_data(5,:);

% Throttle
cmd_thrust_throttle = mission_server_data(6,:);

% Attitude Torque
cmd_torque_roll     = mission_server_data(7,:);
cmd_torque_pitch    = mission_server_data(8,:);
cmd_torque_yaw      = mission_server_data(9,:);

% Attitude Commands
cmd_angle_roll      = mission_server_data(10,:);
cmd_angle_pitch     = mission_server_data(11,:);
cmd_angle_yaw       = mission_server_data(12,:);

% Loopback
loopback_time       = mission_server_data(13,:);

% Communication Watchdog 
comm_issue          = mission_server_data(14,:);

%% P.1 (1 plot) - Reference Commands 

if Plot_command(1)
    figure;
    hold on;
        plot(time, cmd_thrust_throttle, 'b');
        plot(time, cmd_torque_roll, 'r');
        plot(time, cmd_torque_pitch, 'g');
        plot(time, cmd_torque_yaw, 'k');
    hold off; grid on; grid minor; 
    legend('Throttle','Roll','Pitch','Yaw');
    title('Reference Torque commands sent to Stabilizer');
    xlabel('Time (s)');
    ylabel('N, Nm');

    figure;
    hold on;
        plot(time, cmd_thrust_throttle, 'b');
        plot(time, cmd_angle_roll, 'r');
        plot(time, cmd_angle_pitch, 'g');
        plot(time, cmd_angle_yaw, 'k');
    hold off; grid on; grid minor; 
    legend('Throttle','Roll','Pitch','Yaw');
    title('Reference Attitude commands sent to Stabilizer');
    xlabel('Time (s)');
    ylabel('N, rad, rad/s');
end

%% P.2 (1 plot) - Monitoring

if Plot_command(2)
    figure; 
    subplot(3,2,1);  
        plot(time, comm_issue, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Communication Issue');

    subplot(3,2,2);
        plot(time, loopback_time, 'b');
        grid on; grid minor;
    ylabel('s'); xlabel('Time (s)'); title('Loopback Time');

    subplot(3,2,3); 
        plot(time, emergency_abort, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Emergency Abort');

    subplot(3,2,4); 
        plot(time, arm, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Arm');    

    subplot(3,2,5); 
        plot(time, takeoff_land, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Takeoff/Land');    

    subplot(3,2,6); 
        plot(time, joystick_issue, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Joystick Issue');
end

