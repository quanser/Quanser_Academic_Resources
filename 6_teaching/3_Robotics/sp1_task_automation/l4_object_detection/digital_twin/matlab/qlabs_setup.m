caseNum = 2; % 1, 2, 3, or 4

system('quanser_host_peripheral_client.exe -q');
pause(2)
system('quanser_host_peripheral_client.exe -uri tcpip://localhost:18444 &');

% MATLAB Path

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

% Stop RT models
try
    qc_stop_model('tcpip://localhost:17000', 'qbot_platform_driver_virtual')
    pause(1)
    qc_stop_model('tcpip://localhost:17000', 'QBotPlatform_Workspace')
catch error
end
pause(1)

% QLab connection
qlabs = QuanserInteractiveLabs();
connection_established = qlabs.open('localhost');

if connection_established == false
    disp("Failed to open connection.")
    return
end
disp('Connected')
verbose = true;
num_destroyed = qlabs.destroy_all_spawned_actors();

% Flooring
hFloor0 = QLabsQBotPlatformFlooring(qlabs);
    % center
    hFloor0.spawn_id(0, [-0.6, 0.6,   0], [0,0,-pi/2], [1,1,1], 5, false); 
    % corners
    hFloor0.spawn_id(1, [ 0.6, 1.8,   0], [0,0,-pi/2], [1,1,1], 0, false);
    hFloor0.spawn_id(2, [ 1.8,-0.6,   0], [0,0, pi  ], [1,1,1], 0, false);
    hFloor0.spawn_id(3, [-0.6,-1.8,   0], [0,0, pi/2], [1,1,1], 0, false);
    hFloor0.spawn_id(4, [-1.8, 0.6,   0], [0,0,    0], [1,1,1], 0, false);
    % sides
    hFloor0.spawn_id(5, [-0.6, 0.6,   0], [0,0,    0], [1,1,1], 5, false);
    hFloor0.spawn_id(6, [ 0.6, 0.6,   0], [0,0,-pi/2], [1,1,1], 5, false);
    hFloor0.spawn_id(7, [ 0.6,-0.6,   0], [0,0, pi  ], [1,1,1], 5, false);
    hFloor0.spawn_id(8, [-0.6,-0.6,   0], [0,0, pi/2], [1,1,1], 5, false);

% Walls
hWall = QLabsWalls(qlabs, verbose);
    hWall.spawn_degrees([2, 1.2, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([2, 0, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([2, -1.2, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([-2, 1.2, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([-2, 0, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([-2, -1.2, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([1.2, 2, 0.1], [0, 0, 90]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([0, 1.2, 0.1], [0, 0, 0]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([-1.2, 2, 0.1], [0, 0, 90]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([1.2, -2, 0.1], [0, 0, 90]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([0, -2, 0.1], [0, 0, 90]);
    hWall.set_enable_dynamics(true);
    hWall.spawn_degrees([-1.2, -2, 0.1], [0, 0, 90]);
    hWall.set_enable_dynamics(true);

% QBot
hQBot = QLabsQBotPlatform(qlabs, verbose);
location = [0, 0, 0; -1.35, 0.3, 0; -1.5, 0, 0; -1.5, 0, 0];
rotation = [0, 0, 0;    0,   0, 0;   0, 0, 90;  0, 0, -90];
    hQBot.spawn_id_degrees(0, location(caseNum, :), rotation(caseNum, :), [1, 1, 1], 1) ;
    hQBot.possess(hQBot.VIEWPOINT_TRAILING);

    file_workspace = fullfile(getenv('RTMODELS_DIR'), 'QBotPlatform', 'QBotPlatform_Workspace.rt-win64');
    file_driver    = fullfile(getenv('RTMODELS_DIR'), 'QBotPlatform', 'qbot_platform_driver_virtual.rt-win64');


% Start RT models
pause(2)
system(['quarc_run -D -r -t tcpip://localhost:17000 ', file_workspace]);
pause(1)
system(['quarc_run -D -r -t tcpip://localhost:17000 ', file_driver, ' -uri tcpip://localhost:17098']);
pause(3)

