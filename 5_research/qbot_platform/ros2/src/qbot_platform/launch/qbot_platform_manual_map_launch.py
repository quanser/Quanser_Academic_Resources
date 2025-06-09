# This is the launch file that starts up the basic QBot Platform nodes,
# plus the TF node. Then start the cartographer.

import os
import subprocess

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (IncludeLaunchDescription, DeclareLaunchArgument)
from launch.actions import (ExecuteProcess, LogInfo, RegisterEventHandler, OpaqueFunction, TimerAction)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (PathJoinSubstitution, LaunchConfiguration)
from launch.event_handlers import (OnProcessExit, OnProcessStart)

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def exit_qbot_platform_driver_interface_cb(context):
    # We're using a callback function and wrap it in OpaqueFunction() to be
    # passsed to the qbot_platform_driver_interface node's OnProcessExit
    # event handler, instead of using an ExecuteProcess() to stop the driver
    # model. This is because when an user uses Ctrl-C to end the launch file
    # it would cause the entire launch system to close, and during launch
    # system closing, no new ExecuteProcess() will be created, and thus cannot
    # use it to call "quarc_run -q".
    # However, OpaqueFunction callback would still work even during launch
    # system shutdown, and we can call the subprocess.call() to run the
    # "quarc_run -q" command to stop the model.

    # Use "run(capture_output=True)" so that if the rt-model somehow stopped
    # for whatever reason, we won't show the error message, because it doesn't
    # really matter at this point.
    subprocess.run('quarc_run' + ' -q -t tcpip://localhost:17000 qbot_platform_driver_physical', shell=True, capture_output=True)



def generate_launch_description():
    use_sim = LaunchConfiguration('use_sim')
    driver_model_rt_executable = PathJoinSubstitution([FindPackageShare('qbot_platform'), 'rt_models', 'qbot_platform_driver_physical.rt-linux_qbot_platform'])
    rt_model_start = ExecuteProcess(
            cmd=['quarc_run', '-r -t tcpip://localhost:17000', driver_model_rt_executable, '-d %d -uri tcpip://%m:17001'],
            name='QBotPlatformDriverModelStart',
            shell=True
        )

    cartographer_config_dir = PathJoinSubstitution(
        [
            FindPackageShare('qbot_platform'),
            'config',
        ]
    )

    configuration_basename = LaunchConfiguration('configuration_basename')
    resolution = LaunchConfiguration('resolution')
    publish_period_sec = LaunchConfiguration('publish_period_sec', default='0.1')

    qbot_platform_to_lidar_tf_node = Node(
            package='qbot_platform',
            executable='fixed_lidar_frame',
            name='fixed_lidar_frame')

    lidar_node = Node(
            package='qbot_platform',
            executable='lidar',
            name='Lidar')

    joystick_command_node = Node(
        package = 'qbot_platform',
        executable = 'command',
        name = 'joystickCommands'
    )

    qbot_platform_driver_node = Node(
            package='qbot_platform',
            executable='qbot_platform_driver_interface',
            name='QBotPlatformDriver',
            parameters=[{'arm_robot': True}],
        )

    configuration_basename_la = DeclareLaunchArgument(
            'configuration_basename',
            default_value='qbot_platform_2d.lua',
            description='Name of LUA file for cartographer')

    use_sim_la = DeclareLaunchArgument(
            'use_sim',
            default_value='false',
            description='Start robot in Gazebo simulation')

    resolution_la = DeclareLaunchArgument(
            'resolution',
            default_value='0.01',
            description='Resolution of a grid cell of occupancy grid')

    publish_period_sec_la = DeclareLaunchArgument(
            'publish_period_sec',
            default_value='0.1',
            description='Publishing period')

    cartographer_node = Node(
            package='cartographer_ros',
            executable='cartographer_node',
            output='screen',
            arguments=['-configuration_directory', cartographer_config_dir,
                       '-configuration_basename', configuration_basename])

    cartographer_occupancy_grid_node = Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            output='screen',
            arguments=['-resolution', resolution, '-publish_period_sec', publish_period_sec])

    return LaunchDescription([
        rt_model_start,
        qbot_platform_to_lidar_tf_node,
        configuration_basename_la,
        resolution_la,
        use_sim_la,
        publish_period_sec_la,
        cartographer_node,
        cartographer_occupancy_grid_node,
        lidar_node,
        joystick_command_node,
                RegisterEventHandler(
            OnProcessExit(
                target_action=qbot_platform_driver_node,
                on_exit=[
                    OpaqueFunction(function=exit_qbot_platform_driver_interface_cb),
                    LogInfo(msg='QBotPlatformDriver exiting, so stopping the driver model as well.')
                    ]
            )
        ),
        RegisterEventHandler(
            OnProcessStart(
                target_action=rt_model_start,
                on_start=[
                    LogInfo(msg='QBotPlatformDriverModelStart started. Wait for 2 sec, then start the qbot_platform_driver_interface node'),
                    TimerAction(
                        period=2.0,
                        actions=[qbot_platform_driver_node]
                    )
                ]
            )
        )

    ])
