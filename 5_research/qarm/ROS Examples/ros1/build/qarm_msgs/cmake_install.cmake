# Install script for directory: /home/thomas/ros1/src/qarm_msgs

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/home/thomas/ros1/install")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/msg" TYPE FILE FILES
    "/home/thomas/ros1/src/qarm_msgs/msg/AllJointState.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/GripperCommand.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/JointCommand.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/LEDCommand.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/AllCommands.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/QArmAction.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionFeedback.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionGoal.msg"
    "/home/thomas/ros1/src/qarm_msgs/msg/QArmActionResult.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/action" TYPE FILE FILES "/home/thomas/ros1/src/qarm_msgs/action/moveQArm.action")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/msg" TYPE FILE FILES
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmAction.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionGoal.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionResult.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmActionFeedback.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmGoal.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmResult.msg"
    "/home/thomas/ros1/devel/share/qarm_msgs/msg/moveQArmFeedback.msg"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/cmake" TYPE FILE FILES "/home/thomas/ros1/build/qarm_msgs/catkin_generated/installspace/qarm_msgs-msg-paths.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include" TYPE DIRECTORY FILES "/home/thomas/ros1/devel/include/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/roseus/ros" TYPE DIRECTORY FILES "/home/thomas/ros1/devel/share/roseus/ros/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/common-lisp/ros" TYPE DIRECTORY FILES "/home/thomas/ros1/devel/share/common-lisp/ros/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/gennodejs/ros" TYPE DIRECTORY FILES "/home/thomas/ros1/devel/share/gennodejs/ros/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  execute_process(COMMAND "/usr/bin/python3" -m compileall "/home/thomas/ros1/devel/lib/python3/dist-packages/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/python3/dist-packages" TYPE DIRECTORY FILES "/home/thomas/ros1/devel/lib/python3/dist-packages/qarm_msgs")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib/pkgconfig" TYPE FILE FILES "/home/thomas/ros1/build/qarm_msgs/catkin_generated/installspace/qarm_msgs.pc")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/cmake" TYPE FILE FILES "/home/thomas/ros1/build/qarm_msgs/catkin_generated/installspace/qarm_msgs-msg-extras.cmake")
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs/cmake" TYPE FILE FILES
    "/home/thomas/ros1/build/qarm_msgs/catkin_generated/installspace/qarm_msgsConfig.cmake"
    "/home/thomas/ros1/build/qarm_msgs/catkin_generated/installspace/qarm_msgsConfig-version.cmake"
    )
endif()

if("x${CMAKE_INSTALL_COMPONENT}x" STREQUAL "xUnspecifiedx" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/share/qarm_msgs" TYPE FILE FILES "/home/thomas/ros1/src/qarm_msgs/package.xml")
endif()

