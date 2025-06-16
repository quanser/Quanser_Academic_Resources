#include "rclcpp/rclcpp.hpp"

#include "quanser/quanser_messages.h"
#include "quanser/quanser_ranging_sensor.h"

#include "sensor_msgs/msg/laser_scan.hpp"

bool node_running = false;

// RPLIDAR A2M12 parameters
t_double min_distance = 0.0;                    // in metre
t_double max_distance = 10.0;                   // in metre

const t_uint32 max_num_measurements = 1680;     // For RPLIDAR A2M12
t_ranging_distance ranging_distance = RANGING_DISTANCE_LONG;

// modifiable parameters
t_uint32 scan_mode = 1;     // the mode to be used. 0 - RANGING_MEASUREMENT_MODE_NORMAL, 1 - RANGING_MEASUREMENT_MODE_INTERPOLATED
t_uint32 num_scan_points;   // number of points to be sent out of the scan message

rcl_interfaces::msg::SetParametersResult set_parameters_callback(const std::vector<rclcpp::Parameter> & parameters)
{
    rcl_interfaces::msg::SetParametersResult result;
    
    result.successful = true;

    // Loop through the parameters....can happen if set_parameters_atomically() is called
    for (const auto & parameter : parameters)
    {
        if (parameter.get_name().compare("device_type") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("uri") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
        }
        else if (parameter.get_name().compare("scan_mode") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
            else if ((parameter.as_int() < 0) || (parameter.as_int() >= NUMBER_OF_RANGING_MEASUREMENT_MODES))
            {
                std::ostringstream error_stream;

                error_stream << "Paramater value out of range. Valid values must be betwwen 0 and " << (NUMBER_OF_RANGING_MEASUREMENT_MODES - 1);

                result.successful = false;
                result.reason = error_stream.str();
            }
            else if ((parameter.as_int() == RANGING_MEASUREMENT_MODE_NORMAL) && (num_scan_points != max_num_measurements))
            {
                std::ostringstream error_stream;

                error_stream << "num_scan_points must be " << max_num_measurements << " when scan_mode = 0.";

                result.successful = false;
                result.reason = error_stream.str();
            }
            else
            {
                // Normally we don't set a variable in the callback (we call parameter.get_param()
                // to get the parameter at the point we need to use it). But we have to set the
                // "scan_mode" global variable at this point, so that it can be used by
                // "num_scan_points" parameter change.
                scan_mode = parameter.as_int();
            }
        }
        else if (parameter.get_name().compare("num_scan_points") == 0)
        {
            if ((scan_mode == RANGING_MEASUREMENT_MODE_NORMAL) && (parameter.as_int() != max_num_measurements))
            {
                std::ostringstream error_stream;

                error_stream << "num_scan_points must be " << max_num_measurements << " when scan_mode = 0.";

                result.successful = false;
                result.reason = error_stream.str();
            }
            else if ((parameter.as_int() < 0) || (parameter.as_int() > max_num_measurements))
            {
                std::ostringstream error_stream;

                error_stream << "num_scan_points must be between 0 and " << max_num_measurements;

                result.successful = false;
                result.reason = error_stream.str();
            }
            else
            {
                // Normally we don't set a variable in the callback (we call parameter.get_param()
                // to get the parameter at the point we need to use it). But we have to set the
                // "num_scan_points" global variable at this point, so that it can be used by
                // "scan_mode" parameter change.
                num_scan_points = parameter.as_int();
            }
        }
        else if (parameter.get_name().compare("max_interpolated_distance") == 0)
        {
            if ((parameter.as_double() < min_distance) || (parameter.as_double() > max_distance))
            {
                std::ostringstream error_stream;

                error_stream << "max_interpolated_distance must be between " << min_distance << " and " << max_distance;

                result.successful = false;
                result.reason = error_stream.str();
            }
        }
        else if (parameter.get_name().compare("max_interpolated_angle") == 0)
        {
            if ((parameter.as_double() < 0.0) || (parameter.as_double() > 360.0))
            {
                std::ostringstream error_stream;

                error_stream << "max_interpolated_angle must be between 0 and 360.";

                result.successful = false;
                result.reason = error_stream.str();
            }
        }
        else if (parameter.get_name().compare("num_allowable_invalid_data") == 0)
        {
            if ((parameter.as_int() < 0) || (parameter.as_int() > max_num_measurements))
            {
                std::ostringstream error_stream;

                error_stream << "num_allowable_invalid_data must be between 0 and " << max_num_measurements;

                result.successful = false;
                result.reason = error_stream.str();
            }
        }
        else if (parameter.get_name().compare("ranging_distance") == 0)
        {
            if (node_running)
            {
                result.successful = false;
                result.reason = "Cannot change this parameter while node is running.";
            }
            else if ((parameter.as_int() < 0) || (parameter.as_int() >= NUMBER_OF_RANGING_DISTANCES))
            {
                std::ostringstream error_stream;

                error_stream << "Paramater value out of range. Valid values must be betwwen 0 and " << (NUMBER_OF_RANGING_DISTANCES - 1);

                result.successful = false;
                result.reason = error_stream.str();
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
    double publish_rate = 20;           // Hz. RPLIDAR A2M12 can do 21 Hz at device level. So set to 20 Hz for the node.
    
    // parameters change callback
    rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameter_cb;

    // parameters that cannot be changed once node is running
    std::string uri;

    t_ranging_sensor   lidar_sensor;
    t_ranging_measurement measurements[max_num_measurements];
    
    t_error result;

    // Node creaetion
    rclcpp::init(argc, argv);
    rclcpp::NodeOptions options;
    rclcpp::Node::SharedPtr node = rclcpp::Node::make_shared("lidar", options);

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

    /*** Declare the node parameters ***/

    param_desc.description = "Virtual/physical LiDAR flag";
    node->declare_parameter("device_type", "physical", param_desc);


    param_desc.description = "The URI to interface with the Lidar. On QCar 2, the default value of \
\"serial-cpu://localhost:1?baud='256000',word='8',parity='none',stop='1',flow='none',dsr='on'\" \
should be used.";
    node->declare_parameter("uri", "serial-cpu://localhost:1?baud='256000',word='8',parity='none',stop='1',flow='none',dsr='on'", param_desc);

    param_desc.description = "The number of scan points to be sent out in the /scan message.";
    param_desc.additional_constraints = "This parameter must be 1680 if scan_mode is NORMAL (0). This parameter can be between 0 and 1680, if scan_mode is INTERPOLATED (1).";
    node->declare_parameter("num_scan_points", (int)max_num_measurements, param_desc);

    param_desc.description = "The scan mode to use. Recommended to use INTERPOLATION (1) mode for QCar 2.";
    param_desc.additional_constraints = "This parameter must be NORMAL (0) or INTERPOLATED (1).";
    node->declare_parameter("scan_mode", 1, param_desc);

    param_desc.description = "When INTERPOLATION mode is used (scan_mode := 1), \
this parameter is the maximum difference between the distance measurement of contiguous samples \
for which interpolation will be used. Beyond this difference, the distance of the sample with the closest \
angle to the desired heading will be used.";
    param_desc.additional_constraints = "This parameter must be between 0 and 10.0.";
    node->declare_parameter("max_interpolated_distance", 0.05, param_desc);

    param_desc.description = "When INTERPOLATION mode is used (scan_mode := 1), \
this parameter is the maximum difference between the angle measurement of contiguous samples \
for which interpolation will be used. Beyond this difference, the distance and quality will be set to zero.";
    param_desc.additional_constraints = "This parameter must be between 0 and 10.0.";
    node->declare_parameter("max_interpolated_angle", 5.0);

    param_desc.description = "When NORMAL mode is used (scan_mode := 0), \
this parameter is used to indicate how many invalid data points from \
the scan is allowed before the scan is considered un-usable, and thus \
would not be sent on the /scan message.";
    node->declare_parameter("num_allowable_invalid_data", 50);

    param_desc.description = "The ranging distance (short, medium or long).";
    param_desc.additional_constraints = "This parameter can be 0 (short), 1 (medium) or 2 (long).";
    node->declare_parameter("ranging_distance", (int)ranging_distance, param_desc);

    /*** Get node parameters used when opening the device ***/

    //Use device_type to automatically configure for virtual/physical/custom for user defined values
    std::string device_type = node->get_parameter("device_type").as_string();

    if(device_type.compare("physical")==0){
        uri = "serial-cpu://localhost:1?baud='256000',word='8',parity='none',stop='1',flow='none',dsr='on'";
    }
    else if (device_type.compare("virtual")==0)
    {
        uri = "tcpip://localhost:18966";

    }
    else if (device_type.compare("custom")==0)
    {
        uri = node->get_parameter("uri").as_string();
    }
    else
    {
        RCLCPP_ERROR(node->get_logger(), "The device type selected in invalid, please restart the node and select from virtual/physical/custom....");
        return -1;
    }



    scan_mode = node->get_parameter("scan_mode").as_int();
    ranging_distance = (t_ranging_distance)node->get_parameter("ranging_distance").as_int();

    //RCLCPP_INFO(node->get_logger(), "Parameter uri = %s", uri.c_str());
    //RCLCPP_INFO(node->get_logger(), "Parameter scan_mode = %d", scan_mode);
    //RCLCPP_INFO(node->get_logger(), "Parameter ranging_distance = %d", ranging_distance);

    /*** Publisher creation ***/
    rclcpp::Publisher<sensor_msgs::msg::LaserScan>::SharedPtr scan_publisher;
    scan_publisher = node->create_publisher<sensor_msgs::msg::LaserScan>("/scan", 10);

    // Try to open the lidar
    result = rplidar_open(uri.c_str(), ranging_distance, &lidar_sensor);
    if (result >= 0)
    {
        sensor_msgs::msg::LaserScan msgs;
        rclcpp::Time currentScanTime;
        rclcpp::Time previousScanTime;

        t_double max_interpolated_distance;
        t_double max_interpolated_angle;
        t_uint32 num_allowable_invalid_data;

        RCLCPP_INFO(node->get_logger(), "Starting lidar loop...");

        rclcpp::WallRate loop_rate((double)publish_rate);
        node_running = true;
        while (rclcpp::ok())
        {
            /*
            rclcpp::Time beforeReadTime;
            rclcpp::Time afterReadTime;

            beforeReadTime = node->get_clock()->now();
            */
            
            // Get the parameters, these can be changed while the node is running.
            num_scan_points = node->get_parameter("num_scan_points").as_int();
            max_interpolated_distance = node->get_parameter("max_interpolated_distance").as_double();
            max_interpolated_angle = node->get_parameter("max_interpolated_angle").as_double();
            num_allowable_invalid_data = node->get_parameter("num_allowable_invalid_data").as_int();
            
            result = rplidar_read(lidar_sensor, static_cast<t_ranging_measurement_mode>(scan_mode),
                                        max_interpolated_distance, max_interpolated_angle,
                                        measurements, num_scan_points);

            /*
            afterReadTime = node->get_clock()->now();
            RCLCPP_INFO(node->get_logger(), "lidar_read took %lf seconds", afterReadTime.seconds() - beforeReadTime.seconds());
            */
            
            if (result >= 0 && ((t_uint32)result >= (num_scan_points - ((1 - scan_mode) * num_allowable_invalid_data))))
            {
                msgs.header.frame_id = "base_scan";
                msgs.range_min = min_distance;
                msgs.range_max = max_distance;

                currentScanTime = node->get_clock()->now();
                
                msgs.header.stamp = currentScanTime;
                msgs.angle_min = measurements[0].heading;
                msgs.angle_max = measurements[result - 1].heading;
                msgs.angle_increment = msgs.angle_max / result;
                msgs.time_increment = (1.0 / publish_rate) / result;
                msgs.scan_time = currentScanTime.seconds() - previousScanTime.seconds();

                //RCLCPP_INFO(node->get_logger(), "Read %d measurements", result);
                msgs.ranges.clear();
                // Fill msgs.ranges in reverse order to be compatible with the CCW convention
                for (int i = (result - 1); i >= 0; --i)
                {
                    msgs.ranges.push_back(measurements[i].distance);
                }
                
                scan_publisher->publish(msgs);
                //RCLCPP_INFO(node->get_logger(), "Publishing scan with %ld number of data", msgs.ranges.size());

                previousScanTime = currentScanTime;

            }
            else
            {
                if (result < 0)
                {
                    if (result != -QERR_WOULD_BLOCK)
                    {
                        msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
                        RCLCPP_ERROR(node->get_logger(), "Error reading lidar data: %d -> %s", result, error_message);
                    }
                    
                }
                else
                {
                    //RCLCPP_INFO(node->get_logger(), "Too many invalid data from scan. Expected %d, got %d. Not sending scan message", max_num_measurements, result);
                }
            }

            rclcpp::spin_some(node);
            loop_rate.sleep();
        }

        RCLCPP_INFO(node->get_logger(), "lidar loop ended.");
        node_running = false;

        rplidar_close(lidar_sensor);
    }
    else
    {
        msg_get_error_messageA(NULL, result, error_message, ARRAY_LENGTH(error_message));
        RCLCPP_ERROR(node->get_logger(), "Error opening the Lidar: %d -> %s", result, error_message);
    }
    
    return 0;
}
