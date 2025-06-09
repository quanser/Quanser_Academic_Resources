%system variables
K = 23.8;
tau = 0.09;
kp = 1;

wn = 1;
zeta = 1;

% Result in a percent overshoot and peak time of
% Percent overshoot (%)
PO = 1
% Peak time (s)
tp = 1

% Store data from scopes into these variables
t = position(:,1);
step = position(:,2);
read_position = position(:,3);
u = voltage(:,2);

% Plot
subplot(2,1,1);

subplot(2,1,2);

ylabel('V_m (V)');
xlabel('time (s)');