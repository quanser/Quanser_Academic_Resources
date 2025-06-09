% Run the Host Peripheral Client first for port 18978 on the machine where
% the keyboard is connected.
system('quanser_host_peripheral_client.exe -q')
pause(2)
system('quanser_host_peripheral_client.exe -uri tcpip://localhost:18798 &')

% Run the keyboard driver real-time application 
system('quarc_run -q -Q -t tcpip://localhost:17000 *.rt-win64')
pause(2)
keyboard_driver = fullfile(getenv('QAL_DIR'), '0_libraries', 'resources', 'applications', 'KeyboardDriver', 'keyboardDriver30.rt-win64');
system(['quarc_run -D -r -t tcpip://localhost:17000 ', keyboard_driver]);

% Launch the simClient Simulink app
open('simClient.slx');
