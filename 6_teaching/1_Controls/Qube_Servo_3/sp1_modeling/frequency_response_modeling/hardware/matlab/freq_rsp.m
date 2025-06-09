%% Sample Frequency Response Modeling
% Collected load speed data given sine wave frequency and amplitude
data = [ 
%   f (Hz)  Av (V)  wl (rad/s) 
    0.0      0       0;
    0.4      0       0;
    0.8      0       0;
    1.2      0       0;
    1.6      0       0;
    2.0      0       0;
    2.4      0       0;
    2.8      0       0;
    ];
%

%% Interpolate frequency and Gains
% Min, max, and differential frequencies (Hz)
f_min = min(f);
f_max = max(f);
df = 0.01;
% Interpolation frequency (Hz)
fi = f_min:df:f_max; % create steps of 0.01 from min to max frequency

% Interpolate gains at other frequencys (rad/s/V)

% Interpolated gain (dB)


%% Bode plot
% add blue Xs in the positions where data was read
% add red dots in all the interpolated locations


axis([0.4 5 15 30]);
xlabel('f (Hz)')
ylabel('|G(\omega)|_{dB}');
%
