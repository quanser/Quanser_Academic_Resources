close all; warning off;

% Call a function to parse the stored data
parse_vars_mission_server_2QDrones(data);

% Define which plots to be generated
Plot_command = [ 1 ...  % Position Tracking Plots

                ];

% Specify number of QDrones in the swarm
num_qdrones = 2;

% Define subplot layout depending on number of QDrones in the swarm up to 6
subplot_layout = [  1,1; ...
                    2,1; ...
                    3,1; ...
                    2,2; ...
                    3,2; ...
                    3,2 ];

%% P.1 Position Tracking
    % X Position
    figure;
    for i=1:num_qdrones
        subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
        plot(t,eval(['traj_',num2str(i),'(1,:)']),'b');
        hold on
        plot(t,eval(['pos_',num2str(i),'(1,:)']),'r');
        hold off; grid on; grid minor;
        title(['X Position (m) - Vehicle ', num2str(i)]);
        ylabel('X (m)');
        xlabel('Time (s)');
        legend('Desired', 'Measured');
    end

    % Y Position
    figure;
    for i=1:num_qdrones
        subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
        plot(t,eval(['traj_',num2str(i),'(2,:)']),'b');
        hold on
        plot(t,eval(['pos_',num2str(i),'(2,:)']),'r');
        hold off; grid on; grid minor;
        title(['Y Position (m) - Vehicle ', num2str(i)]);
        ylabel('Y (m)');
        xlabel('Time (s)');
        legend('Desired', 'Measured');
    end

    % Z Position
    figure;
    for i=1:num_qdrones
        subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
        plot(t,eval(['traj_',num2str(i),'(3,:)']),'b');
        hold on
        plot(t,eval(['pos_',num2str(i),'(3,:)']),'r');
        hold off; grid on; grid minor;
        title(['Z Position (m) - Vehicle ', num2str(i)]);
        ylabel('Z (m)');
        xlabel('Time (s)');
        legend('Desired', 'Measured');
    end
%% P.2 Measured Orientation (Roll, Pitch, Yaw)

% Roll
figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,eval(['rot_',num2str(i),'(1,:)']));
    grid on; grid minor;
    title(['Roll (rad) - Vehicle ', num2str(i)]);
    ylabel('Roll (rad)');
    xlabel('Time (s)');
end

% Pitch
figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,eval(['rot_',num2str(i),'(2,:)']));
    grid on; grid minor;
    title(['Pitch (rad) - Vehicle ', num2str(i)]);
    ylabel('Pitch (rad)');
    xlabel('Time (s)');
end

% Yaw
figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,eval(['rot_',num2str(i),'(3,:)']));
    grid on; grid minor;
    title(['Yaw (rad) - Vehicle ', num2str(i)]);
    ylabel('Yaw (rad)');
    xlabel('Time (s)');
end
%% P.3 Tracking Status

figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,is_tracking(i,:));
    grid on; grid minor;
    title(['Tracking Status - Vehicle ', num2str(i)]);
    ylabel('is\_tracking');
    xlabel('Time (s)');
    ylim([-0.1 1.1]);
end
%% Communication Issues
figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,comm_issues(i,:));
    grid on; grid minor;
    title(['Comm Issues  - Vehicle ', num2str(i)]);
    ylabel('Comm Issues');
    xlabel('Time (s)');
    ylim([-0.1 1.1]);
end
%% Loop times
figure;
for i=1:num_qdrones
    subplot(subplot_layout(num_qdrones,1),subplot_layout(num_qdrones,2),i);
    plot(t,loop_times(i,:));
    grid on; grid minor;
    title(['Loop Times  - Vehicle ', num2str(i)]);
    ylabel('Loop Time');
    xlabel('Time (s)');
    ylim([0.0 0.3]);
end

%% P.4 System Status and Trajectory Signals

figure;

% Arm signal
subplot(4,1,1);
stairs(t, arm);
grid on; grid minor;
title('Arm Signal');
ylabel('Arm');
ylim([-0.1 1.1]);
xlabel('Time (s)');

% Takeoff signal
subplot(4,1,2);
stairs(t, takeoff);
grid on; grid minor;
title('Takeoff Signal');
ylabel('Takeoff');
ylim([-0.1 1.1]);
xlabel('Time (s)');

% Trajectory Enable signal
subplot(4,1,3);
stairs(t, traj_enable);
grid on; grid minor;
title('Trajectory Enable Signal');
ylabel('Traj Enable');
ylim([-0.1 1.1]);
xlabel('Time (s)');

% Trajectory Play signal
subplot(4,1,4);
stairs(t, traj_play);
grid on; grid minor;
title('Trajectory Play Signal');
ylabel('Traj Play');
ylim([-0.1 1.1]);
xlabel('Time (s)');