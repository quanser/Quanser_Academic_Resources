@REM Batch script to start the Python Script(s) on the QCar

@REM Turn off command echo
@ECHO OFF

@REM Enable local environment so variable values are local to the script
setlocal
@REM Enable delayed expansion for the for loop to function
setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=../config.txt"


@REM Read each line from the config file annd
@REM Set variable values according to config.txt
for /f "usebackq tokens=1,* delims==" %%A in (!configFile!) do (	
    set "key=%%A"
    set "value=%%B"
    set "!key!=!value!"
)

@REM Remove [ and ] in QCAR_IPS string
set "QCAR_IPS=%QCAR_IPS:[=%"
set "QCAR_IPS=%QCAR_IPS:]=%"

@ECHO ON

start "run calibrate.py" python ../python/calibrate.py -ip %QCAR_IPS% -cip %CALIBRATE_IP% -rp %REMOTE_PATH%




