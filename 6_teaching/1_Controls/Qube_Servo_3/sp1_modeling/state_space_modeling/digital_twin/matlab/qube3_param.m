% Resistance
Rm = 7.5;
% Current-torque (N-m/A)
kt = 0.042;
% Back-emf constant (V-s/rad)
km = 0.042;
% Rotor inertia (kg-m^2)
Jr = 1.4e-6;
% Hub mass (kg)
mh = 0.0106; % 9 g
% Hub radius (m)
rh = 22.2/1000/2; % diameter 22.2 mm
% Hub inertia (kg-m^2)
Jh = 0.5*mh*rh^2;
% Disc mass (kg)
md = 0.053;
% Disc radius (m)
rd = 49.5/1000/2; % diameter = 49.5 mm
% Disc moment of inertia (kg-m^2)
Jd = 0.5*md*rd^2;
% Equivalent moment of inertia (kg-m^2)
Jeq = Jr + Jh + Jd;
