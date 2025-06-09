# This is the launch file that starts up the basic QBot Platform nodes,
# plus the TF node. Then start the cartographer.

import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, DeclareLaunchArgument)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (PathJoinSubstitution, LaunchConfiguration)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    use_sim = LaunchConfiguration('use_sim')

    cartographer_config_dir = PathJoinSubstitution(
        [
            FindPackageShare('qcar2_nodes'),
            'config',
        ]
    )
    configuration_basename = LaunchConfiguration('configuration_basename')
    resolution = LaunchConfiguration('resolution')
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='1.0')

    qcar2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('qcar2_nodes'), 'launch', 'qcar2_manual_drive.py')]
        )
    )

    qcar2_to_lidar_tf_node = Node(
            package='qcar2_nodes',
            executable='fixed_lidar_frame',
            name='fixed_lidar_frame')

    configuration_basename_la = DeclareLaunchArgument(
            'configuration_basename',
            default_value='qcar2_2d.lua',
            description='Name of LUA file for cartographer')

    use_sim_la = DeclareLaunchArgument(
            'use_sim',
            default_value='false',
            description='Start robot in Gazebo simulation')

    resolution_la = DeclareLaunchArgument(
            'resolution',
            default_value='0.05',
            description='Resolution of a grid cell of occupancy grid')

    publish_period_sec_la = DeclareLaunchArgument(
            'publish_period_sec',
            default_value='1.0',
            description='Publishing period')

    cartographer_node = Node(
            package='cartographer_ros',
            executable='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim}],
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename])

    cartographer_occupancy_grid_node = Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': use_sim}],
            arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

    return LaunchDescription([
        qcar2_launch,
        configuration_basename_la,
        use_sim_la,
        resolution_la,
        publish_period_sec_la,
        cartographer_node,
        cartographer_occupancy_grid_node,
        qcar2_to_lidar_tf_node,
    ])
