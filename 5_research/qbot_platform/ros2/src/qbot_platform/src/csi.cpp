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
#include "quanser/quanser_video.h"

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
        else if (parameter.get_name().compare("frame_width") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("frame_height") == 0)
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
    char uri[80];

    // parameters change callback
    rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameter_cb;

    // parameters that cannot be changed once node is running
    t_uint32 camera_num;    // = 0;
    t_uint32 frame_width;   // = 640;
    t_uint32 frame_height;  // = 400;
    t_double frame_rate;    // = 120;

    t_uint8 *image_buffer;
	t_video_capture capture;
    
    t_error result;

    // Node creation
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions options;
    rclcpp::Node::SharedPtr node = rclcpp::Node::make_shared("csi", options);

    // Image transport creation
    image_transport::ImageTransport it(node);
    image_transport::Publisher image_pub = it.advertise("camera/downward_image", 1);

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

    param_desc.description = "The camera number of the CSI camera. On QBot Platform, it should normally be 0";
    node->declare_parameter("camera_num", 0, param_desc);
    camera_num = node->get_parameter("camera_num").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter camera_num = %d", camera_num);

    param_desc.description = "The requested frame width of the CSI camera. Only certain combinations of frame_width, frame_height, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t640 x 400 @210.0\n\t640 x 480 @180.0\n\t1280 x 720 @130.0\n\t1280 x 800 @120.0";
    node->declare_parameter("frame_width", 640, param_desc);
    frame_width = node->get_parameter("frame_width").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_width = %d", frame_width);

    param_desc.description = "The requested frame height of the CSI camera. Only certain combinations of frame_width, frame_height, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t640 x 400 @210.0\n\t640 x 480 @180.0\n\t1280 x 720 @130.0\n\t1280 x 800 @120.0";
    node->declare_parameter("frame_height", 400, param_desc);
    frame_height = node->get_parameter("frame_height").as_int();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_height = %d", frame_height);

    param_desc.description = "The requested frame rate of the CSI camera. Only certain combinations of frame_width, frame_height, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
    param_desc.additional_constraints = "Possible values:\n\t640 x 400 @210.0\n\t640 x 480 @180.0\n\t1280 x 720 @130.0\n\t1280 x 800 @120.0";
    node->declare_parameter("frame_rate", 120.0, param_desc);
    frame_rate = node->get_parameter("frame_rate").as_double();
    //RCLCPP_INFO(node->get_logger(), "Parameter frame_rate = %lf", frame_rate);

    if (sprintf(uri, "video://localhost:%d", camera_num) < 0)
    {
        RCLCPP_ERROR(node->get_logger(), "Cannot form camera uri.");
        return -1;
    }
    //RCLCPP_INFO(node->get_logger(), "camera uri: %s", uri);

    // Buffer to be used to grab image from camera
    image_buffer = (t_uint8 *) memory_allocate(frame_width * frame_height * sizeof(t_uint8));

    if (image_buffer == NULL)
    {
        RCLCPP_ERROR(node->get_logger(), "Error allocating memory for image buffer");
        return -1;
    }
    result = video_capture_open(uri,
                                frame_rate,
                                frame_width,
                                frame_height,
                                IMAGE_FORMAT_ROW_MAJOR_GRAYSCALE,
                                IMAGE_DATA_TYPE_UINT8,
                                &capture,
                                NULL,
                                0);

    if (result >= 0)
    {
        result = video_capture_start(capture);
        if (result >= 0)
        {
            cv::Mat image_matrix;

            std_msgs::msg::Header hdr;
            sensor_msgs::msg::Image::SharedPtr msg;
            
            RCLCPP_INFO(node->get_logger(), "Starting image loop...");

            rclcpp::WallRate loop_rate(frame_rate);
            node_running = true;
            while (rclcpp::ok())
            {
                result = video_capture_read(capture, image_buffer);
                if (result >= 0)
                {
                    image_matrix = cv::Mat(frame_height, frame_width, CV_8UC1, image_buffer);
                    
                    // Check if grabbed frame is actually full with some content
                    if (!image_matrix.empty())
                    {
                        msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::MONO8, image_matrix).toImageMsg();
                        msg->header.stamp = node->get_clock()->now();
                        msg->header.frame_id = "downward_image";
                        image_pub.publish(msg);
                    }
                }
                else
                {
                    if (result != -QERR_WOULD_BLOCK)
                    {
                        msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                        RCLCPP_ERROR(node->get_logger(), "Error reading image: %d -> %s", result, error_message);
                    }

                    // Try to send the same frame as last time
                    msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::MONO8, image_matrix).toImageMsg();
                    image_pub.publish(msg);
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

            RCLCPP_INFO(node->get_logger(), "image loop ended.");
            node_running = false;
        }
        else
        {
            msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
            RCLCPP_ERROR(node->get_logger(), "Error starting capture: %d -> %s", result, error_message);
        }

        video_capture_stop(capture);
        video_capture_close(capture);
    }
    else
    {
        msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
        RCLCPP_ERROR(node->get_logger(), "Error opening device. result: %d -> %s", result, error_message);
    }

    memory_free(image_buffer);

    return 0;
}