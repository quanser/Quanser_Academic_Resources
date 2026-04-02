@echo off
setlocal EnableDelayedExpansion

REM Set the log file path
set "LOG_FILE=%CD%\software_requirements.log"

:: Check if the log file exists
if not exist "%LOG_FILE%" (
    echo.
    echo [91mLog file not found at "%LOG_FILE%".[0m
    echo.
    echo [92mPlease run the [96mstep_1_check_requirements.bat[0m [92mfile first.[0m
    pause
    exit /b 1
)


:: Initialize variables
set "missing_requirements="

set "MATLAB_version="
set "QUARC_status="
set "VisualStudio_version="
set "QLabs_status="

:: Parse the log file
for /f "tokens=1,* delims=:" %%a in ('type "%LOG_FILE%" ^| findstr /r "QUARC_user: QSDK_user: QLabs_user: MATLAB/Simulink_user: Python_user: Visual Studio_user:"') do (
    set "key=%%a"
    set "value=%%b"

    :: Trim leading spaces from value
    set "value=!value:~1!"
    call :TrimSpaces value

    :: Assign to appropriate variable based on key
    if "!key!"=="MATLAB/Simulink_user" set "MATLAB_version=!value!"
    if "!key!"=="QUARC_user" set "QUARC_status=!value!"
    if "!key!"=="Visual Studio_user" set "VisualStudio_version=!value!"
    if "!key!"=="QLabs_user" set "QLabs_status=!value!"
)

:: Display extracted values
echo [96m========================================
echo Found by Step 1 - System Check:
echo ========================================[0m
echo MATLAB Version: %MATLAB_version%
echo QUARC Status: %QUARC_status%
echo Visual Studio Version: %VisualStudio_version%
echo QLabs Status: %QLabs_status%
echo [96m========================================[0m

echo.


if "%MATLAB_version%"=="Not Installed" (
    set "missing_requirements=!missing_requirements! MATLAB"
    echo MATLAB is Required and Missing
    echo Please install MATLAB.
    echo For more information, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    echo.
    timeout /t 1 >nul
)


if "%QUARC_status%"=="Not Installed" (
    echo QUARC is Missing - You will need it if running hardware. You can skip it for for virtual only setups.
    echo If you require QUARC, please check the QUARC Installation Guide or contact Quanser tech support at tech@quanser.com
    echo Note: Microsoft Visual Studio is a prerequisite for using QUARC. Please Check QUARC compatibility table to download and install the correct version of Microsoft Visual Studio
    echo see system requirements from https://www.quanser.com/products/quarc-real-time-control-software/
    timeout /t 1 >nul
    echo.
)

if "%QLabs_status%"=="Not Installed" (
    echo Quanser Interactive Labs is not installed, if you are going to use virtual devices, 
    echo download it as described in our resources, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    echo.
    timeout /t 1 >nul
)


if "%QLabs_status%"=="Not Installed" (
    if "%QUARC_status%"=="Not Installed" (
        set "missing_requirements=!missing_requirements! QLabs and/or QUARC,"
        echo You need Quanser Interactive Labs if you are going to run virtual devices and/or QUARC if you are going to run hardware. 
        echo Please check above messages.
        timeout /t 1 >nul
        echo.
    )
)

:: Handle missing requirements
if not "!missing_requirements!"=="" (
    echo [91mMissing Requirements: !missing_requirements![0m
    echo Please install the required software before re-running the script again.
    echo For more information, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    endlocal
    pause
    exit /b 0
)


timeout /t 1 >nul
echo.

:: Setting up environment variables for both Windows and MATLAB
:setup_environment_variables
echo.
echo [92mSetting up Environment Variables...[0m
echo.
:: Define paths
set "QAL_DIR=%USERPROFILE%\Documents\Quanser"
set "RTMODELS_DIR=%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models"

:: Set QAL_DIR
echo [93mSetting QAL_DIR to: %QAL_DIR%[0m
setx QAL_DIR "%QAL_DIR%"
echo.

:: Set RTMODELS_DIR
echo [93mRTMODELS_DIR set to: %RTMODELS_DIR%[0m
setx RTMODELS_DIR "%RTMODELS_DIR%"
echo.


echo [92mUpdating MATLAB Paths...[0m

:: Define MATLAB base path and versions to check
set "MATLAB_BASE=C:\Program Files\MATLAB"
set "MATLAB_VERSIONS=R2026a R2025b R2025a R2024b R2024a R2023b R2023a R2022b R2022a R2021b R2021a R2020b R2020a R2019b R2019a"
set "USER_LIB_PATH=%USERPROFILE%\Documents\Quanser\0_libraries\matlab"
setlocal enabledelayedexpansion
:: Initialize a flag to track if any MATLAB versions are found
set "VERSIONS="
set "FOUND=0"

:: Iterate through each version to check for existence
for %%V in (%MATLAB_VERSIONS%) do (
    if exist "%MATLAB_BASE%\%%V\bin\matlab.exe" (
        echo.
        echo MATLAB version found: %%V
        
        :: Execute the MATLAB command
        start "" "%MATLAB_BASE%\%%V\bin\matlab.exe" -batch "addpath('%USER_LIB_PATH%'); savepath; quit;"
        echo [92mMATLAB path updated for %%V version.[0m
        timeout /t 20
    )
)
goto :ending



:ending
echo.
echo [92mScript completed. System configured for MATLAB/Simulink usage.
echo. 
echo For Python usage, also run configure_python.  
echo PLEASE RESTART YOUR MACHINE FOR CHANGES TO BE APPLIED.[0m
endlocal
pause


endlocal
exit /b 0

:TrimSpaces
setlocal EnableDelayedExpansion
set "var=!%1!"

:TrimLoop
if "!var:~-1!"==" " (
    set "var=!var:~0,-1!"
    goto TrimLoop
)

endlocal & set "%1=%var%"
goto :eof