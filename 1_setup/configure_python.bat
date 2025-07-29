@echo off
setlocal EnableDelayedExpansion

REM Specify the path to the log file
set "LOG_FILE=%CD%\software_requirements.log"

REM Check if the log file exists
if not exist "%LOG_FILE%" (
    echo.
    echo [91mLog file not found at "%LOG_FILE%".[0m
    echo.
    echo [92mPlease run the systemdiag_requirements.bat file first.[0m
    pause
    exit /b 1
)

REM Initialize variables
set "resources="
set "products_content_to_download="
set "py_ver="
set "missing_requirements="
set "not_required_installed="

echo Checking Software Requirements...

REM Parse requirements and system diagnostics
for /f "tokens=1,2 delims=:" %%A in ('findstr /r "Required Optional" "%LOG_FILE%"') do (
    set "requirement=%%A"
    set "status=%%B"
    set "status=!status:~1!"

    call :TrimSpaces status
    echo.
    
    REM Check the requirement status
    if "!status!"=="Required" (
        for /f "tokens=1,2 delims=:" %%X in ('findstr /c:"!requirement!_user:" "%LOG_FILE%"') do (
            set "installed_status=%%Y"
            set "installed_status=!installed_status:~1!"
            REM Loop to trim trailing spaces
            call :TrimSpaces installed_status
            if "!installed_status!"=="Installed" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="3.12" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="3.11" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="3.13" (
                echo !requirement!: Required and Installed
            ) else (
                if "!requirement!"=="QUARC" (
                    echo !requirement!: Required and Missing
                    echo Please check the QUARC Installation Guide or contact Quanser tech support at tech@quanser.com
                    echo Note: Microsoft Visual Studio is a prerequisite for using QUARC. Please Check QUARC compatibility table to download and install the correct version of Microsoft Visual Studio
                    set "missing_requirements=!missing_requirements! !requirement!"
                )
                if "!requirement!"=="QSDK" (
                    echo !requirement!: Missing and Required
                    echo Please download QSDK for Windows from https://github.com/quanser/quanser_sdk_win64
                    echo Please download QSDK for Linux from https://github.com/quanser/quanser_sdk_linux
                    set "missing_requirements=!missing_requirements! !requirement!"
                )
                if "!requirement!"=="QLabs" (
                    echo !requirement!: Missing and Required
                    set "missing_requirements=!missing_requirements! !requirement!"
                )
                if "!requirement!"=="Python" (
                    echo !requirement!: Missing and Required
                    set "missing_requirements=!missing_requirements! !requirement!"
                )
            )
        )
    ) else if "!status!"=="Not Required" (
        for /f "tokens=1,2 delims=:" %%X in ('findstr /c:"!requirement!_user:" "%LOG_FILE%"') do (
            set "installed_status=%%Y"
            set "installed_status=!installed_status:~1!"
            REM Loop to trim trailing spaces
            call :TrimSpaces installed_status
            if "!installed_status!"=="Installed" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="3.12" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="3.11" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="3.13" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else (
                echo !requirement!: Not Required and Missing
            )
        )
    ) else (
        for /f "tokens=1,2 delims=:" %%X in ('findstr /c:"!requirement!_user:" "%LOG_FILE%"') do (
            set "installed_status=%%Y"
            set "installed_status=!installed_status:~1!"
            REM Loop to trim trailing spaces
            call :TrimSpaces installed_status
            if "!installed_status!"=="Installed" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="3.12" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="3.11" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="3.13" (
                echo !requirement!: Optional but is installed
            ) else (
                  echo !requirement!: Optional and is Missing
            )
        )
    )
)

echo.
REM Handle missing requirements
if not "!missing_requirements!"=="" (
    echo [91mMissing Requirements: !missing_requirements![0m
    echo Please install the required software before re-running the script again.
    goto :ending
)

REM Handle not-required installed software
if not "!not_required_installed!"=="" (
    echo [91mInstalled but Not Required: !not_required_installed![0m
    echo Unintall the not required software before re-running the script again.
    goto :ending
)

for /f "tokens=1,* delims=:" %%A in ('findstr /c:"Python_user:" "%LOG_FILE%"') do (
    set "py_ver=%%B"
)

REM Trim leading spaces
set "py_ver=!py_ver:~1!"

REM Installing python whls
::Search for the file that starts with "quanser_api"
for /f "delims=" %%f in ('dir /b /a-d "%QSDK_DIR%python"\quanser_api*') do (
    set FILENAME=%%f
)

echo [93mInstalling Quanser Python API %FILENAME%[0m
py -!py_ver! -m pip install --upgrade pip
py -!py_ver! -m pip install --upgrade --find-links "%QSDK_DIR%python" "%QSDK_DIR%python\%FILENAME%"

goto :setup_environment_variables

rem Setting up environment variables for both Windows and MATLAB
:setup_environment_variables
echo.
echo [93mSetting up Environment Variables[0m
REM Define paths
set "QAL_DIR=%USERPROFILE%\Documents\Quanser"
set "RTMODELS_DIR=%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models"
set "NEW_PYTHON_PATH=%USERPROFILE%\Documents\Quanser\0_libraries\python"
echo.
REM Set QAL_DIR
echo [93mSetting QAL_DIR to: %QAL_DIR%[0m
setx QAL_DIR "%QAL_DIR%"

REM Set RTMODELS_DIR
echo [93mRTMODELS_DIR set to: %RTMODELS_DIR%[0m
setx RTMODELS_DIR "%RTMODELS_DIR%"
echo.

REM Check if PYTHONPATH exists
for /f "tokens=2* delims= " %%a in ('reg query "HKCU\Environment" /v PYTHONPATH 2^>nul') do (
    set "PYTHONPATH=%%b"
)

if defined PYTHONPATH (
    REM If PYTHONPATH exists, add NEW_PYTHON_PATH if not already present
    echo %PYTHONPATH% | find "!NEW_PYTHON_PATH!" >nul
    if errorlevel 1 (
        set "PYTHONPATH=%PYTHONPATH%;!NEW_PYTHON_PATH!"
        echo [93mPYTHONPATH updated: !PYTHONPATH![0m
        setx PYTHONPATH "!PYTHONPATH!"
    ) else (
        echo %NEW_PYTHON_PATH% is already in PYTHONPATH. No changes made.
    )
) else (
    REM If PYTHONPATH does not exist, create it
    echo [93mPYTHONPATH created: !NEW_PYTHON_PATH![0m
    setx PYTHONPATH "!NEW_PYTHON_PATH!"
)
goto :download_from_requirements

REM Download packages from requirements.txt
:download_from_requirements
:: Define the path to requirements.txt
set "REQUIREMENTS_FILE=requirements.txt"

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
echo [93mInstalling packages from %REQUIREMENTS_FILE%...[0m
py -!py_ver! -m pip install -r "%REQUIREMENTS_FILE%"

:: Check the result of the pip install command
if %errorlevel% neq 0 (
    echo [91mSome packages failed to install.[0m
    pause
    exit /b
)
echo.
echo [92mPackages installed successfully.[0m
goto :ending

REM Function to trim trailing spaces
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
echo [92mScript completed.[0m
echo [92mPLEASE RESTART YOUR MACHINE FOR CHANGES TO BE APPLIED.[0m
endlocal
pause