#include <ros/ros.h>
#include <opencv2/core/core.hpp>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/Image.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include "quanser_types.h"
#include "quanser_memory.h"
#include "quanser_messages.h"
#include "quanser_signal.h"
#include "quanser_timer.h"
#include "quanser_video3d.h"

int main(int argc, char **argv)
{
	const t_uint32 frame_width  = 1280;
	const t_uint32 frame_height = 720;
	const t_uint32 frame_rate	= 30;
	t_uint8 *rgbd_color_buffer;
	t_single *rgbd_depth_buffer;
	t_video3d capture;
	t_error result_rgb;
	t_error result_d;
    t_error result;
	t_video3d_stream rgb_stream;
	t_video3d_stream depth_stream;
	t_video3d_frame rgb_frame;
	t_video3d_frame depth_frame;

	
	ros::init(argc, argv, "rgbd_cpp_node");
	ros::NodeHandle n;
	ros::Rate loop_rate(30);
	ros::Publisher rgbd_color_pub = n.advertise<sensor_msgs::Image>("/qcar/rgbd_color", 10);
	ros::Publisher rgbd_depth_pub = n.advertise<sensor_msgs::Image>("/qcar/rgbd_depth", 10);

	rgbd_color_buffer = (t_uint8 *) memory_allocate(frame_width * frame_height * 3 * sizeof(t_uint8));
	rgbd_depth_buffer = (t_single *) memory_allocate(frame_width * frame_height * sizeof(t_single));
	if ((rgbd_color_buffer != NULL) && (rgbd_depth_buffer != NULL))
	{
		result = video3d_open("0", &capture);
		if (result >= 0)
		{
			result_rgb = video3d_stream_open(capture, VIDEO3D_STREAM_COLOR, 0, frame_rate, frame_width, frame_height, IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR, IMAGE_DATA_TYPE_UINT8, &rgb_stream);
			result_d = video3d_stream_open(capture, VIDEO3D_STREAM_DEPTH, 0, frame_rate, frame_width, frame_height, IMAGE_FORMAT_ROW_MAJOR_GRAYSCALE, IMAGE_DATA_TYPE_UINT16, &depth_stream);
			if ((result_rgb >= 0) && (result_d >= 0))
			{
				result = video3d_start_streaming(capture);
				cv_bridge::CvImage img_bridge_rgb;
				sensor_msgs::Image img_msg_rgb;
				std_msgs::Header header_rgb;
				cv_bridge::CvImage img_bridge_d;
				sensor_msgs::Image img_msg_d;
				std_msgs::Header header_d;
				while (ros::ok())
				{
					result_rgb = video3d_stream_get_frame(rgb_stream, &rgb_frame);
					result_d = video3d_stream_get_frame(depth_stream, &depth_frame);
					if ((result_rgb >= 0) && (result_d >= 0))
					{
						result_rgb = video3d_frame_get_data(rgb_frame, rgbd_color_buffer);
						result_d = video3d_frame_get_meters(depth_frame, rgbd_depth_buffer);
						if ((result_rgb >= 0) && (result_d >= 0))
						{
							cv::Size size(frame_width, frame_height);
							cv::Mat cv_rgb(size, CV_8UC3, rgbd_color_buffer);
							cv::Mat cv_d(size, CV_32FC1, rgbd_depth_buffer);
							// cv_d *= 0.02;
							header_rgb.stamp = ros::Time::now();
							header_d.stamp = ros::Time::now();
							img_bridge_rgb = cv_bridge::CvImage(header_rgb, sensor_msgs::image_encodings::BGR8, cv_rgb);
							img_bridge_d = cv_bridge::CvImage(header_d, sensor_msgs::image_encodings::TYPE_32FC1, cv_d);
							img_bridge_rgb.toImageMsg(img_msg_rgb);
							img_bridge_d.toImageMsg(img_msg_d);
							rgbd_color_pub.publish(img_msg_rgb);
							rgbd_depth_pub.publish(img_msg_d);
						}
						else
						{
							// ROS_INFO("get_frame_data results: rgb: %d, d: %d", result_rgb, result_d);
						}
						
						video3d_frame_release(rgb_frame);
						video3d_frame_release(depth_frame);
					}
					else
					{
						// ROS_INFO("get_frame results: rgb: %d, d: %d", result_rgb, result_d);
					}
					
				}
				video3d_stream_close(rgb_stream);
				video3d_stream_close(depth_stream);
			}
			video3d_close(capture);
		}
		else
		{
			char message_rgb[1024];
			msg_get_error_messageA(NULL, result_rgb, message_rgb, ARRAY_LENGTH(message_rgb));
			printf("ERROR: Unable to capture RGB samples. %s\n", message_rgb);
			char message_d[1024];
			msg_get_error_messageA(NULL, result_d, message_d, ARRAY_LENGTH(message_d));
			printf("ERROR: Unable to capture Depth samples. %s\n", message_d);
		}

		memory_free(rgbd_color_buffer);
		memory_free(rgbd_depth_buffer);
	}

}