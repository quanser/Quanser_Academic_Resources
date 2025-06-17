# This script is used to setup the Quanser Interactive Labs (QLabs) workspace
# for a virtual QDrone2.
import sys
import os
sys.path.insert(0, "../")

from pal.resources import rtmodels
from qvl.real_time import QLabsRealTime
import sys
import time


########### Main program #################
PORTS = {"host": "18002",
        "joystick": "18003",
        "traj": "18004"}

# Set the last digit of the IP address for the ground station PC and QDrone2.
# Your ground PC could be the PC connected to your Optitrack system or a
# separate device if using VRPN.
# Note that if using VRPN, you would need to ensure the VRPN Client block in
# the MissionServerVRPN.slx has the IP pointing to the GroundPC IP address,
# and then recompile the model to an RT model file.
IPs = {"GroundPC": "192.168.2.56",
        "QDrone2": "192.168.2.12"}

# Set to 1 if you intend to use VRPN to fly the physical drone
USE_VRPN = 1


def clean_up():
    """
    Close all RT models and consoles
    """
    os.system("taskkill /f /im quarc_run.exe 1>nul 2>&1")
    os.system("taskkill /f /im qlabs_vrpn_server.exe 1>nul 2>&1")
    QLabsRealTime().terminate_all_real_time_models()


def main():

    # Stop any existing realtime models, close consoles, and refresh QLabs
    clean_up()

    # start a console for the Ground station PC
    os.system('start "QUARC PC Console" "quarc_run" -c -t tcpip://{}:17000 *.rt-win64'.format(IPs["GroundPC"]))
    time.sleep(2)

    # start a console for the Qdrone2
    os.system('start "Drone_1_console" "quarc_run" -c -t tcpip://{}:17000 *.rt-linux_qdrone2'.format(IPs["QDrone2"]))
    time.sleep(3)

if __name__ == "__main__":
    main()