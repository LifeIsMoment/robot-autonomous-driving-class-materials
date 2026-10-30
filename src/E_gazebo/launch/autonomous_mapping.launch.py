from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    model = LaunchConfiguration('model')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    rviz_config = PathJoinSubstitution([
        FindPackageShare('E_gazebo'),
        'rviz',
        'mapping.rviz',
    ])

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='custom_world.world',
            description='Gazebo world file',
        ),
        DeclareLaunchArgument('model', default_value='waffle'),
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('E_gazebo'),
                    'launch',
                    'my_world.launch.py',
                ])
            ),
            launch_arguments={
                'world': world,
                'model': model,
                'use_sim_time': 'true',
                'x_pose': x_pose,
                'y_pose': y_pose,
            }.items(),
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
            package='B_lidar',
            executable='corner_escape_oa',
            name='corner_escape_obstacle_avoider',
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
