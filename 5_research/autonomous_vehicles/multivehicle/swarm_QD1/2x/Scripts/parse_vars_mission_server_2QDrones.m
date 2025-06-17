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

	%% Desired Trajectory (x,y,z,heading) for Vehicle 1
	assignin('base','traj_1',input_data(10:13,:));

	%% Desired Trajectory (x,y,z,heading) for Vehicle 2
	assignin('base','traj_2',input_data(14:17,:));

	%% Enable Signal for Swarm Trajectory (for all of the vehicles)
	assignin('base','traj_enable',input_data(18,:));

	%% Play/Pause Signal (1/0) for Swarm Trajectory (for all of the vehicles)
	assignin('base','traj_play',input_data(19,:));

	%% Loop Back Time (s) for each of the vehicles in the Swarm
	assignin('base','loop_times',input_data(20:21,:));

	%% Communiation Issue Flag for each of the vehicles in the Swarm
	assignin('base','comm_issues',input_data(22:23,:));

	%% Arm/Disarm (1/0) Signal from Operator
	assignin('base','arm',input_data(24,:));

	%% Takeoff/Land (1/0) Signal from Operator
	assignin('base','takeoff',input_data(25,:));

	%% Emergency Stop Signal (eStop) from Operator
	assignin('base','estop',input_data(26,:));

	%% Joystick Issue Signal
	assignin('base','joystick_issue',input_data(27,:));

	%% Measured Position (x,y,z) (m) for Vehicle 1
	assignin('base','pos_1',input_data(28:30,:));

	%% Measured Position (x,y,z) (m) for Vehicle 2
	assignin('base','pos_2',input_data(31:33,:));

	%% Measured Orientation (Roll, Pitch, Yaw) (rad) for Vehicle 1
	assignin('base','rot_1',input_data(34:36,:));

	%% Measured Orientation (Roll, Pitch, Yaw) (rad) for Vehicle 2
	assignin('base','rot_2',input_data(37:39,:));

	%% isTracking signal for each of the vehicles in the swarm
	assignin('base','is_tracking',input_data(40:41,:));


end
