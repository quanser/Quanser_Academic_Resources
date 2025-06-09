#include "rclcpp/rclcpp.hpp"

#include <geometry_msgs/msg/twist.hpp>

#include "quanser/quanser_messages.h"
#include "quanser/quanser_memory.h"
#include "std_msgs/msg/header.hpp"

#include "quanser/quanser_hid.h"
#include "qcar2_interfaces/msg/motor_commands.hpp"
#include "qcar2_interfaces/msg/boolean_leds.hpp"


using namespace std::chrono_literals;

bool node_running = false;
// joystick inputs
t_double LLA = 0.0;
t_double LLO = 0.0;
t_double LT  = 0.0;
t_double RLA = 0.0;
t_double RLO = 0.0;
t_double RT  = 0.0;
t_boolean flag_z  = false;
t_boolean flag_rz = false;
t_double A  = 0;
t_double B  = 0;
t_double X  = 0;
t_double Y  = 0;
t_double LB = 0.0;
t_double RB = 0.0;
t_double up = 0.0;
t_double down  = 0.0;
t_double left  = 0.0;
t_double right = 0.0;
t_double command[2];
t_double throttle;
t_double steering;

// joystick definition
t_game_controller gamepad;
t_error result;
t_uint8 controller_number = 1;
t_uint16 buffer_size   = 12;
t_double deadzone[6]   = {0.0};
t_double saturation[6] = {0.0};
t_boolean auto_center  = false;
t_uint16 max_force_feedback_effects = 0;
t_double force_feedback_gain = 0.0;
t_game_controller_states data;
t_boolean is_new;


class CommandPublisher : public rclcpp::Node
{
    public:
    CommandPublisher()
    : Node("joystick_publisher")
    {
    // configuring command publisher
    command_publisher_ = this->create_publisher<qcar2_interfaces::msg::MotorCommands>("qcar2_motor_speed_cmd", 10);
    led_publisher_ = this->create_publisher<qcar2_interfaces::msg::BooleanLeds>("qcar2_led_cmd",10);
    
    // try to connect to joystick
	result = game_controller_open(controller_number, buffer_size, deadzone, saturation, auto_center,
                     max_force_feedback_effects, force_feedback_gain, &gamepad);

    auto timer_callback =
        [this]() -> void {

        rclcpp::Time currentTime;

        if (result >= 0)
	        {   
            
            /*
            logic for using logitec gamepad to drive QCar 2
            Description:
            - LB  : Arm signal to enable joystick
            - RT  : Throtlle value 
            - A   : Change direction
            - LLA : Left jotsick x axis motion for steering            
            */
            while (rclcpp::ok())
            {
                result = game_controller_poll(gamepad, &data, &is_new);
                LLA = -1*data.x;
                RT = data.rz;
                A = (t_uint8)(data.buttons & (1 << 0));
                LB = (t_uint8)((data.buttons & (1 << 4))/16);
                bool led_values[16] = {0};

                // Only enable motion when mobile robot is being armed
                if (LB == 1)
                    {
                        //Turn on Front and back LEDs
                        led_values[8]= 1;
                        led_values[9]= 1;
                        led_values[10]= 1;
                        led_values[11]= 1;
                        led_values[12]= 1;
                        led_values[13]= 1;


                        if (RT == 0){
                            throttle = 0;
                        }
                        else{
                            throttle = 0.3*(0.5+0.5*RT);
                        };

                        //steering values
                        steering = 0.5*LLA;
                        if (steering > 0.01){
                            led_values[14]= 1;
                            led_values[6]= 1;

                        }
                        else if(steering <-0.01){
                            led_values[15]= 1;
                            led_values[7]= 1;

                        }

                        //changing LEDs based on the QCar moving backwards or not
                        if (A == 1)
                        {
                            throttle = -throttle;
                            steering = steering;
                            led_values[4]= 1;
                            led_values[5]= 1;
                        };
                    }
                else
                {
                led_values[0] = 1;
                led_values[1] = 1;
                led_values[2] = 1;
                led_values[3] = 1;
                throttle = 0;
                steering = 0;
                }
                
                // Populate motor command  message for velocity and steering
                qcar2_interfaces::msg::MotorCommands motor_command;

                // // Create a string array for names, and double array for values 
                std::vector<std::string> name;
                std::vector<t_double> val;

                name.push_back("steering_angle");
                name.push_back("motor_throttle");

                val.push_back(steering);
                val.push_back(throttle);
                                                             
                motor_command.motor_names = name;
                motor_command.values = val;


                this->command_publisher_->publish(motor_command);

                // Populate LED commands 
                qcar2_interfaces::msg::BooleanLeds led_commands;

                std::vector<std::string> led_name;
                std::vector<bool> led_value_commands;

                
                
                led_name.push_back("left_outside_brake_light");
                led_name.push_back("left_inside_brake_light");
                led_name.push_back("right_inside_brake_light");    
                led_name.push_back("right_outside_brake_light");   
                led_name.push_back("left_reverse_light");          
                led_name.push_back("right_reverse_light");         
                led_name.push_back("left_rear_signal");            
                led_name.push_back("right_rear_signal");           
                led_name.push_back("left_outside_headlight");      
                led_name.push_back("left_middle_headlight");       
                led_name.push_back("left_inside_headlight");       
                led_name.push_back("right_inside_headlight");      
                led_name.push_back("right_middle_headlight");      
                led_name.push_back("right_outside_headlight");     
                led_name.push_back("left_front_signal");           
                led_name.push_back("right_front_signal");

                for(bool index: led_values)
                {
                    led_value_commands.push_back(index);
                }

                led_commands.led_names = led_name;
                led_commands.values = led_value_commands;
                this->led_publisher_->publish(led_commands);
            };
        game_controller_close(gamepad);

    };
    };

    timer_ = this->create_wall_timer(100ms, timer_callback);
    };

    private:
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<qcar2_interfaces::msg::MotorCommands>::SharedPtr command_publisher_;
        rclcpp::Publisher<qcar2_interfaces::msg::BooleanLeds>::SharedPtr led_publisher_;

};


int main(int argc, char ** argv)
{

    // Node creation
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CommandPublisher>());
    rclcpp::shutdown();

    return 0;
}
