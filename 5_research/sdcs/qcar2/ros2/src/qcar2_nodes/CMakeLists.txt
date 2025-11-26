cmake_minimum_required(VERSION 3.8)
project(qcar2_nodes)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(ament_cmake_python REQUIRED)
find_package(cv_bridge REQUIRED)
find_package(image_transport REQUIRED)
find_package(OpenCV REQUIRED COMPONENTS highgui imgcodecs imgproc videoio)
find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(action_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(control_msgs REQUIRED)
find_package(qcar2_interfaces REQUIRED)
find_package(tf2_ros REQUIRED)

# Need to define _NVIDIA macro since the Quanser SDK has different
# functionalities depending on which platform it's being used.
add_compile_definitions(_NVIDIA)


# The header 'cv_bridge/cv_bridge.hpp' was added in version 3.3.0. For older
# cv_bridge versions, we have to use the header 'cv_bridge/cv_bridge.h'.
if(${cv_bridge_VERSION} VERSION_GREATER_EQUAL "3.3.0")
  set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -DCV_BRDIGE_HAS_HPP")
endif()

#add_executable(qcar2_driver_interface src/qcar2_driver_interface.cpp)
#target_link_libraries(qcar2_driver_interface -lquanser_communications)
#ament_target_dependencies(qcar2_driver_interface rclcpp std_msgs geometry_msgs sensor_msgs control_msgs)


add_executable(command src/command.cpp)
target_link_libraries(command -lquanser_devices -lquanser_communications -lquanser_runtime -lquanser_common)
ament_target_dependencies(command rclcpp geometry_msgs qcar2_interfaces)


add_executable(qcar2_hardware src/qcar2_hardware.cpp)
target_link_libraries(qcar2_hardware -lquanser_devices -lhil -lquanser_runtime -lquanser_common)
ament_target_dependencies(qcar2_hardware rclcpp std_msgs geometry_msgs sensor_msgs control_msgs qcar2_interfaces)

add_executable(rgbd src/rgbd.cpp)
# Orin has OpenCV 4 installed, and put it under the /usr/include/opencv4 directory
# So we need to add this directory to the include directory list for the node to
# compile properly.
target_include_directories(rgbd PUBLIC /usr/include/opencv4)
target_link_libraries(rgbd cv_bridge::cv_bridge image_transport::image_transport opencv_imgcodecs -lquanser_media -lquanser_runtime -lquanser_common)
ament_target_dependencies(rgbd rclcpp cv_bridge image_transport OpenCV std_msgs sensor_msgs)

add_executable(lidar src/lidar.cpp)
target_link_libraries(lidar -lquanser_devices -lquanser_communications -lquanser_runtime -lquanser_common)
ament_target_dependencies(lidar rclcpp sensor_msgs)

add_executable(csi src/csi.cpp)
# Orin has OpenCV 4 installed, and put it under the /usr/include/opencv4 directory
# So we need to add this directory to the include directory list for the node to
# compile properly.
target_include_directories(csi PUBLIC /usr/include/opencv4)
target_link_libraries(csi cv_bridge::cv_bridge image_transport::image_transport opencv_imgcodecs -lquanser_media -lquanser_runtime -lquanser_common)
ament_target_dependencies(csi rclcpp cv_bridge image_transport OpenCV std_msgs sensor_msgs)

# TF
# qcar2 -> lidar
add_executable(fixed_lidar_frame src/fixed_lidar_frame.cpp)
ament_target_dependencies(fixed_lidar_frame geometry_msgs rclcpp tf2_ros)

add_executable(fixed_lidar_frame_virtual src/fixed_lidar_frame_virtual.cpp)
ament_target_dependencies(fixed_lidar_frame_virtual geometry_msgs rclcpp tf2_ros)


# nav2
# nav2 -> qcar2
add_executable(nav2_qcar2_converter src/nav2_qcar_command_convert.cpp)
ament_target_dependencies(nav2_qcar2_converter rclcpp geometry_msgs qcar2_interfaces)

# # Install Python modules
# ament_python_install_package(${PROJECT_NAME})

# # Install Python executables
# install(PROGRAMS
#   src/nav_to_pose.py
#   src/robot_navigator.py
#   DESTINATION lib/${PROJECT_NAME}
# )


# Install nodes
#install(TARGETS qcar2_driver_interface
#  DESTINATION lib/${PROJECT_NAME})
install(TARGETS qcar2_hardware
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS rgbd
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS lidar
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS csi
  DESTINATION lib/${PROJECT_NAME})


install(TARGETS command
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS nav2_qcar2_converter
  DESTINATION lib/${PROJECT_NAME})

# Install TF
install(TARGETS fixed_lidar_frame
  DESTINATION lib/${PROJECT_NAME})

install(TARGETS fixed_lidar_frame_virtual
  DESTINATION lib/${PROJECT_NAME})

# Install launch files
install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}/
)

# Install RT models needed for the qcar2 node
install(DIRECTORY rt_models
  DESTINATION share/${PROJECT_NAME}/
)

# Install configuration needed for the cartographer node
install(DIRECTORY config
  DESTINATION share/${PROJECT_NAME}/
)



if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # comment the line when a copyright and license is added to all source files
  set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # comment the line when this package is in a git repo and when
  # a copyright and license is added to all source files
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
