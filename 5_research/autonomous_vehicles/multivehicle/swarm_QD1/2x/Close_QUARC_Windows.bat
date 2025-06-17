:: Script to clean up QUARC Console windows and tray monitor icons
::
@REM Kill all QUARC Monitor Tray icons
start "Remove Tray Icon" "%QUARC_DIR%\quarc_tray" /q
timeout /t 1

@REM Close QUARC Console Windows
start "Close Console" "taskkill" /im quarc_run.exe
timeout /t 1
