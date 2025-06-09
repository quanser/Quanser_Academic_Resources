classdef MultiAgent < handle

     properties (Constant, Access = private)
        % Constant directory paths for different robot types
        QArmDir = fullfile(getenv('RTMODELS_DIR'), 'QArm');
        QCar2Dir = fullfile(getenv('RTMODELS_DIR'), 'QCar2');
        QBPDir = fullfile(getenv('RTMODELS_DIR'), 'QBotPlatform');
        QBPDriverDir = fullfile(getenv('RTMODELS_DIR'), 'QBotPlatforms');
        QD2Dir = fullfile(getenv('RTMODELS_DIR'), 'QDrone2');
        rtModels = getenv('QUARC_DIR');
        
    end
    
    properties (Access = private)
        % Existing properties remain the same
        fileType = '.rt-win64';
        portNumber = 18799;
        uriPortNumber = 17010;
        driverPortNumber = 18949;
        directory
    end

    properties (Access = public)
        % Existing properties remain the same
        qlabs = [];
        robotActors = {};  % cell array with of qlabs actor objects of the robots that were spawned. Use when using functions from qlabs library.
        robotsDict = struct(); % struct of structs of all spawned robots. Includes the information that is saved into the JSON file.
    end
    
    methods
        function obj = MultiAgent(agentList)
            % Constructor for MultiAgent class
            obj.qlabs = QuanserInteractiveLabs();
            disp('Connecting to QLabs...');
            connection_established = obj.qlabs.open('localhost');
            if connection_established == false
                disp("Unable to connect to QLabs.")
                return
            end
            disp('Connected');

            system("quarc_run -q -Q -t tcpip://localhost:17000 *.rt-win64");
            pause(1)
            system("quarc_run -q -Q -t tcpip://localhost:17000 *.rt-win64");
            pause(1)

            % Destroy existing actors of different robot classes
            QLabsQArm(obj.qlabs).destroy_all_actors_of_class();
            QLabsQCar2(obj.qlabs).destroy_all_actors_of_class();
            QLabsQBotPlatform(obj.qlabs).destroy_all_actors_of_class();
            QLabsQDrone2(obj.qlabs).destroy_all_actors_of_class();
               
            % Create MultiAgent directory
            obj.createMultiAgentDir();

            pause(.5)

            % Preprocess agent list, removing entries without required fields
            processedList = {};
            for i = 1:length(agentList)
                robot = agentList{i};
                if isfield(robot, 'RobotType') && isfield(robot, 'Location')
                    % Set default values if not provided
                    if ~isfield(robot, 'Rotation')
                        robot.Rotation = [0, 0, 0];
                    end
                    if ~isfield(robot, 'Radians')
                        robot.Radians = false;
                    end
                    if ~isfield(robot, 'Scale')
                        robot.Scale = 1;
                    end
                    % only here add to processedList
                    processedList{end+1} = robot; 
                end
            end

            agentList =  processedList;

            robotActors = obj.spawnRobots(agentList);
            obj.robotActors = robotActors;
            

            for i = 1:length(robotActors)
                robot = robotActors{i};
                [name, robotDict] = obj.createRobot(robot);
                obj.robotsDict.(name) = robotDict;                
            end

            % Save robot configurations to JSON
            filePath = fullfile(obj.directory, 'RobotAgents.json');
            jsonStr = jsonencode(obj.robotsDict);
            fid = fopen(filePath, 'w');
            fprintf(fid, '%s', jsonStr);
            fclose(fid);
        end
        % 
        
        function createMultiAgentDir(obj)
            % Create MultiAgent directory
            obj.directory = fullfile(getenv('RTMODELS_DIR'), 'MultiAgent');

            if exist(obj.directory, 'dir')
                rmdir(obj.directory, 's');
            end

            mkdir(obj.directory);
            disp(['Directory ''' obj.directory ''' created successfully.']);
        end
        

        function robotActors = spawnRobots(obj, agentList)
            % Spawn robots based on agent list
            robotActors = cell(1, length(agentList));

            for i = 1:length(agentList)
                robot = agentList{i};
                robotType = lower(robot.RobotType);

                % Select appropriate robot class
                switch robotType
                    case {'qarm', 'qa'}
                        qlabsRobot = QLabsQArm(obj.qlabs);
                    case {'qcar2', 'qcar 2', 'qc2'}
                        qlabsRobot = QLabsQCar2(obj.qlabs);
                    case {'qbotplatform', 'qbot platform', 'qbp'}
                        qlabsRobot = QLabsQBotPlatform(obj.qlabs);
                    case {'qdrone2', 'qdrone 2', 'qd2'}
                        qlabsRobot = QLabsQDrone2(obj.qlabs);
                end

                % Spawn robot
                location = robot.Location;
                rotation = robot.Rotation;
                scale = [robot.Scale, robot.Scale, robot.Scale];
                
                if ~isfield(robot, 'ActorNumber')
                    if robot.Radians
                        qlabsRobot.spawn(location, rotation, scale);
                    else
                        qlabsRobot.spawn_degrees(location, rotation, scale);
                    end
                else
                    actorNumber = robot.ActorNumber;
                    if robot.Radians
                        qlabsRobot.spawn_id(actorNumber,location, rotation, scale);
                    else
                        qlabsRobot.spawn_id_degrees(actorNumber,location, rotation, scale);
                    end
                end
                
                robotActors{i} = qlabsRobot;
            end
        end
        % 

        function [name, robotDict] = createRobot(obj, qLabsActor)
            % Create configuration for a specific robot
            classID = qLabsActor.classID;
            actorNumber = qLabsActor.actorNumber;

            switch classID
                case 10  % QArm
                    [name, robotDict] = obj.createQArm(actorNumber);
                case 23  % QBotPlatform
                    [name, robotDict] = obj.createQBP(actorNumber);
                case 161  % QCar2
                    [name, robotDict] = obj.createQC2(actorNumber);
                case 231  % QDrone2
                    [name, robotDict] = obj.createQD2(actorNumber);
            end
        end


        function [name, robotDict] = createQArm(obj, actorNumber)
            path = obj.copyQArm_files(actorNumber);
            %[path, ~] = fileparts(path);
            
            hilPort = obj.nextNumber();
            videoPort = obj.nextNumber();
            uriPort = obj.nextURINumber();
            
            arguments = sprintf('-uri_hil tcpip://localhost:%d -uri_video tcpip://localhost:%d', ...
                hilPort, videoPort);
            
            fprintf('QArm %d spawned as %s\n', actorNumber, arguments);

            obj.start_real_time_model(path, actorNumber, uriPort, arguments);
        
            name = sprintf('QA_%d', actorNumber);
            robotDict = struct('robotType', 'QArm', ...
                'actorNumber', actorNumber, ...
                'classID', 10, ...
                'hilPort', hilPort, ...
                'videoPort', videoPort);

        end

        
        function [name, robotDict] = createQBP(obj, actorNumber)
            [workspacePath, driverPath] = obj.copyQBP_files(actorNumber);
            %[workspacePath, ~] = fileparts(workspacePath);
            %[driverPath, ~] = fileparts(driverPath);
            
            videoPort = obj.nextNumber();
            video3dPort = obj.nextNumber();
            lidarPort = obj.nextNumber();
            uriPort = obj.nextURINumber();
            
            hilPort = 18950 + actorNumber;
            driverPort = 18970 + actorNumber;
            uriPortDriver = obj.nextURINumber();
            
            arguments = sprintf('-uri_hil tcpip://localhost:%d -uri_video tcpip://localhost:%d -uri_video3d tcpip://localhost:%d -uri_lidar tcpip://localhost:%d', ...
                hilPort, videoPort, video3dPort, lidarPort);
            
            fprintf('QBP %d spawned as %s\n', actorNumber, arguments);

            % Start spawn models
            obj.start_real_time_model(workspacePath, actorNumber, uriPort, arguments);

            driverArguments = sprintf("-uri tcpip://localhost:%d", uriPortDriver);
            obj.start_real_time_model_driver(driverPath, actorNumber, driverArguments);

            
            name = sprintf('QBP_%d', actorNumber);
            robotDict = struct('robotType', 'QBP', ...
                'actorNumber', actorNumber, ...
                'classID', 23, ...
                'hilPort', hilPort, ...
                'videoPort', videoPort, ...
                'video3dPort', video3dPort, ...
                'lidarPort', lidarPort, ...
                'driverPort', driverPort);
        end
        
        function [name, robotDict] = createQC2(obj, actorNumber)
            path = obj.copyQC2_files(actorNumber);
            %[path, ~] = fileparts(path);
            
            hilPort = obj.nextNumber();
            video0Port = obj.nextNumber();
            video1Port = obj.nextNumber();
            video2Port = obj.nextNumber();
            video3Port = obj.nextNumber();
            video3dPort = obj.nextNumber();
            lidarPort = obj.nextNumber();
            gpsPort = obj.nextNumber();
            lidarIdealPort = obj.nextNumber();
            ledPort = obj.nextNumber();
            uriPort = obj.nextURINumber();
            
            arguments = sprintf('-uri_hil tcpip://localhost:%d -uri_video0 tcpip://localhost:%d -uri_video1 tcpip://localhost:%d -uri_video2 tcpip://localhost:%d -uri_video3 tcpip://localhost:%d -uri_video3d tcpip://localhost:%d -uri_lidar tcpip://localhost:%d -uri_gps tcpip://localhost:%d -uri_lidar_ideal tcpip://localhost:%d -uri_led tcpip://localhost:%d', ...
                hilPort, video0Port, video1Port, video2Port, video3Port, video3dPort, lidarPort, gpsPort, lidarIdealPort, ledPort);
            
            fprintf('QCar %d spawned as %s\n', actorNumber, arguments);

            obj.start_real_time_model(path, actorNumber, uriPort, arguments);

            name = sprintf('QC2_%d', actorNumber);
            robotDict = struct('robotType', 'QC2', ...
                'actorNumber', actorNumber, ...
                'classID', 161, ...
                'hilPort', hilPort, ...
                'videoPort', video0Port, ...
                'video3dPort', video3dPort, ...
                'lidarPort', lidarPort, ...
                'gpsPort', gpsPort, ...
                'lidarIdealPort', lidarIdealPort, ...
                'ledPort', ledPort);
        end
        
        function [name, robotDict] = createQD2(obj, actorNumber)
            path = obj.copyQD2_files(actorNumber);
            %[path, ~] = fileparts(path);
            
            hilPort = obj.nextNumber();
            video0Port = obj.nextNumber();
            video1Port = obj.nextNumber();
            video2Port = obj.nextNumber();
            video3Port = obj.nextNumber();
            video3dPort = obj.nextNumber();
            posePort = obj.nextNumber();
            uriPort = obj.nextURINumber();
            
            arguments = sprintf('-uri_hil tcpip://localhost:%d -uri_video0 tcpip://localhost:%d -uri_video1 tcpip://localhost:%d -uri_video2 tcpip://localhost:%d -uri_video3 tcpip://localhost:%d -uri_video3d tcpip://localhost:%d -uri_pose tcpip://localhost:%d', ...
                hilPort, video0Port, video1Port, video2Port, video3Port, video3dPort, posePort);
            
            fprintf('QDrone %d spawned as %s\n', actorNumber, arguments);

            obj.start_real_time_model(path, actorNumber, uriPort, arguments);
           
            
            name = sprintf('QD2_%d', actorNumber);
            robotDict = struct('robotType', 'QD2', ...
                'actorNumber', actorNumber, ...
                'classID', 231, ...
                'hilPort', hilPort, ...
                'videoPort', video0Port, ...
                'video3dPort', video3dPort, ...
                'posePort', posePort);
        end

        % Add these methods to the MultiAgent class within the methods block

        function newPath = copyQArm_files(obj, actorNumber)
            rtFile = 'QArm_Spawn';
            originalFile = [rtFile obj.fileType];
            originalPath = fullfile(obj.QArmDir, originalFile);
            newFile = [rtFile num2str(actorNumber) obj.fileType];
            newPath = fullfile(obj.directory, newFile);
            copyfile(originalPath, newPath);
            pause(0.2);
        end
        
        function [newPathWorkspace, newPathDriver] = copyQBP_files(obj, actorNumber)
            rtFile = 'QBotPlatform_Workspace';
            driverFile = ['qbot_platform_driver_virtual' num2str(actorNumber)];
            
            % Copy workspace file
            originalFile = [rtFile obj.fileType];
            originalPath = fullfile(obj.QBPDir, originalFile);
            newFile = [rtFile num2str(actorNumber) obj.fileType];
            newPathWorkspace = fullfile(obj.directory, newFile);
            copyfile(originalPath, newPathWorkspace);
            
            % Copy driver file
            originalFile = [driverFile obj.fileType];
            originalPath = fullfile(obj.QBPDriverDir, originalFile);
            newFile = [driverFile obj.fileType];
            newPathDriver = fullfile(obj.directory, newFile);
            copyfile(originalPath, newPathDriver);
            
            pause(0.2);
        end
        
        function newPath = copyQC2_files(obj, actorNumber)
            rtFile = 'QCar2_Workspace';
            originalFile = [rtFile obj.fileType];
            originalPath = fullfile(obj.QCar2Dir, originalFile);
            newFile = [rtFile num2str(actorNumber) obj.fileType];
            newPath = fullfile(obj.directory, newFile);
            copyfile(originalPath, newPath);
            pause(0.2);
        end
        
        function newPath = copyQD2_files(obj, actorNumber)
            rtFile = 'QDrone2_Workspace';
            originalFile = [rtFile obj.fileType];
            originalPath = fullfile(obj.QD2Dir, originalFile);
            newFile = [rtFile num2str(actorNumber) obj.fileType];
            newPath = fullfile(obj.directory, newFile);
            copyfile(originalPath, newPath);
            pause(0.2);
        end

        function cmdString = start_real_time_model(obj, modelName, actorNumber, uriPort, additionalArguments)
            
            [ ~ ,name, ~] = fileparts(modelName);
            initial = sprintf(' start \"QLabs_%s_%d\" \"%s\\quarc_run\" -D -r -t tcpip://localhost:17000  \"%s\"', name,actorNumber, obj.rtModels, modelName);
            %create spawn model string
            defaultFunction = " -uri tcpip://localhost:" + uriPort +" -hostname localhost -devicenum " + actorNumber + " ";
            QUARCRUN = initial + defaultFunction + additionalArguments;
            cmdString = QUARCRUN;
            %disp(cmdString)
            % Start spawn model
            system(cmdString);
        end

        function cmdString = start_real_time_model_driver(obj, modelName, actorNumber, additionalArguments)
            
            [ ~ ,name, ~] = fileparts(modelName);
            initial = sprintf(' start \"QLabs_%s_%d\" \"%s\\quarc_run\" -D -r -t tcpip://localhost:17000  \"%s\" ', name,actorNumber, obj.rtModels, modelName);
            %create spawn model string
            QUARCRUN = initial + additionalArguments;
            cmdString = QUARCRUN;
            %disp(cmdString)
            % Start spawn model
            system(cmdString);
        end

        function port = nextNumber(obj)
            obj.portNumber = obj.portNumber + 1;
            port = obj.portNumber;
        end

        function port = nextURINumber(obj)
            obj.uriPortNumber = obj.uriPortNumber + 1;
            port = obj.uriPortNumber;
        end
    end
        
end

% % MOVE THIS TO NEW FILE function to read robots configuration
% function robotsDict = readRobots()
%     directory = fullfile(getenv('RTMODELS_DIR'), 'MultiAgent');
%     filePath = fullfile(directory, 'RobotAgents.json');
% 
%     % Read JSON file
%     fid = fopen(filePath, 'r');
%     raw = fread(fid, inf);
%     fclose(fid);
% 
%     robotsDict = jsondecode(char(raw'));
% end
