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

using namespace std::chrono_literals;
using namespace std::placeholders;


class RGBD: public rclcpp::Node
{
    public:
    RGBD(): Node("rgbd")
    {

        // Parameters initialization
        try
        {
            parameter_cb = this->add_on_set_parameters_callback(std::bind(&RGBD::set_parameters_callback, this, _1));
        }
        catch (const std::bad_alloc& e)
        {
            RCLCPP_ERROR(this->get_logger(), "Error setting up parameters callback. %s", e.what());
            return;
        }

        // Configure ROS2 paramters
        this->parameterSetup();

        // Read Parameters once node has started
        this->getParameters();

        //Use device_type to automatically configure for virtual or physical, leave blank to use custom values
        if(device_type.compare("physical")==0){
            camera_identifier = "0";
        }
        else if (device_type.compare("virtual")==0)
        {
            camera_identifier ="0@tcpip://localhost:18965";
        }
        else if (device_type.compare("custom")==0)
        {
            camera_identifier = camera_num.append(device_num);
        }
        else
            {RCLCPP_ERROR(this->get_logger(), "The device type selected in invalid, please restart the node and select from virtual/physical/custom....");
            return;
            }

        // Logger info for user to be aware of how the camera was configured
        RCLCPP_INFO(this->get_logger(),"Camera identifier is: %s ",camera_identifier.c_str());


        //Open the video3D device using the passed parameters
		result = video3d_open(camera_identifier.c_str(), &capture);
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_open error: %s", error_message);
            return;
        }
        else if (result>=0)
        {
            // Open video3d stream
            result_rgb = video3d_stream_open(capture, VIDEO3D_STREAM_COLOR, 0, frame_rate_param, frame_width_rgb, frame_height_rgb, IMAGE_FORMAT_ROW_MAJOR_INTERLEAVED_BGR, IMAGE_DATA_TYPE_UINT8, &rgb_stream);
            result_depth = video3d_stream_open(capture, VIDEO3D_STREAM_DEPTH, 0, frame_rate_param, frame_width_depth, frame_height_depth, IMAGE_FORMAT_ROW_MAJOR_GRAYSCALE, IMAGE_DATA_TYPE_UINT16, &depth_stream);
            // RCLCPP_INFO(this->get_logger(),"Result_rgb, Result_depth: %i,%i ",result_rgb,result_depth);

            if ((result_rgb >= 0) && (result_depth >= 0))
                {
                    // Start streaming images from camera
                    result = video3d_start_streaming(capture);
                }
            else
            {
                msg_get_error_messageA(NULL, result_rgb, error_message, sizeof(error_message));
                RCLCPP_ERROR(this->get_logger(), "streaming rgb Error: %s", error_message);
                msg_get_error_messageA(NULL, result_depth, error_message, sizeof(error_message));
                RCLCPP_ERROR(this->get_logger(), "streaming depth Error: %s", error_message);
                return;
            }
        }



        frame_rate_milliseconds = int((1/frame_rate_param)*1000.0);
        // Timer to publish images periodically
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(frame_rate_milliseconds),
            std::bind(&RGBD::publishImages, this)
        );

    }

    void parameterSetup(){
        auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};


        param_desc.description = "Virtual/physical/custom camera flag";
        param_desc.additional_constraints = "This flag is used to automatically set the camera info to switch from virtual/physical/custom";
        this->declare_parameter("device_type",device_type,param_desc);


        param_desc.description = "Camera Number Configuration";
        param_desc.additional_constraints = "The camera number of the RGBD camera. On QBot Platform, it should normally be 0";
        this->declare_parameter("camera_num",camera_num_identifier,param_desc);

        param_desc.description = "Device Number Configuration";
        param_desc.additional_constraints = "The device number parameter is used to switch between information coming from the virtual QCar2 RGBD camera or the physical QCar2";
        this->declare_parameter("device_num",device_num_identifier, param_desc);

        param_desc.description = "The requested frame width of the RGB stream. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
        param_desc.additional_constraints = "Possible values:\n\t320 x 180 @???\n\t320 x 240 @???\n\t424 x 240 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t960 x 540 @???\n\t1280 x 720 @???\n\t1920 x 1080 @???";
        this->declare_parameter("frame_width_rgb", 1280, param_desc);

        param_desc.description = "The requested frame height of the RGB stream. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
        param_desc.additional_constraints = "Possible values:\n\t320 x 180 @???\n\t320 x 240 @???\n\t424 x 240 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t960 x 540 @???\n\t1280 x 720 @???\n\t1920 x 1080 @???";
        this->declare_parameter("frame_height_rgb", 720, param_desc);

        param_desc.description = "The requested frame width of the Depth stream. Only certain combinations of frame_width_depth, frame_height_depth, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
        param_desc.additional_constraints = "Possible values:\n\t256 x 144 @???\n\t848 x 100 @???\n\t424 x 240 @???\n\t480 x 270 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t1280 x 720 @???";
        this->declare_parameter("frame_width_depth", 1280, param_desc);

        param_desc.description = "The requested frame height of the Depth stream. Only certain combinations of frame_width_depth, frame_height_depth, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
        param_desc.additional_constraints = "Possible values:\n\t256 x 144 @???\n\t848 x 100 @???\n\t424 x 240 @???\n\t480 x 270 @???\n\t640 x 360 @???\n\t640 x 480 @???\n\t848 x 480 @???\n\t1280 x 720 @???";
        this->declare_parameter("frame_height_depth", 720, param_desc);

        param_desc.description = "The requested frame rate of the CSI camera. Only certain combinations of frame_width_rgb, frame_height_rgb, and frame_rate parameters can be used. Refer to the following Additional constraints for details.";
        param_desc.additional_constraints = "Possible values:\n\t640 x 400 @210.0\n\t640 x 480 @180.0\n\t1280 x 720 @130.0\n\t1280 x 800 @120.0";
        this->declare_parameter("frame_rate", 30.0, param_desc);

    }

    void getParameters(){

        // Info for user to know what has been configured
        device_type = this->get_parameter("device_type").as_string();

        rclcpp::Parameter camera_num_param  = this->get_parameter("camera_num");
        camera_num = camera_num_param.as_string();

        rclcpp::Parameter device_num_param  = this->get_parameter("device_num");
        device_num = device_num_param.as_string();

        frame_width_rgb = this->get_parameter("frame_width_rgb").as_int();
        frame_height_rgb = this->get_parameter("frame_height_rgb").as_int();

        frame_width_depth = this->get_parameter("frame_width_depth").as_int();
        frame_height_depth = this->get_parameter("frame_height_depth").as_int();


        frame_rate_param = this->get_parameter("frame_rate").as_double();

    }

    void ImageTransportSetup(){

        // Now that we are sure the node is a shared_ptr, we can use shared_from_this()
        image_transport::ImageTransport it(shared_from_this());

        // Advertise RGB and Depth topics using image_transport
        rgb_pub_ = it.advertise("camera/color_image", 1);
        depth_pub_ = it.advertise("camera/depth_image", 1);
    }


    ~RGBD()
    {
        int result;

        result = video3d_close(capture);
        if (result <0)
            RCLCPP_ERROR(this->get_logger(),"Closing the RGBD camera with error: %d", result);

        node_running = false;
        RCLCPP_INFO(this->get_logger(),"rgbd exit");

    }
    private:

    void publishImages()
    {

        // Allocate memory for reading image information
        buffer_rgb = (t_uint8 *) memory_allocate(frame_width_rgb * frame_height_rgb * 3 * sizeof(t_uint8));
        buffer_depth = (t_uint16 *) memory_allocate(frame_width_depth * frame_height_depth * sizeof(t_uint16));


        if ((buffer_rgb != NULL) && (buffer_depth != NULL))
	    {

            // if the image buffers area not NULL then let's generate RGB and depth info based on video3d get frame
            t_video3d_frame rgb_frame;
            t_video3d_frame depth_frame;

            cv::Mat color_matrix;
            cv::Mat depth_matrix;

            std_msgs::msg::Header hdr;
            sensor_msgs::msg::Image::SharedPtr msg;

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
                        msg->header.stamp = this->get_clock()->now();
                        msg->header.frame_id = "color_image";
                        rgb_pub_.publish(*msg);
                    }
                }
                else
                {
                    msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(this->get_logger(), "Error getting data from rgb frame: %d -> %s", result, error_message);
                }

                video3d_frame_release(rgb_frame);
            }
            else
            {
                if (result != -QERR_WOULD_BLOCK)
                {
                    msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(this->get_logger(), "Error getting frame from rgb stream: %d -> %s", result, error_message);
                }

                    // Try to send the same frame as last time
                    msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::BGR8, color_matrix).toImageMsg();
                    rgb_pub_.publish(*msg);
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
                        msg->header.stamp = this->get_clock()->now();
                        msg->header.frame_id = "depth_image";
                        depth_pub_.publish(*msg);
                    }
                }
                else
                {
                    msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                    RCLCPP_ERROR(this->get_logger(), "Error getting data from depth frame: %d -> %s", result, error_message);
                }

                video3d_frame_release(depth_frame);
            }
            else
                    {
                        if (result != -QERR_WOULD_BLOCK)
                        {
                            msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                            RCLCPP_ERROR(this->get_logger(), "Error getting frame from depth stream: %d -> %s", result, error_message);
                        }

                        // Try to send the same frame as last time
                        msg = cv_bridge::CvImage(hdr, sensor_msgs::image_encodings::MONO16, depth_matrix).toImageMsg();
                        depth_pub_.publish(*msg);
                    }

        }

        memory_free(buffer_rgb);
		memory_free(buffer_depth);


    }
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
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("device_num") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("frame_width_rgb") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("frame_height_rgb") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("frame_width_depth") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("frame_height_depth") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("frame_rate") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
        }

        return result;
    }

        // check for node running
        bool node_running = false;

        // parameters change callback
        rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameter_cb;


        // Sample time to get data from rgb image
        int frame_rate_milliseconds;

        // Used for identifying quarc error message
        char error_message[1024];


        // parameters that cannot be changed once node is running
        std::string camera_num_identifier = "0";
        std::string device_num_identifier = "";
        std::string device_type = "physical";


        std::string camera_num;
        std::string device_num;


        std::string camera_identifier = " ";
        t_uint32 frame_width_rgb = 1280;
        t_uint32 frame_height_rgb = 720;
        t_uint32 frame_width_depth = 1280;
        t_uint32 frame_height_depth = 720;
        t_double frame_rate_param = 30.0;

        t_uint8  *buffer_rgb;
        t_uint16 *buffer_depth;

        t_video3d capture;
        t_error result, result_rgb, result_depth;
        t_video3d_stream rgb_stream;
        t_video3d_stream depth_stream;


        // Image publishers
        image_transport::Publisher rgb_pub_;
        image_transport::Publisher depth_pub_;

        // Timer for periodic publishing
        rclcpp::TimerBase::SharedPtr timer_;

};




int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);

    // Node creation
    auto node = std::make_shared<RGBD>();

    // Now we can safely call setup() because node is a shared_ptr
    node->ImageTransportSetup();

    // Get a multi-threaded executor
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(node);

    RCLCPP_INFO(node->get_logger(), "Starting rgbd camera loop...");
    executor.spin();


    RCLCPP_INFO(node->get_logger(), "rgbd camera ended.");
    rclcpp::shutdown();

    return 0;
}