% Load QUBE-Servo 3 model parameters
qube3_rotpen_param;
% Load state-space model for pendulum in downward configuration
rotpen_ABCD_eqns_down;
% Create Matlab state-space object for analysis
sys = ss(A,B,C,D);
