import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    bringup_dir = get_package_share_directory('qbot_platform_issac_nav2')
    nav2_dir = get_package_share_directory('nav2_bringup')

    # QBot Platform Cartographer launch
    qbot_platform_cartographer_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_dir, 'launch', 'qbot_platform_cartographer_launch.py')
        )
    )

    # Nav2 params
    nav2_params = os.path.join(bringup_dir, 'config', 'qbot_platform_slam_and_nav.yaml')

    # Nav2 launch
    nav2_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(nav2_dir, 'launch', 'navigation_launch.py')
        ),
        launch_arguments={
            'use_sim_time': 'false',
            'params_file': nav2_params,
            'slam': 'False',
            'localization': 'False',
            'map': ''
        }.items()
    )

    # TwistStamped → Twist bridge node
    twist_bridge_node = Node(
        package='qbot_platform_issac_nav2',
        executable='twist_stamped_to_twist.py',
        name='twist_stamped_to_twist',
        output='screen',
        # remappings=[
        #     ('/cmd_vel_twist', '/cmd_vel')  # Isaac Sim subscribes to /cmd_vel
        # ]
    )

    # Build LaunchDescription
    ld = LaunchDescription([
        qbot_platform_cartographer_launch,
        nav2_launch,
        twist_bridge_node
    ])

    return ld
