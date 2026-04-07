# This is the launch file that starts up the QCar2 nodes for 2D lidar scan matching

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    # Declare launch arguments with default values
    declare_args = [
        DeclareLaunchArgument('odom_pub', default_value='false'),
        DeclareLaunchArgument('scan_tf_pub', default_value='false'),
        DeclareLaunchArgument('calibrate', default_value='false'),
        DeclareLaunchArgument('ekf_tf_pub', default_value='false'),
        DeclareLaunchArgument('init_pose',default_value='[0.0, 0.0, 0.0]'),
    ]



    qcar2_hardware = Node(
        package='qcar2_nodes',
        executable='qcar2_hardware',
        name='QCar2Hardware'
    )

    lidar_node = Node(
            package='qcar2_nodes',
            executable='lidar',
            name='Lidar'
        )
    
    fixed_frame = Node(
            package='qcar2_nodes',
            executable='fixed_lidar_frame',
            name='lidar_frame',
        )

    quarc_scan_matcher = Node(
            package='qcar2_nodes',
            executable='scan_match.py',
            name='scan_matcher',
            parameters=[{
                'odom_pub': LaunchConfiguration('odom_pub'),
                'tf_pub': LaunchConfiguration('scan_tf_pub'),
                'calibrate': LaunchConfiguration('calibrate'),
                'init_pose': LaunchConfiguration('init_pose'),
                }]
            )
    
    ekf_fusor = Node(
            package='qcar2_nodes',
            executable='ekf_fusor.py',
            name='ekf_fusor',
            parameters=[{
                'tf_pub': LaunchConfiguration('ekf_tf_pub'),
                }]
            )

    return LaunchDescription(
        declare_args+[
        qcar2_hardware,
        lidar_node,
        fixed_frame,
        quarc_scan_matcher,
        ekf_fusor
    ])
