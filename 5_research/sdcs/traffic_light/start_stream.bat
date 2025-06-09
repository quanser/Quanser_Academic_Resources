::   use this when you want to control the traffic light through stream. 
::   Refer to user_manuals/traffic_light for more information.

@echo off
set /p ip="Enter the IP address (e.g., 192.168.2.3): "

rem Perform the curl request and capture the output
for /f %%i in ('curl -s -o nul -w "%%{http_code}" http://%ip%:5000/start_stream') do set STATUS=%%i

echo Response Code: %STATUS%

rem Check if the request was successful
if "%STATUS%"=="200" (
    echo Stream started successfully.
) else (
    echo Failed to start stream. Please check the IP address or if the Traffic light is connected to the correct network.
)

echo:
pause