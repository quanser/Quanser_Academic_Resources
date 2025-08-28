@REM Batch script to download the QUARC Server file from the host to the Traffic Light

@REM Turn off command echo
@ECHO OFF

@REM Found out the location of the batch file
@REM NOTE: It could be launched from command prompt or double clicking.
@REM        If through double-clicking, %CD% would be the default system shell path.
@REM        So that will not work as we do not know where the source files might be.
@REM        We are making the assumption that at least we know where the source
@REM        files are relative to this BATCH script file itself.
@REM NOTE: %~dp0% returns the final slash "\" so no need to add one when augmenting.
set PATH_BATCH=%~dp0%

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

@REM Define initial time delay to ensure the Raspberry Pi has completed startup properly
set TRAFFIC_LIGHT_INITIAL_WAIT=15

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
    start "QUARC Server" "%QUARC_DIR%quarc_run" -D -t tcpip://!TRAFFIC_LIGHT_IP!:17000 %PATH_BATCH%!TRAFFIC_LIGHT_SERVER! -d /tmp -uri tcpip://!TRAFFIC_LIGHT_IP!:17001
    timeout /t 3
)

