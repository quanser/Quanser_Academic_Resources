
#define _USE_MATH_DEFINES
#include <cmath>
#include <memory>
#include <vector>
#include <deque>

#include "rclcpp/rclcpp.hpp"
#include "nav_msgs/msg/odometry.hpp"
#include "geometry_msgs/msg/pose_with_covariance_stamped.hpp"
#include "geometry_msgs/msg/accel_with_covariance_stamped.hpp"
#include "sensor_msgs/msg/imu.hpp"
#include "sensor_msgs/msg/joint_state.hpp"
#include "qcar2_interfaces/msg/motor_commands.hpp"

#include <tf2_geometry_msgs/tf2_geometry_msgs.hpp>
#include <tf2/LinearMath/Quaternion.h>
#include <tf2/LinearMath/Matrix3x3.h>

using std::placeholders::_1;

class ScanMatcherInterface : public rclcpp::Node
{
public:
  ScanMatcherInterface()
  : Node("scan_matcher_interface"),
    joint_arrived_(false),
    imu_arrived_(false),
    motor_command_arrived_(false),
    scan_matcher_arrived_(false)
  {
    // Subscribers
    encoder_sub_ = this->create_subscription<sensor_msgs::msg::JointState>("/qcar2_joint", 10, std::bind(&ScanMatcherInterface::encoder_callback, this, _1));
    steering_sub_ = this->create_subscription<qcar2_interfaces::msg::MotorCommands>("/qcar2_motor_speed_cmd", 10, std::bind(&ScanMatcherInterface::steering_callback, this, _1));
    imu_sub_ = this->create_subscription<sensor_msgs::msg::Imu>("/qcar2_imu", 10, std::bind(&ScanMatcherInterface::imu_callback, this, _1));
    pose_sub_ = this->create_subscription<nav_msgs::msg::Odometry>("/scan_matcher", 10, std::bind(&ScanMatcherInterface::pose_callback, this, _1));

    // Publishers
    kinematic_state_pub_ = this->create_publisher<nav_msgs::msg::Odometry>("/localization/kinematic_state", 10);
    accel_pub_ = this->create_publisher<geometry_msgs::msg::AccelWithCovarianceStamped>("/localization/acceleration", 10);

    // Timer
    double period_s = 0.025;  // 20 Hz
    timer_ = this->create_wall_timer(std::chrono::duration<double>(period_s),std::bind(&ScanMatcherInterface::on_timer, this));
    
    auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
    param_desc.description = "Starting x.";
    param_desc.additional_constraints = "This is starting pose x";
    this->declare_parameter("init_x",0.0,param_desc);

    param_desc.description = "Starting y.";
    param_desc.additional_constraints = "This is starting pose y";
    this->declare_parameter("init_y",0.0,param_desc);

    param_desc.description = "Starting theta.";
    param_desc.additional_constraints = "This is starting pose th";
    this->declare_parameter("init_th",0.0,param_desc);

    init_x_ = this->get_parameter("init_x").as_double();
    init_y_ = this->get_parameter("init_y").as_double();
    init_th_ = this->get_parameter("init_th").as_double();
    RCLCPP_INFO(this->get_logger(),"Initial pose: x = %.3f, y = %.3f, theta = %.3f",
    init_x_, init_y_, init_th_);
  }

private:
  // Initial values
  double scaling_factor = 10.0;
  double front_axle_to_body = 0.13;
  double rear_axle_to_body = 0.13;
  double init_x_, init_y_, init_th_;

  // for receiving data
  double latest_x_,latest_y_,latest_th_;
  geometry_msgs::msg::Quaternion latest_quat_;
  double latest_steering_ang_;
  sensor_msgs::msg::Imu::SharedPtr latest_imu_;
  std::deque<sensor_msgs::msg::JointState> joint_state_queue_;
  std::deque<sensor_msgs::msg::Imu> imu_queue_;
  bool joint_arrived_, imu_arrived_, motor_command_arrived_, scan_matcher_arrived_ ;


  // Subscribers
  rclcpp::Subscription<sensor_msgs::msg::JointState>::SharedPtr encoder_sub_;
  rclcpp::Subscription<qcar2_interfaces::msg::MotorCommands>::SharedPtr steering_sub_;
  rclcpp::Subscription<sensor_msgs::msg::Imu>::SharedPtr imu_sub_;
  rclcpp::Subscription<nav_msgs::msg::Odometry>::SharedPtr pose_sub_;

  // Publishers
  rclcpp::Publisher<nav_msgs::msg::Odometry>::SharedPtr kinematic_state_pub_;
  rclcpp::Publisher<geometry_msgs::msg::AccelWithCovarianceStamped>::SharedPtr accel_pub_;

  rclcpp::TimerBase::SharedPtr timer_;


  // For computing angular acceleration
  rclcpp::Time last_imu_time_;
  geometry_msgs::msg::Vector3 last_angular_velocity_;

  void encoder_callback(const sensor_msgs::msg::JointState::ConstSharedPtr encoder_msg_ptr)
  {
    joint_arrived_ = true;
    joint_state_queue_.push_back(*encoder_msg_ptr);
  }

  void steering_callback(const qcar2_interfaces::msg::MotorCommands &cmd_msg)
  {
    motor_command_arrived_ = true;
    latest_steering_ang_ = cmd_msg.values.front();
  }

  void imu_callback(const sensor_msgs::msg::Imu::ConstSharedPtr imu_msg_ptr)
  {
    imu_arrived_ = true;
    imu_queue_.push_back(*imu_msg_ptr);
  }

  void pose_callback(const nav_msgs::msg::Odometry &scan_match_pose)
  {
    scan_matcher_arrived_ = true;
    latest_x_ = scan_match_pose.pose.pose.position.x - init_x_;
    latest_y_ = scan_match_pose.pose.pose.position.y - init_y_;

    // Variables to store roll, pitch, and yaw
    double roll, pitch, yaw, quat_x, quat_y, quat_z, quat_w;
    
    // Convert quaternion to roll, pitch, and yaw
    quat_x = scan_match_pose.pose.pose.orientation.x;
    quat_y = scan_match_pose.pose.pose.orientation.y;
    quat_z = scan_match_pose.pose.pose.orientation.z;
    quat_w = scan_match_pose.pose.pose.orientation.w;

    tf2::Quaternion tf_quat(quat_x, quat_y, quat_z, quat_w);
    tf2::Matrix3x3(tf_quat).getRPY(roll, pitch, yaw);

    latest_th_ = yaw - init_th_;

    latest_th_ = fmod(latest_th_ + M_PI, 2 * M_PI);
    if (latest_th_ < 0)
    {
        latest_th_ += 2 * M_PI;
    }
    latest_th_ =  latest_th_ - M_PI;
    // RCLCPP_INFO(this->get_logger(),"Converted orientation: r = %.3f, p = %.3f, y = %.3f",
    // roll, pitch, yaw);
    
    tf2::Quaternion quaternion_tf2;
    quaternion_tf2.setRPY(roll, pitch, latest_th_);
    latest_quat_ = tf2::toMsg(quaternion_tf2);

  }

  void on_timer()
  {
    // Need pose + imu at least
    if (!joint_arrived_ || !imu_arrived_ || !scan_matcher_arrived_) {
        return;
    }
    if (!motor_command_arrived_){
        latest_steering_ang_ = 0;
    }
    if (joint_state_queue_.empty()) {
        // not output error and clear queue
        return;
    }
    if (imu_queue_.empty()) {
        // not output error and clear queue
        return;
    }

    // velocity_status (longitutdina, lateral speed, heading rate)
    double v_mean = 0;
    for (const auto & joint_state : joint_state_queue_) {
        // convert encoder speed to vx
        v_mean += (joint_state.velocity.front()/(720.0*4.0))*((13.0*19.0)/(70.0*30.0))*(2.0*M_PI)*0.033;
    }
    v_mean /= static_cast<double>(joint_state_queue_.size());
    double beta, v_x, v_y , heading_rate;
    beta = std::atan(std::tan(latest_steering_ang_)*rear_axle_to_body/
                                        (front_axle_to_body+rear_axle_to_body));
    v_x = std::cos(beta)*v_mean;
    v_y = std::sin(beta)*v_mean;
    heading_rate = std::tan(latest_steering_ang_)/((front_axle_to_body+rear_axle_to_body))*v_mean; //w=(1/R*)*v 
    // body speed estimation in 1.10th scale first, then convert
    v_x *= scaling_factor;
    v_y *= scaling_factor;

    // build kinematic state message
    nav_msgs::msg::Odometry kinematic_state_msg;
    rclcpp::Time now = this->now();

    // Pose
    kinematic_state_msg.header.stamp = now;
    kinematic_state_msg.header.frame_id = "map";  // or your frame
    kinematic_state_msg.child_frame_id = "base_link";

    kinematic_state_msg.pose.pose.position.x = latest_x_;
    kinematic_state_msg.pose.pose.position.y = latest_y_;
    kinematic_state_msg.pose.pose.position.z = 0.0;

    kinematic_state_msg.pose.pose.orientation = latest_quat_;

    // Fill covariance (36 entries)
    for (int i = 0; i < 36; i++) {
    kinematic_state_msg.pose.covariance[i] = 0.0;
    }
    // Example: small covariance values in x, y, yaw
    kinematic_state_msg.pose.covariance[0] = 0.0001;
    kinematic_state_msg.pose.covariance[7] = 0.0001;
    kinematic_state_msg.pose.covariance[35] = 0.0001;

    // Twist
    kinematic_state_msg.twist.twist.linear.x = v_x;
    kinematic_state_msg.twist.twist.linear.y = v_y;
    kinematic_state_msg.twist.twist.linear.z = 0.0;

    kinematic_state_msg.twist.twist.angular.x = 0.0;
    kinematic_state_msg.twist.twist.angular.y = 0.0;
    kinematic_state_msg.twist.twist.angular.z = heading_rate;

    for (int i = 0; i < 36; i++) {
        kinematic_state_msg.twist.covariance[i] = 0.0;
    }
    kinematic_state_msg.twist.covariance[0] = 0.0001;
    kinematic_state_msg.twist.covariance[7] = 0.0001;
    kinematic_state_msg.twist.covariance[35] = 0.0001;

    kinematic_state_pub_->publish(kinematic_state_msg);

    // acceleration
    // // transform gyro frame
    // for (auto & gyro : gyro_queue_) {
    //     geometry_msgs::msg::Vector3Stamped angular_velocity;
    //     angular_velocity.header = gyro.header;
    //     angular_velocity.vector = gyro.angular_velocity;

    //     geometry_msgs::msg::Vector3Stamped transformed_angular_velocity;
    //     transformed_angular_velocity.header = tf_imu2base_ptr->header;
    //     tf2::doTransform(angular_velocity, transformed_angular_velocity, *tf_imu2base_ptr);

    //     gyro.header.frame_id = output_frame_;
    //     gyro.angular_velocity = transformed_angular_velocity.vector;
    //     gyro.angular_velocity_covariance = transform_covariance(gyro.angular_velocity_covariance);
    // }
    double imu_x_mean = 0;
    double imu_y_mean = 0;

    for (const auto & imu_data : imu_queue_) {
        // convert encoder speed to vx
        imu_x_mean += imu_data.linear_acceleration.x;
        imu_y_mean += imu_data.linear_acceleration.y;
    }
    imu_x_mean /= static_cast<double>(imu_queue_.size());
    imu_y_mean /= static_cast<double>(imu_queue_.size());

    // --- Build Acceleration message ---

    geometry_msgs::msg::AccelWithCovarianceStamped accel_msg;
    const auto latest_imu_stamp = rclcpp::Time(imu_queue_.back().header.stamp);
    accel_msg.header.stamp = latest_imu_stamp;
    accel_msg.header.frame_id = "base_link";  // or base frame

    // Linear acceleration from IMU (body frame)
    accel_msg.accel.accel.linear.x = imu_x_mean;
    accel_msg.accel.accel.linear.y = imu_y_mean;
    accel_msg.accel.accel.linear.z = 0.0;
    accel_msg.accel.accel.angular.x = 0.0;
    accel_msg.accel.accel.angular.y = 0.0;
    accel_msg.accel.accel.angular.z = 0.0;


    // Covariance
    for (int i = 0; i < 36; i++) {
        accel_msg.accel.covariance[i] = 0.0;
    }
    accel_msg.accel.covariance[0] = 0.001;
    accel_msg.accel.covariance[7] = 0.001;

    accel_pub_->publish(accel_msg);

    joint_state_queue_.clear();
    imu_queue_.clear();
  }

};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ScanMatcherInterface>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}
