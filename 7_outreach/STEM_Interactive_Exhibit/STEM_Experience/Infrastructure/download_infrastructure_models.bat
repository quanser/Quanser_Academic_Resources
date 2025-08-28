@REM Batch script to download the QUARC model(s) to the local run-time manager

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

@REM Downloading the model(s) to the local QUARC run-time manager
@REM (Assumption: The QUARC models is available to be downloaded to the target)
@REM Please contact Quanser support (tech@quanser.com) if the QUARC Server Model is missing

@REM Main
start "Infrastructure Main" "%QUARC_DIR%quarc_run" -D -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_MAIN%\%MODEL_MAIN%.%POSTFIX_BIN% -d %PATH_MAIN% -uri shmem://%URL_INFRASTRUCTURE%:2

@REM V2V
start "Infrastructure V2V" "%QUARC_DIR%quarc_run" -D -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_V2V%\%MODEL_V2V%.%POSTFIX_BIN% -d %PATH_V2V% -uri shmem://%URL_INFRASTRUCTURE%:3

@REM NN
start "Infrastructure NN" "%QUARC_DIR%quarc_run" -D -t shmem://%URL_INFRASTRUCTURE%:1 %PATH_NN%\%MODEL_NN%.%POSTFIX_BIN% -d %PATH_NN% -uri shmem://%URL_INFRASTRUCTURE%:4
