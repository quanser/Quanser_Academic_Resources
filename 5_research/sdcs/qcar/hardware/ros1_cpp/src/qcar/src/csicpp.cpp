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
#include "quanser_video.h"

static int stop = 0;

void signal_handler(int signal)
{
	
	stop = 1;
}

int main(int argc, char **argv) //int main(int argc, char * argv[]) <-- this is what showned in quanser doc
{
	// qsigaction_t action;

	// action.sa_handler = signal_handler;
	// action.sa_flags = 0;
	// qsigemptyset(&actopm.sa_mask);
	// qsigaction(SIGINT, &action, NULL);

	const t_uint32 frame_width  = 640;
	const t_uint32 frame_height = 480;
	const t_uint32 frame_rate	= 30;
	t_uint8 *csi_front;
	t_video_capture capture;
	t_error result;
	// t_uint8	csi_front[frame_width*frame_height*3];
	// t_timeout	timeout, interval;

	// timeout_get_timeout(&interval, period);
	// timeout_get_current_time(&timeout);

	
	ros::init(argc, argv, "csi_cpp_node");
	ros::NodeHandle n;
	ros::Rate loop_rate(30);
	ros::Publisher csi_front_pub = n.advertise<sensor_msgs::Image>("/qcar/csi_front", 10);

	csi_front = (t_uint8 *) memory_allocate(frame_width * frame_height * 3 * sizeof(t_uint8));
	if (csi_front != NULL)
	{
		result = video_capture_open("video://localhost:3", frame_rate, frame_width, frame_height, IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR, IMAGE_DATA_TYPE_UINT8, csi_front, &capture, NULL, 0);
		if (result >= 0)
		{
			result = video_capture_start(capture);
			cv_bridge::CvImage img_bridge;
			sensor_msgs::Image img_msg;
			std_msgs::Header header;
			while (ros::ok())
			{
				result = video_capture_read(capture);
				if (result >= 0)
				{
					cv::Size size(frame_width, frame_height);
					cv::Mat cv_csi_front(size,CV_8UC3, csi_front);
					header.stamp = ros::Time::now();
					img_bridge = cv_bridge::CvImage(header, sensor_msgs::image_encodings::BGR8, cv_csi_front);
					img_bridge.toImageMsg(img_msg);
					csi_front_pub.publish(img_msg);
				}
			}
			video_capture_stop(capture);
			video_capture_close(capture);
		}
		else
		{
			char message[1024];
			msg_get_error_messageA(NULL, result, message, ARRAY_LENGTH(message));
			printf("ERROR: Unable to capture video samples. %s\n", message);
		}

		memory_free(csi_front);
	}


	



}