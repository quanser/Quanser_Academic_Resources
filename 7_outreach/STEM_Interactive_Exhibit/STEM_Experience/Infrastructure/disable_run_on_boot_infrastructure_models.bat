@REM Batch script to configure/disable the QUARC models to run on boot

@REM Turn off command echo
@ECHO OFF

@REM Define name of the main infrastructure model
set MODEL_MAIN=STEM_Infrastructure_Main

@REM Define name of the V2V model
set MODEL_V2V=STEM_Infrastructure_V2V

@REM Define name of the NN model
set MODEL_NN=STEM_Infrastructure_NN

@REM Define the URL of the local QUARC run-time manager
set URL_INFRASTRUCTURE=quarc-target

@REM Define the binary extension
set POSTFIX_BIN=rt-win64

@REM Turn command echo back on
@ECHO ON

@REM Disabling the QUARC models from running on boot
@REM (Assumption: QUARC models had already been downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing

@REM Main
start "Infrastructure Main" "%QUARC_DIR%quarc_run" -n -t shmem://%URL_INFRASTRUCTURE%%:1 %MODEL_MAIN%.%POSTFIX_BIN% -uri shmem://%URL_INFRASTRUCTURE%%:2

@REM V2V
start "Infrastructure V2V" "%QUARC_DIR%quarc_run" -n -t shmem://%URL_INFRASTRUCTURE%%:1 %MODEL_V2V%.%POSTFIX_BIN% -uri shmem://%URL_INFRASTRUCTURE%%:3

@REM NN
start "Infrastructure NN" "%QUARC_DIR%quarc_run" -n -t shmem://%URL_INFRASTRUCTURE%%:1 %MODEL_NN%.%POSTFIX_BIN% -uri shmem://%URL_INFRASTRUCTURE%%:4

@REM removing yolo client on start up apps
set "SHORTCUT_NAME=start_yolo"
set "STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup"
set "SHORTCUT_PATH=%STARTUP_FOLDER%\%SHORTCUT_NAME%.lnk"

if exist "%SHORTCUT_PATH%" (
    del "%SHORTCUT_PATH%"
    echo Shortcut removed: %SHORTCUT_PATH%
) else (
    echo Shortcut not found: %SHORTCUT_PATH%
)