@REM Batch script to download the QUARC model(s) to the QCar

@REM Turn off command echo
@ECHO OFF

@REM Enable local environment so variable values are local to the script
setlocal
@REM Enable delayed expansion for the for loop to function
setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=..\..\..\config.txt"

@REM Read each line from the config file annd
@REM Set variable values according to config.txt
for /f "usebackq tokens=1,* delims==" %%A in (!configFile!) do (
	set "key=%%A"
	set "value=%%B"
	set "!key!=!value!"
)
set "QCAR_SUBNET_PREFIX=%IP_GATEWAY:~0,-2%"

@ECHO ON
@REM transfer the reference scans to the cars
for /l %%Q in (1, 1, 5) do (
    set QCAR_IP=%QCAR_SUBNET_PREFIX%.1%%Q%
    ssh -o ConnectTimeout=2 nvidia@!QCAR_IP! "rm -f ~/Documents/*.mat" 
    scp -o ConnectTimeout=2 %CAR_TYPE%/*.mat nvidia@!QCAR_IP!:~/Documents
)

