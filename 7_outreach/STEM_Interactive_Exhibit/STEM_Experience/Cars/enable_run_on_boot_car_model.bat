@REM Batch script to configure/enable the QUARC model(s) to run on boot on the QCar

@REM Turn off command echo
@ECHO OFF

@REM Enable local environment so variable values are local to the script
setlocal
@REM Enable delayed expansion for the for loop to function
setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=..\..\config.txt"

@REM Read each line from the config file annd
@REM Set variable values according to config.txt (Initial_time_delay & IP_GATEWAY)
for /f "usebackq tokens=1,* delims==" %%A in (!configFile!) do (
	set "key=%%A"
	set "value=%%B"
	set "!key!=!value!"
)
set "QCAR_SUBNET_PREFIX=%IP_GATEWAY:~0,-2%"

@REM Define the working directory in the remote target
set PATH_REMOTE=/home/nvidia/Documents

@REM Define name the the RT file
@REM Define the binary extension
if %CAR_TYPE%==QCar2 (
    set "MODEL_MAIN=STEM_QCar2"
    set "POSTFIX_BIN=rt-linux_qcar2"
)
if %CAR_TYPE%==QCar1 (
    set "MODEL_MAIN=STEM_Cars"
    set "POSTFIX_BIN=rt-linux_nvidia"
)

@REM Turn command echo back on
@ECHO ON

@REM Configuring the QUARC Server to run on boot
@REM (Assumption: QUARC Server Model had already been downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing
for /l %%Q in (1, 1, 5) do (
    set QCAR_IP=%QCAR_SUBNET_PREFIX%.1%%Q%
    start "QCar Model" "%QUARC_DIR%quarc_run" -B -t tcpip://!QCAR_IP!:17000 %MODEL_MAIN%.%POSTFIX_BIN% -td %QCAR_INITIAL_WAIT% -d %PATH_REMOTE% -uri tcpip://!QCAR_IP!:17001
    timeout /t 2
)