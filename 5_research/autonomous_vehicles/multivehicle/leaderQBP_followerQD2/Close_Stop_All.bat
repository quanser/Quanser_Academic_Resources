:: Script to clean up QUARC Console windows and tray monitor icons
::

::The following drone IDs can be found by 
::looking into the router's list of connected devices. 
::These are all the robot's IDs X. Set the last digits 
:: of your drone IP after the corresponding parameter. 
:: They will be used below in the IP address format - 192.168.2.X

set drone_id=192.168.2.11
set qbot_id=192.168.2.21

@REM PC
start "ExitPC" "quarc_run" -q -Q -t tcpip://localhost:17000 *.rt-win64

@REM QDrone2
start "ExitDrone2" "quarc_run" -q -Q -t tcpip://%drone_id%:17000 *.rt-linux_qdrone2

@REM QBotPlatform
start "ExitQBotPlat" "quarc_run" -q -Q -t tcpip://%qbot_id%:17000 *.rt-linux_qbot_platform


@REM QUARC/Quanser Host Peripheral Client
start "HostPeripheral" "quanser_host_peripheral_client.exe" -q

@REM Kill all QUARC Monitor Tray icons
start "Remove Tray Icon" "%QUARC_DIR%\quarc_tray" /q
timeout /t 1

@REM Close QUARC Console Windows
start "Close Console" "taskkill" /im quarc_run.exe
timeout /t 1
