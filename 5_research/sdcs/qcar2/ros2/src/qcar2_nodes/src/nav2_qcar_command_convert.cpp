#include "rclcpp/rclcpp.hpp"

#include <geometry_msgs/msg/twist.hpp>

#include "quanser/quanser_messages.h"
#include "quanser/quanser_memory.h"
#include "std_msgs/msg/header.hpp"
#include <chrono>
#include <thread>

#include "quanser/quanser_hid.h"
#include "qcar2_interfaces/msg/boolean_leds.hpp"
#include "qcar2_interfaces/msg/motor_commands.hpp"


using namespace std::chrono_literals;



class Nav2QCarConverter : public rclcpp::Node
{


    public:
    Nav2QCarConverter()
    : Node("nav2_qcar2_command_converter")
    {
    // configuring command publisher
    command_publisher_  = this->create_publisher<qcar2_interfaces::msg::MotorCommands>("qcar2_motor_speed_cmd", 1);
    // led_publisher_      = this->create_publisher<qcar2_interfaces::msg::BooleanLeds>("qcar2_led_cmd",10);

    //configure nav2 subscriber
    nav2_subscriber_ = this->create_subscription<geometry_msgs::msg::Twist>("/cmd_vel_nav",1,std::bind(&Nav2QCarConverter::nav2_command_callback, this, std::placeholders::_1));
    
    //publishing timer for converted command
    timer_ = this->create_wall_timer(1ms, std::bind(&Nav2QCarConverter::command_plublish, this));

    //publishing timer for converted command
    timer2_ = this->create_wall_timer(33ms, std::bind(&Nav2QCarConverter::led_publish, this));



    }

    private:       
        void nav2_command_callback(const geometry_msgs::msg::Twist &nav2_commands){
            nav2_speed = nav2_commands.linear.x;
            nav2_steering = nav2_commands.angular.z;

        }


        void command_plublish(){
        
            //configure publisher for LEDS and motor commands:
            // Populate motor command  message for velocity and steering
            qcar2_interfaces::msg::MotorCommands motor_command;

            // // Create a string array for names, and double array for values 
            std::vector<std::string> name;
            std::vector<t_double> val;

            name.push_back("steering_angle");
            name.push_back("motor_throttle");

            val.push_back(nav2_steering);
            val.push_back(nav2_speed);
                                                            
            motor_command.motor_names = name;
            motor_command.values = val;


            this->command_publisher_->publish(motor_command);


        }



        void led_publish(){
            
            
            
            if (nav2_speed !=0) {
                //set LEDs for QCar moving
                led_values[8]= 1;
                led_values[9]= 1;
                led_values[10]= 1;
                led_values[11]= 1;
                led_values[12]= 1;
                led_values[13]= 1;

                if(nav2_steering > 0.01){
                    led_values[14]= 1;
                    led_values[6]= 1;

                }
                else if(nav2_steering <-0.01){
                    led_values[15]= 1;
                    led_values[7]= 1;

                }

            }
            else if (nav2_speed == 0 ){
                led_values[0] = 1;
                led_values[1] = 1;
                led_values[2] = 1;
                led_values[3] = 1;
            }          
            
            
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
            // this->led_publisher_->publish(led_commands);
         }


        bool led_values[16] = {0};

        double nav2_speed = 0;
        double nav2_steering = 0;

        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::TimerBase::SharedPtr timer2_;


        rclcpp::Publisher<qcar2_interfaces::msg::MotorCommands>::SharedPtr command_publisher_;
        rclcpp::Publisher<qcar2_interfaces::msg::BooleanLeds>::SharedPtr led_publisher_;
        rclcpp::Subscription<geometry_msgs::msg::Twist>::SharedPtr nav2_subscriber_;
        
};


int main(int argc, char ** argv)
{

    // Node creation
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<Nav2QCarConverter>());
    rclcpp::shutdown();

    return 0;
}
