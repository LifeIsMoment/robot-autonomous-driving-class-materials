from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='custom_world.world'),
        DeclareLaunchArgument('model', default_value='waffle'),
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('E_gazebo'),
                    'launch',
                    'my_world.launch.py',
                ])
            ),
            launch_arguments={
                'world': LaunchConfiguration('world'),
                'model': LaunchConfiguration('model'),
                'x_pose': LaunchConfiguration('x_pose'),
                'y_pose': LaunchConfiguration('y_pose'),
                'use_sim_time': LaunchConfiguration('use_sim_time'),
            }.items(),
        ),
    ])
