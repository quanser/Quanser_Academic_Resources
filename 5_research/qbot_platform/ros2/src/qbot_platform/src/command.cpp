#include "rclcpp/rclcpp.hpp"

#include <geometry_msgs/msg/twist.hpp>

#include "quanser/quanser_messages.h"
#include "quanser/quanser_memory.h"
#include "std_msgs/msg/header.hpp"

#include "quanser/quanser_hid.h"

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


    command_publisher_ = this->create_publisher<geometry_msgs::msg::Twist>("cmd_vel", 10);
    // try to connect to joystick
	result = game_controller_open(controller_number, buffer_size, deadzone, saturation, auto_center,
                     max_force_feedback_effects, force_feedback_gain, &gamepad);

    auto timer_callback =
        [this]() -> void {

        rclcpp::Time currentTime;

        if (result >= 0)
	        {

            while (rclcpp::ok())
            {
                result = game_controller_poll(gamepad, &data, &is_new);
                LLA = -1*data.x;
                RT = data.rz;
                A = (t_uint8)(data.buttons & (1 << 0));
                LB = (t_uint8)((data.buttons & (1 << 4))/16);

                // Only enable motion when the QBot is being armed
                if (LB == 1)
                    {
                        //not moving in reverse
                        if (RT == 0){
                            throttle = 0;
                        }
                        else{
                            throttle = 0.3*(0.5+0.5*RT);
                        };

                        steering = 0.5*LLA;
                        if (A == 1)
                        {
                            throttle = -throttle;
                            steering = steering;

                        };

                    }
                else
                {
                throttle = 0;
                steering = 0;
                }

                geometry_msgs::msg::Twist twist;
                twist.linear.x = throttle;
                twist.angular.z = steering;
                this->command_publisher_->publish(twist);

            }



            };
        game_controller_close(gamepad);




    };

    timer_ = this->create_wall_timer(100ms, timer_callback);
    };

    private:
        rclcpp::TimerBase::SharedPtr timer_;
        rclcpp::Publisher<geometry_msgs::msg::Twist>::SharedPtr command_publisher_;

};


int main(int argc, char ** argv)
{


    // Node creation
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<CommandPublisher>());
    rclcpp::shutdown();

    return 0;
}
