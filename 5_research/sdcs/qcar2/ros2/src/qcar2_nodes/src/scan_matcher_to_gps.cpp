#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "std_msgs/msg/header.hpp"

#include <chrono>
#include <cmath>

using namespace std::placeholders;

class ScanMatcher2GPS : public rclcpp::Node
{
public:
    ScanMatcher2GPS()
    : Node("ScanMatcher2GPS")
    {
        scan_matcher_pose_subscriber_ = this->create_subscription<nav_msgs::msg::Odometry>("/scan_matcher",10,std::bind(&ScanMatcher2GPS::sub_callback,this,_1));
        // gps_publisher_ this->create_publisher<>;

        auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
        param_desc.description = "Starting x.";
        param_desc.additional_constraints = "This is starting pose x";
        this->declare_parameter("starting_x",starting_x,param_desc);

        param_desc.description = "Starting y.";
        param_desc.additional_constraints = "This is starting pose y";
        this->declare_parameter("starting_y",starting_y,param_desc);

        param_desc.description = "Starting theta.";
        param_desc.additional_constraints = "This is starting pose th";
        this->declare_parameter("starting_th",starting_th,param_desc);

        starting_x = this->get_parameter("starting_x").as_double();
        starting_y = this->get_parameter("starting_y").as_double();
        starting_th = this->get_parameter("starting_th").as_double();


    }

private:

    void sub_callback(const nav_msgs::msg::Odometry &scan_match_pose)
    {
        double x = scan_match_pose.pose.pose.position.x - starting_x;
        double y = scan_match_pose.pose.pose.position.y - starting_y;
        double th = scan_match_pose.pose.pose.orientation.z - starting_th;

        th = fmod(th + M_PI, 2 * M_PI);
        if (th < 0)
        {
            th += 2 * M_PI;
        }
        th =  th - M_PI;

    }

    rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr scan_matcher_pose_subscriber_;
    double starting_x = 0.0;
    double starting_y = 0.0;
    double starting_th = 0.0;

};

int main(int argc, char * argv[])
{
    // Initialize the ROS environment
    rclcpp::init(argc, argv);

    // Instantiate the node
    rclcpp::Node::SharedPtr node = std::make_shared<ScanMatcher2GPS>();

    // Get a multi-threaded executor
    rclcpp::executors::MultiThreadedExecutor executor;
    executor.add_node(node);

    RCLCPP_INFO(node->get_logger(), "Starting scan_matcher_to_gps loop...");
    executor.spin();
    RCLCPP_INFO(node->get_logger(), "scan_matcher_to_gps loop ended.\n");

    // Shutdown and exit
    rclcpp::shutdown();
    return 0;
}