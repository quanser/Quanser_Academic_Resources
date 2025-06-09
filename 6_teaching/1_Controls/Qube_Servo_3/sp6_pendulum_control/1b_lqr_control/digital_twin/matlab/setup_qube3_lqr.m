%% Load Model
qube3_rotpen_param;
% Set open-loop state-space model of rotary single-inverted pendulum (SIP)
rotpen_ABCD_eqns_ip;
% Display matrices
A
B

%% Balance Control
% Find Q, R and K matrices
% LQR Weighting Matrices
Q = diag([1 0 0 0]);
R = 1;
K = lqr(A,B,Q,R);
display(K);