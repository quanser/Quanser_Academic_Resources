::Batch Script to be used with the Mission_Server_Swarm_3QDrones.mdl model. 
::Once that model is fully running, run this script by double-clicking on the batch script in your Windows explorer
::----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
::Note that a double colon is a comment

::Drone Communication set up: 
::The following drone IDs can be found by looking into the router's list of connected devices. 
::These are all the drone IDs X. Set the last digits of your drone IP after the corresponding parameter. They will be used below in the IP address format - 192.168.2.X
set drone_1_id=21
set drone_2_id=22
set drone_3_id=23

::This is the last digit(s) H of your PC's IP address. Typically set to 3 or 5, 
::which will be used in the format - 192.168.2.H
set pc_id=3

::These are the ports on which the drones communicate with the Mission Server. 
::The IP address to talk to will be - 192.168.2.H:URI_Host_VX
::You can verify these port numbers by looking at the MEX-fiel Arguments for the mission server
set URI_Host_V1=18001
set URI_Host_V2=18002
set URI_Host_V3=18003

:: Define the name of the QUARC model to be launched by this script to the drones
:: Update the name here if needed
:: Example binary for the QDrone is %QUARC_MODEL_NAME%.rt-linux_x64
set QUARC_MODEL_NAME=Commander_Stabilizer_QDrone

::----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
::Start a series of Quarc Monitors to be able to monitor all 3 drones and the PC
@REM QUARC Tray - monitoring localhost processes
start "PC_Tray" "%QUARC_DIR%\quarc_tray" /t tcpip://localhost:17000
timeout /t 1

@REM QUARC Tray - monitoring localhost processes
start "Drone_1_Tray" "%QUARC_DIR%\quarc_tray" /t tcpip://192.168.2.%drone_1_id%:17000
timeout /t 1

@REM QUARC Tray - monitoring localhost processes
start "Drone_2_Tray" "%QUARC_DIR%\quarc_tray" /t tcpip://192.168.2.%drone_2_id%:17000
timeout /t 1

@REM QUARC Tray - monitoring localhost processes
start "Drone_3_Tray" "%QUARC_DIR%\quarc_tray" /t tcpip://192.168.2.%drone_3_id%:17000
timeout /t 1

::----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
::Start a QUARC Console for each of the 3 drones and the PC 
@REM QUARC Console - error/warning/status message monitoring
start "PC_console" "%QUARC_DIR%\quarc_run" -c -t tcpip://localhost:17000 *.rt-win64
timeout /t 1

@REM QUARC Console - error/warning/status message monitoring
start "Drone_1_console" "%QUARC_DIR%\quarc_run" -c -t tcpip://192.168.2.%drone_1_id%:17000 *.rt-linux_x64
timeout /t 1

@REM QUARC Console - error/warning/status message monitoring
start "Drone_2_console" "%QUARC_DIR%\quarc_run" -c -t tcpip://192.168.2.%drone_2_id%:17000 *.rt-linux_x64
timeout /t 1

@REM QUARC Console - error/warning/status message monitoring
start "Drone_3_console" "%QUARC_DIR%\quarc_run" -c -t tcpip://192.168.2.%drone_3_id%:17000 *.rt-linux_x64
timeout /t 1

::----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
::Generic Timeout
@REM Waiting for console start up
timeout /t 3

::Start deploying and running models on 3 drones
::The current batch script expects as .rt-linux_x64 file with the following name: 
::Commander_Stabilizer_Qdrone.rt-linux_x64. 
::If you update the name of the .rt-linux_x64, which gets generated during model compilation, 
::please update the %QUARC_MODEL_NAME% variable defintion at the beginning of this script.

@REM Drone 1 Model
start "drone_1_Commander_Stabilizer_Qdrone" "%QUARC_DIR%\quarc_run" -D -r -t tcpip://192.168.2.%drone_1_id%:17000 %QUARC_MODEL_NAME%.rt-linux_x64 -uri tcpip://192.168.2.%drone_1_id%:17001?retries=10 -URI_Host "tcpip://192.168.2.%pc_id%:%URI_Host_V1%"
timeout /t 1

@REM Drone 2 Model
start "drone_2_Commander_Stabilizer_Qdrone" "%QUARC_DIR%\quarc_run" -D -r -t tcpip://192.168.2.%drone_2_id%:17000 %QUARC_MODEL_NAME%.rt-linux_x64 -uri tcpip://192.168.2.%drone_2_id%:17001?retries=10 -URI_Host "tcpip://192.168.2.%pc_id%:%URI_Host_V2%"
timeout /t 1

@REM Drone 3 Model
start "drone_3_Commander_Stabilizer_Qdrone" "%QUARC_DIR%\quarc_run" -D -r -t tcpip://192.168.2.%drone_3_id%:17000 %QUARC_MODEL_NAME%.rt-linux_x64 -uri tcpip://192.168.2.%drone_3_id%:17001?retries=10 -URI_Host "tcpip://192.168.2.%pc_id%:%URI_Host_V3%"
timeout /t 1

