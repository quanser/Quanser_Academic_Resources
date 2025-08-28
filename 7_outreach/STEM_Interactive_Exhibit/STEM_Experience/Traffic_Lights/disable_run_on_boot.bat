@REM Batch script to configure/enable the QUARC Server on the Traffic Light to run on boot

@REM Turn off command echo
@ECHO OFF

@REM Enable local environment so variable values are local to the script
setlocal
@REM Enable delayed expansion for the for loop to function
setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=..\..\config.txt"

@REM Read each line from the config file annd
@REM Set variable values according to config.txt
for /f "usebackq tokens=1,* delims==" %%A in (!configFile!) do (
	set "key=%%A"
	set "value=%%B"
	set "!key!=!value!"
)
set "TRAFFIC_LIGHT_SUBNET_PREFIX=%IP_GATEWAY:~0,-2%"

@REM Define the QUARC Server model name
set POSTFIX_BIN=rt-linux_raspbian

@REM Turn command echo back on
@ECHO ON

@REM Define which Traffic Light to launch the QUARC Server at
@REM The TRAFFIC_LIGHT_ID can be either "20" or "21"
@REM Define Traffic Light IP address based on the ID
@REM Launching the QUARC Server 
@REM (Assumption: QUARC Server Model had already been downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing
for /l %%Q in (0, 1, 1) do (
    set "TRAFFIC_LIGHT_ID=2%%Q%"
    set "TRAFFIC_LIGHT_IP=%TRAFFIC_LIGHT_SUBNET_PREFIX%.!TRAFFIC_LIGHT_ID!"
    set "TRAFFIC_LIGHT_SERVER=traffic_light_target_!TRAFFIC_LIGHT_ID!.%POSTFIX_BIN%"
    start "QUARC Server" "%QUARC_DIR%quarc_run" -n -t tcpip://!TRAFFIC_LIGHT_IP!:17000 !TRAFFIC_LIGHT_SERVER! -uri tcpip://!TRAFFIC_LIGHT_IP!:17001
    timeout /t 3
)
