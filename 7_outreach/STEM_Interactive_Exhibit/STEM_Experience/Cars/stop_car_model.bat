@REM Batch script to stop the QCar model(s)

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
set "QCAR_SUBNET_PREFIX=%IP_GATEWAY:~0,-2%"

@REM Define the binary extension
if %CAR_TYPE%==QCar2 (
    set "POSTFIX_BIN=rt-linux_qcar2"
)
if %CAR_TYPE%==QCar1 (
    set "POSTFIX_BIN=rt-linux_nvidia"
)

@REM Turn command echo back on
@ECHO ON

@REM Stopping all of the models
for /l %%Q in (1, 1, 5) do (
    set QCAR_IP=%QCAR_SUBNET_PREFIX%.1%%Q%
    start "Stopping QUARC Models" "%QUARC_DIR%quarc_run" -q -Q -t tcpip://!QCAR_IP!:17000 *.%POSTFIX_BIN%
)