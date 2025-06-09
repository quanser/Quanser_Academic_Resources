#if defined(CV_BRDIGE_HAS_HPP)
#include <cv_bridge/cv_bridge.hpp>
#else
#include <cv_bridge/cv_bridge.h>
#endif

#include "image_transport/image_transport.hpp"

#include "opencv2/core/mat.hpp"
#include "opencv2/highgui.hpp"
#include "opencv2/videoio.hpp"

#include "rclcpp/rclcpp.hpp"

#include "quanser/quanser_messages.h"
#include "quanser/quanser_memory.h"
#include "quanser/quanser_video3d.h"

#include "std_msgs/msg/header.hpp"

bool node_running = false;

rcl_interfaces::msg::SetParametersResult set_parameters_callback(const std::vector<rclcpp::Parameter> & parameters)
{
    rcl_interfaces::msg::SetParametersResult result;
    
    result.successful = true;

    // Loop through the parameters....can happen if set_parameters_atomically() is called
    for (const auto & parameter : parameters)
    {
        if (parameter.get_name().compare("camera_num") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_width_rgb") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_height_rgb") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_width_depth") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_height_depth") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_rate") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else
        {
            result.successful = false;
            result.reason = "The parameter is invalid.";
        }
    }
    
    return result;
}


int main(int argc, char ** argv)
{
    char error_message[1024];
    char device_num[80];

    // parameters change callback
    rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameter_cb;

    // parameters that cannot be changed once node is running
    t_uint32 camera_num;    // = 0;
    t_uint32 frame_width_rgb = 1280;
	t_uint32 frame_height_rgb = 720;
    t_uint32 frame_width_depth = 1280;
	t_uint32 frame_height_depth = 720;
	t_double frame_rate = 30.0;
	
    t_uint8  *buffer_rgb;
	t_uint16 *buffer_depth;

	t_video3d capture;
	t_error result, result_rgb, result_depth;

    // Node creation
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions options;
    rclcpp::Node::SharedPtr node = rclcpp::Node::make_shared("rgbd", options);
    
    // Image transport creation
    image_transport::ImageTransport it(node);
    image_transport::Publisher color_pub = it.advertise("camera/color_image", 1);
    image_transport::Publisher depth_pub = it.advertise("camera/depth_image", 1);

    // Parameters initialization
    try
    {
        parameter_cb = node->add_on_set_parameters_callback(set_parameters_callback);
    }
    catch (const std::bad_alloc& e)
    {
        RCLCPP_ERROR(node->get_logger(), "Error setting up parameters callback. %s", e.what());
    }
    auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};

    param_desc.description = "The camera number of the RGBD camera. On QBot Platform, it should normally be 0";
    node->declare_parameter("camera_num", 0, param_desc);
    camera_num = node->get_parameter("camera_num").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter camera_num = %d", camera_num);

    param_desc.description = "The requested frame width of the RGB stream. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t320 x 180 @???\n\t320 x 240 @???\n\t424 x 240 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t960 x 540 @???\n\t1280 x 720 @???\n\t1920 x 1080 @???";
    node->declare_parameter("frame_width_rgb", 1280, param_desc);
    frame_width_rgb = node->get_parameter("frame_width_rgb").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_width_rgb = %d", frame_width_rgb);

    param_desc.description = "The requested frame height of the RGB stream. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t320 x 180 @???\n\t320 x 240 @???\n\t424 x 240 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t960 x 540 @???\n\t1280 x 720 @???\n\t1920 x 1080 @???";
    node->declare_parameter("frame_height_rgb", 720, param_desc);
    frame_height_rgb = node->get_parameter("frame_height_rgb").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_height_rgb = %d", frame_height_rgb);

    param_desc.description = "The requested frame width of the Depth stream. Only certain combinations of frame_width_depth, frame_height_depth, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t256 x 144 @???\n\t848 x 100 @???\n\t424 x 240 @???\n\t480 x 270 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t1280 x 720 @???";
    node->declare_parameter("frame_width_depth", 1280, param_desc);
    frame_width_depth = node->get_parameter("frame_width_depth").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_width_depth = %d", frame_width_depth);

    param_desc.description = "The requested frame height of the Depth stream. Only certain combinations of frame_width_depth, frame_height_depth, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t256 x 144 @???\n\t848 x 100 @???\n\t424 x 240 @???\n\t480 x 270 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t1280 x 720 @???";
    node->declare_parameter("frame_height_depth", 720, param_desc);
    frame_height_depth = node->get_parameter("frame_height_depth").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_height_depth = %d", frame_height_depth);

    param_desc.description = "The requested frame rate of the CSI camera. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t640 x 400 @210.0\n\t640 x 480 @180.0\n\t1280 x 720 @130.0\n\t1280 x 800 @120.0";
    node->declare_parameter("frame_rate", 30.0, param_desc);
    frame_rate = node->get_parameter("frame_rate").as_double();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_rate = %lf", frame_rate);

    if (sprintf(device_num, "%d", camera_num) < 0)
    {
        RCLCPP_ERROR(node->get_logger(), "Cannot form camera device_num.");
        return -1;
    }

    buffer_rgb = (t_uint8 *) memory_allocate(frame_width_rgb * frame_height_rgb * 3 * sizeof(t_uint8));
	buffer_depth = (t_uint16 *) memory_allocate(frame_width_depth * frame_height_depth * sizeof(t_uint16));
    
    if ((buffer_rgb != NULL) && (buffer_depth != NULL))
	{
		result = video3d_open(device_num, &capture);
		if (result >= 0)
		{
            t_video3d_stream rgb_stream;
            t_video3d_stream depth_stream;

			result_rgb = video3d_stream_open(capture, VIDEO3D_STREAM_COLOR, 0, frame_rate, frame_width_rgb, frame_height_rgb, IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR, IMAGE_DATA_TYPE_UINT8, &rgb_stream);
            result_depth = video3d_stream_open(capture, VIDEO3D_STREAM_DEPTH, 0, frame_rate, frame_width_depth, frame_height_depth, IMAGE_FORMAT_ROW_MAJOR_GRAYSCALE, IMAGE_DATA_TYPE_UINT16, &depth_stream);
			if ((result_rgb >= 0) && (result_depth >= 0))
			{
				result = video3d_start_streaming(capture);
                if (result >= 0)
                {
                    t_video3d_frame rgb_frame;
                    t_video3d_frame depth_frame;

                    cv::Mat color_matrix;
                    cv::Mat depth_matrix;

                    std_msgs::msg::Header hdr;
                    sensor_msgs::msg::Image::SharedPtr msg;
                    
                    RCLCPP_INFO(node->get_logger(), "Starting image loop...");

                    rclcpp::WallRate loop_rate(frame_rate);
                    node_running = true;
                    while (rclcpp::ok())
                    {
                        // RGB stream
                        result = video3d_stream_get_frame(rgb_stream, &rgb_frame);
					    if (result >= 0)
                        {
                            result = video3d_frame_get_data(rgb_frame, buffer_rgb);
                            if (result >= 0)
                            {
                                color_matrix = cv::Mat(frame_height_rgb, frame_width_rgb, CV_8UC3, buffer_rgb);
                                // Check if grabbed frame is actually full with some content
                                if (!color_matrix.empty())
                                {
                                    msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::BGR8, color_matrix).toImageMsg();
                                    msg->header.stamp = node->get_clock()->now();
                                    msg->header.frame_id = "color_image";
                                    color_pub.publish(msg);
                                }    
                            }
                            else
                            {
                                msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                                RCLCPP_ERROR(node->get_logger(), "Error getting data from rgb frame: %d -> %s", result, error_message);
                            }

                            video3d_frame_release(rgb_frame);
                        }
                        else
                        {
                            if (result != -QERR_WOULD_BLOCK)
                            {
                                msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                                RCLCPP_ERROR(node->get_logger(), "Error getting frame from rgb stream: %d -> %s", result, error_message);
                            }

                            // Try to send the same frame as last time
                            msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::BGR8, color_matrix).toImageMsg();
                            color_pub.publish(msg);
                        }

                        // Depth stream
                        result = video3d_stream_get_frame(depth_stream, &depth_frame);
                        if (result >= 0)
                        {
                            result = video3d_frame_get_data(depth_frame, buffer_depth);
                            if (result >= 0)
                            {
                                depth_matrix = cv::Mat(frame_height_depth, frame_width_depth, CV_16UC1, buffer_depth);
                                
                                // Check if grabbed frame is actually full with some content
                                if (!depth_matrix.empty())
                                {
                                    msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::MONO16, depth_matrix).toImageMsg();
                                    msg->header.stamp = node->get_clock()->now();
                                    msg->header.frame_id = "depth_image";
                                    depth_pub.publish(msg);
                                }    
                            }
                            else
                            {
                                msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                                RCLCPP_ERROR(node->get_logger(), "Error getting data from depth frame: %d -> %s", result, error_message);
                            }
                            
						    video3d_frame_release(depth_frame);
                        }
                        else
                        {
                            if (result != -QERR_WOULD_BLOCK)
                            {
                                msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                                RCLCPP_ERROR(node->get_logger(), "Error getting frame from depth stream: %d -> %s", result, error_message);
                            }

                            // Try to send the same frame as last time
                            msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::MONO16, depth_matrix).toImageMsg();
                            depth_pub.publish(msg);
                        }

                        try
                        {
                            rclcpp::spin_some(node);
                            loop_rate.sleep();
                        }
                        catch(...)
                        {
                            // ImageTransport and the Node seems to both handle the Ctrl-C interrupt.
                            // One of them tries to shtudown and causes a rclcpp::execptions::RCLError exception
                            // with the error being:
                            //      failed to create guard condition: the given context is not valid,
                            //      either rcl_init() was not called or rcl_shutdown() was called.
                            //
                            // At this point, we're shutting down anyways, so just ignore the exception.
                            //RCLCPP_ERROR(node->get_logger(), "Caught exception");
                        }
                    }
                }
                else
                {
                    msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(node->get_logger(), "Error starting stream: %d -> %s", result, error_message);
                }

                RCLCPP_INFO(node->get_logger(), "image loop ended.");
                node_running = false;
                video3d_stream_close(rgb_stream);
				video3d_stream_close(depth_stream);
            }
            else
            {
                if (result_rgb < 0)
                {
                    msg_get_error_messageA(NULL, result_rgb, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(node->get_logger(), "Error opening RGB stream. result: %d -> %s", result_rgb, error_message);
                }

                if (result_depth < 0)
                {
                    msg_get_error_messageA(NULL, result_depth, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(node->get_logger(), "Error opening Depth stream. result: %d -> %s", result_depth, error_message);
                }
            }

            video3d_close(capture);
        }
        else
        {
            msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
            RCLCPP_ERROR(node->get_logger(), "Error opening device. result: %d -> %s", result, error_message);
        }

        memory_free(buffer_rgb);
		memory_free(buffer_depth);
        //memory_free(rgbd_buffer_depth);
    }
    else
    {
        RCLCPP_ERROR(node->get_logger(), "Error allocating memory for image buffer");
    }
    
    return 0;
}