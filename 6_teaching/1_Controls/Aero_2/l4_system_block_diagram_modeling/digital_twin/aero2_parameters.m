%% AERO 2 Parameters
Dt = 0.16743;       % distance from pivot to center of rotor/propeller (m)
Mb = 1.07;          % total aero body mass (kg)
Dm = 2.7e-3;        % distance from aero body plane to center of mass below (m)
Jp = 0.0231;        % Moment of inertia about pitch-axis (kg-m^2) from CAD: 23188500.45 g-mm^2
kt_p = 0.0006;      % thrust constant of propeller (N-s/rad)
g = 9.81;           % Gravity (m/s^2)
Dp = 0.008;         % pitch pivot damping (Nm-s/rad)

%% Thruster Parameters
Rm = 8.4;           % Motor coil resistance (ohms)
kt = 4.2*10^(-2);   % Motor torque constant (N-m/A)
km = 4.2*10^(-2);   % Back EMF constant (V/rad-s)
kd = 8*10^(-5);     % Propeller Drag (N-m-s/rad)
Lm = 1.16;          % Motor inductance (mH)
mh = 3.0*10^(-3);   % Hub mass (kg)
rh = 9/1000/2;      % Hub radius (m)
Jr = 4.0*10^(-6);   % Rotor inertia (kgm^2)
Jprop = 4.0*10^(-5);% missing prop interia prev Jp
Jh = 0.5*mh*rh^2;   % Hub inertia (kg-m^2)
Jeq = Jr + Jprop + Jh; % Equivalent moment of inertia (kg-m^2)