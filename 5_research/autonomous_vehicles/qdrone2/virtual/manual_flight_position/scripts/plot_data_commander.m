close all;

index = 1;

nSize = 1;
t = commander_data(index:(index+nSize-1),:);
index = index + nSize;

Plot_command = [1;... % P.1 - Pose Plots
                1;... % P.2 - FSM Monitoring Plots
                1;... % P.3 - FSM State Plots
                1];   % P.4 - Unsaturated Controller Commands 

%% FSM Monitor Log (2:21) [20]

% Monitoring signals 
%state_prev                  = commander_data(2,:);
nSize = 1;
state_prev = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%initializing                = commander_data(3,:);
nSize = 1;
initializing = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%comm_issue                  = commander_data(4,:);
nSize = 1;
comm_issue = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%optitrack_issue             = commander_data(5,:);
nSize = 1;
optitrack_issue = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%low_battery                 = commander_data(6,:);
nSize = 1;
low_battery = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%arm                         = commander_data(7,:);
nSize = 1;
arm = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%cmd_takeoff                 = commander_data(8,:);
nSize = 1;
cmd_takeoff = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%estop                       = commander_data(9,:);
nSize = 1;
estop = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%joystick_issue              = commander_data(10,:);
nSize = 1;
joystick_issue = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%throttle_at_trim            = commander_data(11,:);
nSize = 1;
throttle_at_trim = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%throttle_near_zero          = commander_data(12,:);
nSize = 1;
throttle_near_zero = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ctrl_throttle_near_zero     = commander_data(13,:);
nSize = 1;
ctrl_throttle_near_zero = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%takeoff_success             = commander_data(14,:);
nSize = 1;
takeoff_success = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%flying_too_low              = commander_data(15,:);
nSize = 1;
flying_too_low = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%flying_too_high             = commander_data(16,:);
nSize = 1;
flying_too_high = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%close_to_ground             = commander_data(17,:);
nSize = 1;
close_to_ground = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%sensor_failure              = commander_data(18,:);
nSize = 1;
sensor_failure = commander_data(index:(index+nSize-1),:);
index = index + nSize;

% FSM States 
%state_next                  = commander_data(19,:);
nSize = 1;
state_next = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%fsm_error                   = commander_data(20,:);
nSize = 1;
fsm_error = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%stop_model                  = commander_data(21,:);
nSize = 1;
stop_model = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%% IF Pose Information (22:29) [8]

% Measured Pose from Optitrack  
%IF_Measured_x               = commander_data(22,:);
nSize = 1;
IF_Measured_x = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Measured_y               = commander_data(23,:);
nSize = 1;
IF_Measured_y = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Measured_z               = commander_data(24,:);
nSize = 1;
IF_Measured_z = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Measured_Yaw             = commander_data(25,:);
nSize = 1;
IF_Measured_Yaw = commander_data(index:(index+nSize-1),:);
index = index + nSize;

% Switchbox Conditioned Pose Commands
%IF_Desired_x                = commander_data(26,:);
nSize = 1;
IF_Desired_x = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Desired_y                = commander_data(27,:);
nSize = 1;
IF_Desired_y = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Desired_z                = commander_data(28,:);
nSize = 1;
IF_Desired_z = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%IF_Desired_Yaw              = commander_data(29,:);
nSize = 1;
IF_Desired_Yaw = commander_data(index:(index+nSize-1),:);
index = index + nSize;


%% Unsaturated Controller Commands (30:33)[4]

%ref_roll_unsat              = commander_data(30,:);
nSize = 1;
ref_roll_unsat = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_pitch_unsat             = commander_data(31,:);
nSize = 1;
ref_pitch_unsat = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_thrust_unsat            = commander_data(32,:);
nSize = 1;
ref_thrust_unsat = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_yaw_unsat               = commander_data(33,:);
nSize = 1;
ref_yaw_unsat = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%% Saturated Controller Commands (34:37)[4]

%ref_Thrust                  = commander_data(34,:);
nSize = 1;
ref_Thrust = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_torque_roll             = commander_data(35,:);
nSize = 1;
ref_torque_roll = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_torque_pitch            = commander_data(36,:);
nSize = 1;
ref_torque_pitch = commander_data(index:(index+nSize-1),:);
index = index + nSize;

%ref_torque_yaw              = commander_data(37,:);
nSize = 1;
ref_torque_yaw = commander_data(index:(index+nSize-1),:);
index = index + nSize;


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



