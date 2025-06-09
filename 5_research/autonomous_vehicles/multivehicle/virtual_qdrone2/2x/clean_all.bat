:: Run this script to Terminate any real time models, and close any open consoles
start "Close Console" "taskkill" /im quarc_run.exe /nobreak > nul
quarc_run -q -Q -t tcpip://localhost:17000 *.rt-win64 /nobreak > nul
timeout /t 1 /nobreak > nul