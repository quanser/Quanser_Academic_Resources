clc ; close all; clear all 

%% Load all the data motor prop data
% 7 inch data 
load('BrotherHobby_7inch.mat')


%% Data Parsing 

ESC_signal = HQ(:,2);
Motor_torque = -1*HQ(:,6);
Propeller_Thrust = -1*HQ(:,7);
Battery_Voltage = HQ(:,8);


%% Total Battery and ESC relationship (Dutty Cycle)
Percentage_CMD = (ESC_signal-1000)./1000;
%Predicted Battery CMD 
Volt_CMD_Pred = Battery_Voltage.*Percentage_CMD;


%% Thrust fitting
K_T = polyfit(Volt_CMD_Pred,Propeller_Thrust,2) 
Thrust_pred = zeros(size(Propeller_Thrust));
Thrust_pred = K_T(1).*Volt_CMD_Pred.^2+K_T(2).*Volt_CMD_Pred+K_T(3).*ones(size(Propeller_Thrust));
K_Tau = polyfit(Motor_torque,Propeller_Thrust,1)




%% Reverse, given throttle what should ESC signal be? 
T = linspace(0,max(Propeller_Thrust),100);
Volt_CMD_Theo = -0.5*K_T(2)/K_T(1)+ sqrt(K_T(2)^2-4*K_T(1)*(K_T(3)-T))/(2*K_T(1));

%% Data plotting 
figure(1)
hold on
plot( Volt_CMD_Pred, Propeller_Thrust)
plot( Volt_CMD_Pred, Thrust_pred)
hold off
legend('Measured','Predicted')
title('Volt CMD Pred Vs Propeller Thrust')
xlabel('Volt CMD Pred');ylabel('Thrust (N)')
grid on; grid minor

figure(2)
plot(Volt_CMD_Theo, T)
title('Volt CMD Theo Vs Propeller Thrust')
xlabel('Volt CMD Theo');ylabel('Thrust (N)')
grid on; grid minor


figure(3)
plot(Motor_torque,Propeller_Thrust)
title('Motor torque Vs Propeller Thrust')
xlabel('Torque (N.m)');ylabel('Thrust (N)')
grid on; grid minor

figure(4) 
plot(Percentage_CMD,Battery_Voltage);
title('Percentage CMD Vs Battery Voltage')
xlabel('Percentage CMD ');ylabel('Battery Voltage (V)')
grid on; grid minor
