import os
import sys
import numpy as np

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar import QLabsQCar
from qvl.qcar2 import QLabsQCar2
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
from qvl.basic_shape import QLabsBasicShape
import pal.resources.rtmodels as rtmodels
from pal.products.qcar import QCAR_CONFIG

def setup(
        initialPosition=[0, 0, 0.000],
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
        location=[x*10 for x in initialPosition],
        rotation=initialOrientation,
        waitForConfirmation=True
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn([8.484, 1.973, 12.209], [-0, 0.748, 0.792])
    hqcar.possess()


    x_min = -30
    x_max = 20
    y_min = 7
    y_max = 50
    y_mid = (y_max - y_min) / 2
    hBasicShape = QLabsBasicShape(qlabs)

    #region Spawn Boundary
    if False:
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=0,
            startLocation=[x_min, y_min, 0],
            endLocation=[x_max, y_min, 0],
            height=3,
            thickness=1,
            color=[1,0,0],
            waitForConfirmation=False
        )
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=1,
            startLocation=[x_max, y_min, 0],
            endLocation=[x_max, y_max, 0],
            height=3,
            thickness=1,
            color=[1,0,0],
            waitForConfirmation=False
        )
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=2,
            startLocation=[x_min, y_max, 0],
            endLocation=[x_max, y_max, 0],
            height=3,
            thickness=1,
            color=[1,0,0],
            waitForConfirmation=False
        )
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=3,
            startLocation=[x_min, y_min, 0],
            endLocation=[x_min, y_max, 0],
            height=3,
            thickness=1,
            color=[1,0,0],
            waitForConfirmation=False
        )
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=4,
            startLocation=[x_min + 10, y_mid+7, 0],
            endLocation=[x_max - 10, y_mid+7, 0],
            height=3,
            thickness=25,
            color=[1,0,0],
            waitForConfirmation=False
        )
    #endregion
    else:
        xOff = 5.86
        yOff = -2.59
        # Parking Lot Box
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=0,
            startLocation=[-14+xOff, 25+yOff, 0],
            endLocation=[-14+xOff, 35+yOff, 0],
            height=5,
            thickness=10,
            color=[1,0,0],
            waitForConfirmation=False
        )

        # Plus
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=2,
            startLocation=[1+xOff, 2.5+yOff, 0],
            endLocation=[10+xOff, 2.5+yOff, 0],
            height=5,
            thickness=2,
            color=[1,0,0],
            waitForConfirmation=False
        )
        hBasicShape.spawn_id_box_walls_from_end_points(
            actorNumber=3,
            startLocation=[5.5+xOff, 7+yOff, 0],
            endLocation=[5.5+xOff, -2+yOff, -0],
            height=5,
            thickness=2,
            color=[1,0,0],
            waitForConfirmation=False
        )
        # Cylinder
        hBasicShape.spawn_id_degrees(
            actorNumber=4,
            location=[9.9+xOff, 41+yOff, 0],
            rotation=[0,0,45],
            scale=[7, 7, 15],
            configuration=hBasicShape.SHAPE_CYLINDER,

            waitForConfirmation=True
        )






    # Start spawn model
    QLabsRealTime().start_real_time_model(rtModel)

    return hqcar

def terminate():
    QLabsRealTime().terminate_real_time_model("QCar_Workspace")
    QLabsRealTime().terminate_real_time_model("QCar2_Workspace")

if __name__ == '__main__':
    # Add processing of command line arguments
    setup()