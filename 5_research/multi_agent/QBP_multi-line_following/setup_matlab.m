% MultiAgent QBot Platform Example
% ----------------------------------
% 
% .. note::
% 
%     Make sure you have Quanser Interactive Labs open in Open World/Warehouse
%     environment before running this example.  
%     First run this file to set up the environment. Then use
%     line_folowing.slx and a joystick to control the QBots Line following.
% 

close all;
clear all;
clc;

% --------------------------------------------------------------
% Setting MATLAB Path for the libraries
% Always keep at the start, it will make sure it finds the correct references
newPathEntry = fullfile(getenv('QAL_DIR'), '0_libraries', 'matlab', 'qvl');
pathCell = regexp(path, pathsep, 'split');
if ispc  % Windows is not case-sensitive
  onPath = any(strcmpi(newPathEntry, pathCell));
else
  onPath = any(strcmp(newPathEntry, pathCell));
end

if onPath == 0
    path(path, newPathEntry)
    savepath
end
% --------------------------------------------------------------

fprintf('\n\n------------------------------ Communications --------------------------------\n\n');

qlabs =  QuanserInteractiveLabs();
connection_established = qlabs.open('localhost');

if connection_established == false
    disp("Failed to open connection.")
    return
end

disp('Connected')

num_destroyed = qlabs.destroy_all_spawned_actors();

fprintf('%d actors destroyed', num_destroyed, '');


% Initialize an instance of a camera 
camera = QLabsFreeCamera(qlabs);

% Set the spawn of the camera in a specific location 
camera.spawn_degrees([-1.771, 0.293, 1.169], [0, 39.681, -18.909])

% Spawn the camera
camera.possess();


% Initialize an instance of each configuration of floor mat 
floor = QLabsQBotPlatformFlooring(qlabs);
floor.spawn([ 0, 1.2,   0],[0,0,-pi/2])
floor.spawn([ 0, 0,   0],[0,0,-pi/2],[1,1,1],1)
floor.spawn([ 0, -2.4,   0],[0,0,0],[1,1,1], 3)
floor.spawn([ -1.2, 0,   0],[0,0,0])
floor.spawn([ -1.2, 0,   0],[0,0,-pi/2],[1,1,1], 1)
floor.spawn([ -1.2, -2.4,   0],[0,0,0],[1,1,1], 3)
 
coverup = QLabsBasicShape(qlabs);

%             location      rotation  scale
coverup.spawn([0.6,-0.6,0], [0,0,0], [0.59,0.7,0.007])

%                               color   roughness
coverup.set_material_properties([0,0,0], 0.6)

coverup.spawn([0.01,-0.6,0], [0,0,0], [0.55,0.7,0.007])
coverup.set_material_properties([0,0,0], 0.6)

coverup.spawn([-0.6,-0.6,0], [0,0,0], [0.59,0.7,0.007])
coverup.set_material_properties([0,0,0], 0.6)

coverup.spawn([-1.21,-0.6,0], [0,0,0], [0.59,0.7,0.007])
coverup.set_material_properties([0,0,0], 0.6)

pause(1);

% Closing qlabs
qlabs.close();
disp('Finish Flooring Spawn!');

%%

QBots = {};

QBots{end+1} = struct(...
    'RobotType', 'QBP', ...
    'Location', [.26, -.5, -0], ...
    'Rotation', [0, 0, -90] ...
);

QBots{end+1} = struct(...
    'RobotType', 'QBP', ...
    'Location', [0, 0.89, -0], ...
    'Rotation', [0, 0, 180] ...
);

QBots{end+1} = struct(...
    'RobotType', 'QBP', ...
    'Location', [-0.9, -1.1, -0], ...
    'Rotation', [0, 0, -90] ...
);


% Spawn robots
mySpawns = MultiAgent(QBots);

disp(mySpawns.robotActors)

mySpawns.qlabs.close()










