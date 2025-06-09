::   use this when you want to stop controlling the traffic light through stream. 
::   Refer to user_manuals/traffic_light for more information.

@echo off
set /p ip="Enter the IP address (e.g., 192.168.2.3): "

rem Perform the curl request and capture the output
for /f %%i in ('curl -s -o nul -w "%%{http_code}" http://%ip%:5000/close_stream') do set STATUS=%%i

echo Response Code: %STATUS%

rem Check if the request was successful
if "%STATUS%"=="200" (
    echo Stream stopped successfully. Serial connection is back up.
) else (
    echo Failed to stop the stream. Please check the IP address or network connection.
)

echo:
pause