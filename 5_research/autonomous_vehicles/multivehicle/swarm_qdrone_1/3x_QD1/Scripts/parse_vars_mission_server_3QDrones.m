%% Auto-generated script file for parsing the stored variables
%
function parse_vars( input_data )
%

	%% Default Model Time vector - always in the first row of the data file
	assignin('base','t',input_data(1,:));

	%% Initial Home POSE (x,y,z,heading) for Vehicle 1
	assignin('base','pose_home_1',input_data(2:5,:));

	%% Initial Home POSE (x,y,z,heading) for Vehicle 2
	assignin('base','pose_home_2',input_data(6:9,:));

	%% Initial Home POSE (x,y,z,heading) for Vehicle 3
	assignin('base','pose_home_3',input_data(10:13,:));

	%% Desired Trajectory (x,y,z,heading) for Vehicle 1
	assignin('base','traj_1',input_data(14:17,:));

	%% Desired Trajectory (x,y,z,heading) for Vehicle 2
	assignin('base','traj_2',input_data(18:21,:));

	%% Desired Trajectory (x,y,z,heading) for Vehicle 3
	assignin('base','traj_3',input_data(22:25,:));

	%% Enable Signal for Swarm Trajectory (for all of the vehicles)
	assignin('base','traj_enable',input_data(26,:));

	%% Play/Pause Signal (1/0) for Swarm Trajectory (for all of the vehicles)
	assignin('base','traj_play',input_data(27,:));

	%% Loop Back Time (s) for each of the vehicles in the Swarm
	assignin('base','loop_times',input_data(28:30,:));

	%% Communiation Issue Flag for each of the vehicles in the Swarm
	assignin('base','comm_issues',input_data(31:33,:));

	%% Arm/Disarm (1/0) Signal from Operator
	assignin('base','arm',input_data(34,:));

	%% Takeoff/Land (1/0) Signal from Operator
	assignin('base','takeoff',input_data(35,:));

	%% Emergency Stop Signal (eStop) from Operator
	assignin('base','estop',input_data(36,:));

	%% Joystick Issue Signal
	assignin('base','joystick_issue',input_data(37,:));

	%% Measured Position (x,y,z) (m) for Vehicle 1
	assignin('base','pos_1',input_data(38:40,:));

	%% Measured Position (x,y,z) (m) for Vehicle 2
	assignin('base','pos_2',input_data(41:43,:));

	%% Measured Position (x,y,z) (m) for Vehicle 3
	assignin('base','pos_3',input_data(44:46,:));

	%% Measured Orientation (Roll, Pitch, Yaw) (rad) for Vehicle 1
	assignin('base','rot_1',input_data(47:49,:));

	%% Measured Orientation (Roll, Pitch, Yaw) (rad) for Vehicle 2
	assignin('base','rot_2',input_data(50:52,:));

	%% Measured Orientation (Roll, Pitch, Yaw) (rad) for Vehicle 3
	assignin('base','rot_3',input_data(53:55,:));

	%% isTracking signal for each of the vehicles in the swarm
	assignin('base','is_tracking',input_data(56:58,:));


end
