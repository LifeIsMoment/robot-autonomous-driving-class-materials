from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    world = LaunchConfiguration('world')
    model = LaunchConfiguration('model')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    autonomous_motion = LaunchConfiguration('autonomous_motion')
    ekf_config = PathJoinSubstitution([
        FindPackageShare('G_custom_config'),
        'config',
        'ekf.yaml',
    ])
    slam_config = PathJoinSubstitution([
        FindPackageShare('G_custom_config'),
        'config',
        'mapper_params_online_async.yaml',
    ])
    rviz_config = PathJoinSubstitution([
        FindPackageShare('E_gazebo'),
        'rviz',
        'mapping.rviz',
    ])

    return LaunchDescription([
        DeclareLaunchArgument('world', default_value='custom_world.world'),
        DeclareLaunchArgument('model', default_value='waffle'),
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        DeclareLaunchArgument(
            'autonomous_motion',
            default_value='false',
            description='Start corner-escape autonomous motion when true',
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('G_custom_config'),
                    'launch',
                    'my_world.launch.py',
                ])
            ),
            launch_arguments={
                'world': world,
                'model': model,
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
                    FindPackageShare('G_custom_config'),
                    'launch',
                    'online_async_launch.py',
                ])
            ),
            launch_arguments={
                'use_sim_time': 'true',
                'slam_params_file': slam_config,
            }.items(),
        ),
        Node(
            package='B_lidar',
            executable='corner_escape_oa',
            name='corner_escape_obstacle_avoider',
            condition=IfCondition(autonomous_motion),
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
