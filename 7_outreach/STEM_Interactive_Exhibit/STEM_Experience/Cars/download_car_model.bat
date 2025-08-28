@REM Batch script to download the QUARC model(s) to the QCar

@REM Turn off command echo
@ECHO OFF

@REM Enable local environment so variable values are local to the script
setlocal
@REM Enable delayed expansion for the for loop to function
setlocal enabledelayedexpansion

@REM Found out the location of the batch file
@REM NOTE: It could be launched from command prompt or double clicking.
@REM        If through double-clicking, %CD% would be the default system shell path.
@REM        So that will not work as we do not know where the source files might be.
@REM        We are making the assumption that at least we know where the source
@REM        files are relative to this BATCH script file itself.
@REM NOTE: %~dp0% returns the final slash "\" so no need to add one when augmenting.
set PATH_BATCH=%~dp0%

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

@REM Define path to the main car model
set PATH_MAIN=%PATH_BATCH%src

@REM Define the remote working folder location
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

@REM Downloading the model(s) onto the specific QCar
@REM (Assumption: The QUARC models is available to be downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing
for /l %%Q in (1, 1, 5) do (
    set QCAR_IP=%QCAR_SUBNET_PREFIX%.1%%Q%
    start "QCar Model" "%QUARC_DIR%quarc_run" -Q -D -t tcpip://!QCAR_IP!:17000 %PATH_MAIN%\%MODEL_MAIN%.%POSTFIX_BIN% -d %PATH_REMOTE% -uri tcpip://!QCAR_IP!:17001
    timeout /t 2
)