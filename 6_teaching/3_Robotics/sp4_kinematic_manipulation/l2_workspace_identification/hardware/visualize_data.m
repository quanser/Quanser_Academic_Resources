% Close existing figures and load data into workspace
clear
close all;
load('position.mat');

% Initialize data vectors
t = p(1,:);
x = p(2,:);
y = p(3,:);
z = p(4,:);

% First Figure: 3D Workspace Display
figure('Name', 'QArm Workspace');
hold on;
    % Plot the entire end-effector trajectory
    plot3(x, y, z, 'b');
    % Mark the last position with a red X
    plot3(x(end), y(end), z(end), 'rX');
    % Mark the first position with a green X
    plot3(x(1), y(1), z(1), 'gX');
hold off;
grid on;
grid minor;
title('QArm Workspace');
xlabel('X (m)');
ylabel('Y (m)');
zlabel('Z (m)');

% Second Figure: Trajectory over time
figure('Name', 'End-effector Trajectory');
hold on;
    plot(t, x, 'b');
    plot(t, y, 'r');
    plot(t, z, 'g');
hold off;
grid on;
grid minor;
title('QArm End-Effector Position');
xlabel('time (s)');
ylabel('value (m)');
legend('X', 'Y', 'Z');