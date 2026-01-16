@echo off
setlocal EnableDelayedExpansion

:: Redirect all output to log file
set "LOGFILE=software_requirements.log"

:: Define symbols for the truth table
set "CHECK=1"
set "CROSS=0"
set "QUESTION=*"

:: Initialize variables for the truth table
set "QUARC=%QUESTION%"
set "QSDK=%QUESTION%"
set "QLABS=%QUESTION%"
set "MATLAB_SIMULINK=%QUESTION%"
set "PYTHON=%CROSS%"
set "VS=%QUESTION%"
set "RESEARCH_FLAG=%QUESTION%"
set "RESEARCH_TEACH_FLAG=0"

@REM :: Prompt for downloading the content resources
@REM :resource_choice
@REM echo Choose the resources you want to download:
@REM echo 1. Teaching Resources only
@REM echo 2. Research Resources only
@REM echo 3. Both Teaching and Research Resources
@REM set /p resources="Enter choice (1/2/3): "
@REM echo.
echo. > %LOGFILE%
@REM echo ================================ >> %LOGFILE%
@REM if "%resources%"=="1" echo Content to Download: Teaching Resources >> %LOGFILE%
@REM if "%resources%"=="2" echo Content to Download: Research Resources >> %LOGFILE%
@REM if "%resources%"=="3" echo Content to Download: Teaching Resources, Research Resources >> %LOGFILE%

@REM if "%resources%"=="1" echo You selected: [92mTeaching Resources only[0m
@REM if "%resources%"=="2" echo You selected: [92mResearch Resources only[0m
@REM if "%resources%"=="3" echo You selected: [92mBoth Teaching and Research Resources[0m
@REM echo.

@REM if "%resources%"=="3" set "RESEARCH_TEACH_FLAG=1"
@REM if "%resources%"=="1" goto :product_choice
@REM if "%resources%"=="2" goto :Reseach_only_python_matlab
@REM if "%resources%"=="3" goto :product_choice

@REM echo [91mInvalid choice. Please try again.[0m
@REM goto resource_choice

@REM :: Prompt for Product selection
@REM :product_choice
@REM set "VALID_OPTIONS=1 2 3"
@REM :: Display available products in a table format

@REM echo +-----------------------------------------------------------------------+
@REM echo ^|[93m                           Available Products                          [0m^| 
@REM echo +-----------------------------------------------------------------------+
@REM echo ^| [1] 1_Controls (Qube-Servo 3, Aero 2)                                 ^|
@REM echo ^| [2] 2_Robotics (QArm, QBot Platform)                                  ^|
@REM echo ^| [3] 3_Autonomous_System (QCar 2, QDrone 2)                            ^|
@REM echo +-----------------------------------------------------------------------+
@REM echo.

@REM :: Prompt user for product selection
@REM echo Please select one or more products by entering their numbers, separated by spaces.
@REM echo For example: 1 3
@REM set /p "USER_SELECTION=Enter your selection(s): "

@REM :: Check if input is empty
@REM if "%USER_SELECTION%"=="" (
@REM     echo [91mNo input provided. Please try again.[0m
@REM     echo.
@REM     goto :product_choice
@REM )

@REM :: Validate user input
@REM set "INVALID=0"
@REM for %%i in (%USER_SELECTION%) do (
@REM     set "FOUND=0"
@REM     for %%j in (%VALID_OPTIONS%) do (
@REM         if "%%i"=="%%j" set "FOUND=1"
@REM     )
@REM     if !FOUND! == 0 (
@REM         echo [91mInvalid selection - "%%i"[0m
@REM         set "INVALID=1"
@REM     )
@REM )

@REM :: If invalid input is found, prompt again
@REM if %INVALID%==1 (
@REM     echo Please enter only valid product numbers.
@REM     echo.
@REM     goto :product_choice
@REM )

@REM :: Parse user input and set corresponding product variables
@REM set "PRODUCT_SELECTION="
@REM for %%i in (%USER_SELECTION%) do (
@REM     if %%i==1 set "PRODUCT_SELECTION=!PRODUCT_SELECTION!1_Controls, "
@REM     if %%i==2 set "PRODUCT_SELECTION=!PRODUCT_SELECTION!2_Robotics, "
@REM     if %%i==3 set "PRODUCT_SELECTION=!PRODUCT_SELECTION!3_Autonomous_System, "
@REM )

@REM :: Trim the trailing comma and space
@REM set "PRODUCT_SELECTION=%PRODUCT_SELECTION:~0,-2%"

@REM :: Display selected products
@REM echo.
@REM echo You selected: [92m%PRODUCT_SELECTION%[0m
@REM echo User Product Selection: %PRODUCT_SELECTION% >> %LOGFILE%
@REM echo. >>  %LOGFILE%
@REM echo.

@REM if "%resources%"=="1" goto :software_choice
@REM if "%resources%"=="3" goto :check_reseach_student_matlab

@REM :: Check Matlab usage for when user selects Research and Student Content option
@REM :check_reseach_student_matlab
@REM echo Requirements and System Diagnostics Log >> %LOGFILE%
@REM echo ================================ >> %LOGFILE%
@REM if "!RESEARCH_TEACH_FLAG!" NEQ "0" (
@REM     echo Note: Python is a requirement with Research Content
@REM     set /p "matlab_option=Do you want to use MATLAB for Student/Research Content? (y/n): "
@REM     echo.

@REM     if "!matlab_option!"=="y" goto matlab_python_options
@REM     if "!matlab_option!"=="n" goto python_options
@REM ) else (
@REM     goto software_choice
@REM )

@REM echo [91mInvalid choice. Please try again.[0m
@REM goto check_reseach_student_matlab

:: Prompt for software choice
:software_choice
echo Choose the software you want to use:
echo 1. Python only
echo 2. MATLAB only
echo 3. Both Python and MATLAB
set /p software="Enter choice (1/2/3): "
echo.

echo Requirements and System Diagnostics Log >> %LOGFILE%
echo ================================ >> %LOGFILE%

if "%software%"=="1" echo You selected: [92mPython only[0m
if "%software%"=="2" echo You selected: [92mMATLAB only[0m
if "%software%"=="3" echo You selected: [92mBoth Python and MATLAB[0m
echo.

if "%software%"=="1" goto python_options
if "%software%"=="2" goto matlab_options
if "%software%"=="3" goto matlab_python_options

echo [91mInvalid choice. Please try again.[0m
goto software_choice

:: Python Options
:python_options
echo Choose your Device usage:
echo 1. Virtual only
echo 2. Hardware only
echo 3. Both virtual and hardware
set /p python_usage="Enter choice (1/2/3): "
echo.

if "%python_usage%"=="1" echo You selected: [92mVirtual only[0m
if "%python_usage%"=="2" echo You selected: [92mHardware only[0m
if "%python_usage%"=="3" echo You selected: [92mBoth virtual and hardware[0m
echo.

if "%python_usage%"=="1" goto check_python_virtual
if "%python_usage%"=="2" goto check_python_hardware
if "%python_usage%"=="3" goto check_python_both

echo [91mInvalid choice. Please try again.[0m
goto python_options

:: MATLAB Options
:matlab_options
echo Choose your Device usage:
echo 1. Virtual only
echo 2. Hardware only
echo 3. Both virtual and hardware
set /p matlab_usage="Enter choice (1/2/3): "
echo.

if "%matlab_usage%"=="1" echo You selected: [92mVirtual only[0m
if "%matlab_usage%"=="2" echo You selected: [92mHardware only[0m
if "%matlab_usage%"=="3" echo You selected: [92mBoth virtual and hardware[0m
echo.

if "%matlab_usage%"=="1" goto check_matlab_virtual
if "%matlab_usage%"=="2" goto check_matlab_hardware
if "%matlab_usage%"=="3" goto check_matlab_both

echo [91mInvalid choice. Please try again.[0m
goto matlab_options

:: MATLAB and Python Options

:matlab_python_options
echo Choose your Device usage:
echo 1. Virtual only
echo 2. Hardware only
echo 3. Both virtual and hardware
set /p matlab_py_usage="Enter choice (1/2/3): "
echo.

if "%matlab_py_usage%"=="1" echo You selected: [92mVirtual only[0m
if "%matlab_py_usage%"=="2" echo You selected: [92mHardware only[0m
if "%matlab_py_usage%"=="3" echo You selected: [92mBoth virtual and hardware[0m
echo.

if "%matlab_py_usage%"=="1" goto check_matlab_python_virtual
if "%matlab_py_usage%"=="2" goto check_matlab_python_hardware
if "%matlab_py_usage%"=="3" goto check_matlab_python_both

echo [91mInvalid choice. Please try again.[0m
goto matlab_python_options

:: Check Python Virtual Only
:check_python_virtual
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Virtual"
set "QUARC_REQ=*"
set "QSDK_REQ=1"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=*"
set "PYTHON_REQ=1"

echo Requirements for Python Virtual only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=Python"
echo ^| %LANGUAGE%   ^| %PLATFORM%  ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Optional >> %LOGFILE%
echo QSDK: Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Optional >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete
 

:: Check Python Hardware Only
:check_python_hardware
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Hardware"
set "QUARC_REQ=*"
set "QSDK_REQ=1"
set "QLABS_REQ=*"
set "MAT_SIM_REQ=*"
set "PYTHON_REQ=1"

echo Requirements for Python Hardware only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=Python"
echo ^| %LANGUAGE%   ^| %PLATFORM% ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Optional >> %LOGFILE%
echo QSDK: Required >> %LOGFILE%
echo QLabs: Optional >> %LOGFILE%
echo MATLAB/Simulink: Optional >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check Python Both (Virtual + Hardware)
:check_python_both
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Both"
set "QUARC_REQ=*"
set "QSDK_REQ=1"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=*"
set "PYTHON_REQ=1"

echo Requirements for Python Hardware and Virtual...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=Python"
echo ^| %LANGUAGE%   ^|   %PLATFORM%   ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: Hardware, Virtual >> %LOGFILE%
echo QUARC: Optional >> %LOGFILE%
echo QSDK: Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Optional >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check MATLAB Virtual Only
:check_matlab_virtual
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Virtual"
set "QUARC_REQ=0"
set "QSDK_REQ=0"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=*"

echo Requirements for MATLAB Virtual only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=MATSIM"
echo ^| %LANGUAGE%   ^| %PLATFORM%  ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Not Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Optional >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check MATLAB Hardware Only
:check_matlab_hardware
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Hardware"
set "QUARC_REQ=1"
set "QSDK_REQ=0"
set "QLABS_REQ=*"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=*"

echo Requirements for MATLAB Hardware only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=MATSIM"
echo ^| %LANGUAGE%   ^| %PLATFORM% ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Optional >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Optional >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check MATLAB Both (Virtual + Hardware)
:check_matlab_both
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Both"
set "QUARC_REQ=1"
set "QSDK_REQ=0"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=*"

echo Requirements for MATLAB both Virtual and Hardware...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=MATSIM"
echo ^| %LANGUAGE%   ^|   %PLATFORM%   ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: %LANGUAGE% >> %LOGFILE%
echo Platform: Hardware, Virtual >> %LOGFILE%
echo QUARC: Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Optional >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check Python + MATLAB Virtual Only
:check_matlab_python_virtual
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Virtual"
set "QUARC_REQ=0"
set "QSDK_REQ=1"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=1"

echo Requirements for Python and MATLAB Virtual only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=PY^&MAT "
echo ^| %LANGUAGE%  ^| %PLATFORM%  ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: Python, Mat/Sim >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Not Required >> %LOGFILE%
echo QSDK: Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check Python + MATLAB Hardware Only
:check_matlab_python_hardware
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Hardware"
set "QUARC_REQ=1"
set "QSDK_REQ=0"
set "QLABS_REQ=*"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=1"

echo Requirements for Python and MATLAB Hardware only...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=PY^&MAT"
echo ^| %LANGUAGE%   ^| %PLATFORM% ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: Python, Mat/Sim >> %LOGFILE%
echo Platform: %PLATFORM% >> %LOGFILE%
echo QUARC: Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Optional >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check Python + MATLAB Both (Virtual + Hardware)
:check_matlab_python_both
call :legend
echo [93mChecking system... please wait...[0m
timeout /t 3 >nul
echo.
set "PLATFORM=Both"
set "QUARC_REQ=1"
set "QSDK_REQ=0"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=1"

echo Requirements for Python and MATLAB both Virtual and Hardware...
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=PY^&MAT"
echo ^| %LANGUAGE%   ^|   %PLATFORM%   ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo Language: Python, Mat/Sim >> %LOGFILE%
echo Platform: Hardware, Virtual >> %LOGFILE%
echo QUARC: Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
goto :sys_diag_complete

:: Check Local systems variables already available
:check_local_system
set CHECK_FAIL=0 
echo Checking what is presently installed in the Local Machine...
::call :check_var QUARC_DIR QUARC
set "quarc_dir=C:\Program Files\Quanser\QUARC\quarc_run.exe"
if exist "%quarc_dir%" ( set "QUARC=%CHECK%") else ( set "QUARC=%CROSS%")
::call :check_var QSDK_DIR QSDK
set "qsdk_dir=C:\Program Files\Quanser\Quanser SDK"
if exist "%qsdk_dir%" ( set "QSDK=%CHECK%") else ( set "QSDK=%CROSS%")

::Check if Lang is Python, users has QUARC installed, set QSDK to 1
if "%LANGUAGE%"=="Python" if "%QUARC%"=="%CHECK%" set "QSDK=%CHECK%"
::Check if Research flag is set to one, QUARC is 1 then QSDK is 1
::if "%RESEARCH_FLAG%"=="1" set "QSDK=%CHECK%"

:: Define the QLABS directory path
set "qlabs_dir=C:\Program Files\Quanser\Quanser Interactive Labs"
if exist "%qlabs_dir%" ( set "QLABS=%CHECK%") else ( set "QLABS=%CROSS%")

:: Define the MATLAB installation directory and versions to check
set "matlab_dir=C:\Program Files\MATLAB"
set "versions=R2025b R2025a R2024b R2024a R2023b R2023a R2022b R2022a R2021b R2021a R2020b R2020a R2019b R2019a"

:: Loop through versions and check if they exist
for %%v in (%versions%) do (
    if exist "%matlab_dir%\%%v\bin\matlab.exe" ( set "MATLAB_SIMULINK=%%v" & goto :next) else ( set "MATLAB_SIMULINK=%CROSS%")
)

:next

set "vs_dir_2022=C:\Program Files\Microsoft Visual Studio\2022"
if exist "%vs_dir_2022%" (set "VS=2022" & goto :next1) else (set "VS=%CROSS%")

:: Define the VS directory path
set "vs_dir=C:\Program Files (x86)\Microsoft Visual Studio"
set "version=2019 2017 2015"

:: Loop through versions and check if they exist
for %%v in (%version%) do (
    if exist "%vs_dir%\%%v" (set "VS=%%v" & goto :next1) else (set "VS=%CROSS%")
)


:next1

:: List all installed Python versions
for /f "tokens=2 delims=:" %%v in ('py -0 2^>nul') do (
    for /f "tokens=1,2 delims=. " %%a in ("%%v") do (
        set "MINOR=%%b"
        :: Extract only the first two characters
        set "MINOR=!MINOR:~0,2!"  

        if %%a equ 3 (
            if "!MINOR!"=="14" (set "PYTHON=3.14" & goto :FOUND)
            if "!MINOR!"=="13" (set "PYTHON=3.13" & goto :FOUND)
            if "!MINOR!"=="12" (set "PYTHON=3.12" & goto :FOUND)
            if "!MINOR!"=="11" (set "PYTHON=3.11" & goto :FOUND)
        )
    )
)

:FOUND
::echo Python Version Found: %PYTHON%

:: Logging information before changing Colors
echo. >> %LOGFILE%
echo User System >> %LOGFILE%
echo ================================ >> %LOGFILE%

if "%QUARC%"=="1" (
    echo QUARC_user: Installed >> %LOGFILE%
) else (
    echo QUARC_user: Not Installed >> %LOGFILE%
)
if "%QSDK%"=="1" (
    echo QSDK_user: Installed >> %LOGFILE%
) else (
    echo QSDK_user: Not Installed >> %LOGFILE%
)
if "%QLABS%"=="1" (
    echo QLabs_user: Installed >> %LOGFILE%
) else (
    echo QLabs_user: Not Installed >> %LOGFILE%
)
if "%MATLAB_SIMULINK%"=="0" (
    echo MATLAB/Simulink_user: Not Installed >> %LOGFILE%
) else (
    echo MATLAB/Simulink_user: %MATLAB_SIMULINK% >> %LOGFILE%
)
if "%PYTHON%"=="0" (
    echo Python_user: Not Installed >> %LOGFILE%
) else (
    echo Python_user: %PYTHON% >> %LOGFILE%
)
if "%VS%"=="0" (
    echo Visual Studio_user: Not Installed >> %LOGFILE%
) else (
    echo Visual Studio_user: %VS% >> %LOGFILE%
)

:: Compare QUARC with requirements table and update color
if "%QUARC_REQ%"=="1" (
    if "%QUARC%"=="1" (
        :: Set color to GREEN
        set QUARC=[92m%QUARC%[0m
    ) else if "%QUARC%"=="0" (
        :: Set color to RED
        set QUARC=[91m%QUARC%[0m
        set "CHECK_FAIL=1"
    )
) else if "%QUARC_REQ%"=="*" (
    if "%QUARC%"=="1" (
        :: Set color to GREEN
        set QUARC=[92m%QUARC%[0m
    ) else if "%QUARC%"=="0" (
        :: Color is not set
        set QUARC=%QUARC%
    ) 
) else if "%QUARC_REQ%"=="0" (
    if "%QUARC%"=="1" (
        :: Set color to RED
        set QUARC=[91m%QUARC%[0m
        set "CHECK_FAIL=1"
    ) else if "%QUARC%"=="0" (
        :: Set Color to GREEN
        set QUARC=[92m%QUARC%[0m
    ) 
)

:: Compare QSDK with requirements table and update color
if "%QSDK_REQ%"=="1" (
    if "%QSDK%"=="1" (
        :: Set color to GREEN
        set QSDK=[92m%QSDK%[0m
    ) else if "%QSDK%"=="0" (
        :: Set color to RED
        set QSDK=[91m%QSDK%[0m
        set "CHECK_FAIL=1"
    )
) else if "%QSDK_REQ%"=="*" (
    if "%QSDK%"=="1" (
        :: Set color to GREEN
        set QSDK=[92m%QSDK%[0m
    ) else if "%QSDK%"=="0" (
        :: Color is not set
        set QSDK=%QSDK%
    ) 
) else if "%QSDK_REQ%"=="0" (
    if "%QSDK%"=="1" (
        :: Set color to RED
        set QSDK=[91m%QSDK%[0m
        set "CHECK_FAIL=1"
    ) else if "%QSDK%"=="0" (
        :: Set Color to GREEN
        set QSDK=[92m%QSDK%[0m
    ) 
)

:: Compare QLABS with requirements table and update color
if "%QLABS_REQ%"=="1" (
    if "%QLABS%"=="1" (
        :: Set color to GREEN
        set QLABS=[92m%QLABS%[0m
    ) else if "%QLABS%"=="0" (
        :: Set color to RED
        set QLABS=[91m%QLABS%[0m
        set "CHECK_FAIL=1"
    )
) else if "%QLABS_REQ%"=="*" (
    if "%QLABS%"=="1" (
        :: Set color to GREEN
        set QLABS=[92m%QLABS%[0m
    ) else if "%QLABS%"=="0" (
        :: Color is not set
        set QLABS=%QLABS%
    ) 
) else if "%QLABS_REQ%"=="0" (
    if "%QLABS%"=="1" (
        :: Set color to RED
        set QLABS=[91m%QLABS%[0m
        set "CHECK_FAIL=1"
    ) else if "%QLABS%"=="0" (
        :: Set Color to GREEN
        set QLABS=[92m%QLABS%[0m
    ) 
)

:: Compare MATLAB_SIMULINK with requirements table and update color
if "%MAT_SIM_REQ%"=="1" (
    if "%MATLAB_SIMULINK%" NEQ "0" (
        :: Set color to GREEN
        set MATLAB_SIMULINK=[92m%MATLAB_SIMULINK%[0m
    ) else if "%MATLAB_SIMULINK%"=="0" (
        :: Set color to RED
        set MATLAB_SIMULINK=[91m%MATLAB_SIMULINK%[0m
        set "CHECK_FAIL=1"
    )
) else if "%MAT_SIM_REQ%"=="*" (
    if "%MATLAB_SIMULINK%" NEQ "0" (
        :: Set color to GREEN
        set MATLAB_SIMULINK=[92m%MATLAB_SIMULINK%[0m
    ) else if "%MATLAB_SIMULINK%"=="0" (
        :: Color is not set
        set MATLAB_SIMULINK=%MATLAB_SIMULINK%
    ) 
) else if "%MAT_SIM_REQ%"=="0" (
    if "%MATLAB_SIMULINK%" NEQ "0" (
        :: Set color to RED
        set MATLAB_SIMULINK=[91m%MATLAB_SIMULINK%[0m
        set "CHECK_FAIL=1"
    ) else if "%MATLAB_SIMULINK%"=="0" (
        :: Set Color to GREEN
        set MATLAB_SIMULINK=[92m%MATLAB_SIMULINK%[0m
    ) 
)

:: Compare PYTHON with requirements table and update color
if "%PYTHON_REQ%"=="1" (
    if "%PYTHON%" NEQ "0" (
        :: Set color to GREEN
        set PYTHON=[92m%PYTHON%[0m
    ) else if "%PYTHON%"=="0" (
        :: Set color to RED
        set PYTHON=[91m%PYTHON%[0m
        set "CHECK_FAIL=1"
    )
) else if "%PYTHON_REQ%"=="*" (
    if "%PYTHON%" NEQ "0" (
        :: Set color to GREEN
        set PYTHON=[92m%PYTHON%[0m
    ) else if "%PYTHON%"=="0" (
        :: Color is not set
        set PYTHON=%PYTHON%
    ) 
) else if "%PYTHON_REQ%"=="0" (
    if "%PYTHON%" NEQ "0" (
        :: Set color to RED
        set PYTHON=[91m%PYTHON%[0m
        set "CHECK_FAIL=1"
    ) else if "%PYTHON%"=="0" (
        :: Set Color to GREEN
        set PYTHON=[92m%PYTHON%[0m
    ) 
)


call :display_system_table
goto :eof

:: Function to check if environment variables exist
:check_var
set "value=!%1!"
if "!value!"=="" (
    set "%2=%CROSS%"
) else (
    set "%2=%CHECK%"
)
goto :eof

:: Function to display Python truth table
:display_system_table
echo.
set "LANGUAGE=N/A"
set "PLATFORM=N/A"
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^|    %LANGUAGE%   ^|    %PLATFORM%   ^|   %QUARC%   ^|  %QSDK%   ^|   %QLABS%   ^|      %MATLAB_SIMULINK%     ^|  %PYTHON%  ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
goto :eof

:: Display LEGEND
:legend
::color 0E
echo +-----------------------------------------------------------------------+
echo ^|                               [93mLEGEND[0m                                  ^|
echo +-----------------------------------------------------------------------+
echo ^|  0 - Not required                                                     ^|
echo ^|  1 - Required                                                         ^|
echo ^|  * - Optional                                                         ^|
echo +-----------------------------------------------------------------------+
echo.
goto :eof

:tee
echo %* 
echo %* >> %LOGFILE%
goto :eof

:Reseach_only_python_matlab
call :legend
echo Research Content Requirements...
set "PLATFORM=HW ^& VIR"
set "QUARC_REQ=1"
set "QSDK_REQ=0"
set "QLABS_REQ=1"
set "MAT_SIM_REQ=1"
set "PYTHON_REQ=1"

set "RESEARCH_FLAG=1"
echo.
echo +----------+----------+-------+------+-------+-----------------+--------+
echo ^| Language ^| Platform ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
set "LANGUAGE=PY^&MAT"
echo ^| %LANGUAGE%   ^| %PLATFORM% ^|   %QUARC_REQ%   ^|  %QSDK_REQ%   ^|   %QLABS_REQ%   ^|        %MAT_SIM_REQ%        ^|    %PYTHON_REQ%   ^|
echo +----------+----------+-------+------+-------+-----------------+--------+
echo.
echo. >> %LOGFILE%
echo Requirements and System Diagnostics Log >> %LOGFILE%
echo ================================ >> %LOGFILE%
echo Language: Python, Mat/Sim >> %LOGFILE%
echo Platform: Hardware, Virtual >> %LOGFILE%
echo QUARC: Required >> %LOGFILE%
echo QSDK: Not Required >> %LOGFILE%
echo QLabs: Required >> %LOGFILE%
echo MATLAB/Simulink: Required >> %LOGFILE%
echo Python: Required >> %LOGFILE%

call :check_local_system
echo To install QSDK, Please visit: https://github.com/quanser/quanser_sdk_win64
echo To install QUARC, Please contact Quanser Tech Support, tech@quanser.com
echo. 
goto :sys_diag_complete


:sys_diag_complete
if "%CHECK_FAIL%"=="1" (
    echo [91mSystem Diagnosis Complete.[0m
    echo [91mPlease note that your system may not have all the required software installed.[0m
    echo For futher assistance, please contact Quanser Tech Support, tech@quanser.com
    echo.
    echo. >> %LOGFILE%
    echo STATUS: FAILED >> %LOGFILE% 
    pause
) else (
    echo [92mSystem Diagnosis Complete. 
    echo Please run the necessary setup files.[0m
    echo.
    echo. >> %LOGFILE%
    echo STATUS: PASSED >> %LOGFILE% 
    pause
)