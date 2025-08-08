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
            ) else if "!installed_status!"=="R2025a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2025b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2023a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2023b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2024a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2024b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2022a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2022b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2021a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2021b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2020a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2020b" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2019a" (
                echo !requirement!: Required and Installed
            ) else if "!installed_status!"=="R2019b" (
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
                if "!requirement!"=="MATLAB/Simulink" (
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
            ) else if "!installed_status!"=="R2025a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2025b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2023a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2023b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2024a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2024b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2022a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2022b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2021a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2021b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2020a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2020b" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2019a" (
                echo !requirement!: Not Required but Installed
                set "not_required_installed=!not_required_installed! !requirement!"
            ) else if "!installed_status!"=="R2019b" (
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
            ) else if "!installed_status!"=="R2025a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2025b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2023a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2023b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2024a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2024b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2022a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2022b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2021a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2021b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2020a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2020b" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2019a" (
                echo !requirement!: Optional but is installed
            ) else if "!installed_status!"=="R2019b" (
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

rem Setting up environment variables for both Windows and MATLAB
:setup_environment_variables
echo.
echo [93mSetting up Environment Variables[0m
REM Define paths
set "QAL_DIR=%USERPROFILE%\Documents\Quanser"
set "RTMODELS_DIR=%USERPROFILE%\Documents\Quanser\0_libraries\resources\rt_models"
echo.
REM Set QAL_DIR
echo [93mSetting QAL_DIR to: %QAL_DIR%[0m
setx QAL_DIR "%QAL_DIR%"

REM Set RTMODELS_DIR
echo [93mRTMODELS_DIR set to: %RTMODELS_DIR%[0m
setx RTMODELS_DIR "%RTMODELS_DIR%"
echo.

REM Define MATLAB base path and versions to check
set "MATLAB_BASE=C:\Program Files\MATLAB"
set "MATLAB_VERSIONS=R2025b R2025a R2024b R2024a R2023b R2023a R2022b R2022a R2021b R2021a R2020b R2020a R2019b R2019a"
set "USER_LIB_PATH=%USERPROFILE%\Documents\Quanser\0_libraries\matlab"
setlocal enabledelayedexpansion
REM Initialize a flag to track if any MATLAB versions are found
set "VERSIONS="
set "FOUND=0"

REM Iterate through each version to check for existence
for %%V in (%MATLAB_VERSIONS%) do (
    if exist "%MATLAB_BASE%\%%V\bin\matlab.exe" (
        echo.
        echo MATLAB version found: %%V
        
        REM Execute the MATLAB command
        ::powershell -Command "Start-Process -FilePath 'matlab' -ArgumentList '-batch \"addpath(''%USER_LIB_PATH%''); savepath; quit;\"' -NoNewWindow"
        start "" "%MATLAB_BASE%\%%V\bin\matlab.exe" -batch "addpath('%USER_LIB_PATH%'); savepath; quit;"
        echo [92mMATLAB path updated for %%V version.[0m
        timeout /t 20
    )
)
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