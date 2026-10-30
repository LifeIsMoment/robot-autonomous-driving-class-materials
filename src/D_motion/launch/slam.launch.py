from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('turtlebot3_gazebo'),
                    'launch',
                    'turtlebot3_world.launch.py',
                ])
            )
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('slam_toolbox'),
                    'launch',
                    'online_async_launch.py',
                ])
            ),
            launch_arguments={'use_sim_time': 'true'}.items(),
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ])
