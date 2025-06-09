#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float32.h"
#include "geometry_msgs/Vector3Stamped.h"


#include "quanser_types.h"
#include "quanser_memory.h"
#include "quanser_messages.h"
#include "quanser_signal.h"
#include "quanser_timer.h"
#include "quanser_hid.h"
// #include "quanser_host_game_controller.h"

#include <sstream>

int main(int argc, char **argv)
{
	t_double LLA = 0.0;
	t_double LLO = 0.0;
	t_double LT = 0.0;
	t_double RLA = 0.0;
	t_double RLO = 0.0;
	t_double RT = 0.0;
	t_boolean flag_z = false;
	t_boolean flag_rz = false;
	t_double A = 0.0;
	t_double B = 0.0;
	t_uint8 X = 0.0;
	t_double Y = 0.0;
	t_uint8 LB = 0.0;
	t_double RB = 0.0;
	t_double up = 0.0;
	t_double right = 0.0;
	t_double left = 0.0;
	t_double down = 0.0;
	t_double command[2];
	t_double throttle;
	t_double steering;

	t_game_controller gamepad;
	t_error result;
	t_uint8 controller_number = 1;
	t_uint16 buffer_size = 12;
	t_double deadzone[6] = {0.0};
	t_double saturation[6] = {0.0};
	t_boolean auto_center = false;
	t_uint16 max_force_feedback_effects = 0;
	t_double force_feedback_gain = 0.0;
	t_game_controller_states data;
	t_boolean is_new;

	ros::init(argc, argv, "command_cpp_node");
	ros::NodeHandle n;
	ros::Rate loop_rate(1000);
	ros::Publisher command_pub = n.advertise<geometry_msgs::Vector3Stamped>("/qcar/user_command", 1000);

	result = game_controller_open(controller_number, buffer_size, deadzone, saturation, auto_center,
                     max_force_feedback_effects, force_feedback_gain, &gamepad);

	if (result >= 0)
	{
		geometry_msgs::Vector3Stamped command_msgs;

		while (ros::ok())
		{
			result = game_controller_poll(gamepad, &data, &is_new);
			LLA = -1*data.x;
			
			if (data.rz == 0 && !(flag_rz))
			{
				RT = 0;
			}
			else
			{
				RT = 0.5 + 0.5*data.rz;
				flag_rz = true;
			}
		

			A = (t_uint8)(data.buttons & (1 << 0));
			LB = (t_uint8)((data.buttons & (1 << 4))/16);
			if (is_new == true)
			{
				if (LB == 1)
				{
					if (A == 1)
					{
						throttle = RT * -0.3;
						steering = LLA * 0.5;
					}
					else
					{
						throttle = RT * 0.3;
						steering = LLA * 0.5;
					}
				}
				else
				{
					throttle = 0;
					steering = 0;
				}
				command_msgs.header.stamp = ros::Time::now();
				command_msgs.header.frame_id = std::string("command_input");
				command_msgs.vector.x = throttle;
				command_msgs.vector.y = steering;
				command_pub.publish(command_msgs);
			}
		}
		game_controller_close(gamepad);
	}

}