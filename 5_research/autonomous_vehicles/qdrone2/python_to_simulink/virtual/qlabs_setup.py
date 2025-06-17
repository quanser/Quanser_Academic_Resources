# This script is used to setup the Quanser Interactive Labs (QLabs) workspace
# for a virtual QDrone2.
import sys
import os
sys.path.insert(0, "../")

from pal.resources import rtmodels
from qvl.qlabs import QuanserInteractiveLabs
from qvl.qdrone2 import QLabsQDrone2
from qvl.real_time import QLabsRealTime
import sys
import time

QuanserAppsRoot = os.environ["QAL_DIR"]
VRPN_SERVER = os.path.normpath(
    os.path.join(QuanserAppsRoot,
    "0_libraries/resources/applications/QLabsVRPNServer/qlabs_vrpn_server.exe"))


########### Main program #################
PORTS = {"hil"      : "18981",
        "video0"    : "18982",
        "video1"    : "18983",
        "video2"    : "18984",
        "video3"    : "18985",
        "video3d"   : "18986",
        "pose"      : "18800",
        "host"      : "18002",
        "joystick"  : "18003",
        "traj"      : "18004"}

# Set to 1 if you intend to use VRPN to fly the physical drone
USE_VRPN = 0


def clean_up():
    """
    Close all RT models and consoles
    """
    os.system("taskkill /f /im quarc_run.exe 1>nul 2>&1")
    os.system("taskkill /f /im qlabs_vrpn_server.exe 1>nul 2>&1")
    QLabsRealTime().terminate_all_real_time_models()


def main():

    qlabs = QuanserInteractiveLabs()

    print("Connecting to QLabs...")
    if (not qlabs.open("localhost")):
        print("Unable to connect to QLabs")
        return    

    print("Connected")

    # clear the existing Qlabs workspace
    qlabs.destroy_all_spawned_actors()

    # Stop any existing realtime models, close consoles, and refresh QLabs
    clean_up()

    # spawn a virtual qdrone2 a the origin 0, 0, 0 with orientation 0.0, 0.0, 0.0
    hQDrone = QLabsQDrone2(qlabs, True)
    hQDrone.actorNumber=0
    hQDrone.destroy()
    hQDrone.spawn_id_degrees(actorNumber=0, location=[0, 0, 0], rotation=[0, 0, 0], scale=[1,1,1], configuration=0)
    hQDrone.possess(hQDrone.VIEWPOINT_TRAILING)

    # Set number of drones. Note that this example only supports 1 drone.
    num_drones = 1

    # start a console
    os.system('start "QUARC Console" "quarc_run" -c -t tcpip://localhost:17000 *.rt-win64')

    # start Qdrone2 workspace model. For testing, change path to where spawn model is located
    model_path = rtmodels.QDRONE2 # Your 'RTMODELS_DIR' system environment variable must be set correctly.
    hil     = "-uri_hil tcpip://localhost:{}".format(PORTS["hil"])
    pose    = "-uri_pose tcpip://localhost:{}".format(PORTS["pose"])
    video0  = "-uri_video0 tcpip://localhost:{}".format(PORTS["video0"])
    video1  = "-uri_video1 tcpip://localhost:{}".format(PORTS["video1"])
    video2  = "-uri_video2 tcpip://localhost:{}".format(PORTS["video2"])
    video3  = "-uri_video3 tcpip://localhost:{}".format(PORTS["video3"])
    video3d = "-uri_video3d tcpip://localhost:{}".format(PORTS["video3d"])

    additional_args = "".join("{} {} {} {} {} {} {}".format(hil, pose, video0, video1, video2, video3, video3d))
    QLabsRealTime().start_real_time_model(modelName=model_path, actorNumber=0, additionalArguments=additional_args)

    qlabs.close()
    print("Done!")

    # start vrpn server - the code below start the vrpn server that broadcasts
    # the pose of the virtual qdrone2 to the VRPN client block in the Mission server.
    sleep_for = 0.5 # seconds
    if USE_VRPN:
        # os.system("start {}".format("qlabs_vrpn_server.exe {}".format(num_drones)))
        os.system("start {} {}".format(VRPN_SERVER, num_drones))
        time.sleep(sleep_for)


if __name__ == "__main__":
    main()