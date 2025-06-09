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

