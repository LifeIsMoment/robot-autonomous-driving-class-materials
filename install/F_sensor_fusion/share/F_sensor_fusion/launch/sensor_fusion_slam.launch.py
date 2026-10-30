from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    model = LaunchConfiguration('model')
    world = LaunchConfiguration('world')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    ekf_config = PathJoinSubstitution([
        FindPackageShare('F_sensor_fusion'),
        'config',
        'ekf.yaml',
    ])
    rviz_config = PathJoinSubstitution([
        FindPackageShare('E_gazebo'),
        'rviz',
        'mapping.rviz',
    ])

    return LaunchDescription([
        DeclareLaunchArgument('model', default_value='waffle'),
        DeclareLaunchArgument('world', default_value='custom_world.world'),
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
                'model': model,
                'world': world,
                'x_pose': x_pose,
                'y_pose': y_pose,
                'use_sim_time': 'true',
            }.items(),
        ),
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            parameters=[ekf_config, {'use_sim_time': True}],
            output='screen',
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
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': True}],
            output='screen',
        ),
    ])
