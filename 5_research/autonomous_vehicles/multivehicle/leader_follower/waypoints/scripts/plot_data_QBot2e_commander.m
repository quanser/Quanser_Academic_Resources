close all;
t = QBot2e_Commander(1,:);

Plot_command = [ 1 ... % P.1 - State Plot
                 2 ... % P.2 - Command Plots
                 3 ... % P.3 - Tracking Plots
               ; ];


%% FSM State (2) [1]
state   = QBot2e_Commander(2,:);

%% QBot 2e command - Mode 1 (Sequential) (3:4) [2]
cmd_v_mode_1        = QBot2e_Commander(3,:);
cmd_omega_mode_1    = QBot2e_Commander(4,:);

%% QBot 2e command - Mode 2 (Simultaneous) (5:6) [2]
cmd_v_mode_2        = QBot2e_Commander(5,:);
cmd_omega_mode_2    = QBot2e_Commander(6,:);

%% QBot 2e desired pose (7:10) [4]
cmd_x               = QBot2e_Commander(7,:);
cmd_y               = QBot2e_Commander(8,:);
cmd_dummy_z         = QBot2e_Commander(9,:);
cmd_dummy_heading   = QBot2e_Commander(10,:);

%% QBot 2e measured pose (11:14) [4]
meas_x              = QBot2e_Commander(11,:);
meas_y              = QBot2e_Commander(12,:);
meas_z              = QBot2e_Commander(13,:);
meas_heading        = QBot2e_Commander(14,:);


%% State Plot

if Plot_command(1)
    figure;
    plot(t,state);
    ylabel('QBot 2e State');
    xlabel('time(s)');
    grid on; grid minor;
end

%% Command Plots

if Plot_command(2)
    figure;
    subplot(2,2,1);
        plot(t, cmd_v_mode_1);
        ylabel('Linear Velocity Command (m/s) - Mode 1 (Sequential)');
        xlabel('time(s)');
        grid on; grid minor;
    subplot(2,2,2);
        plot(t, cmd_omega_mode_1);
        ylabel('Angular Velocity Command (rad/s) - Mode 1 (Sequential)');
        xlabel('time(s)');
        grid on; grid minor;
    subplot(2,2,3);
        plot(t, cmd_v_mode_2);
        ylabel('Linear Velocity Command (m/s) - Mode 2 (Simultaneous)');
        xlabel('time(s)');
        grid on; grid minor;
    subplot(2,2,4);
        plot(t, cmd_omega_mode_2);
        ylabel('Angular Velocity Command (rad/s) - Mode 2 (Simultaneous)');
        xlabel('time(s)');
        grid on; grid minor;
end

%% Tracking Plots

if Plot_command(3)
    figure;
    subplot(2,1,1);
        hold on;
        plot(t,meas_x,'r');
        plot(t,cmd_x,'b');
        hold off;
        ylabel('X Position Tracking');
        xlabel('time(s)');
        grid on; grid minor;
        legend('Measured','Commanded');
    subplot(2,1,2);
        hold on;
        plot(t,meas_y,'r');
        plot(t,cmd_y,'b');
        hold off;
        ylabel('Y Position Tracking');
        xlabel('time(s)');
        grid on; grid minor;
        legend('Measured','Commanded');
end

