%% =====================Motor Mapping script============================
% The following script is used to load the motor mapping matrix which will
% be used by the commander/stabilizer and the stabilizer models

% Parameters for 7 inch QDrone 

L_Roll  = 10*(25.4/1000); %m
L_Pitch = 8*(25.4/1000); %m
K_Tau   = 68.9055; 
KT = [0.03616,0.117,-0.01215]; 
Motor_Matrix = [ 0.25   -1/(2*L_Roll)    1/(2*L_Pitch)    K_Tau/4;...
                 0.25   -1/(2*L_Roll)   -1/(2*L_Pitch)   -K_Tau/4;...
                 0.25    1/(2*L_Roll)    1/(2*L_Pitch)   -K_Tau/4;...
                 0.25    1/(2*L_Roll)   -1/(2*L_Pitch)    K_Tau/4];