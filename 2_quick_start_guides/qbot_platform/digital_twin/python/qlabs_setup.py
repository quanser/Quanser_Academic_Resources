#-----------------------------------------------------------------------------#
#--------------------Quanser Interactive Labs Setup for-----------------------#
#---------------------------Mobile Robotics Lab-------------------------------#
#-----------------(Environment: QBot Platform / Warehouse)--------------------#
#-----------------------------------------------------------------------------#

from qvl.walls import QLabsWalls
from qvl.qlabs import QuanserInteractiveLabs
from qvl.qbot_platform import QLabsQBotPlatform
from qvl.qbot_platform_flooring import QLabsQBotPlatformFlooring
from qvl.real_time import QLabsRealTime
import pal.resources.rtmodels as rtmodels
import time
import numpy as np
import os
import subprocess

#------------------------------ Main program ----------------------------------

def setup(
        locationQBotP       = [0, 0, 0.1],
        verbose             = True,
        rtModel_workspace   = rtmodels.QBOT_PLATFORM,
        rtModel_driver      = rtmodels.QBOT_PLATFORM_DRIVER
        ):

    subprocess.Popen(['quanser_host_peripheral_client.exe', '-q'])
    time.sleep(2.0)
    subprocess.Popen(['quanser_host_peripheral_client.exe', '-uri', 'tcpip://localhost:18444'])

    qrt = QLabsRealTime()
    if verbose: print("Stopping any pre-existing RT models")
    qrt.terminate_real_time_model(rtModel_workspace)
    time.sleep(1.0)
    qrt.terminate_real_time_model(rtModel_driver)
    time.sleep(1.0)
    qrt.terminate_all_real_time_models()

    qlabs = QuanserInteractiveLabs()
    if verbose: print("Connecting to QLabs ...")
    try:
        qlabs.open("localhost")
    except:
        print("Unable to connect to QLabs")
        return
    if verbose: print("Connected!")

    qlabs.destroy_all_spawned_actors()

    #---------------------------- QBot Platform ---------------------------
    if verbose: print("Spawning QBot Platform ...")
    hQBot = QLabsQBotPlatform(qlabs)
    hQBot.spawn_id_degrees(actorNumber=0,
                        location=locationQBotP,
                        rotation=[0,0,90],
                        scale=[1,1,1],
                        configuration=1,
                        waitForConfirmation= False)
    hQBot.possess(hQBot.VIEWPOINT_TRAILING)
    #------------------------------- Walls --------------------------------
    if verbose: print("Spawning walls ...")
    hWall = QLabsWalls(qlabs)
    hWall.spawn_degrees(location=[2, 1.2, 0.1], rotation=[0, 0, 0])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[2, 0, 0.1], rotation=[0, 0, 0])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[2, -1.2, 0.1], rotation=[0, 0, 0])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[-2, 1.2, 0.1], rotation=[0, 0, 0])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[-2, 0, 0.1], rotation=[0, 0, 0])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[-2, -1.2, 0.1], rotation=[0, 0, 0])

    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[1.2, 2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[0, 2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[-1.2, 2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[1.2, -2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[0, -2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    hWall.spawn_degrees(location=[-1.2, -2, 0.1], rotation=[0, 0, 90])
    hWall.set_enable_dynamics(True)
    #----------------------------- Flooring -------------------------------
    if verbose: print("Spawning flooring ...")
    hFloor0 = QLabsQBotPlatformFlooring(qlabs)
    _ = hFloor0.spawn_id(actorNumber = 0,
                        location = [-0.6,-0.6,   0],
                        rotation = [0,0,0],
                        scale = [1,1,1],
                        configuration = 5,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 1,
                        location = [ 0.6, 1.8,   0],
                        rotation = [0,0,-np.pi/2],
                        scale = [1,1,1],
                        configuration = 0,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 2,
                        location = [ 1.8,-0.6,   0],
                        rotation = [0,0, np.pi],
                        scale = [1,1,1],
                        configuration = 0,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 3,
                        location = [-0.6,-1.8,   0],
                        rotation = [0,0, np.pi/2],
                        scale = [1,1,1],
                        configuration = 0,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 4,
                        location = [-1.8, 0.6,   0],
                        rotation = [0,0,0],
                        scale = [1,1,1],
                        configuration = 0,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 5,
                        location = [-0.6, 0.6,   0],
                        rotation = [0,0,0],
                        scale = [1,1,1],
                        configuration = 1,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 6,
                        location = [ 0.6, 0.6,   0],
                        rotation = [0,0,-np.pi/2],
                        scale = [1,1,1],
                        configuration = 1,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 7,
                        location = [ 0.6,-0.6,   0],
                        rotation = [0,0, np.pi],
                        scale = [1,1,1],
                        configuration = 1,
                        waitForConfirmation= False)
    _ = hFloor0.spawn_id(actorNumber = 8,
                        location = [-0.6,-0.6,   0],
                        rotation = [0,0, np.pi/2],
                        scale = [1,1,1],
                        configuration = 1,
                        waitForConfirmation= False)
    #----------------------------- RT Models -------------------------------
    if verbose: print("Starting RT models...")
    time.sleep(2)
    qrt.start_real_time_model(rtModel_workspace, userArguments=False)
    time.sleep(1)
    qrt.start_real_time_model(rtModel_driver, userArguments=True, additionalArguments="-uri tcpip://localhost:17098")
    if verbose: print('QLabs setup completed')
    return hQBot

if __name__ == '__main__':
    setup(locationQBotP       = [0, -0.1, 0.1], verbose=True)