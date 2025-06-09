#include <ros/ros.h>
#include "sensor_msgs/LaserScan.h"

#include "quanser_types.h"
#include "quanser_memory.h"
#include "quanser_messages.h"
#include "quanser_signal.h"
#include "quanser_timer.h"
#include "quanser_ranging_sensor.h"

#include <iostream>
#include <algorithm>
using namespace std;

void reverse(t_ranging_measurement arr[], int low, int high)
{
	if (low < high)
	{
		swap<t_ranging_measurement>(arr[low], arr[high]);
		reverse(arr, low + 1, high - 1);
	}
}

int main(int argc, char **argv)
{
	 const t_uint32 num_measurements    = 720;
	 static const char uri[]            = "serial-cpu://localhost:2?baud='115200',word='8',parity='none',stop='1',flow='none',dsr='on'";
	 
	//  t_double measurements[num_measurements];
	 t_ranging_measurement measurements[num_measurements]   = {0.0};
	 t_double max_distance				= 10;
	 t_ranging_sensor   rplidar;
	 t_error            result;
	
	ros::init(argc, argv, "lidar_cpp_node");
	ros::NodeHandle n;
	ros::Rate loop_rate(30);
	ros::Publisher lidar_pub = n.advertise<sensor_msgs::LaserScan>("/scan", 1000);

	 result = rplidar_open(uri, RANGING_DISTANCE_SHORT, &rplidar);
	 if (result >= 0)
	 {
		sensor_msgs::LaserScan scan_msgs;
		ros::Time start_scan_time;
    	ros::Time end_scan_time;
		double scan_duration;
		while (ros::ok())
		{
			start_scan_time = ros::Time::now();
			result = rplidar_read(rplidar, RANGING_MEASUREMENT_MODE_INTERPOLATED, max_distance, measurements, num_measurements);
			end_scan_time = ros::Time::now();
			scan_duration = (end_scan_time - start_scan_time).toSec();
			scan_msgs.header.stamp = ros::Time::now();
			scan_msgs.header.frame_id = std::string("lidar");
			scan_msgs.angle_min = 0.0;
			scan_msgs.angle_max = 6.2744;
			scan_msgs.angle_increment = 0.0174532923847;
			scan_msgs.time_increment = 0.000132342218421;
			scan_msgs.scan_time = scan_duration;
			scan_msgs.range_min = 0.15;
			scan_msgs.range_max = 10.0;
			reverse(measurements, 0, 179);
			reverse(measurements, 180, 719);
			scan_msgs.ranges.resize(num_measurements);
			for (size_t i = 0; i < num_measurements; i++) {
					scan_msgs.ranges[i] = measurements[i].distance;
			}
	
			lidar_pub.publish(scan_msgs);
		}
		result = rplidar_close(rplidar);
	 }
	 else
	 {
		 char message[1024];
		msg_get_error_messageA(NULL, result, message, ARRAY_LENGTH(message));
		printf("ERROR: Unable to open RPLidar. %s\n", message);
	 }
	 
}