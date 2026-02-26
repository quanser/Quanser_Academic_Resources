@echo off
setlocal EnableDelayedExpansion
 
echo Opening computer setup documentation...
echo Make sure you have followed the instructions in the website prior to continuing setup.
echo Return to this terminal window once the GitHub page has opened.
echo.
timeout /t 5 >nul
start "" "https://github.com/quanser/Quanser_Academic_Resources/blob/dev-windows/docs/pc_setup.md"
timeout /t 2 >nul

:: color options are here https://learn.microsoft.com/en-us/windows/console/console-virtual-terminal-sequences 

:: Redirect all output to log file
set "LOGFILE=software_requirements.log"

:: Define symbols for the truth table
set "CHECK=1"
set "CROSS=0"
set "QUESTION=*"

:: Initialize variables for the truth table
set "usable_with="
set "QUARC=%QUESTION%"
set "QSDK=%QUESTION%"
set "QLABS=%QUESTION%"
set "MATLAB_SIMULINK=%QUESTION%"
set "PYTHON=%CROSS%"
set "VS=%QUESTION%"
set "RESEARCH_FLAG=%QUESTION%"
set "RESEARCH_TEACH_FLAG=0"

:: empty the log file
echo. > %LOGFILE%

echo Requirements and System Diagnostics Log >> %LOGFILE%
echo ================================ >> %LOGFILE%


::  Check for quarc dir existing
set "quarc_dir=C:\Program Files\Quanser\QUARC\lib"
if exist "%quarc_dir%" ( set "QUARC=%CHECK%") else ( set "QUARC=%CROSS%")

::  Check for qsdk dir existing
set "qsdk_dir=C:\Program Files\Quanser\Quanser SDK"
if exist "%qsdk_dir%" ( set "QSDK=%CHECK%") else ( set "QSDK=%CROSS%")

::if quarc exists, we assume qsdk also exiscmdts
if "%QUARC%"=="%CHECK%" set "QSDK=%CHECK%"

:: Check if qlabs exists
set "qlabs_dir=C:\Program Files\Quanser\Quanser Interactive Labs"
if exist "%qlabs_dir%" ( set "QLABS=%CHECK%") else ( set "QLABS=%CROSS%")

:: Define the MATLAB installation directory and versions to check
set "matlab_dir=C:\Program Files\MATLAB"
set "versions=R2026a R2025b R2025a R2024b R2024a R2023b R2023a R2022b R2022a R2021b R2021a R2020b R2020a R2019b R2019a R2018b R2018a"

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

:: List all installed Python versions and check backwards from python 3.14 till 3.11
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

:: Display what is needed depending on the use case 

echo The following table shows the requirements depending on usage. 
echo [92mNote that if are using both MATLAB/Simulink and Python, with Quanser's hardware 
echo you only need the QUARC software, it installs Quanser SDK (QSDK) that supports Python.[0m   
echo +-----------------+-------+------+-------+-----------------+--------+
echo ^|                 ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +-----------------+-------+------+-------+-----------------+--------+
echo ^| MATLAB Hardware ^|   1   ^|  -   ^|   -   ^|         1       ^|    -   ^|
echo +-----------------+-------+------+-------+-----------------+--------+
echo ^| MATLAB Virtual  ^|   0   ^|  -   ^|   1   ^|         1       ^|    -   ^|
echo +-----------------+-------+------+-------+-----------------+--------+
echo ^| Python Hardware ^|   -   ^|  1   ^|   -   ^|         -       ^|    1   ^|
echo +-----------------+-------+------+-------+-----------------+--------+
echo ^| Python Virtual  ^|   -   ^|  1   ^|   1   ^|         -       ^|    1   ^|
echo +-----------------+-------+------+-------+-----------------+--------+
echo For more detailed info and download links, ctrl + click the following link: [94mhttps://www.quanser.com/pcsetup[0m 
echo.

timeout /t 1 >nul

:: Check Local systems variables already available
::echo Checking installs in the local machine and logging system state to [96m%LOGFILE%[0m ...

::timeout /t 1 >nul

:: Logging information 
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

timeout /t 1 >nul

if "%PYTHON%"=="0" (
    set "PYTHON= 0  "
)

if "%MATLAB_SIMULINK%"=="0" (
    set "MATLAB_SIMULINK=   0  "
)

:: Function to display what is in the current device
:display_system_table

echo System check complete. System state logged in [96m%LOGFILE%[0m ...
echo.
echo The following table shows what is installed on your system:
echo +-------------+-------+------+-------+-----------------+--------+
echo ^|             ^| QUARC ^| QSDK ^| QLabs ^| MATLAB/Simulink ^| Python ^|
echo +-------------+-------+------+-------+-----------------+--------+
echo ^| Your System ^|   %QUARC%   ^|  %QSDK%   ^|   %QLABS%   ^|      %MATLAB_SIMULINK%     ^|  %PYTHON%  ^|
echo +-------------+-------+------+-------+-----------------+--------+
echo.

timeout /t 2 >nul

:: MATLAB Requirements
if not "%MATLAB_SIMULINK%"=="0" (
    if "%QUARC%"=="1" (
        set "usable_with=!usable_with! MATLAB Hardware," 
    )
    if "%QLABS%"=="1" (
        set "usable_with=!usable_with! MATLAB Virtual,"
    )
)

:: Python Requirements
if "%QSDK%"=="1" (
    if not "%PYTHON%"=="0" (
        set "usable_with=!usable_with! Python Hardware,"
        if "%QLABS%"=="1" (
            set "usable_with=!usable_with! Python Virtual,"
        )
    )
)

if not "!usable_with!"=="" (
    set "trimmed=!usable_with:~0,-1!"
    echo [92mYour system supports:!trimmed!.[0m
) else (
    echo [91mYour system does not support any of the available use cases. Refer to the tables above for more information.[0m
)
echo.

goto :sys_diag_complete


:sys_diag_complete

echo [92mDepending on the language you will use, please run configure_matlab and/or configure_python. [0m
echo. >> %LOGFILE%
pause