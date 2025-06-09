close all; warning off;

index = 1;

nSize = 1;
t = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;


%% QDrone2 log (2:55) [54]

%IMU_0BF = QDrone_data(index:index+9-1,:);
%index = index + size(IMU_0BF,1);
nSize = 9;
IMU_0BF = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%IMU_1BF = QDrone_data(index:index+9-1,:);
%index = index + size(IMU_1BF,1);
nSize = 9;
IMU_1BF = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%motor_CMD = QDrone_data(index:index+4-1,:);
%index = index + size(motor_CMD,1);
nSize = 4;
motor_CMD = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%battery = QDrone_data(index,:);
%index = index + size(battery,1);
nSize = 1;
battery = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%electronics_current = QDrone_data(index,:);
%index = index + size(electronics_current,1);
nSize = 1;
electronics_current = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%motor_Current = QDrone_data(index,:);
%index = index + size(motor_Current,1);
nSize = 1;
motor_current = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%IMU_0 = QDrone_data(index:index+6-1,:);
%index = index + size(IMU_0,1);
nSize = 6;
IMU_0 = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%IMU_1 = QDrone_data(index:index+6-1,:);
%index = index + size(IMU_1,1);
nSize = 6;
IMU_1 = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%OpticalFlow = QDrone_data(index:index+7-1,:);
%index = index + size(OpticalFlow,1);
nSize = 7;
OpticalFlow = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%range_data = QDrone_data(index,:);
%index = index + size(range_data,1);
nSize = 1;
range_data = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%telemetry = QDrone_data(index:index+8-1,:);
%index = index + size(telemetry,1);
nSize = 8;
telemetry = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%timing = QDrone_data(index:index+2-1,:);
%index = index + size(timing,1);
nSize = 2;
timing = QDrone_data(index:(index+nSize-1),:);
index = index + nSize;

%% Plotting Section

figure(1)
sgtitle('Motor Telemetry')
subplot(2,2,1)
plot(t, telemetry(1,:));
hold on
plot(t, telemetry(2,:));
title('Motor 4 (front left)')
grid on; grid minor ;
subplot(2,2,2)
plot(t, telemetry(3,:));
hold on
plot(t, telemetry(4,:));
title('Motor 2 (front right)')
grid on; grid minor ;
subplot(2,2,3)
plot(t, telemetry(5,:));
hold on
plot(t, telemetry(6,:));
title('Motor 3 (back left)')
grid on; grid minor ;
subplot(2,2,4)
plot(t, telemetry(7,:));
hold on
plot(t, telemetry(8,:));
title('Motor 1 (back right)')
grid on; grid minor ;

figure(2)
sgtitle('IMU 0 Attitude Estimate (rad)')
subplot(1,3,1)
plot(t, IMU_0BF(1,:));
hold on
plot(t, IMU_0BF(2,:));
plot(t, IMU_0BF(3,:));
legend('Roll X','Pitch Y','Yaw Z')
title('Orientation rad')
grid on; grid minor ;
subplot(1,3,2)
plot(t, IMU_0BF(4,:));
hold on
plot(t, IMU_0BF(5,:));
plot(t, IMU_0BF(6,:));
legend('X','Y','Z')
title('Speed rad/s')
grid on; grid minor ;
subplot(1,3,3)
plot(t, IMU_0BF(7,:));
hold on
plot(t, IMU_0BF(8,:));
plot(t, IMU_0BF(9,:));
legend('X','Y','Z')
title('Acceleration rad/s/s')
grid on; grid minor ;

figure(3)
sgtitle('IMU 1 Attitude Estimate (rad)')
subplot(1,3,1)
plot(t, IMU_1BF(1,:));
hold on
plot(t, IMU_1BF(2,:));
plot(t, IMU_1BF(3,:));
legend('Roll X','Pitch Y','Yaw Z')
title('Orientation rad')
grid on; grid minor ;
subplot(1,3,2)
plot(t, IMU_1BF(4,:));
hold on
plot(t, IMU_1BF(5,:));
plot(t, IMU_1BF(6,:));
legend('X','Y','Z')
title('Speed rad/s')
grid on; grid minor ;

subplot(1,3,3)
plot(t, IMU_1BF(7,:));
hold on
plot(t, IMU_1BF(8,:));
plot(t, IMU_1BF(9,:));
legend('X','Y','Z')
title('Acceleration rad/s/s')
grid on; grid minor ;

figure(4)
sgtitle('Optical Flow Data')
subplot(2,1,1)
plot(t, OpticalFlow(1,:));
title('Movement X (px/s)')
grid on; grid minor ;

subplot(2,1,2)
plot(t, OpticalFlow(2,:));
title('Movement Y (px/s)')
grid on; grid minor ;

figure(5)
plot(t, range_data(1,:));
title('Drone Height')
grid on; grid minor ; 

figure(6)
plot(t, battery(1,:));
title('Battery Level (V)')
grid on; grid minor ;

figure(7)
subplot(2,1,1)
plot(t, electronics_current(1,:));
title('Electronics Current')
grid on; grid minor ;
subplot(2,1,2)
plot(t, motor_current(1,:));
title('Motor Current')
grid on; grid minor ;


