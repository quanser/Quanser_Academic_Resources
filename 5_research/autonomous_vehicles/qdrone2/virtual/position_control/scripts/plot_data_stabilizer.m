close all;

index = 1;

nSize = 1;
t = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

Plot_command = [1;... % P.1 - Reference Commands
                1;... % P.2 - Connection Issues
                1];   % P.3 - Sample and Computation Time

%% Safety log (2:6) [5]

%sample_time                 = stabilizer_data(2,:);
nSize = 1;
sample_time = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%computation_time            = stabilizer_data(3,:);
nSize = 1;
computation_time = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%stop_model                  = stabilizer_data(4,:);
nSize = 1;
stop_model = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%comm_issue                  = stabilizer_data(5,:);
nSize = 1;
comm_issue = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%watchdog_issue              = stabilizer_data(6,:);
nSize = 1;
watchdog_issue = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%% Mode (7) [1] 

%flight_mode                 = stabilizer_data(7,:);
nSize = 1;
flight_mode = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%% Controller log (8:20) [14]

% Throttle
nSize = 1;
cmd_throttle = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

% Attitude Commands
%cmd_angle_roll              = stabilizer_data(8,:);
nSize = 1;
cmd_angle_roll = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%cmd_angle_pitch             = stabilizer_data(9,:);
nSize = 1;
cmd_angle_pitch = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%cmd_angle_yaw               = stabilizer_data(10,:);
nSize = 1;
cmd_angle_yaw = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

% Attitude Torques
%cmd_torque_roll             = stabilizer_data(11,:);
nSize = 1;
cmd_torque_roll = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%cmd_torque_pitch            = stabilizer_data(12,:);
nSize = 1;
cmd_torque_pitch = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%cmd_torque_yaw              = stabilizer_data(13,:);
nSize = 1;
cmd_torque_yaw = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

% Controller Output Torque
%ctrl_torque_roll_unsat      = stabilizer_data(14,:); 
nSize = 1;
ctrl_torque_roll_unsat = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%ctrl_torque_pitch_unsat     = stabilizer_data(15,:);
nSize = 1;
ctrl_torque_pitch_unsat = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%ctrl_torque_yaw_unsat       = stabilizer_data(16,:);
nSize = 1;
ctrl_torque_yaw_unsat = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

% Generatlized Force
%cmd_thrust_throttle         = stabilizer_data(17,:); 
nSize = 1;
cmd_thrust_throttle = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%net_torque_roll             = stabilizer_data(18,:); 
nSize = 1;
net_torque_roll = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%net_torque_pitch            = stabilizer_data(19,:); 
nSize = 1;
net_torque_pitch = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;

%net_torque_yaw              = stabilizer_data(20,:); 
nSize = 1;
net_torque_yaw = stabilizer_data(index:(index+nSize-1),:);
index = index + nSize;



%% P.1 (1 plot) - Reference Commands 

if Plot_command(1)
    figure;
    hold on;
        plot(t, cmd_thrust_throttle, 'b');
        plot(t, cmd_torque_roll, 'r');
        plot(t, cmd_torque_pitch, 'g');
        plot(t, cmd_torque_yaw, 'k');
    hold off; grid on; grid minor; 
    legend('Throttle','Roll','Pitch','Yaw');
    title('Reference Torque commands received by Stabilizer (Unsaturated)');
    xlabel('Time (s)');
    ylabel('N, Nm');

    figure;
    hold on;
        plot(t, cmd_thrust_throttle, 'b');
        plot(t, cmd_angle_roll, 'r');
        plot(t, cmd_angle_pitch, 'g');
        plot(t, cmd_angle_yaw, 'k');
    hold off; grid on; grid minor; 
    legend('Throttle','Roll','Pitch','Yaw');
    title('Reference Attitude commands received by Stabilizer');
    xlabel('Time (s)');
    ylabel('N, rad, rad/s');

    figure;
    hold on;
        plot(t, cmd_thrust_throttle, 'b');
        plot(t, net_torque_roll, 'r');
        plot(t, net_torque_pitch, 'g');
        plot(t, net_torque_yaw, 'k');
    hold off; grid on; grid minor; 
    legend('Throttle','Roll','Pitch','Yaw');
    title('Generalized Force Command  ');
    xlabel('Time (s)');
    ylabel('N, Nm');
end


%% P.2 (1 plot) - Connection Issues

if Plot_command(2)
    figure; 
    subplot(3,1,1);  
        plot(t, comm_issue, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Communication Issue');

    subplot(3,1,2); 
        plot(t, stop_model, 'b');
        grid on; grid minor;
    ylabel('bool'); xlabel('Time (s)'); title('Stop Model');
    
    subplot(3,1,3); 
        plot(t, watchdog_issue, 'b');
        grid on; grid minor; 
    ylabel('bool'); xlabel('Time (s)'); title('Watchdog timeout');
    
end

%% P.3 (1 plot) - Sample and Computation Time

if Plot_command(3)
    figure;
    hold on;
        plot(t, sample_time, 'b');
        plot(t, computation_time, 'r');
    hold off; grid on; grid minor; 
    legend('Sample Time','Computation Time');
    title('Model Sample and Computation Time');
    xlabel('Time (s)');
    ylabel('s');
end


