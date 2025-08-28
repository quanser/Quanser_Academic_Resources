@REM Batch script to configure/enable the QUARC Server on the Traffic Light to run on boot

@REM Turn off command echo
@ECHO OFF

setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=../../config.txt"

@REM Read each line from the config file annd
@REM Set variable values according to config.txt (Initial_time_delay & IP_GATEWAY)
for /f "usebackq tokens=1,* delims==" %%A in (!configFile!) do (
	set "key=%%A"
	set "value=%%B"
	set "!key!=!value!"
)

@REM Found out the location of the batch file
@REM NOTE: It could be launched from command prompt or double clicking.
@REM        If through double-clicking, %CD% would be the default system shell path.
@REM        So that will not work as we do not know where the source files might be.
@REM        We are making the assumption that at least we know where the source
@REM        files are relative to this BATCH script file itself.
@REM NOTE: %~dp0% returns the final slash "\" so no need to add one when augmenting.
set PATH_BATCH=%~dp0%

@REM Define name of the main infrastructure model
set PATH_MAIN=%PATH_BATCH%src
set MODEL_MAIN=STEM_Infrastructure_Main

@REM Define name of the V2V model
set PATH_V2V=%PATH_BATCH%src
set MODEL_V2V=STEM_Infrastructure_V2V

@REM Define name of the NN model
set PATH_NN=%PATH_BATCH%src\NN
set MODEL_NN=STEM_Infrastructure_NN

@REM Define the URL of the local QUARC run-time manager
set URL_INFRASTRUCTURE=quarc-target

@REM Define the binary extension
set POSTFIX_BIN=rt-win64

@REM Turn command echo back on
@ECHO ON

@REM Configuring the models to run on boot
@REM (Assumption: QUARC model(s) had already been downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing

@REM Main
start "Infrastructure Main" "%QUARC_DIR%quarc_run" -B -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_MAIN%\%MODEL_MAIN%.%POSTFIX_BIN% -td %INFRASTRUCTURE_INITIAL_WAIT% -d %PATH_MAIN% -uri shmem://%URL_INFRASTRUCTURE%:2 -IP_GATEWAY %IP_GATEWAY%

@REM V2V
start "Infrastructure V2V" "%QUARC_DIR%quarc_run" -B -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_V2V%\%MODEL_V2V%.%POSTFIX_BIN% -td %INFRASTRUCTURE_INITIAL_WAIT% -d %PATH_V2V% -uri shmem://%URL_INFRASTRUCTURE%:3 -IP_GATEWAY %IP_GATEWAY%

@REM NN
start "Infrastructure NN" "%QUARC_DIR%quarc_run" -B -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_NN%\%MODEL_NN%.%POSTFIX_BIN% -td %INFRASTRUCTURE_INITIAL_WAIT% -d %PATH_NN% -uri shmem://%URL_INFRASTRUCTURE%:4 -IP_GATEWAY %IP_GATEWAY%

@REM Creating short cut to start_yolo.bat and move it to start up folder
set "BAT_FILE=%~dp0src/NN/start_yolo.bat"
set "SHORTCUT_NAME=start_yolo"
set "VBS_FILE=%TEMP%\create_shortcut.vbs"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\%SHORTCUT_NAME%.lnk"

@REM Create VBScript to make the shortcut
> "%VBS_FILE%" echo Set shell = CreateObject("WScript.Shell")
>> "%VBS_FILE%" echo Set shortcut = shell.CreateShortcut("%SHORTCUT_PATH%")
>> "%VBS_FILE%" echo shortcut.TargetPath = "cmd.exe"
>> "%VBS_FILE%" echo shortcut.Arguments = "/c ""%BAT_FILE%"""
>> "%VBS_FILE%" echo shortcut.WorkingDirectory = "%~dp0src/NN/"
>> "%VBS_FILE%" echo shortcut.IconLocation = "cmd.exe,0"
>> "%VBS_FILE%" echo shortcut.Save

rem Run the VBScript
cscript //nologo "%VBS_FILE%"

rem Cleanup
del "%VBS_FILE%"

echo Shortcut created in Startup folder: %SHORTCUT_PATH%
