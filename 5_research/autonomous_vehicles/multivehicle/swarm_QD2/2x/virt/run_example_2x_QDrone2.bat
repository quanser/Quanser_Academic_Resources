@echo off

:: Terminate any real time models, close any open consoles
start "Close Console" "taskkill" /im quarc_run.exe
quarc_run -q -Q -t tcpip://localhost:17000 QDrone2_Virtual_0_qd2.rt-win64
quarc_run -q -Q -t tcpip://localhost:17000 QDrone2_Virtual_1_qd2.rt-win64
timeout /t 1 /nobreak > nul

:: Create 2x spawn models for spawning the 2 QDrones
copy /Y %RTMODELS_DIR%\QDrone2\QDrone2_Workspace.rt-win64 rt_models\QDrone2_Virtual_0_qd2.rt-win64 /nobreak > nul
copy /Y %RTMODELS_DIR%\QDrone2\QDrone2_Workspace.rt-win64 rt_models\QDrone2_Virtual_1_qd2.rt-win64 /nobreak > nul

timeout /t 1 /nobreak > nul

:: Set up QLabs environment
python qlabs_setup.py

:: QUARC Console - error/warning/status message monitoring
start "QUARC Console" quarc_run -c -t tcpip://localhost:17000 *.rt-win64
timeout /t 1 /nobreak > nul

:: Start RT/spawn models
quarc_run -D -r -t tcpip://localhost:17000 rt_models/QDrone2_Virtual_0_qd2.rt-win64 -uri tcpip://localhost:17001 -uri_hil tcpip://localhost:18981 -uri_video0 tcpip://localhost:18982^
 -uri_video1 tcpip://localhost:18983 -uri_video2 tcpip://localhost:18984 -uri_video3 tcpip://localhost:18985 -uri_video3d tcpip://localhost:18986 -uri_pose tcpip://localhost:18987 -devicenum 0

quarc_run -D -r -t tcpip://localhost:17000 rt_models/QDrone2_Virtual_1_qd2.rt-win64 -uri tcpip://localhost:17002 -uri_hil tcpip://localhost:18991 -uri_video0 tcpip://localhost:18992^
 -uri_video1 tcpip://localhost:18993 -uri_video2 tcpip://localhost:18994 -uri_video3 tcpip://localhost:18995 -uri_video3d tcpip://localhost:18996 -uri_pose tcpip://localhost:18997 -devicenum 1

timeout /t 2 /nobreak > nul

:: Start User/stabilizer models
quarc_run -D -r -t tcpip://localhost:17000 rt_models\DStack_18981.rt-win64 -uri tcpip://localhost:17003 -URI_Host tcpip://localhost:18001
timeout /t 1 /nobreak > nul

quarc_run -D -r -t tcpip://localhost:17000 rt_models\DStack_18991.rt-win64 -uri tcpip://localhost:17004 -URI_Host tcpip://localhost:18002
timeout /t 1 /nobreak > nul
