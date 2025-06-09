clc; close all;

format long;

M_b = 0.267; % mass of battery
M_d = 0.854; % mass of drone
M = M_b + M_d; % total mass of drone
lin_hover_trim = 0.538; % hover trim (motor command)
g = 9.81; % acceleration due to gravity
L_roll = 0.2136; % roll motor to motor distance
L_pitch = 0.1758; % pitch motor to motor distance
kt = 1/(70*pi); % motor torque constant Nm/A
kv = 1/(70*pi); % motor speed constant Vs/rad
Ahover = 5.8239; % maximum motor current at 100% throttle
Jxx = 0.0100000; % kg*m^2
Jyy = 0.0082000; % kg*m^2
Jzz = 0.0148000; % kg*m^2
Vd = 12.6; % maximum battery voltage in Volts

%%
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
display(F_to_m);

Forces = m_to_F*[1; 1; 1; 1];
disp('Maximum Linear Thrust (N) = '); display(Forces(1));

Forces = m_to_F*[0; 0; 1; 1];
disp('Maximum Linear Roll Torque (Nm) = '); display(Forces(2));

Forces = m_to_F*[1; 0; 1; 0];
disp('Maximum Linear Pitch Torque (Nm) = '); display(Forces(3));

Forces = m_to_F*[1; 0; 0; 1];
disp('Maximum Linear Yaw Torque (Nm) = '); display(Forces(4));

disp('Linear hover trim (%) = '); disp(lin_hover_trim);

%%
disp("********************************************************************");
disp("************************ Non-Linear Mapping ************************");

disp('Kveff in RPM/V'); Kveff = 1295.4; disp(Kveff); % RPM/V, motor command to speed constant
disp('omega_c in RPM'); omega_c = 2132.6; disp(omega_c); % RPM, motor command to speed bias
disp('Ct in N/RPM^2'); Ct = 2.0784*10^(-8); disp(Ct); % N/RPM^2
disp('omega_f in RPM'); omega_f = 1004.5; disp(omega_f); % RPM, omega to force bias
disp('Fb in N'); Fb = -0.2046; disp(Fb); % Nm
disp('k_tau in N/Nm'); k_tau = 81.0363; disp(k_tau); % N/Nm

gen_F_to_F =          [   1/(4) ,  -1/(2*L_roll) ,  1/(2*L_pitch) ,  k_tau/(4)  ;...
                          1/(4) ,  -1/(2*L_roll) , -1/(2*L_pitch) , -k_tau/(4)  ;...
                          1/(4) ,   1/(2*L_roll) ,  1/(2*L_pitch) , -k_tau/(4)  ;...
                          1/(4) ,   1/(2*L_roll) , -1/(2*L_pitch) ,  k_tau/(4) ];
display(gen_F_to_F);

disp('Maximum Non-Linear Thrust (N) = '); disp(30.7);
disp('Maximum Non-Linear Roll Torque (Nm) = '); disp(1.6373);
disp('Maximum Non-Linear Pitch Torque (Nm) = '); disp(1.3476);
disp('Maximum Non-Linear Yaw Torque (Nm) = '); disp(0.1892);
disp('Non-linear hover trim (%) = '); disp(lin_hover_trim);

%%
% plots
m = 0:0.01:1;

F_l = zeros(1,length(m));
for i = 1:length(m)
   f1 = m_to_F*[m(i); m(i); m(i); m(i)]; 
   F_l(i) = f1(1);
end

f_to_gen_F = inv(gen_F_to_F);
F_nl = zeros(1,length(m));
    voltage = Vd.*m;
    omega = Kveff.*voltage + omega_c;
    fm = Ct*(omega + omega_f).^2 + Fb;
    for i = 1:length(m)
        gen_F = f_to_gen_F*[fm(i);fm(i);fm(i);fm(i)];
        F_nl(i) = gen_F(1);
    end

Forces = m_to_F*[1; 1; 1; 1];

figure;
hold on;
plot(m, F_l, 'b');
plot(m, F_nl, 'r');
plot(m, lin_hover_trim*Forces(1).*ones(1,length(F_l)), 'g');
hold off
legend('Linear Mapping', 'Non-linear Mapping');
xlabel('Motor Command (%)');
ylabel('Thrust Generated (N)');
title('Comparing the Linear and Non-linear mapping');
grid minor;

figure;
hold on;
plot(omega, fm, 'b');
hold off
xlabel('Angular Velocity (RPM)');
ylabel('Thrust Generated per Motor (N)');
title('Thrust Generated vs. Angular Velocity in the Non-linear mapping');
grid minor;

figure;
hold on;
plot(voltage, omega, 'b');
hold off
xlabel('Motor Command (V)');
ylabel('Angular Velocity (RPM)');
title('Angular Velocity vs. the Voltage Command in the Non-linear mapping');
grid minor;
