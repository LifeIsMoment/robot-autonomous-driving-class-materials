from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    rviz_config = (
        get_package_share_directory('B_lidar')
        + '/rviz/tb3_gazebo_slow_view.rviz'
    )
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'turtlebot3_world.launch.py',
            ])
        )
    )

    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle'),
        gazebo_launch,
        Node(
            package='B_lidar',
            executable='simple_oa',
            name='simple_obstacle_avoider',
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ])
