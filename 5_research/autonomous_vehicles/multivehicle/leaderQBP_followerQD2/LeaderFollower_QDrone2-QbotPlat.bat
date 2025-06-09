@REM Startup script for QDrone2 and QBot Platform Leader Follower
@REM Assuming all executibles have been compiled and in the current folder

::The following drone IDs can be found by 
::looking into the router's list of connected devices. 
::These are all the robot's IDs X. Set the last digits 
:: of your drone IP after the corresponding parameter. 
:: They will be used below in the IP address format - 192.168.2.X

set drone_id=192.168.2.11
set qbot_id=192.168.2.21

@REM CLOSE TRAY, PERIPHERAL AND CONSOLES

@REM QUARC Console - error/warning/status message monitoring
taskkill /im quarc_run.exe /t

@REM QUARC Tray - monitoring localhost processes
start "Master" "quarc_tray" /q

@REM QUARC/Quanser Host Peripheral Client
start "HostPeripheral" "quanser_host_peripheral_client.exe" -q

timeout /t 5 

@REM ------------------------OPEN TRAY AND CONSOLES -----------------------------------------

@REM QUARC Tray - monitoring localhost processes
start "Master" "quarc_tray" /l

timeout /t 2

@REM QUARC Console - error/warning/status message monitoring
start "Master" "quarc_run" -c *.rt-win64

@REM QUARC Console Drone - error/warning/status message monitoring
start "Drone" "quarc_run" -c -t tcpip://%drone_id%:17000 *.rt-linux_qdrone2

@REM QUARC Console QBot - error/warning/status message monitoring
start "QBot" "quarc_run"  -c -t tcpip://%qbot_id%:17000 *.rt-linux_qbot_platform

@REM Waiting for console start up
timeout /t 2  

@REM ------------------------ QUIT ALL MODELS ---------------------------------------------

@REM Mission Server
start "LeaderFollower" "quarc_run" -q -Q MS_Drone1_Qbot1.rt-win64
@REM Drone
start "Drone" "quarc_run" -q -Q -t tcpip://%drone_id%:17000 QDrone.rt-linux_qdrone2 -uri tcpip://%drone_id%:17001
@REM QBot
start "QBot" "quarc_run" -q -Q -t tcpip://%qbot_id%:17000 qbot_driver.rt-linux_qbot_platform -uri tcpip://%qbot_id%:17001

@REM ------------------------OPEN PERIPHERAL CLIENT AND RUN FILES ------------------------------

@REM QUARC/Quanser Host Peripheral Client
start "HostPeripheral" "quanser_host_peripheral_client.exe" -window:no -uri tcpip://localhost:18005

@REM WaitForStop
timeout /t 3  

@REM RUN ALL MODELS

@REM Mission Server
start "LeaderFollower" "quarc_run" -r  MS_QD2_QBPlat.rt-win64 -drone_ip %drone_id% -qbot_ip %qbot_id%
@REM Wait for Mission Server Startup
timeout /t 20
@REM Drone
start "Drone" "quarc_run" -r -t tcpip://%drone_id%:17000 QDrone.rt-linux_qdrone2 -uri tcpip://%drone_id%:17001?retries=10
@REM QBot
start "QBot" "quarc_run" -r -t tcpip://%qbot_id%:17000 qbot_driver.rt-linux_qbot_platform -uri tcpip://%qbot_id%:17001?retries=10
