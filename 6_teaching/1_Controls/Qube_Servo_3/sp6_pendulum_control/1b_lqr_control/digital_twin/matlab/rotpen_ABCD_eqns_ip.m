% Find Total Inertia
Jt = 1;

% 
% State Space Representation
A = eye(4,4);

B = [0; 0; 0; 0];
C = eye(2,4);
D = zeros(2,1);
% 
% Convert torque input to voltage input

