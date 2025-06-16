# region: package imports
import os
import sys
import numpy as np

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar2 import QLabsQCar2
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime

# environment objects
from qvl.crosswalk import QLabsCrosswalk
from qvl.roundabout_sign import QLabsRoundaboutSign
from qvl.yield_sign import QLabsYieldSign
from qvl.traffic_light import QLabsTrafficLight
from qvl.basic_shape import QLabsBasicShape
from qvl.stop_sign import QLabsStopSign
import pal.resources.rtmodels as rtmodels
import time
#endregion

def setup(
        initialPosition=[-0.031, 1.311, 0.000],
        initialOrientation=[0, 0, -np.pi/2],
        rtModel=rtmodels.QCAR2
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
    time.sleep(0.5)
    # region: QCar spawn description


    # Spawn a QCar at the given initial pose
    hqcar = QLabsQCar2(qlabs)
    hqcar.spawn_id(
        actorNumber=0,
        location=[x for x in initialPosition],
        rotation=initialOrientation,
        waitForConfirmation=True
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn([8.484, 1.973, 12.209], [-0, 0.748, 0.792])
    hqcar.possess()
    # endregion



    # endregion

    # region: crosswalk
    NUMCROSSWALKS = 4
    walks = []

    for i in range(NUMCROSSWALKS):

        # Initialize cone
        walks.append(QLabsCrosswalk(qlabs))

    walks[0].spawn(location =[-5, 9.5, 0],
                    rotation=[0,0,np.pi/2], scale = [1,1,0.75],
                    configuration = 0)

    walks[1].spawn(location =[1.3, 16, 0],
                rotation=[0,0,0], scale = [1,1,0.75],
                configuration = 0)

    walks[2].spawn(location =[7.7, 9.5, 0],
            rotation=[0,0,np.pi/2], scale = [1,1,0.75],
            configuration = 0)

    walks[3].spawn(location =[1.3, 3, 0],
            rotation=[0,0,0], scale = [1,1,0.75],
            configuration = 0)
    # endregion

    # region: Traffic Light
    NUMTRAFFICLIGHTS = 4
    lights = []
    for i in range(NUMTRAFFICLIGHTS):

        # Initialize cone
        lights.append(QLabsTrafficLight(qlabs))

    lights[0].spawn(location =[-3.77, 13, 0],
                    rotation=[0,0,np.pi/2],
                    configuration = 0)

    lights[1].spawn(location =[4.9, 14.8, 0],
                rotation=[0,0,0],
                configuration = 0)

    lights[2].spawn(location =[6.7, 5.7, 0],
            rotation=[0,0,-np.pi/2],
            configuration = 0)

    lights[3].spawn(location =[-2, 4.27, 0],
            rotation=[0,0,np.pi],
            configuration = 0)
    # endregion

    # region: Yield sign

    yieldSigns = QLabsYieldSign(qlabs)

    yieldSigns.spawn(location =[0.4,-13, 0],
                        rotation=[0,0,np.pi])
     # endregion

    # region: roundabout
    NUMROUNDABOUTSIGNS = 3
    roundAboutSigns = []

    for i in range(NUMROUNDABOUTSIGNS):

        # Initialize cone
        roundAboutSigns.append(QLabsRoundaboutSign(qlabs))

    roundAboutSigns[0].spawn(location =[24.5,33, 0],
                        rotation=[0,0,-np.pi/2])

    roundAboutSigns[1].spawn(location =[4.5,40, 0],
                        rotation=[0,0,np.pi])

    roundAboutSigns[2].spawn(location =[10.6,28.5, 0],
                        rotation=[0,0,np.pi])

    # endregion

    # region: Spawning Basic Shapes
    hBasicShape = QLabsBasicShape(qlabs)
    xOff = 0 #0.586

    # Plus
    hBasicShape.spawn_id_box_walls_from_end_points(
        actorNumber=2,
        startLocation=[-13.64, 3.82, 0.0],
        endLocation=[-3.08, -7.062, 0.0],
        height=5,
        thickness=3,
        color=[(154/255),(101/255),(14/255)],
        waitForConfirmation=False
    )
    hBasicShape.spawn_id_box_walls_from_end_points(
        actorNumber=3,
        startLocation=[-3.93, 4.00, -0],
        endLocation=[-10.034, -3.102, -0],
        height=5,
        thickness=3,
        color=[(154/255),(101/255),(14/255)],
        waitForConfirmation=False
    )

    # Roundabout Box
    hBasicShape.spawn_id_box_walls_from_end_points(
        actorNumber=4,
        startLocation=[12.104, 38.266, 0],
        endLocation=[18.345, 38.433, 0],
        height=5,
        thickness=4,
        color=[(154/255),(101/255),(14/255)],
        waitForConfirmation=False
    )

    # Basic Building Box
    hBasicShape.spawn_id_box_walls_from_end_points(
    actorNumber=5,
    startLocation=[5.969, 0.072, 0.385],
    endLocation=[16.578, -0.016, 0],
    height=5,
    thickness=8.5,
    color=[(154/255),(101/255),(14/255)],
    waitForConfirmation=False)
    # endregion

    # region: Spawn stopsign
    stop = QLabsStopSign(qlabs)
    stop.spawn(location=[-0.508, -7.327, 0.2], rotation=[0,0, np.pi/2],
            scale=[1,1,1], configuration=0, waitForConfirmation=True)
    # endregion

    # Start spawn model
    QLabsRealTime().start_real_time_model(rtModel)


    return hqcar


if __name__ == '__main__':
    # XXX Add processing of command line arguments
    setup()