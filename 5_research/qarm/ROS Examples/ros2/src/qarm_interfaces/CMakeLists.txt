cmake_minimum_required(VERSION 3.8)
project(qarm_interfaces)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(action_msgs REQUIRED)
find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# ## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
# find_package(catkin REQUIRED COMPONENTS
#   actionlib_msgs
#   geometry_msgs
#   message_generation
#   moveit_msgs
#   rospy
#   sensor_msgs
#   std_msgs
# )

## Generate messages in the 'msg' folder
rosidl_generate_interfaces(${PROJECT_NAME}
  # "msg/AllJointState.msg"
  # "msg/GripperCommand.msg"
  # "msg/JointCommand.msg"
  # "msg/LEDCommand.msg"
  # "msg/AllCommands.msg"
  "msg/QArmDiagnostics.msg"
  "action/MoveQArm.action"
  DEPENDENCIES 
    std_msgs
    action_msgs
    sensor_msgs
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

ament_export_dependencies(rosidl_default_runtime)

ament_package()
