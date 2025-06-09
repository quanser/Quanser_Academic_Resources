Fs = 500;
x = XData(:,2);
L = length(x);
Y = fft(x);
P2 = abs(Y/L);
P1 = P2(1:L/2+1);
P1(2:end-1) = 2*P1(2:end-1);
f = Fs*(0:(L/2))/L;
plot(f,P1)
title('Power Spectrum')
xlabel('f (Hz)')
ylabel('|P1(f)|')
ylim([0 0.3]);
xlim([0 150]);