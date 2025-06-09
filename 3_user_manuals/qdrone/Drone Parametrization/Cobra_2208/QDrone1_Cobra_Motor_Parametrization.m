clc; clear; close all; 
format long;

%% Load data files 
load('Cobra_data.mat')

% Motor Data:
Cobra_2208_Kv = 2000; % Ideal motor KV value
Cobra_2208_ESC_signal = ESC_data;
Cobra_2208_Motor_torque = Torque_data;
Cobra_2208_Propeller_Thrust = Thrust_data;
Cobra_2208_Battery_Voltage = Cobra2208_2000Kv.VoltageV(:,1);
Cobra_2208_Motor_Speed = Speed_data*60/(2*pi); %RPM
Cobra_2208_Motor_Current = Cobra2208_2000Kv.CurrentA;

%% QDrone System parameters:

M_b = 0.267; % mass of battery
M_d = 0.854; % mass of drone
M = M_b + M_d; % total mass of drone
lin_hover_trim = 0.61698; % hover trim (motor command)which is about 2.7N @7.774V
g = 9.81; % acceleration due to gravity
L_roll = 0.2136; % roll motor to motor distance
L_pitch = 0.1758; % pitch motor to motor distance
kt = 60/(2*pi*Cobra_2208_Kv); % motor torque constant Nm/A
kv = Cobra_2208_Kv*(2*pi/60); % motor speed constant rad/sV
Ahover = 5.7856; % maximum motor current at 100% throttle
Jxx = 0.0100000; % kg*m^2
Jyy = 0.0082000; % kg*m^2
Jzz = 0.0148000; % kg*m^2
Vd = 12.6; % maximum battery voltage in Volts

disp("********************************************************************");
disp("************************** Linear Mapping **************************");
disp('Kf in N'); Kf = M*g/(4*lin_hover_trim); disp(Kf);
disp('Kt in Nm'); Kt = kt*Ahover/lin_hover_trim; disp(Kt);

m_to_F = [   Kf           ,   Kf           ,   Kf           ,   Kf           ;...
            -Kf*L_roll/2  ,  -Kf*L_roll/2  ,   Kf*L_roll/2  ,   Kf*L_roll/2  ;...
             Kf*L_pitch/2 ,  -Kf*L_pitch/2 ,   Kf*L_pitch/2 ,  -Kf*L_pitch/2 ;...
             Kt           ,  -Kt           ,  -Kt           ,   Kt           ];
display(m_to_F);

F_to_m = [   1/(4*Kf) ,  -1/(2*Kf*L_roll) ,  1/(2*Kf*L_pitch) ,  1/(4*Kt)  ;...
              1/(4*Kf) ,  -1/(2*Kf*L_roll) , -1/(2*Kf*L_pitch) , -1/(4*Kt)  ;...
              1/(4*Kf) ,   1/(2*Kf*L_roll) ,  1/(2*Kf*L_pitch) , -1/(4*Kt)  ;...
              1/(4*Kf) ,   1/(2*Kf*L_roll) , -1/(2*Kf*L_pitch) ,  1/(4*Kt) ];

Force_Hover = M*g;
display('Force for hover is:'); display(Force_Hover);

Forces = m_to_F*[1; 1; 1; 1];
disp('Maximum Linear Thrust (N) = '); display(Forces(1));

Forces = m_to_F*[0; 0; 1; 1];
disp('Maximum Linear Roll Torque (Nm) = '); display(Forces(2));

Forces = m_to_F*[1; 0; 1; 0];
disp('Maximum Linear Pitch Torque (Nm) = '); display(Forces(3));

Forces = m_to_F*[1; 0; 0; 1];
disp('Maximum Linear Yaw Torque (Nm) = '); display(Forces(4));

disp('Linear hover trim (%) = '); disp(lin_hover_trim);


% Motors 1-4 get equal commands from 0 to 1 (0 to 100%)
Command_Range  = linspace(0,1,100)';
Motor_Commands = ones(length(Command_Range), 4);
Motor_Commands = Motor_Commands.*Command_Range;
F = Motor_Commands*m_to_F;
F_net = sum(F,2);

% For plotting hover command:
F_Hover = ones(100,4).*lin_hover_trim*m_to_F;
F_Hover = sum(F_Hover,2);

%% Total Battery and ESC relationship (Dutty Cycle)

% Cobra motor data
Cobra_2208_Percentage_CMD = (Cobra_2208_ESC_signal-1000)./1000;
%Predicted Battery CMD 
Cobra_2208_Volt_CMD_Pred = Cobra_2208_Battery_Voltage.*Cobra_2208_Percentage_CMD;


%% Thrust fitting

% Cobra motor data
Cobra_2208_Thrust_param = polyfit(Cobra_2208_Motor_Speed,Cobra_2208_Propeller_Thrust,2);

% Constants described in non-linear mapping for equation 8:
Ct = Cobra_2208_Thrust_param(1);
wf = Cobra_2208_Thrust_param(2)/(2*Ct);
Fb = Cobra_2208_Thrust_param(3)-Ct*wf^2;

% Omega offset: 
wc = sqrt(-Fb/Ct)-wf;

% Used to calculate thrust from a series of angular rate commands
Cobra_Thrust_pred = zeros(size(Cobra_2208_Propeller_Thrust));
Motor_Speed_Command = linspace(0,max(Cobra_2208_Motor_Speed),100);
Cobra_Thrust_pred = Ct.*(Motor_Speed_Command+wf).^2+Fb;


% linear fit for motor speed vs voltage:
Cobra_2208_Thrust_linear = polyfit(Cobra_2208_Volt_CMD_Pred,Cobra_2208_Motor_Speed,1);
Kv_eff = Cobra_2208_Thrust_linear(1);
Omega_linear = Cobra_2208_Volt_CMD_Pred*Kv_eff +wc;
Omega_points = zeros(size(Cobra_2208_Volt_CMD_Pred));
Omega_points = Kv_eff.*Cobra_2208_Volt_CMD_Pred+wc;

% Motor torque linear fit: 
Cobra_2208_K_Tau = polyfit(Cobra_2208_Motor_torque, Cobra_2208_Propeller_Thrust,1);
k_tau = Cobra_2208_K_Tau(1);
Torque_CMD = linspace(0,Cobra_2208_Motor_torque(end), length(Cobra_2208_Motor_torque));
Cobra_2208_Thrust_From_Torque = k_tau.*Torque_CMD;

%%
disp("********************************************************************");
disp("************************ Non-Linear Mapping ************************");

disp('Kveff in RPM/V'); disp(Kv_eff); % RPM/V, motor command to speed constant
disp('omega_c in RPM'); disp(wc); % RPM, motor command to speed bias
disp('Ct in N/RPM^2');  disp(Ct); % N/RPM^2
disp('omega_f in RPM'); disp(wf); % RPM, omega to force bias
disp('Fb in N'); disp(Fb); % Nm
disp('k_tau in N/Nm'); disp(k_tau); % N/Nm

gen_F_to_F =          [   1/(4) ,  -1/(2*L_roll) ,  1/(2*L_pitch) ,  k_tau/(4)  ;...
                          1/(4) ,  -1/(2*L_roll) , -1/(2*L_pitch) , -k_tau/(4)  ;...
                          1/(4) ,   1/(2*L_roll) ,  1/(2*L_pitch) , -k_tau/(4)  ;...
                          1/(4) ,   1/(2*L_roll) , -1/(2*L_pitch) ,  k_tau/(4) ];
display(gen_F_to_F);

% Convert from Motor Forces to Force and 3 torques:
Inv_gen_F_to_F = inv(gen_F_to_F);
Omega_Non_Lin = max(Omega_linear);
Motor_max_non_lin = Ct*(Omega_Non_Lin+wc)^2+Fb

%  Max Thrust
Forces = Motor_max_non_lin*[1; 1; 1; 1];
F_max_Non_Lin = sum(Inv_gen_F_to_F*Forces);

% Max Roll 
Forces = Motor_max_non_lin*[0; 0; 1; 1];
Roll_Max_Non_Lin = Inv_gen_F_to_F*Forces;

% Max Pitch 
Forces = Motor_max_non_lin*[1; 0; 1; 0];
Pitch_Max_Non_Lin = Inv_gen_F_to_F*Forces;

% Max Yaw
Forces = Motor_max_non_lin*[1; 0; 0; 1];
Yaw_Max_Non_Lin = Inv_gen_F_to_F*Forces;

% Hover Trim
Hover_Force = [Force_Hover;Force_Hover;Force_Hover;Force_Hover]*(1/4);
Omega_Hover_Non_Lin = sqrt((1/Ct)*(Hover_Force-Fb))-wf;
V_Hover = (1/Kv_eff)*(Omega_Hover_Non_Lin-wc);
Hover_Trim = V_Hover/Vd;

disp('Maximum Non-Linear Thrust (N) = '); disp(F_max_Non_Lin);
disp('Maximum Non-Linear Roll Torque (Nm) = '); disp(Roll_Max_Non_Lin(2));
disp('Maximum Non-Linear Pitch Torque (Nm) = '); disp(Pitch_Max_Non_Lin(3));
disp('Maximum Non-Linear Yaw Torque (Nm) = '); disp(Yaw_Max_Non_Lin(4));
disp('Non-linear hover trim (%) = '); disp(Hover_Trim(1));

% For plotting non-linear thrust:
Force_Commands = linspace(0,F_max_Non_Lin/4,100)';
Omega_Non_Lin = sqrt((1/Ct)*(Force_Commands-Fb))-wf;
V_Non_Lin_Command = (1/Kv_eff)*(Omega_Non_Lin-wc);
Percent_Command = (V_Non_Lin_Command/Vd)';
Non_Linear_Net_Force = sum([Force_Commands,Force_Commands,Force_Commands,Force_Commands],2)';

%% Data plotting 

%  Relationship between motor speed and voltage command 
figure(1)
hold on 
plot(Cobra_2208_Volt_CMD_Pred, Cobra_2208_Motor_Speed,'b')
plot(Cobra_2208_Volt_CMD_Pred,Omega_points,'r')
hold off 
legend('Cobra 2208','Linear Fit ')
title('Angular Velocity (RPM) Vs Motor Command (V)')
xlabel('Motor Command (V)');ylabel('Angular Velocity (RPM)')
grid on; grid minor


%  Torque vs Thurst comparison bettwen Cobra 2208-2000Kv and QDrone 2206-2100KV
figure(2)
hold on 
plot(Cobra_2208_Motor_torque, Cobra_2208_Propeller_Thrust, 'b')
plot(Torque_CMD,Cobra_2208_Thrust_From_Torque,'r')
hold off
legend('Raw-Cobra 2208','Linear Fit ')
title('Thrust Force (N) Vs Motor Torque(Nm)')
xlabel('Motor Torque(Nm)');ylabel('Thrust Force (N)')
grid on; grid minor

figure(3)
hold on 
plot(Cobra_2208_Motor_Speed, Cobra_2208_Propeller_Thrust,'r')
plot(linspace(0,max(Cobra_2208_Motor_Speed),length(Motor_Speed_Command)), Cobra_Thrust_pred,'b')
hold off
legend('Actual Thurst','Predicted Thrust')
title('Thrust Force (N) Vs Angular Velocity (RPM)')
xlabel('Angular Velocity (RPM)');ylabel('Thrust (N)')
grid on; grid minor

figure(4)
hold on
plot(Command_Range.*100,F_net,'b')
plot(Percent_Command*100,Non_Linear_Net_Force,'r')
plot(Command_Range.*100,F_Hover, 'g')
hold off
legend('Linear Mapping','Non-Linear Mapping')
title('Comparing Linear and Non-Linear Mapping')
xlabel('Motor Command (%)');ylabel('Thrust (N)')
grid on; grid minor