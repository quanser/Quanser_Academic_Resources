@REM Batch script to start the QUARC models on the Infrastructure PC

@REM Turn off command echo
@ECHO OFF

setlocal enabledelayedexpansion

@REM Path to the config file
set "configFile=../../config.txt"

@REM Read each line from the config file annd
@REM Set variable values according to config.txt
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
@ECHO ON

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

@REM Launching the models on infrastructure PC
@REM (Assumption: The QUARC models had already been downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing

@REM Main
start "Infrastructure Main" "%QUARC_DIR%\quarc_run" -l -t shmem://%URL_INFRASTRUCTURE%:1 %MODEL_MAIN%.%POSTFIX_BIN% -d %PATH_MAIN% -uri shmem://%URL_INFRASTRUCTURE%:2 -IP_GATEWAY %IP_GATEWAY%

@REM V2V
start "Infrastructure V2V" "%QUARC_DIR%\quarc_run" -l -t shmem://%URL_INFRASTRUCTURE%:1 %MODEL_V2V%.%POSTFIX_BIN% -d %PATH_V2V% -uri shmem://%URL_INFRASTRUCTURE%:3 -IP_GATEWAY %IP_GATEWAY%

@REM NN
start "Infrastructure NN" "%QUARC_DIR%\quarc_run" -l -t shmem://%URL_INFRASTRUCTURE%:1 %MODEL_NN%.%POSTFIX_BIN% -d %PATH_NN% -uri shmem://%URL_INFRASTRUCTURE%:4 -IP_GATEWAY %IP_GATEWAY%
for /l %%Q in (1, 1, 5) do (
    set "port=1869%%Q%"
    start "YOLO client %%Q%" /b pythonw src/NN/yolo_client.py -p !port!
    timeout /t 1
)
