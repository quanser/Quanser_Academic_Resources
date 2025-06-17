close all; warning off;

% Call a function to parse the stored data
parse_vars_mission_server_6QDrones(mission_server_data);

% Define which plots to be generated
Plot_command = [ 1 ...  % Position Tracking Plots

                ];

% Specify number of QDrones in the swarm
num_qdrones = 6;

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
