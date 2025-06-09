close all;
t = commander_data(1,:);

Plot_command = [1;... % P.1 - Pose Plots
                1;... % P.2 - FSM Monitoring Plots
                1;... % P.3 - FSM State Plots
                1];   % P.4 - Unsaturated Controller Commands 

%% FSM Monitor Log (2:21) [20]

% Monitoring signals 
state_prev                  = commander_data(2,:);
initializing                = commander_data(3,:);
optitrack_issue             = commander_data(5,:);
comm_issue                  = commander_data(4,:);
low_battery                 = commander_data(6,:);
arm                         = commander_data(7,:);
cmd_takeoff                 = commander_data(8,:);
estop                       = commander_data(9,:);
joystick_issue              = commander_data(10,:);
throttle_at_trim            = commander_data(11,:);
throttle_near_zero          = commander_data(12,:);
ctrl_throttle_near_zero     = commander_data(13,:);
takeoff_success             = commander_data(14,:);
flying_too_low              = commander_data(15,:);
flying_too_high             = commander_data(16,:);
close_to_ground             = commander_data(17,:);
sensor_failure              = commander_data(18,:);

% FSM States 
state_next                  = commander_data(19,:);
fsm_error                   = commander_data(20,:);
stop_model                  = commander_data(21,:);

%% IF Pose Information (22:29) [8]

% Measured Pose from Optitrack  
IF_Measured_x               = commander_data(22,:);
IF_Measured_y               = commander_data(23,:);
IF_Measured_z               = commander_data(24,:);
IF_Measured_Yaw             = commander_data(25,:);

% Switchbox Conditioned Pose Commands
IF_Desired_x                = commander_data(26,:);
IF_Desired_y                = commander_data(27,:);
IF_Desired_z                = commander_data(28,:);
IF_Desired_Yaw              = commander_data(29,:);


%% Unsaturated Controller Commands (30:33)[4]

ref_roll_unsat              = commander_data(30,:);
ref_pitch_unsat             = commander_data(31,:);
ref_thrust_unsat            = commander_data(32,:);
ref_yaw_unsat               = commander_data(33,:);

%% Saturated Controller Commands (34:37)[4]

ref_Thurst                  = commander_data(34,:);
ref_torque_roll             = commander_data(35,:);
ref_torque_pitch            = commander_data(36,:);
ref_torque_yaw              = commander_data(37,:);


%% Pose Plots

if Plot_command(1)
    figure; 
    subplot(2,2,1);
        hold on;
        plot(t, IF_Measured_x, 'r');
        plot(t, IF_Desired_x, 'b');
        hold off;
        ylabel('X (m)');
        xlabel('time (s)');
        grid on; grid minor;
        legend('Estimated','Commanded');
    subplot(2,2,2);
        hold on;
        plot(t, IF_Measured_y, 'r');
        plot(t, IF_Desired_y, 'b');
        hold off;
        ylabel('Y (m)');
        xlabel('time (s)');
        grid on; grid minor;
        legend('Estimated','Commanded');
    subplot(2,2,3);
        hold on;
        plot(t, IF_Measured_z, 'r');
        plot(t, IF_Desired_z, 'b');
        hold off;
        ylabel('Z (m)');
        xlabel('time (s)');
        grid on; grid minor;
        legend('Estimated','Commanded');
    subplot(2,2,4);
        hold on;
        plot(t, IF_Measured_Yaw.*180/pi, 'r');
        plot(t, IF_Desired_Yaw.*180/pi, 'b');
        hold off;
        ylabel('Yaw (deg)');
        xlabel('time (s)');
        grid on; grid minor;
        legend('Estimated','Commanded');
end

%% FSM Monitoring Plots

if Plot_command(2)
    figure;
    subplot(4,4,1);
        plot(t, initializing);
        grid on; grid minor;
        title('Initializing');

    subplot(4,4,2);
        plot(t, joystick_issue);
        grid on; grid minor;
        title('Joystick Issue');

    subplot(4,4,3);
        plot(t, optitrack_issue);
        grid on; grid minor;
        title('OptiTrack Issue');

    subplot(4,4,4);
        plot(t, comm_issue);
        grid on; grid minor;
        title('Communication Issue with Mission Server');

    subplot(4,4,5);
        plot(t, low_battery);
        grid on; grid minor;
        title('Low Battery');

    subplot(4,4,6);
        plot(t, arm);
        grid on; grid minor;
        title('Arm');

    subplot(4,4,7);
        plot(t, cmd_takeoff);
        grid on; grid minor;
        title('Takeoff');

    subplot(4,4,8);
        plot(t, estop);
        grid on; grid minor;
        title('Emergency Stop');

    subplot(4,4,9);
        plot(t, throttle_at_trim);
        grid on; grid minor;
        title('Commanded Throttle at Trim value');

    subplot(4,4,10);
        plot(t, throttle_near_zero);
        grid on; grid minor;
        title('Commanded Throttle near Zero');

    subplot(4,4,11);
        plot(t, ctrl_throttle_near_zero);
        grid on; grid minor;
        title('Controller Throttle at Zero');

    subplot(4,4,12);
        plot(t, takeoff_success);
        grid on; grid minor;
        title('Takeoff Success');

    subplot(4,4,13);
        plot(t, flying_too_low);
        grid on; grid minor;
        title('Flying Too Low');

    subplot(4,4,14);
        plot(t, flying_too_high);
        grid on; grid minor;
        title('Flying Too High');

    subplot(4,4,15);
        plot(t, close_to_ground);
        grid on; grid minor;
        title('Close To Ground');

    subplot(4,4,16);
        plot(t, sensor_failure);
        grid on; grid minor;
        title('Sensor Failure');
end    

%% FSM State Plots

if Plot_command(3)
    figure;
    hold on;
        plot(t, 0.1.*state_prev, 'r');
        plot(t, 0.1.*state_next, 'b');
        plot(t, fsm_error, 'g');
        plot(t, stop_model, 'k');
        hold off;
        grid on; grid minor;
        title('State Machine Data');
        xlabel('Time (s)');
        legend('Previous State','Next State','Error', 'Stop Model');
end

%% Generalized Controller Commands (Unsaturated)

if Plot_command(4)
    figure
    hold on;
    subplot(2,2,1);
        plot(t,ref_thrust_unsat)     
        grid on; grid minor;
        title('Ref thrust (Unsaturated) ');
        ylabel('N');
    
    subplot(2,2,2);
        plot(t,ref_roll_unsat)     
        grid on; grid minor;
        title('Ref Roll (Unsaturated) ');
        ylabel('rad');
      
    subplot(2,2,3);
        plot(t,ref_pitch_unsat)     
        grid on; grid minor;
        title('Ref Pitch (Unsaturated) ');
        ylabel('rad');
      
    subplot(2,2,4);
        plot(t,ref_yaw_unsat)     
        grid on; grid minor;
        title('Ref Yaw (Unsaturated) ');
        ylabel('rad/s');
end 



