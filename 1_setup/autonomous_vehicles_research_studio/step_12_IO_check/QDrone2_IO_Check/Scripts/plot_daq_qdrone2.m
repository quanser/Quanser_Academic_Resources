%close all
%clc

index = 1;

times = QDrone_data(index,:);
index = index + size(times,1);

IMU_0BF = QDrone_data(index:index+9-1,:);
index = index + size(IMU_0BF,1);

IMU_1BF = QDrone_data(index:index+9-1,:);
index = index + size(IMU_1BF,1);

motor_CMD = QDrone_data(index:index+4-1,:);
index = index + size(motor_CMD,1);

battery = QDrone_data(index,:);
index = index + size(battery,1);

electronics_current = QDrone_data(index,:);
index = index + size(electronics_current,1);

motor_Current = QDrone_data(index,:);
index = index + size(motor_Current,1);

IMU_0 = QDrone_data(index:index+6-1,:);
index = index + size(IMU_0,1);

IMU_1 = QDrone_data(index:index+6-1,:);
index = index + size(IMU_1,1);

OpticalFlow = QDrone_data(index:index+7-1,:);
index = index + size(OpticalFlow,1);

range_data = QDrone_data(index,:);
index = index + size(range_data,1);

telemetry = QDrone_data(index:index+8-1,:);
index = index + size(telemetry,1);

timing = QDrone_data(index:index+2-1,:);
index = index + size(timing,1);

figure(1)
sgtitle('Motor Telemetry')
subplot(2,2,1)
plot(times, telemetry(1,:));
hold on
plot(times, telemetry(2,:));
title('Motor 4 (front left)')
subplot(2,2,2)
plot(times, telemetry(3,:));
hold on
plot(times, telemetry(4,:));
title('Motor 2 (front right)')
subplot(2,2,3)
plot(times, telemetry(5,:));
hold on
plot(times, telemetry(6,:));
title('Motor 3 (back left)')
subplot(2,2,4)
plot(times, telemetry(7,:));
hold on
plot(times, telemetry(8,:));
title('Motor 1 (back right)')

figure(2)
sgtitle('IMU 0 Attitude Estimate (rad)')
subplot(1,3,1)
plot(times, IMU_0BF(1,:));
hold on
plot(times, IMU_0BF(2,:));
plot(times, IMU_0BF(3,:));
legend('Roll X','Pitch Y','Yaw Z')
title('Orientation rad')
subplot(1,3,2)
plot(times, IMU_0BF(4,:));
hold on
plot(times, IMU_0BF(5,:));
plot(times, IMU_0BF(6,:));
legend('X','Y','Z')
title('Speed rad/s')
subplot(1,3,3)
plot(times, IMU_0BF(7,:));
hold on
plot(times, IMU_0BF(8,:));
plot(times, IMU_0BF(9,:));
legend('X','Y','Z')
title('Acceleration rad/s/s')

figure(3)
sgtitle('IMU 1 Attitude Estimate (rad)')
subplot(1,3,1)
plot(times, IMU_1BF(1,:));
hold on
plot(times, IMU_1BF(2,:));
plot(times, IMU_1BF(3,:));
legend('Roll X','Pitch Y','Yaw Z')
title('Orientation rad')
subplot(1,3,2)
plot(times, IMU_1BF(4,:));
hold on
plot(times, IMU_1BF(5,:));
plot(times, IMU_1BF(6,:));
legend('X','Y','Z')
title('Speed rad/s')
subplot(1,3,3)
plot(times, IMU_1BF(7,:));
hold on
plot(times, IMU_1BF(8,:));
plot(times, IMU_1BF(9,:));
legend('X','Y','Z')
title('Acceleration rad/s/s')

figure(4)
sgtitle('Optical Flow Data')
subplot(2,1,1)
plot(times, OpticalFlow(1,:));
title('Movement X (px/s)')
subplot(2,1,2)
plot(times, OpticalFlow(2,:));
title('Movement Y (px/s)')

figure(5)
plot(times, range_data(1,:));
title('Drone Height')

figure(6)
plot(times, battery(1,:));
title('Battery Level (V)')

figure(7)
subplot(2,1,1)
plot(times, electronics_current(1,:));
title('Electronics Current')
subplot(2,1,2)
plot(times, motor_Current(1,:));
title('Motor Current')



