setlocal enabledelayedexpansion
@echo off
set "desktopPath=%USERPROFILE%\Desktop"
for /l %%Q in (1, 1, 5) do (
    set "port=1869%%Q%"
    start "YOLO client %%Q%" /b pythonw yolo_client.py -p !port!
    timeout /t 1
)
