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
    
    csi_camera_node = Node(
            package='qcar2_nodes',
            executable='csi',
            name='csi_camera'
        )
    
    qcar2_hardware = Node(
            package='qcar2_nodes',
            executable='qcar2_hardware',
            name='qcar2_hardware',
        )
     
    return LaunchDescription([
        lidar_node,
        # realsense_camera_node,
        csi_camera_node,
        qcar2_hardware,
    ])
