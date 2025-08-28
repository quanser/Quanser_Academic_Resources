@REM Batch script to stop the infrastructure models

@REM Turn off command echo
@ECHO OFF

@REM Define the URL of the local QUARC run-time manager
set URL_INFRASTRUCTURE=quarc-target

@REM Define the binary extension
set POSTFIX_BIN=rt-win64

@REM Turn command echo back on
@ECHO ON

@REM Stopping all of the models
start "Stopping QUARC Models" "%QUARC_DIR%\quarc_run" -q -Q -t shmem://%URL_INFRASTRUCTURE%:1 *.%POSTFIX_BIN%
taskkill -f -im python*
