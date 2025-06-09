% Find Total Inertia
Jt = Jr*Jp - mp^2*l^2*r^2;
% 
% State Space Representation -- TO BE COMPLETED
A = zeros(4,4);
B = [0; 0; 1; 1];
C = zeros(2,4);
D = zeros(4,1);
% 
% Convert torque input to voltage input
A(3,3) = A(3,3) - km*km/Rm*B(3);
A(4,3) = A(4,3) - km*km/Rm*B(4);
B = km * B / Rm;
