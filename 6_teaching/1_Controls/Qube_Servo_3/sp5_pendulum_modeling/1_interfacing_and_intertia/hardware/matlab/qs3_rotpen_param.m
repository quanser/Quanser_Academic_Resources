%% Motor
% Resistance
Rm = 0;
% Current-torque (N-m/A)
kt = 0;
% Back-emf constant (V-s/rad)
km = 0;
%
%% Rotary Arm
% Mass (kg)
mr = 0;
% Total length (m)
r = 0;
% Moment of inertia about pivot (kg-m^2)
Jr = 0;
% Equivalent Viscous Damping Coefficient (N-m-s/rad)
br = 1e-3; % damping tuned heuristically to match QUBE-Sero 3 response
%
%% Pendulum Link
% Mass (kg)
mp = 0;
% Total length (m)
Lp = 0;
% Pendulum center of mass (m)
l = 0;
% Moment of inertia about pivot (kg-m^2)
Jp = 0;
% Equivalent Viscous Damping Coefficient (N-m-s/rad)
bp = 5e-5; % damping tuned heuristically to match QUBE-Sero 3 response
% Gravity Constant
g = 9.81;
