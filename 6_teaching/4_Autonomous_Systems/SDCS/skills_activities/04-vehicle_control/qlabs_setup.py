import os
import sys

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar import QLabsQCar
from qvl.qcar2 import QLabsQCar2
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
import pal.resources.rtmodels as rtmodels
from pal.products.qcar import QCAR_CONFIG

def setup(
        initialPosition=[0, 0, 0],
        initialOrientation=[0, 0, 0],
        rtModel=rtmodels.QCAR
    ):

    # Try to connect to Qlabs
    os.system('cls')
    qlabs = QuanserInteractiveLabs()
    # Ensure that QLabs is running on your local machine
    print("Connecting to QLabs...")
    if (not qlabs.open("localhost")):
        print("Unable to connect to QLabs")
        sys.exit()  
        return
    print("Connected to QLabs")

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()

    # Spawn a QCar at the given initial pose
    if QCAR_CONFIG['cartype']==1:
        hqcar = QLabsQCar(qlabs)
        rtModel = rtmodels.QCAR
    elif QCAR_CONFIG['cartype']==2:
        hqcar = QLabsQCar2(qlabs)
        rtModel = rtmodels.QCAR2

    hqcar.spawn_id(
        actorNumber=0,
        location=[p*10 for p in initialPosition],
        rotation=initialOrientation,
        waitForConfirmation=True
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn()
    hqcar.possess()

    # Start spawn model
    QLabsRealTime().start_real_time_model(rtModel)

    return hqcar

def terminate():
    QLabsRealTime().terminate_real_time_model("QCar_Workspace")
    QLabsRealTime().terminate_real_time_model("QCar2_Workspace")

if __name__ == '__main__':
    setup()