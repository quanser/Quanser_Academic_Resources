@echo off
setlocal EnableDelayedExpansion

:: Specify the path to the log file
set "LOG_FILE=%CD%\software_requirements.log"

:: Check if the log file exists
if not exist "%LOG_FILE%" (
    echo.
    echo [91mLog file not found at "%LOG_FILE%".[0m
    echo.
    echo [92mPlease run the [96mstep_1_check_requirements.bat[0m file first.[0m
    pause
    exit /b 1
)

:: Initialize variables
set "missing_requirements="

set "Python_version="
set "QSDK_status="
set "QLabs_status="

:: Parse the log file
for /f "tokens=1,* delims=:" %%a in ('type "%LOG_FILE%" ^| findstr /r "QSDK_user: QLabs_user: Python_user:"') do (
    set "key=%%a"
    set "value=%%b"
    
    :: Trim leading spaces from value
    set "value=!value:~1!"
    call :TrimSpaces value

    :: Assign to appropriate variable based on key
    if "!key!"=="Python_user" set "Python_version=!value!"
    if "!key!"=="QSDK_user" set "QSDK_status=!value!"
    if "!key!"=="QLabs_user" set "QLabs_status=!value!"
)

:: Display extracted values
echo [96m========================================
echo Found by Step 1 - System Check:
echo ========================================[0m
echo Python Version: %Python_version%
echo QSDK Status: %QSDK_status%
echo QLabs Status: %QLabs_status%
echo [96m========================================[0m

echo.

if "%Python_version%"=="Not Installed" (
    set "missing_requirements=!missing_requirements! Python,"
    echo Python is Required and Missing 
    echo No Python installation found on your system. Please install a suitable Python version [3.11-3.14]
    echo and add to path before running this script. 
    echo For download links, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    echo.
    timeout /t 1 >nul
)

:: QSDK/QUARC VERSION CHECK 
if "%QSDK_status%"=="Not Installed" (
    set "missing_requirements=!missing_requirements! QUARC or Quanser SDK"
    echo QUARC or Quanser SDK is Required and Missing 
    echo They are needed to use Quanser's devices with Python.
    echo For more information, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    echo or contact Quanser tech support at tech@quanser.com
    echo.
    timeout /t 1 >nul
)

if "%QLabs_status%"=="Not Installed" (
    echo Quanser Interactive Labs is not installed, if you are going to use virtual devices, 
    echo download it as described in our resources, ctrl + click: [94mhttps://www.quanser.com/pcsetup[0m 
    echo.
    timeout /t 1 >nul
)

:: Handle missing requirements
if not "!missing_requirements!"=="" (
    echo [91mMissing Requirements: !missing_requirements![0m
    echo Please install the required software before re-running the script again.
    endlocal
    pause
    exit /b 0
)

timeout /t 1 >nul
echo.

echo [92mInstalling Quanser's Python Packages...[0m

echo.

set "py_ver=!Python_version!"

:: Installing python whls
::Search for the file that starts with "quanser_api"
for /f "delims=" %%f in ('dir /b /a-d "%QSDK_DIR%python"\quanser_api*') do (
    set FILENAME=%%f
)

echo [93mDeleting pip cache[0m
py -!py_ver! -m pip cache purge

echo [93mInstalling Quanser Python API %FILENAME%[0m
py -!py_ver! -m pip install --upgrade pip
py -!py_ver! -m pip install --upgrade --find-links "%QSDK_DIR%python" "%QSDK_DIR%python\%FILENAME%"

timeout /t 2 >nul

echo.
echo.

:: SETTING UP ENVIRONMENT VARIABLES

echo [92mSetting up Environment Variables...[0m
:: Define paths
set "QAL_DIR=%USERPROFILE%\Documents\Quanser"
set "RTMODELS_DIR=%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models"
set "NEW_PYTHON_PATH=%USERPROFILE%\Documents\Quanser\0_libraries\python"
echo.
:: Set QAL_DIR
echo [93mSetting QAL_DIR to: %QAL_DIR%[0m
setx QAL_DIR "%QAL_DIR%"
echo.

:: Set RTMODELS_DIR
echo [93mRTMODELS_DIR set to: %RTMODELS_DIR%[0m
setx RTMODELS_DIR "%RTMODELS_DIR%"
echo.

:: Check if PYTHONPATH exists
for /f "tokens=2* delims= " %%a in ('reg query "HKCU\Environment" /v PYTHONPATH 2^>nul') do (
    set "PYTHONPATH=%%b"
)

if defined PYTHONPATH (
    :: If PYTHONPATH exists, add NEW_PYTHON_PATH if not already present
    echo %PYTHONPATH% | find "!NEW_PYTHON_PATH!" >nul
    if errorlevel 1 (
        set "PYTHONPATH=%PYTHONPATH%;!NEW_PYTHON_PATH!"
        echo [93mPYTHONPATH updated: !PYTHONPATH![0m
        setx PYTHONPATH "!PYTHONPATH!"
    ) else (
        echo %NEW_PYTHON_PATH% is already in PYTHONPATH. No changes made.
    )
) else (
    :: If PYTHONPATH does not exist, create it
    echo [93mPYTHONPATH created: !NEW_PYTHON_PATH![0m
    setx PYTHONPATH "!NEW_PYTHON_PATH!"
)

:: Define the path to requirements.txt
set "REQUIREMENTS_FILE=requirements.txt"

echo.
echo.
:: Install the required packages using pip
echo [92mInstalling Python packages from %REQUIREMENTS_FILE%, please wait...[0m
echo.

:: Check if the requirements.txt file exists
if not exist "%REQUIREMENTS_FILE%" (
    echo [91mrequirements.txt not found![0m
    pause
    exit /b
)
:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [91mPython is not installed or not found in PATH.[0m
    pause
    exit /b
)

:: Install the required packages using pip
py -!py_ver! -m pip install -r "%REQUIREMENTS_FILE%"

:: Check the result of the pip install command
if %errorlevel% neq 0 (
    echo [91mSome packages failed to install.[0m
    pause
    exit /b
)
echo [92mPackages installed successfully.[0m
goto :ending

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


:ending
echo.
echo [92mScript completed. System configured for Python usage.
echo. 
echo For MATLAB usage, also run configure_matlab.  
echo PLEASE RESTART YOUR MACHINE FOR CHANGES TO BE APPLIED.[0m
endlocal
pause