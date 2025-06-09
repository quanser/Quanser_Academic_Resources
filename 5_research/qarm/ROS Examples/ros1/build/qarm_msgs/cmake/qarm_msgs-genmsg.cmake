# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "qarm_msgs: 16 messages, 0 services")

set(MSG_I_FLAGS "-Iqarm_msgs:/home/thomas/ros1/src/qarm_msgs/msg;-Iqarm_msgs:/home/thomas/ros1/devel/share/qarm_msgs/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg;-Igeometry_msgs:/opt/ros/melodic/share/geometry_msgs/cmake/../msg;-Iactionlib_msgs:/opt/ros/melodic/share/actionlib_msgs/cmake/../msg;-Imoveit_msgs:/opt/ros/melodic/share/moveit_msgs/cmake/../msg;-Isensor_msgs:/opt/ros/melodic/share/sensor_msgs/cmake/../msg;-Itrajectory_msgs:/opt/ros/melodic/share/trajectory_msgs/cmake/../msg;-Ishape_msgs:/opt/ros/melodic/share/shape_msgs/cmake/../msg;-Iobject_recognition_msgs:/opt/ros/melodic/share/object_recognition_msgs/cmake/../msg;-Ioctomap_msgs:/opt/ros/melodic/share/octomap_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(qarm_msgs_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" "std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" ""
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" ""
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" ""
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" "qarm_msgs/LEDCommand:std_msgs/Header:qarm_msgs/JointCommand:qarm_msgs/GripperCommand"
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" "actionlib_msgs/GoalID:qarm_msgs/QArmActionFeedback:qarm_msgs/QArmActionResult:qarm_msgs/AllJointState:qarm_msgs/QArmActionGoal:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" "actionlib_msgs/GoalID:std_msgs/Header:qarm_msgs/AllJointState"
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" "actionlib_msgs/GoalID:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" "actionlib_msgs/GoalID:qarm_msgs/moveQArmFeedback:qarm_msgs/moveQArmGoal:qarm_msgs/QArmActionFeedback:qarm_msgs/QArmActionResult:qarm_msgs/moveQArmActionResult:qarm_msgs/AllJointState:qarm_msgs/moveQArmResult:qarm_msgs/moveQArmActionFeedback:qarm_msgs/QArmActionGoal:actionlib_msgs/GoalStatus:std_msgs/Header:qarm_msgs/moveQArmActionGoal"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" "qarm_msgs/QArmActionGoal:actionlib_msgs/GoalID:std_msgs/Header:qarm_msgs/moveQArmGoal"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" "actionlib_msgs/GoalID:qarm_msgs/QArmActionResult:qarm_msgs/moveQArmResult:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" "actionlib_msgs/GoalID:qarm_msgs/moveQArmFeedback:qarm_msgs/QArmActionFeedback:qarm_msgs/AllJointState:actionlib_msgs/GoalStatus:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" "qarm_msgs/QArmActionGoal:actionlib_msgs/GoalID:std_msgs/Header"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" "actionlib_msgs/GoalID:actionlib_msgs/GoalStatus:std_msgs/Header:qarm_msgs/QArmActionResult"
)

get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_custom_target(_qarm_msgs_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "qarm_msgs" "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" "actionlib_msgs/GoalID:std_msgs/Header:qarm_msgs/AllJointState:qarm_msgs/QArmActionFeedback"
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg;/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_cpp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
)

### Generating Services

### Generating Module File
_generate_module_cpp(qarm_msgs
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(qarm_msgs_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(qarm_msgs_generate_messages qarm_msgs_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_cpp _qarm_msgs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(qarm_msgs_gencpp)
add_dependencies(qarm_msgs_gencpp qarm_msgs_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS qarm_msgs_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg;/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)
_generate_msg_eus(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
)

### Generating Services

### Generating Module File
_generate_module_eus(qarm_msgs
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(qarm_msgs_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(qarm_msgs_generate_messages qarm_msgs_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_eus _qarm_msgs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(qarm_msgs_geneus)
add_dependencies(qarm_msgs_geneus qarm_msgs_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS qarm_msgs_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg;/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)
_generate_msg_lisp(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
)

### Generating Services

### Generating Module File
_generate_module_lisp(qarm_msgs
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(qarm_msgs_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(qarm_msgs_generate_messages qarm_msgs_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_lisp _qarm_msgs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(qarm_msgs_genlisp)
add_dependencies(qarm_msgs_genlisp qarm_msgs_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS qarm_msgs_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg;/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)
_generate_msg_nodejs(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
)

### Generating Services

### Generating Module File
_generate_module_nodejs(qarm_msgs
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(qarm_msgs_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(qarm_msgs_generate_messages qarm_msgs_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_nodejs _qarm_msgs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(qarm_msgs_gennodejs)
add_dependencies(qarm_msgs_gennodejs qarm_msgs_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS qarm_msgs_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg;/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
  "${MSG_I_FLAGS}"
  "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalStatus.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)
_generate_msg_py(qarm_msgs
  "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
  "${MSG_I_FLAGS}"
  "/opt/ros/melodic/share/actionlib_msgs/cmake/../msg/GoalID.msg;/opt/ros/melodic/share/std_msgs/cmake/../msg/Header.msg;/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg;/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
)

### Generating Services

### Generating Module File
_generate_module_py(qarm_msgs
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(qarm_msgs_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(qarm_msgs_generate_messages qarm_msgs_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg" NAME_WE)
add_dependencies(qarm_msgs_generate_messages_py _qarm_msgs_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(qarm_msgs_genpy)
add_dependencies(qarm_msgs_genpy qarm_msgs_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS qarm_msgs_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/qarm_msgs
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(qarm_msgs_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()
if(TARGET geometry_msgs_generate_messages_cpp)
  add_dependencies(qarm_msgs_generate_messages_cpp geometry_msgs_generate_messages_cpp)
endif()
if(TARGET actionlib_msgs_generate_messages_cpp)
  add_dependencies(qarm_msgs_generate_messages_cpp actionlib_msgs_generate_messages_cpp)
endif()
if(TARGET moveit_msgs_generate_messages_cpp)
  add_dependencies(qarm_msgs_generate_messages_cpp moveit_msgs_generate_messages_cpp)
endif()
if(TARGET sensor_msgs_generate_messages_cpp)
  add_dependencies(qarm_msgs_generate_messages_cpp sensor_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/qarm_msgs
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(qarm_msgs_generate_messages_eus std_msgs_generate_messages_eus)
endif()
if(TARGET geometry_msgs_generate_messages_eus)
  add_dependencies(qarm_msgs_generate_messages_eus geometry_msgs_generate_messages_eus)
endif()
if(TARGET actionlib_msgs_generate_messages_eus)
  add_dependencies(qarm_msgs_generate_messages_eus actionlib_msgs_generate_messages_eus)
endif()
if(TARGET moveit_msgs_generate_messages_eus)
  add_dependencies(qarm_msgs_generate_messages_eus moveit_msgs_generate_messages_eus)
endif()
if(TARGET sensor_msgs_generate_messages_eus)
  add_dependencies(qarm_msgs_generate_messages_eus sensor_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/qarm_msgs
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(qarm_msgs_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()
if(TARGET geometry_msgs_generate_messages_lisp)
  add_dependencies(qarm_msgs_generate_messages_lisp geometry_msgs_generate_messages_lisp)
endif()
if(TARGET actionlib_msgs_generate_messages_lisp)
  add_dependencies(qarm_msgs_generate_messages_lisp actionlib_msgs_generate_messages_lisp)
endif()
if(TARGET moveit_msgs_generate_messages_lisp)
  add_dependencies(qarm_msgs_generate_messages_lisp moveit_msgs_generate_messages_lisp)
endif()
if(TARGET sensor_msgs_generate_messages_lisp)
  add_dependencies(qarm_msgs_generate_messages_lisp sensor_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/qarm_msgs
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(qarm_msgs_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()
if(TARGET geometry_msgs_generate_messages_nodejs)
  add_dependencies(qarm_msgs_generate_messages_nodejs geometry_msgs_generate_messages_nodejs)
endif()
if(TARGET actionlib_msgs_generate_messages_nodejs)
  add_dependencies(qarm_msgs_generate_messages_nodejs actionlib_msgs_generate_messages_nodejs)
endif()
if(TARGET moveit_msgs_generate_messages_nodejs)
  add_dependencies(qarm_msgs_generate_messages_nodejs moveit_msgs_generate_messages_nodejs)
endif()
if(TARGET sensor_msgs_generate_messages_nodejs)
  add_dependencies(qarm_msgs_generate_messages_nodejs sensor_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs)
  install(CODE "execute_process(COMMAND \"/usr/bin/python3\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/qarm_msgs
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(qarm_msgs_generate_messages_py std_msgs_generate_messages_py)
endif()
if(TARGET geometry_msgs_generate_messages_py)
  add_dependencies(qarm_msgs_generate_messages_py geometry_msgs_generate_messages_py)
endif()
if(TARGET actionlib_msgs_generate_messages_py)
  add_dependencies(qarm_msgs_generate_messages_py actionlib_msgs_generate_messages_py)
endif()
if(TARGET moveit_msgs_generate_messages_py)
  add_dependencies(qarm_msgs_generate_messages_py moveit_msgs_generate_messages_py)
endif()
if(TARGET sensor_msgs_generate_messages_py)
  add_dependencies(qarm_msgs_generate_messages_py sensor_msgs_generate_messages_py)
endif()
