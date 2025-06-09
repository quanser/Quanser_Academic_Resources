close all;
t = QBot2e_Stablizer(1,:);

Plot_command = [1 ...  % P.1 - States
                ];

%% Status signals (2:5) [4]

% Battery level
battery_level   = QBot2e_Stabilizer(2,:);

% Rate estimates
BF_est_linear_speed     = QBot2e_Stabilizer(3,:);
BF_est_angular_speed    = QBot2e_Stabilizer(4,:);

% gyro rate
gyro_yaw                = QBot2e_Stabilizer(5,:);

%% P.1 (1 plot) - Status signals

if Plot_command(1)
    figure;
    subplot(2,2,1);
        plot(t, battery_level); grid on; grid minor;
        ylabel('V'); xlabel('Time (s)');
        title('Battery Voltage');

    subplot(2,2,2);
        plot(t, BF_est_linear_speed); grid on; grid minor;
        ylabel('m/s'); xlabel('Time (s)');
        title('Estimated Linear Speed');

    subplot(2,2,3);
        plot(t, BF_est_angular_speed.*180/pi); grid on; grid minor;
        ylabel('deg/s'); xlabel('Time (s)');
        title('Estimated Linear Speed');

    subplot(2,2,4);
        plot(t, gyro_yaw.*180/pi); grid on; grid minor;
        ylabel('deg/s'); xlabel('Time (s)');
        title('Estimated Gyro Yaw Rate');
end
