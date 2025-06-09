%clear current figures
close all

%%
%========================================
%Section 1 Input the Qube-Servo 3 parameters
K = 
tau = 

%%
%========================================
% Section 2 Defining the transfer functions

% Enter the plant transfer function
P = tf([],[]);

% Enter the integrator transfer function
I = tf([],[]);

% Combine the P and I transfer functions using the series() function
Pi = series()

%%
%========================================
% Section 3 Extracting gain Kc from the Bode Plot

% Set the desired crossover frequency to search for
cross_freq_des = ;

% Find the Kc that corresponds to the desired crossover frequency defined 
% above
Kc = 

%%
%========================================
% Section 4 Adding phase to the system and calculating the new bandwidth

% Obtain the phase margin of the system with the new gain
bode_info1 = allmargin(Kc*Pi);
PM_meas = 

% Obtain the phase lead that is necessary to achieve the target PM
PM_des = 
phi_m = 

% Calculate the gain alpha using phi_m
a = 

% Using alpha (a) find the dB value to search for in the Bode plot of
% Kc*Pi(s)
search_gain =

% The following code will find the corresponding frequency on the bode plot
% based on the search gain provided.
w = 10^-1:0.1:10^3;
mag = 20*log10(abs(squeeze(freqresp(Kc*Pi,w))));
w_m = w(find(mag<search_gain,1))

%%
%========================================
% Section 5 Deriving the lead compensator transfer function

% Calculate the lead compensator parameter: T
T = 

% Using alpha and T, define the lead compensator transfer function
LEAD = 

% Complete Compensator: C(s) = (1+a*Ts)/(1+T*s)*Kc/s
C = Kc*series(LEAD,I);

% Loop transfer function: L(s) = C(s)*P(s)
L = series(P,C);

%Get the resulting phase margin from the closed-loop system with the
%compensator
bode_info2 = allmargin(L);
final_PM = 

%%
%========================================
% Section 6 Simulate the step response

% Step amplitude (rad/s)
R0 = 4.0;
% Closed-loop system
G = feedback(L,1);

figure(1)
step(2+R0*G);
axis([0 1 0 7])
stepinfo(2+R0*G)

%%
%========================================
% Section 7 Compare the original bode plot to the fully compensated one

clf(figure(2))

figure(2)
hold on
margin(Pi)
margin(L)
hold off
