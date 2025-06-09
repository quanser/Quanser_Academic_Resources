# This is the launch file that starts up the basic QCar2 nodes

import subprocess

from launch import LaunchDescription
from launch.actions import (ExecuteProcess, LogInfo, RegisterEventHandler, OpaqueFunction, TimerAction)
from launch.substitutions import PathJoinSubstitution
from launch.event_handlers import (OnProcessExit, OnProcessStart)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
        
    lidar_node = Node(
            package='qcar2_nodes',
            executable='lidar',
            name='Lidar'
        )
    
    realsense_camera_node = Node(
            package='qcar2_nodes',
            executable='rgbd',
            name='RealsenseCamera'
        )
    
    downward_facing_camera_node = Node(
            package='qcar2_nodes',
            executable='csi',
            name='DownwardFacingCamera'
        )
    
    qcar2_hardware = Node(
            package='qcar2_nodes',
            executable='qcar2_hardware',
            name='qcar2_hardware',
        )

    joystick_command = Node(
        package = 'qcar2_nodes',
        executable = 'command',
        name = 'joystick_command'
    )        
    return LaunchDescription([
        lidar_node,
        realsense_camera_node,
        downward_facing_camera_node,
        qcar2_hardware,
        joystick_command
    ])
