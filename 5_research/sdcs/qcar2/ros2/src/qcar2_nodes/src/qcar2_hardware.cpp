#include <chrono>
#include <functional>
#include <memory>
#include <map>
#include <string>

#include "rclcpp/rclcpp.hpp"

#include "quanser/hil.h"
#include "quanser/quanser_messages.h"
#include "quanser/quanser_types.h"
#include "quanser/quanser_led.h"
#include "sensor_msgs/msg/battery_state.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/joint_state.hpp"

#include "qcar2_interfaces/msg/motor_commands.hpp"
#include "qcar2_interfaces/msg/boolean_leds.hpp"

#define LED_STRIP_SIZE  33

using namespace std::chrono_literals;
using namespace std::placeholders;

class QCar2 : public rclcpp::Node
{
public:
    QCar2()
    : Node("qcar2")
    {
        t_int result;

        other_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);
        timer_cb_group_ = this->create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

        rclcpp::SubscriptionOptions sub_options;
        sub_options.callback_group = other_cb_group_;

        rclcpp::PublisherOptions pub_options;
        pub_options.callback_group = other_cb_group_;

        auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};

        // Declare Gyro parameters
        param_desc.description = "Gyro configuration.";
        param_desc.additional_constraints = "This gyro parameter is for setting the QCar2 onboard gyroscrope parameters.";
        this->declare_parameter("gyro.fs", gyro_fs, param_desc);
        this->declare_parameter("gyro.rate", gyro_rate, param_desc);
        this->declare_parameter("gyro.bw", gyro_bw, param_desc);
        this->declare_parameter("gyro.ord", gyro_ord, param_desc);

        // Declare Accel parameters
        param_desc.description = "Accelerometer configuration.";
        param_desc.additional_constraints = "This accel parameter is for setting the QCar2 onboard accelerometer parameters.";
        this->declare_parameter("accel.fs", accel_fs, param_desc);
        this->declare_parameter("accel.rate", accel_rate, param_desc);
        this->declare_parameter("accel.bw", accel_bw, param_desc);
        this->declare_parameter("accel.ord", accel_ord, param_desc);

        param_desc.description = "IMU temperature bandwidth.";
        param_desc.additional_constraints = "This option sets the temperature sensor's filter bandwidth. Valid values range from 5 to 4000. The units are Hz.";
        this->declare_parameter("temp_bw", temp_bw, param_desc);

        param_desc.description = "Steering bias.";
        param_desc.additional_constraints = "The QCar 2 chassis sometimes has a bias in the steering so that driving the steering output with zero does not produce a zero angle on the wheels i.e., the car may not drive in a straight line when the steering output is set to zero. To adjust for this bias, the steer_bias option may be used to add a small offset to the steering output to eliminate this bias. The value specified should be in radians and may be positive or negative as appropriate. Suitable values are typically between 0.03 and 0.09.";
        this->declare_parameter("steer_bias", steer_bias, param_desc);

        param_desc.description = "Device_Type.";
        param_desc.additional_constraints = "This parameter allows you to switch between the ID of a physical and virtual QCar2";
        this->declare_parameter("device_type", device_type, param_desc);

        param_desc.description = "LED Strip Color";
        param_desc.additional_constraints = "This parameter allows you to set the LEDs for the QCar2";
        this->declare_parameter("led_color_id", 0, param_desc);


        // Parameters initialization
        try
        {
            parameter_cb = this->add_on_set_parameters_callback(std::bind(&QCar2::set_parameters_callback, this, _1));
        }
        catch (const std::bad_alloc& e)
        {
            RCLCPP_ERROR(this->get_logger(), "Error setting up parameters callback. %s", e.what());
            return;
        }

        // Actually get the parameters
        std::string device_type = this->get_parameter("device_type").as_string();
        std::string uri_param;
        std::string LED_uri_param;

        if (device_type.compare("physical")==0){
            uri_param = "0";
            LED_uri_param ="spi://localhost:1?memsize=420,word=8,baud=3333333,lsb=off,frame=1";
        }
        else if (device_type.compare("virtual")==0){
            uri_param = "0@tcpip://localhost:18960";
            LED_uri_param ="tcpip://localhost:18969";
        }
        else {
            RCLCPP_ERROR(this->get_logger(), "Invalid device type, stop node and input either virtual/physical...");
            return;
        }

        RCLCPP_INFO(this->get_logger(),"Current HIL URI for device is: %s", uri_param.c_str() );
        RCLCPP_INFO(this->get_logger(),"Current LED URI for device is: %s", LED_uri_param.c_str() );

        // Open the LED strip device
        result =  aaaf5050_mc_k12_open(LED_uri_param.c_str(), LED_STRIP_SIZE, &led_strip);
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "LED result message is: %s", error_message);
            return;
        }

        // Open the HIL "card"
        result = hil_open("qcar2", uri_param.c_str(), &card);
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_open error: %s", error_message);
            return;
        }

        // Actually get the parameters
        std::map<std::string, double> params;
        std::map<std::string, double>::iterator it;

        // Get the Gyro params
        if (this->get_parameters({"gyro"}, params))
        {
            // RCLCPP_INFO(this->get_logger(), "Gyro parameters:");
            for (it = params.begin(); it != params.end(); it++)
            {
                // RCLCPP_INFO(this->get_logger(), "%s: %lf", it->first.c_str(), it->second);

                if (it->first.compare("fs") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"fs\" so assign to the right var");
                    gyro_fs = it->second;
                }
                else if (it->first.compare("rate") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"rate\" so assign to the right var");
                    gyro_rate = it->second;
                }
                else if (it->first.compare("bw") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"bw\" so assign to the right var");
                    gyro_bw = it->second;
                }
                else if (it->first.compare("ord") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"ord\" so assign to the right var");
                    gyro_ord = it->second;
                }
                // Any other gyro.* parameters won't get in here anyways because ROS will not pass
                // non declared parameters in.
            }
        }

        // Get the Accel params
        if (this->get_parameters({"accel"}, params))
        {
            //RCLCPP_INFO(this->get_logger(), "Accel parameters:");
            for (it = params.begin(); it != params.end(); it++)
            {
                //RCLCPP_INFO(this->get_logger(), "%s: %lf", it->first.c_str(), it->second);

                if (it->first.compare("fs") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"fs\" so assign to the right var");
                    accel_fs = it->second;
                }
                else if (it->first.compare("rate") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"rate\" so assign to the right var");
                    accel_rate = it->second;
                }
                else if (it->first.compare("bw") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"bw\" so assign to the right var");
                    accel_bw = it->second;
                }
                else if (it->first.compare("ord") == 0)
                {
                    //RCLCPP_INFO(this->get_logger(), "This param is \"ord\" so assign to the right var");
                    accel_ord = it->second;
                }
                // Any other accel.* parameters won't get in here anyways because ROS will not pass
                // non declared parameters in.
            }
        }

        temp_bw = this->get_parameter("temp_bw").as_double();
        //RCLCPP_INFO(this->get_logger(), "Parameter temp_bw = %lf", temp_bw);

        steer_bias = this->get_parameter("steer_bias").as_double();
        //RCLCPP_INFO(this->get_logger(), "Parameter temp_bw = %lf", temp_bw);

        std::ostringstream bso_stream;
        bso_stream << "gyro_fs=" << gyro_fs << ";"
                   << "gyro_rate=" << gyro_rate << ";"
                   << "gyro_bw=" << gyro_bw << ";"
                   << "gyro_ord=" << gyro_ord << ";"
                   << "accel_fs=" << accel_fs << ";"
                   << "accel_rate=" << accel_rate << ";"
                   << "accel_bw=" << accel_bw << ";"
                   << "accel_ord=" << accel_ord << ";"
                   << "temp_bw=" << temp_bw << ";"
                   << "steer_bias=" << steer_bias << ";"
                   << "enc0_dir=0;enc1_dir=0;enc2_dir=0";

        //RCLCPP_INFO(this->get_logger(), "bso is \"%s\".", bso_stream.str().c_str());
        result = hil_set_card_specific_options(card, bso_stream.str().c_str(), bso_stream.str().length());
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_set_card_specific_options error: %s", error_message);
            return;
        }

        result = hil_watchdog_clear(card);
        if (result < 0 && result != -QERR_HIL_WATCHDOG_CLEAR)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_watchdog_clear error: %s", error_message);
            return;
        }

        // Create the publishers
        battery_state_publisher_ = this->create_publisher<sensor_msgs::msg::BatteryState>("qcar2_battery", 1, pub_options);
        imu_publisher_ = this->create_publisher<sensor_msgs::msg::Imu>("qcar2_imu", 1, pub_options);
        joint_state_publisher_ = this->create_publisher<sensor_msgs::msg::JointState>("qcar2_joint", 1, pub_options);

        // Create the subscribers
        led_cmd_subscriber_ = this->create_subscription<qcar2_interfaces::msg::BooleanLeds>("qcar2_led_cmd", 1, std::bind(&QCar2::led_command_callback, this, _1), sub_options);
        motor_cmd_subscriber_ = this->create_subscription<qcar2_interfaces::msg::MotorCommands>("qcar2_motor_speed_cmd", 1, std::bind(&QCar2::motor_command_callback, this, _1), sub_options);

        //RCLCPP_INFO(this->get_logger(), "driver_comm_sample_time.count: %ld", driver_comm_sample_time.count());
        timer_ = this->create_wall_timer(driver_comm_sample_time, std::bind(&QCar2::timer_callback, this), timer_cb_group_);

        //timer for controlling speed
        timer_speed_control_ = this->create_wall_timer(15ms, std::bind(&QCar2::speed_controller, this));

        //timer for controlling speed
        timer_led_callback_ = this->create_wall_timer(500ms, std::bind(&QCar2::led_timer, this));

        node_running = true;

    }

    ~QCar2()
    {
        int result;
        result = hil_close(card);

        if (result < 0)
            RCLCPP_ERROR(this->get_logger(), "Closing the card with error: %d", result);

        // desired LED color
        t_led_color color[LED_STRIP_SIZE];

        for(int i = 0; i < LED_STRIP_SIZE; i++)
        {
            color[i] = { 0, 0, 0 };
        }

        // Turn off the LED strip when we shut the node down
        aaaf5050_mc_k12_write(led_strip, color, LED_STRIP_SIZE);

        result = aaaf5050_mc_k12_close(led_strip);
        if (result < 0)
            RCLCPP_ERROR(this->get_logger(), "Closing LED strip with error: %i", result);

        node_running = false;
        RCLCPP_INFO(this->get_logger(), "qcar2 exit");
    }

private:

    void led_timer()
    {
        this->get_parameter("led_color_id",led_color_id);
        if (response != led_color_id)
        {
            LED_Set();
            // RCLCPP_INFO(this->get_logger(),"Setting new LED Value %i",led_color_id);
            response = led_color_id;
        }
    }

    void LED_Set()
    {
        //desired LED color
        t_led_color color[LED_STRIP_SIZE];
        t_led_color color_value  = {0,0,0};

        // color ID selection
        if (led_color_id == 0)
            {color_value = { 255, 0, 0 };}
        if (led_color_id == 1)
            {color_value = { 0, 255, 0 }; }
        if (led_color_id == 2)
            {color_value = { 0, 0, 255 };}
        if (led_color_id == 3)
            {color_value = { 255, 255, 0 };}
        if (led_color_id == 4)
            {color_value = { 0, 255, 255 };}
        if (led_color_id == 5)
            {color_value = { 255, 0, 255 };}

        // { 255, 0, 0 };        /* LED #0: red     */
        // { 0, 255, 0 },        /* LED #1: green   */
        // { 0, 0, 255 },        /* LED #2: blue    */
        // { 255, 255, 0 },      /* LED #3: yellow  */
        // { 0, 255, 255 },      /* LED #4: cyan    */
        // { 255, 0, 255 },      /* LED #5: magenta */

        for(int i = 0; i < LED_STRIP_SIZE; i++)
        {
            color[i] = color_value;
        }

        t_int result;
        auto start_time = clock_.now();
        rclcpp::Duration delta_time = clock_.now()-start_time;
        while ( delta_time.seconds() < 0.2)
        {
            delta_time = clock_.now()-start_time;
            result = aaaf5050_mc_k12_write(led_strip, color, LED_STRIP_SIZE);
            if (result < 0)
            {
                msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
                RCLCPP_ERROR(this->get_logger(), "Error writing to LED strip error: %s", error_message);
            }
        }
    }

    void speed_controller()
    {
        auto start_time = clock_.now();
        // time delta calculation
        rclcpp::Duration delta_time = start_time-end_time_;
        double measured_speed = 0;
        // method used for constructing a PD speed controller for QCar2
        //Convert desired linear speed to desired motor speed

        if (desired_speed != 0)
        {
            measured_speed = (joint_speed_measured/(720.0*4.0))*((13.0*19.0)/(70.0*30.0))*(2.0*M_PI)*0.033;
            speed_error = desired_speed-measured_speed;
            motor_speed_cmd = motor_speed_cmd+ (speed_error*kp+((speed_error-prior_speed_error)/delta_time.seconds())*kd)*0.0047/battery_voltage;
            prior_speed_error = speed_error;

            // clip pwm command to not exceed 0.3
            if (motor_speed_cmd>0.3)
                motor_speed_cmd =0.3;

            // check for motor deadband at PWM ~|0.03|
            if (motor_speed_cmd<0.01 && motor_speed_cmd >=0 && desired_speed > 0)
                motor_speed_cmd =0.01+motor_speed_cmd;
            if (motor_speed_cmd<0.0 && motor_speed_cmd >=-0.01&& desired_speed < 0)
                motor_speed_cmd =-0.01+motor_speed_cmd;

            if (motor_speed_cmd<-0.3)
                motor_speed_cmd = -0.3;
        }
        else
        {
            motor_speed_cmd = 0;
        }

        // motor channel mapping
        std::map<std::string, int> motor_channel_map {{"steering_angle", 1000},
                                                    {"motor_throttle", 11000}};

        size_t motor_commands_size = motor_channel_map.size();

        //values for writting command to HIL device
        t_uint32 *channels = new t_uint32[motor_commands_size];
        t_double *buffer = new t_double[motor_commands_size];
        t_uint32 num_channels = 2;

        channels[0] = 1000;
        channels[1] = 11000;

        buffer[0] = desired_steering;
        buffer[1] = motor_speed_cmd;

        t_error result;

        result = hil_write_other(card, channels, num_channels, buffer);
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_write_other error: %s", error_message);
        }

        delete[] channels;
        delete[] buffer;

        // RCLCPP_INFO(this->get_logger(),"Measured Linear Speed is %f", measured_speed);
        // RCLCPP_INFO(this->get_logger(),"Speed Error is %f", speed_error);
        // RCLCPP_INFO(this->get_logger(),"Command is %f", motor_speed_cmd);
        // RCLCPP_INFO(this->get_logger(),"Time is %f", delta_time.seconds());

        end_time_ = start_time;
    }

    void timer_callback()
    {
        t_error result;
        rclcpp::Time hil_read_time;

        t_uint32 AIChannels[] = { 0,   // analog input 0
                                  1,   // analog inptu 1
                                  2,   // battery voltage
                                  3,   // electronics current
                                  4};  // motor current

        t_double AIBuffer[ARRAY_LENGTH(AIChannels)];

        t_uint32 ENChannels[] = {0,     // motor encoder
                                 1,     // user encoder 0
                                 2};    // user encoder 1

        t_int32 ENBuffer[ARRAY_LENGTH(ENChannels)];

        t_uint32 DIChannels[] = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, // bi-directional digital input
                                  11,   // user button 0
                                  12,   // user button 1
                                  13,   // user button 2
                                  14};  // over current condition

        t_boolean DIBuffer[ARRAY_LENGTH(DIChannels)];

        t_uint32 OIChannels[] = {3000, 3001, 3002,  // angular velocity (from gyroscope)
                                 4000, 4001, 4002,  // lineaear acceleration (from accelerometer)
                                 10000,             // IMU temperature
                                 14000};            // Motor Speed

        t_double OIBuffer[ARRAY_LENGTH(OIChannels)];

        // Read from QCar2 via HIL APIs
        result = hil_read(card,
                        AIChannels, ARRAY_LENGTH(AIChannels),
                        ENChannels, ARRAY_LENGTH(ENChannels),
                        DIChannels, ARRAY_LENGTH(DIChannels),
                        OIChannels, ARRAY_LENGTH(OIChannels),
                        AIBuffer,
                        ENBuffer,
                        DIBuffer,
                        OIBuffer
                        );
        if (result < 0)
        {
            msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
            RCLCPP_ERROR(this->get_logger(), "hil_read error: %s", error_message);
            return;
        }

        hil_read_time = this->get_clock()->now();

        /* Battery State message */
        auto battery_state = sensor_msgs::msg::BatteryState();
        battery_state.voltage = AIBuffer[2];
        battery_voltage = AIBuffer[2];
        battery_state.temperature = std::numeric_limits<double>::quiet_NaN();
        battery_state.current = std::numeric_limits<double>::quiet_NaN();
        battery_state.charge = std::numeric_limits<double>::quiet_NaN();
        battery_state.capacity = std::numeric_limits<double>::quiet_NaN();
        battery_state.design_capacity = 7.0;    // ??
        battery_state.percentage = std::numeric_limits<double>::quiet_NaN();
        battery_state.power_supply_status = sensor_msgs::msg::BatteryState::POWER_SUPPLY_STATUS_DISCHARGING;
        battery_state.power_supply_health = sensor_msgs::msg::BatteryState::POWER_SUPPLY_HEALTH_GOOD;
        battery_state.power_supply_technology = sensor_msgs::msg::BatteryState::POWER_SUPPLY_TECHNOLOGY_LIPO;
        battery_state.present = true;

        battery_state.header.stamp = hil_read_time;
        battery_state.header.frame_id = "base_link";
        battery_state_publisher_->publish(battery_state);

        /* Imu message */
        auto imu = sensor_msgs::msg::Imu();
        imu.linear_acceleration.x = OIBuffer[3];
        imu.linear_acceleration.y = OIBuffer[4];
        imu.linear_acceleration.z = OIBuffer[5];
        imu.angular_velocity.x = OIBuffer[0];
        imu.angular_velocity.y = OIBuffer[1];
        imu.angular_velocity.z = OIBuffer[2];

        imu.header.stamp = hil_read_time;
        imu.header.frame_id = "base_link";
        imu_publisher_->publish(imu);

        /* Joint State message */
        auto joint_state = sensor_msgs::msg::JointState();
        joint_state.position.clear();
        joint_state.position.push_back(ENBuffer[0]);
        joint_state.velocity.clear();
        joint_state.velocity.push_back(OIBuffer[7]);
        joint_speed_measured = OIBuffer[7];
        joint_state.effort.clear();
        joint_state.effort.push_back(AIBuffer[4]);

        joint_state.header.stamp = hil_read_time;
        joint_state.header.frame_id = "base_link";
        joint_state_publisher_->publish(joint_state);
    }

    void led_command_callback(const qcar2_interfaces::msg::BooleanLeds &led_commands)
    {
        size_t led_commands_size = led_commands.led_names.size();
        std::map<std::string, int> led_channel_map {{"left_outside_brake_light",    11},
                                                    {"left_inside_brake_light",     12},
                                                    {"right_inside_brake_light",    13},
                                                    {"right_outside_brake_light",   14},
                                                    {"left_reverse_light",          15},
                                                    {"right_reverse_light",         16},
                                                    {"left_rear_signal",            17},
                                                    {"right_rear_signal",           18},
                                                    {"left_outside_headlight",      19},
                                                    {"left_middle_headlight",       20},
                                                    {"left_inside_headlight",       21},
                                                    {"right_inside_headlight",      22},
                                                    {"right_middle_headlight",      23},
                                                    {"right_outside_headlight",     24},
                                                    {"left_front_signal",           25},
                                                    {"right_front_signal",          26}};
        std::map<std::string, int>::iterator it;

        if (led_commands_size > led_channel_map.size())
        {
            RCLCPP_WARN(this->get_logger(), "In %s - size of BooleanLeds message must be between 0 and %ld, but received size is: %ld...ignore", __FUNCTION__, led_channel_map.size(), led_commands_size);
            return;
        }

        t_uint32 *channels = new t_uint32[led_commands_size];
        t_boolean *buffer = new t_boolean[led_commands_size];
        t_uint32 num_channels = 0;
        t_boolean valid_name = true;

        for (unsigned int i = 0; i < led_commands_size; i++)
        {
            it = led_channel_map.find(led_commands.led_names[i]);
            if (it == led_channel_map.end())
            {
                RCLCPP_WARN(this->get_logger(), "In %s - BooleanLeds message led_name %s is invalid...ignoring", __FUNCTION__, led_commands.led_names[i].c_str());
                valid_name = false;
                break;
            }

            channels[num_channels] = it->second;
            buffer[num_channels] = led_commands.values[i];
            num_channels++;
        }

        if (valid_name)
        {
            t_error result;
            result = hil_write_digital(card, channels, num_channels, buffer);
            if (result < 0)
            {
                msg_get_error_messageA(NULL, result, error_message, sizeof(error_message));
                RCLCPP_ERROR(this->get_logger(), "hil_write_digital error: %s", error_message);
            }
        }

        delete[] channels;
        delete[] buffer;
    }

    void motor_command_callback(const qcar2_interfaces::msg::MotorCommands &motor_commands)
    {
        size_t motor_commands_size = motor_commands.motor_names.size();
        std::map<std::string, int> motor_channel_map {{"steering_angle", 1000},
                                                      {"motor_throttle", 11000}};
        std::map<std::string, int>::iterator it;

        if (motor_commands_size > motor_channel_map.size())
        {
            RCLCPP_WARN(this->get_logger(), "In %s - size of MotorCommands message must be between 0 and %ld, but received size is: %ld...ignore", __FUNCTION__, motor_channel_map.size(), motor_commands_size);
            return;
        }

        for (unsigned int i = 0; i < motor_commands_size; i++)
        {
            it = motor_channel_map.find(motor_commands.motor_names[i]);
            if (it == motor_channel_map.end())
            {
                RCLCPP_WARN(this->get_logger(), "In %s - MotorCommands message command_name %s is invalid...ignoring", __FUNCTION__, motor_commands.motor_names[i].c_str());
                break;
            }

            if (i == 0)
                desired_steering = motor_commands.values[0];

            if (i == 1)
                desired_speed = motor_commands.values[1];
        }
    }

    rcl_interfaces::msg::SetParametersResult set_parameters_callback(const std::vector<rclcpp::Parameter> & parameters)
    {
        rcl_interfaces::msg::SetParametersResult result;

        result.successful = true;

        // Loop through the parameters....can happen if set_parameters_atomically() is called
        for (const auto & parameter : parameters)
        {
            if (parameter.get_name().compare(0, 5, "gyro.") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "Cannot change this parameter while node is running.";
                }
            }
            else if (parameter.get_name().compare(0, 6, "accel.") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "Cannot change this parameter while node is running.";
                }
            }
            else if (parameter.get_name().compare("temp_bw") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "Cannot change this parameter while node is running.";
                }
                else
                {
                    if ((parameter.as_double() < min_temp_bw) || (parameter.as_double() > max_temp_bw))
                    {
                        std::ostringstream error_stream;

                        error_stream << "temp_bw must be between " << min_temp_bw << " and " << max_temp_bw << ".";

                        result.successful = false;
                        result.reason = error_stream.str();
                    }
                }
            }
            else if (parameter.get_name().compare("steer_bias") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "Cannot change this parameter while node is running.";
                }
            }
            else if (parameter.get_name().compare("device_type") == 0)
            {
                if (node_running)
                {
                    result.successful = false;
                    result.reason = "This parameter cannot change while node is running.";
                }
            }
            else if (parameter.get_name().compare("led_color_id") == 0)
            {
                if(node_running == false)
                {
                this->get_parameter("led_color_id",led_color_id);
                RCLCPP_INFO(this->get_logger(),"New LED ID is %i", led_color_id);
                LED_Set();
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

    rclcpp::CallbackGroup::SharedPtr other_cb_group_;
    rclcpp::CallbackGroup::SharedPtr timer_cb_group_;

    rclcpp::TimerBase::SharedPtr timer_;
    rclcpp::TimerBase::SharedPtr timer_led_callback_;

    //LED ID selector
    int led_color_id;
    int response = -1;


    // speed controller parameters
    double desired_rotation_speed = 0;
    double speed_error = 0;
    double kp = 20;
    double kd = 0.1;
    double ki = 0.01;
    double km = 0.0047; // v/rad/s
    double joint_speed_measured = 0.0;
    double battery_voltage = 0;
    double desired_speed= 0;
    double desired_steering = 0;
    double prior_speed_error =0;
    double motor_speed_cmd = 0;
    rclcpp::Clock clock_;
    rclcpp::Time end_time_;
    rclcpp::TimerBase::SharedPtr timer_speed_control_;

    t_aaaf5050_mc_k12 led_strip;

    rclcpp::Publisher<sensor_msgs::msg::BatteryState>::SharedPtr battery_state_publisher_;
    rclcpp::Publisher<sensor_msgs::msg::Imu>::SharedPtr imu_publisher_;
    rclcpp::Publisher<sensor_msgs::msg::JointState>::SharedPtr joint_state_publisher_;

    rclcpp::Subscription<qcar2_interfaces::msg::BooleanLeds>::SharedPtr led_cmd_subscriber_;
    rclcpp::Subscription<qcar2_interfaces::msg::MotorCommands>::SharedPtr motor_cmd_subscriber_;

    char error_message[512];
    t_card card;

    // parameters change callback
    rclcpp::Node::OnSetParametersCallbackHandle::SharedPtr parameter_cb;

    // Sample time to get data from QCar2
    std::chrono::milliseconds driver_comm_sample_time{1};

    bool node_running = false;

    const t_double min_temp_bw = 5.0;
    const t_double max_temp_bw = 4000.0;

    // parameters
    t_double gyro_fs   = 250.0;
    t_double gyro_rate = 500.0;
    t_double gyro_bw   = 125.0;
    t_double gyro_ord  = 3.0;

    t_double accel_fs   = 16.0;
    t_double accel_rate = 1000.0;
    t_double accel_bw   = 250.0;
    t_double accel_ord  = 3.0;

    t_double temp_bw = 4000;
    t_double steer_bias = 0.05;
    std::string device_type = "physical";
};

int main(int argc, char * argv[])
{
    // Initialize the ROS environment
    rclcpp::init(argc, argv);

    // Instantiate the node
    rclcpp::Node::SharedPtr qcars_node = std::make_shared<QCar2>();

    // Get a multi-threaded executor
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(qcars_node);

    RCLCPP_INFO(qcars_node->get_logger(), "Starting qcar2 loop...");
    executor.spin();
    RCLCPP_INFO(qcars_node->get_logger(), "qcar2 loop ended.\n");

    // Shutdown and exit
    rclcpp::shutdown();
    return 0;
}