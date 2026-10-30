from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('G_custom_config'),
                    'launch',
                    'spawn_turtlebot3.launch.py',
                ])
            ),
            launch_arguments={
                'x_pose': LaunchConfiguration('x_pose'),
                'y_pose': LaunchConfiguration('y_pose'),
                'use_sim_time': LaunchConfiguration('use_sim_time'),
            }.items(),
        ),
    ])