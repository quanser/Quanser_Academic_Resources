#include <chrono>
#include <functional>
#include <memory>

#include "geometry_msgs/msg/transform_stamped.hpp"
#include "rclcpp/rclcpp.hpp"
#include "tf2/LinearMath/Quaternion.h"
// #include "tf2_ros/transform_broadcaster.h"
#include "tf2_ros/static_transform_broadcaster.h"


int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);

  //new, no node object spinning on timer
  auto node = std::make_shared<rclcpp::Node>("sensor_frame_transform");
  std::shared_ptr<tf2_ros::StaticTransformBroadcaster> tf_broadcaster_;
  tf_broadcaster_ = std::make_shared<tf2_ros::StaticTransformBroadcaster>(node);

  geometry_msgs::msg::TransformStamped t;

  t.header.stamp = node->get_clock()->now();
  t.header.frame_id = "base_link";
  t.child_frame_id = "base_scan";
  t.transform.translation.x = 0.118; // base link centered on back axle
  t.transform.translation.y = 0.0;
  t.transform.translation.z = 0.193; // 

  tf2::Quaternion q;
  q.setRPY(0.0, 0.0, -3.14159265359);

  t.transform.rotation.x = q.x();
  t.transform.rotation.y = q.y();
  t.transform.rotation.z = q.z();
  t.transform.rotation.w = q.w();

  tf_broadcaster_->sendTransform(t);


  t.header.stamp = node->get_clock()->now();
  t.header.frame_id = "base_link";
  t.child_frame_id = "imu";
  t.transform.translation.x = 0.0;
  t.transform.translation.y = 0.0;
  t.transform.translation.z = 0.0;

  tf2::Quaternion q2;
  q2.setRPY(0.0, 0.0, 0.0);

  t.transform.rotation.x = q2.x();
  t.transform.rotation.y = q2.y();
  t.transform.rotation.z = q2.z();
  t.transform.rotation.w = q2.w();

  tf_broadcaster_->sendTransform(t);
  

  rclcpp::spin(node);
  //end

  rclcpp::shutdown();
  return 0;
}