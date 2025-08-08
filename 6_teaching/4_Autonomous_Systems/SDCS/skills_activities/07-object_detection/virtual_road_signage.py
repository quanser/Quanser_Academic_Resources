# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : File Description and Imports
'''
virtual_road_signage.py

Setup scrip for the virtual envirionment where road signs and traffic light are 
spawned. In addition QCar is spawned and can be moved to any location via terminal
input. The script also allows for the weather to be changed in the environment.
'''
import numpy as np
import os

from qvl.qlabs import QuanserInteractiveLabs
from qvl.qcar2 import QLabsQCar2
from qvl.qcar import QLabsQCar
from qvl.free_camera import QLabsFreeCamera
from qvl.real_time import QLabsRealTime
from qvl.traffic_light import QLabsTrafficLight
from qvl.yield_sign import QLabsYieldSign
from qvl.stop_sign import QLabsStopSign
from qvl.environment_outdoors import QLabsEnvironmentOutdoors

import pal.resources.rtmodels as rtmodels
from pal.products.qcar import QCAR_CONFIG
import time
#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Main Loop
#=================== Virtual Env Setup ===================
# Connecting to Quanser Interactive Labs

def setup(
        initialPosition=[16.6, 2, 0.000],
        initialOrientation=[0,0,np.pi/2],
        rtModel=rtmodels.QCAR2
    ):
    # Try to connect to Qlabs
    qlabs = QuanserInteractiveLabs()
    print("Connecting to QLabs...")
    try:
        qlabs.open("localhost")
        print("Connected to QLabs")
    except:
        print("Unable to connect to QLabs")
        quit()

    # Delete any previous QCar instances and stop any running spawn models
    qlabs.destroy_all_spawned_actors()
    QLabsRealTime().terminate_all_real_time_models()
    time.sleep(0.5)

    # Spawn a QCar at the given initial pose
    if QCAR_CONFIG['cartype']==1:
        hqcar = QLabsQCar(qlabs)
        rtModel = rtmodels.QCAR
    elif QCAR_CONFIG['cartype']==2:
        hqcar = QLabsQCar2(qlabs)
        rtModel = rtmodels.QCAR2
        
    hqcar.spawn_id(
        actorNumber=0,
        location=initialPosition,
        rotation=initialOrientation,
        waitForConfirmation=True
    )

    # Create a new camera view and attach it to the QCar
    hcamera = QLabsFreeCamera(qlabs)
    hcamera.spawn([8.484, 1.973, 12.209], [-0, 0.748, 0.792])
    hqcar.possess()

    # instantiate outdoor environment
    hEnvironmentOutdoors = QLabsEnvironmentOutdoors(qlabs)

    # instantiate objects of insterests
    trafficLight = QLabsTrafficLight(qlabs)
    yieldsign = QLabsYieldSign(qlabs)
    stopsign = QLabsStopSign(qlabs)


    # Start spawn model
    QLabsRealTime().start_real_time_model(rtModel)

    task=input('What is the current task? (type the same task as in object_detection.py):')
    if task in ['threshold','detect']:
        trafficLight.spawn(location=[0.782,-11.755,0.005], rotation=[0,0,np.pi], scale=[1,1,1], configuration=0)
        stopsign.spawn(location=[0.7,-8.527,0.005], rotation=[0,0,np.pi/2], scale=[1,1,1])
    elif task == 'classify':
        stopsign.spawn(location=[0.7,-8.527,0.005], rotation=[0,0,np.pi/2], scale=[1,1,1])
        yieldsign.spawn(location=[2.2,-8.527,0.005], rotation=[0,0,np.pi/2], scale=[1,1,1])

    MAXSPACE = 100 #m
    try: 
        while True:
            text = "Enter location of qcar in space X,Y,Z,Roll,Pitch,Yaw. All values should be floating points, separated by a comma, and angles in radians:.. "
            qcarPose = input(text)
            userDefinedLocation = np.array(qcarPose.split(","), dtype= np.float32)
            numLocations = len(userDefinedLocation)
            print("your input is: ",userDefinedLocation )
            try: 
                if userDefinedLocation[2] < 0:
                    print("Board bellow ground, setting height to 0")
                    userDefinedLocation[2] = 0
                if np.absolute(userDefinedLocation[0]) > MAXSPACE or np.absolute(userDefinedLocation[1]) > MAXSPACE :
                    text = "cannot spawn object outside of workspace. Setting spawn location to origin."
                    print(text)
                    userDefinedLocation[0] = 0
                    userDefinedLocation[1] = 0
                    
            except numLocations > 6 or numLocations < 6:
                text ="Invalid locations entries! setting spawn point to origin with zero orientations"
                print(text)
                userDefinedLocation = np.zeros((1,6), dtype= np.float32)


            qcarLocation    = userDefinedLocation[0:3]
            qcarOrientation = userDefinedLocation[3:6]

            hqcar.set_transform_and_request_state(location = qcarLocation, 
                                                  rotation = qcarOrientation,
                                                  enableDynamics = False, 
                                                  headlights = False, 
                                                  leftTurnSignal = False, 
                                                  rightTurnSignal = False, 
                                                  brakeSignal = False, 
                                                  reverseSignal = False, 
                                                  waitForConfirmation = True)
            
            weather_id = int(input("Enter the weather preset ID (0-10):.. "))
            print("your input is: ",weather_id )
            try:
                hEnvironmentOutdoors.set_weather_preset(weather_id)
            except weather_id>10 or weather_id<0:
                print("Invalid weather ID! Setting weather to default.")
                hEnvironmentOutdoors.set_weather_preset(0)


    
    except KeyboardInterrupt: 
        qlabs.close()
        print("Done!")  

def terminate():
    QLabsRealTime().terminate_real_time_model("QCar_Workspace")
    QLabsRealTime().terminate_real_time_model("QCar2_Workspace")

#endregion

# -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

#region : Run
def main():
    setup(initialPosition=[0, 0, 0], initialOrientation=[0, 0, 3*np.pi/2])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Done')
    finally:
        terminate()
#endregion