import json
import os
import time
import numpy as np

from qvl.actor import QLabsActor
import shutil
from qvl.real_time import QLabsRealTime
from qvl.qlabs import QuanserInteractiveLabs
from qvl.qarm import QLabsQArm
from qvl.qcar2 import QLabsQCar2
from qvl.qbot_platform import QLabsQBotPlatform
from qvl.qdrone2 import QLabsQDrone2


class MultiAgent():
    """This class is for spawning multiple agents in Quanser Interactive Labs that will then
    be controlled through QUARC/Quanser SKD. 

    When initializing the class, it will delete all QArms, QCar 2s, QBot Platforms and QDrone 2s in the space.

    """

    # location of RT models and creation of new MultiAgent folder
    __qalDirPath = os.environ.get('RTMODELS_DIR')
    
    _QArmDir = os.path.normpath(
        os.path.join(__qalDirPath, 'QArm'))
    _QCar2Dir = os.path.normpath(
        os.path.join(__qalDirPath, 'QCar2'))
    _QBPDir = os.path.normpath(
        os.path.join(__qalDirPath, 'QBotPlatform'))
    _QBPDriverDir = os.path.normpath(
        os.path.join(__qalDirPath, 'QBotPlatforms'))
    _QD2Dir = os.path.normpath(
        os.path.join(__qalDirPath, 'QDrone2'))
    _directory = os.path.normpath(
        os.path.join(__qalDirPath, 'MultiAgent'))
    
    robotActors = None
    """ List of qlabs actor objects of the robots that were spawned. 
    Use when using functions from qlabs library."""

    robotsDict = {}
    """ Dictionary of dictionaries of all spawned robots. Includes the information that is saved
    into the JSON file. Including robotType, actorNumber, classID as well as all ports used for the RT file."""

    def __init__(self, agentList):
        """
        Constructor Method

        :param agentList: A list of dictionaries of the spawned robots.  
        :type agentList: list of dictionaries
        """

        # The dictionaries can have the following keys (one per robot that will be spawned):
        # - "RobotType": string - can be "QC2"/"QCar2", "QBP", "QArm"/"QA", or "QDrone2"/"QD2"
        # - "Location": float array[3] - for spawning in x, y, z of the QLabs environment
        # - "Rotation": (Optional) float array[3] - for spawning in x, y, z. Can be in Degrees or Radians. If it is radians, set the "Radians" key to True. If not defined, will spawn with [0, 0, 0] rotation
        # - "Radians": (Optional) boolean - defaults to False. Only needed if rotation is in Radians
        # - "Scale": (Optional) float - if you want to change the scaling of the spawned object. If not defined, will spawn with scaling of 1. The scaling will apply in x, y, and z
        # - "actorNumber": (Optional) int - set only if you want a predefined actor number for your robot. If not, it will use the next available number for the type of robot. If the number is already in use, it will overwrite it. We do not recommend using it unless tracking of actors is done manually by the user.
        
        
        self.qlabs = QuanserInteractiveLabs()
        print("Connecting to QLabs...")
        if (not self.qlabs.open("localhost")):
            print("Unable to connect to QLabs")   

        print("Connected")

        cmd = QLabsRealTime().terminate_all_real_time_models()
        time.sleep(1)
        cmd = QLabsRealTime().terminate_all_real_time_models()
        time.sleep(1)


        QLabsQArm(self.qlabs).destroy_all_actors_of_class()
        QLabsQCar2(self.qlabs).destroy_all_actors_of_class()
        QLabsQBotPlatform(self.qlabs).destroy_all_actors_of_class()
        QLabsQDrone2(self.qlabs).destroy_all_actors_of_class()


        self._fileType = '.rt-win64' # will need a check once we have multiple OS support
        self._portNumber = 18799
        self._uriPortNumber = 17010
        self._driverPortNumber = 18949 

        created = self._createMultiAgentDir()

        time.sleep(.5)
        # if not created:
        #     print ('Directory not created successfully. Aborting.')
        #     break/continue?
        
        
        # remove robot if not RobotType or Location defined
        for robot in agentList[:]:
            if "RobotType" not in robot:
                agentList.remove(robot)
                print("Removed the following entry due to no RobotType defined:")
                print(robot)
            if "Location" not in robot:
                agentList.remove(robot)
                print("Removed the following entry due to no Location defined:")
                print(robot)

        # fill empty rotation, radians and scaling if not defined
        for robot in agentList:
            if "Rotation" not in robot:
                # If "Rotation" is not defined, set it to the default value
                robot["Rotation"] = [0,0,0]
            if "Radians" not in robot:
                # If "Radians" is not defined, set it to the default value of False
                robot["Radians"] = False
            if "Scale" not in robot:
                # If "Scaling" is not defined, set it to the default value
                robot["Scale"] = 1
        
        robotActors = self._spawnRobots(agentList)
        # finished spawning

        self.robotActors = robotActors
        # dictionary of qlabs actors
        
        x = 0
        for actor in robotActors:
            scale = agentList[x]["Scale"] 
            name, robotDict = self.createRobot(actor, scale)
            self.robotsDict[name] = robotDict
            # dictionary of robots and their properties for the json file
            x=x+1

        filePath = os.path.join(MultiAgent._directory,"RobotAgents.json")
        with open(filePath, "w") as outfile: 
            json.dump(self.robotsDict, outfile)

        
    def _createMultiAgentDir(self):
        """ Internal method to create the MultiAgent directory in the RTMODELS_DIR directory"""
        try:
            os.mkdir(MultiAgent._directory)
            print(f"Directory '{MultiAgent._directory}' created successfully.")
            return True
        except FileExistsError:
            print(f"Deleting existing directory '{MultiAgent._directory}'...")
            shutil.rmtree(MultiAgent._directory)
            os.mkdir(MultiAgent._directory)
            print(f"Directory '{MultiAgent._directory}' created successfully.")
            return True
        except PermissionError:
            print(f"Permission denied: Unable to create '{MultiAgent._directory}'.")
            return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
      
    def _spawnRobots(self, agentList):
        """ Internal method to spawn the robots in the QLabs environment.
            returns a list of the qlabs objects (spawned robots)"""
        robotActors = [0] * len(agentList)
        x = 0
        for robot in agentList:
            qlabsRobot = 0
            robotType = robot["RobotType"].lower()
            if robotType == "qarm" or robotType == "qa":
                qlabsRobot = QLabsQArm(self.qlabs)
            if robotType == "qcar2" or robotType == "qcar 2" or robotType == "qc2":
                qlabsRobot = QLabsQCar2(self.qlabs)
            if robotType == "qbotplatform" or robotType == "qbot platform" or robotType == "qbp":
                qlabsRobot = QLabsQBotPlatform(self.qlabs)
            if robotType == "qdrone2" or robotType == "qdrone 2" or robotType == "qd2":
                qlabsRobot = QLabsQDrone2(self.qlabs)
            
            location = robot["Location"]
            rotation = robot["Rotation"]
            scale = [robot["Scale"], robot["Scale"], robot["Scale"]]
            
            if "ActorNumber" not in robot: # spawn degrees or spawn
                if robot["Radians"] == True:
                    qlabsRobot.spawn(location=location, rotation=rotation, scale=scale)
                else:
                    qlabsRobot.spawn_degrees(location=location, rotation=rotation, scale=scale)
            else: # spawn id or spawn ID degrees
                actorNumber = robot["ActorNumber"]
                if robot["Radians"] == True:
                    qlabsRobot.spawn_id(actorNumber=actorNumber,location=location, rotation=rotation, scale=scale)
                else:
                    qlabsRobot.spawn_id_degrees(actorNumber=actorNumber, location=location, rotation=rotation, scale=scale)

            robotActors[x] = qlabsRobot 
        
            x = x + 1

        return robotActors

    def createRobot(self, QLabsActor, scale):
        """ Internal method to call functions to copy rt files and start them to be able to control the robots"""
        classID = QLabsActor.classID
        actorNumber = QLabsActor.actorNumber
        if classID == 10: #QArm
            name, robotDict = self._createQArm(actorNumber)
        if classID == 23: # QBP
            name, robotDict = self._createQBP(actorNumber)
        if classID == 161: #QCar2
            name, robotDict = self._createQC2(actorNumber, scale)
        if classID == 231: #QDrone2
            name, robotDict = self._createQD2(actorNumber)
        
        return name, robotDict

    def _createQArm(self, actorNumber):
        """ Internal method to initialize the rt model for the QArm. Calls function to create
        copy of the rt files into the MultiAgent folder and then starts the rt model"""
        path = self._copyQArm_files(actorNumber)
        path, ext = os.path.splitext(path)

        hilPort = self._nextNumber()
        videoPort = self._nextNumber()
        uriPort = self._nextURINumber()

        arguments = '-uri_hil tcpip://localhost:' + str(hilPort) + ' ' + \
                    '-uri_video tcpip://localhost:' + str(videoPort)
        
        display = 'QArm ' + str(actorNumber) + ' spawned as ' + arguments
        print(display)

        #Start spawn model
        QLabsRealTime().start_real_time_model(path, actorNumber=actorNumber, uriPort = uriPort, additionalArguments=arguments)

        name = 'QA_' + str(actorNumber)
        robotDict = {
            "robotType": "QArm",
            "actorNumber": actorNumber,
            "classID": 10,
            "hilPort" : hilPort,
            "videoPort" : videoPort
        }

        return name, robotDict

    def _createQBP(self, actorNumber):
        """ Internal method to initialize the rt model and driver for the QBot Platform. Calls function to create
        copy of the rt files into the MultiAgent folder and then starts the rt model"""
        workspacePath, driverPath = self._copyQBP_files(actorNumber)

        workspacePath, ext = os.path.splitext(workspacePath)

        driverPath, ext = os.path.splitext(driverPath)

        videoPort = self._nextNumber()
        video3dPort = self._nextNumber()
        lidarPort = self._nextNumber()
        uriPort = self._nextURINumber()

        # hilPort, driverPort = self._nextDriverNumber()
        hilPort = 18950 + actorNumber
        driverPort = 18970 + actorNumber
        uriPortDriver = self._nextURINumber()
    
        arguments = '-uri_hil tcpip://localhost:'    + str(hilPort) + ' ' + \
                    '-uri_video tcpip://localhost:' + str(videoPort) + ' ' + \
                    '-uri_video3d tcpip://localhost:'+ str(video3dPort) + ' ' + \
                    '-uri_lidar tcpip://localhost:'  + str(lidarPort)  
        
        display = 'QBP ' + str(actorNumber) + ' spawned as ' + arguments + ' driverPort ' + str(driverPort)
        print(display)

        #Start spawn model
        QLabsRealTime().start_real_time_model(workspacePath, actorNumber=actorNumber, uriPort = uriPort, additionalArguments=arguments)

        arguments = '-uri tcpip://localhost:'+ str(uriPortDriver) 
        QLabsRealTime().start_real_time_model(driverPath, actorNumber=actorNumber, userArguments=False, additionalArguments= arguments)
        

        name = 'QBP_' + str(actorNumber)
        robotDict = {
            "robotType": "QBP",
            "actorNumber": actorNumber,
            "classID": 23,
            "hilPort" : hilPort,
            "videoPort" : videoPort,
            "video3dPort" : video3dPort,
            "lidarPort" : lidarPort,
            "driverPort" : driverPort
        }

        return name, robotDict

    def _createQC2(self, actorNumber, scale):
        """ Internal method to initialize the rt model for the QCar 2. Calls function to create
        copy of the rt files into the MultiAgent folder and then starts the rt model"""
        path = self._copyQC2_files(actorNumber, scale)
        path, ext = os.path.splitext(path)

        hilPort = self._nextNumber()
        video0Port = self._nextNumber()
        video1Port = self._nextNumber()
        video2Port = self._nextNumber()
        video3Port = self._nextNumber()
        video3dPort = self._nextNumber()
        lidarPort = self._nextNumber()
        gpsPort = self._nextNumber()
        lidarIdealPort = self._nextNumber()
        ledPort = self._nextNumber()

        uriPort = self._nextURINumber()
    
        arguments = '-uri_hil tcpip://localhost:'    + str(hilPort) + ' ' + \
                    '-uri_video0 tcpip://localhost:' + str(video0Port) + ' ' + \
                    '-uri_video1 tcpip://localhost:' + str(video1Port) + ' ' + \
                    '-uri_video2 tcpip://localhost:' + str(video2Port) + ' ' + \
                    '-uri_video3 tcpip://localhost:' + str(video3Port) + ' ' + \
                    '-uri_video3d tcpip://localhost:'+ str(video3dPort) + ' ' + \
                    '-uri_lidar tcpip://localhost:'  + str(lidarPort) + ' ' + \
                    '-uri_gps tcpip://localhost:'    + str(gpsPort) + ' ' + \
                    '-uri_lidar_ideal tcpip://localhost:'  + str(lidarIdealPort) + ' ' + \
                    '-uri_led tcpip://localhost:'    + str(ledPort)
        
        display = 'QCar ' + str(actorNumber) + ' spawned as ' + arguments
        print(display)

        #Start spawn model
        QLabsRealTime().start_real_time_model(path, actorNumber=actorNumber, uriPort = uriPort, additionalArguments=arguments)

        name = 'QC2_' + str(actorNumber)
        robotDict = {
            "robotType": "QC2",
            "actorNumber": actorNumber,
            "classID": 161,
            "hilPort" : hilPort,
            "videoPort" : video0Port,
            "video3dPort" : video3dPort,
            "lidarPort" : lidarPort,
            "gpsPort" : gpsPort,
            "lidarIdealPort" : lidarIdealPort,
            "ledPort" : ledPort
        }

        return name, robotDict
  
    def _createQD2(self, actorNumber):
        """ Internal method to initialize the rt model for the QDrone 2. Calls function to create
        copy of the rt files into the MultiAgent folder and then starts the rt model"""
        path = self._copyQD2_files(actorNumber)
        path, ext = os.path.splitext(path)

        hilPort = self._nextNumber()
        video0Port = self._nextNumber()
        video1Port = self._nextNumber()
        video2Port = self._nextNumber()
        video3Port = self._nextNumber()
        video3dPort = self._nextNumber()
        posePort = self._nextNumber()

        uriPort = self._nextURINumber()

        arguments = '-uri_hil tcpip://localhost:'    + str(hilPort) + ' ' + \
                    '-uri_video0 tcpip://localhost:' + str(video0Port) + ' ' + \
                    '-uri_video1 tcpip://localhost:' + str(video1Port) + ' ' + \
                    '-uri_video2 tcpip://localhost:' + str(video2Port) + ' ' + \
                    '-uri_video3 tcpip://localhost:' + str(video3Port) + ' ' + \
                    '-uri_video3d tcpip://localhost:'+ str(video3dPort) + ' ' + \
                    '-uri_pose tcpip://localhost:'  + str(posePort) 
    
        
        display = 'QDrone ' + str(actorNumber) + ' spawned as ' + arguments
        print(display)

        #Start spawn model
        QLabsRealTime().start_real_time_model(path, actorNumber=actorNumber, uriPort = uriPort, additionalArguments=arguments)

        name = 'QD2_' + str(actorNumber)
        robotDict = {
            "robotType": "QD2",
            "actorNumber": actorNumber,
            "classID": 231,
            "hilPort" : hilPort,
            "videoPort" : video0Port,
            "video3dPort" : video3dPort,
            "posePort" : posePort
        }

        return name, robotDict

    def _copyQArm_files(self,actorNumber):
        rtFile = 'QArm_Spawn'

        # create copy of rt file workspace
        originalFile = rtFile + self._fileType
        originalPath = os.path.join(MultiAgent._QArmDir,originalFile)
        newFile = rtFile + str(actorNumber) + self._fileType
        newPath = os.path.join(MultiAgent._directory,newFile)
        shutil.copy(originalPath, newPath)

        time.sleep(0.2)
        return newPath

    def _copyQBP_files(self,actorNumber):
        rtFile = 'QBotPlatform_Workspace' # change _debug
        driverFile = 'qbot_platform_driver_virtual' + str(actorNumber)

        # create copy of rt file workspace
        originalFile = rtFile + self._fileType
        originalPath = os.path.join(MultiAgent._QBPDir,originalFile)
        newFile = rtFile + str(actorNumber) + self._fileType
        newPathWorkspace = os.path.join(MultiAgent._directory,newFile)
        shutil.copy(originalPath, newPathWorkspace)

        # create copy of driver _QBPDriverDir
        originalFile = driverFile + self._fileType
        originalPath = os.path.join(MultiAgent._QBPDriverDir,originalFile)
        newFile = driverFile + self._fileType
        newPathDriver = os.path.join(MultiAgent._directory,newFile)
        shutil.copy(originalPath, newPathDriver)

        time.sleep(0.2) # change! back to 0.2
        return newPathWorkspace, newPathDriver

    def _copyQC2_files(self, actorNumber, scale):
        rtFile = 'QCar2_Workspace'
        if scale == 0.1:
            rtFile = 'QCar2_Workspace_studio'

        # create copy of rt file workspace
        originalFile = rtFile + self._fileType
        originalPath = os.path.join(MultiAgent._QCar2Dir,originalFile)
        newFile = rtFile + str(actorNumber) + self._fileType
        newPath = os.path.join(MultiAgent._directory,newFile)
        shutil.copy(originalPath, newPath)

        time.sleep(0.2)
        return newPath
    
    def _copyQD2_files(self,actorNumber):
        rtFile = 'QDrone2_Workspace'

        # create copy of rt file workspace
        originalFile = rtFile + self._fileType
        originalPath = os.path.join(MultiAgent._QD2Dir,originalFile)
        newFile = rtFile + str(actorNumber) + self._fileType
        newPath = os.path.join(MultiAgent._directory,newFile)
        shutil.copy(originalPath, newPath)

        time.sleep(0.2)
        return newPath
    
    def _nextNumber(self):
        self._portNumber = self._portNumber + 1
        return self._portNumber
    
    def _nextURINumber(self):
        self._uriPortNumber = self._uriPortNumber + 1
        return self._uriPortNumber
    
    def _nextDriverNumber(self):
        self._driverPortNumber = self._driverPortNumber + 1
        driverPort = self._driverPortNumber + 20
        return self._driverPortNumber, driverPort
    
    
def readRobots():
    """ 
    Function to read the JSON file created after spawning the robots. 
    The file contains all necessary port/URI numbers to initialize the robots.
    The function will return the dictionary that was created when spawning the robots
    it contains the the robots and their properties.
    The function makes sure that the file is not being used by another process before reading it.""" 

    # This function is not part of the MultiAgent class. Do not initialize a MultiAgent object only to use this function.
    
    directory = os.path.normpath(
        os.path.join(os.environ['RTMODELS_DIR'], 'MultiAgent'))
    
    filePath = os.path.join(directory,"RobotAgents.json")
    tmpPath = os.path.join(directory,"tmp.csv")
    
    wait = True

    while wait:
        tmpExists = os.path.isfile(tmpPath)
        
        if not tmpExists: 
            open(tmpPath, 'a').close() # temporary file to prevent robotJSON from opening if its already used by someone else
            with open(filePath, 'r') as file:
                robotsDict = json.load(file)
            os.remove(tmpPath)
            wait = False
        
        else:
            time.sleep(0.05)
        
    return robotsDict