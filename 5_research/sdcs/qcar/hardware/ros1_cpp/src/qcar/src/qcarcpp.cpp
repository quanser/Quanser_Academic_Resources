#include "ros/ros.h"
#include "std_msgs/String.h"
#include "std_msgs/Float32.h"
#include "geometry_msgs/Vector3Stamped.h"
#include "quanser_types.h"
#include "hil.h"
#include <sstream>
t_double	throttle;
// t_double	steering;
t_double	other_channel_buffer[9] = {0.0};



void cmd_sub(const geometry_msgs::Vector3Stamped::ConstPtr& msg)
{
	// t_double	throttle;
	t_double	steering;

	throttle = -msg->vector.x;
	steering = -msg->vector.y;
	

	// throttle = std::max(0.2, std::min(-0.2, throttle));

	// ROS_INFO("I heard: [%f]", throttle);
	
	other_channel_buffer[0] = steering;


}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "qcar");

	static const char	board_type[] = "qcar";
	static const char	board_identifier[] = "0";
	static char			message[512];

	t_double	command[2];
	// t_double	write_pwm_buffer_throttle;
	// t_double	write_pwm_buffer_throttle;
	// t_double	write_other_buffer_LEDs[];
	t_boolean	enable;

	t_card		board;
	t_error 	result;
	result = hil_open(board_type, board_identifier, &board);
	if (result == 0)
	{
		const t_uint32 write_pwm_channel_throttle	= 0;
		const t_uint32 write_other_channel_steering	= 0;
		const t_uint32 write_other_channels_str_LEDs[]	= {1000, 11008, 11009, 11010, 11011, 11000, 11001, 11002, 11003};
		const t_uint32 write_digital_coast 			= 40;

		t_pwm_mode pwm_mode[]							= {PWM_DUTY_CYCLE_MODE};
		t_double	pwm_frequency[]						= {60e6/4096};

		result = hil_set_pwm_mode(board, &write_pwm_channel_throttle, 1, pwm_mode);
		// ROS_INFO("Hil_set_pwm_mode return value:  [%d]", result);
		result = hil_set_pwm_frequency(board, &write_pwm_channel_throttle, 1, pwm_frequency);
		// ROS_INFO("Hil_set_frequency_mode return value:  [%d]", result);
		result = hil_write_digital(board, &write_digital_coast, 1, 0);
		// ROS_INFO("Hil_write_coast return value:  [%d]", result);
		ros::NodeHandle n;

		ros::Rate loop_rate(500);

		ros::Subscriber sub = n.subscribe("/qcar/user_command", 100, cmd_sub);

		while (ros::ok())
		{
			// ROS_INFO("Thorttle: [%f]   Steering: [%f]", throttle, other_channel_buffer[0]);
			result = hil_write(board, NULL, 0, &write_pwm_channel_throttle, 1, NULL, 0, write_other_channels_str_LEDs, 9, NULL, &throttle, NULL, other_channel_buffer);
			// ROS_INFO("I heard: [%d]", result);
			ros::spinOnce();
			loop_rate.sleep();
		}
		

		throttle = 0;
		other_channel_buffer[0] = {0.0};

		hil_write(board, NULL, 0, &write_pwm_channel_throttle, 1, NULL, 0, write_other_channels_str_LEDs, 9, NULL, &throttle, NULL, other_channel_buffer);
	
		hil_close(board);
	}

	return 0;
}