from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    use_sim_time = LaunchConfiguration('use_sim_time')
    model_path = PathJoinSubstitution([
        FindPackageShare('G_custom_config'),
        'models',
        'turtlebot3_burger',
        'model.sdf',
    ])
    bridge_config = PathJoinSubstitution([
        FindPackageShare('G_custom_config'),
        'config',
        'turtlebot3_burger_bridge.yaml',
    ])

    return LaunchDescription([
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'burger'),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([
                FindPackageShare('G_custom_config'),
                'models',
            ]),
        ),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'models',
            ]),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                PathJoinSubstitution([
                    FindPackageShare('turtlebot3_gazebo'),
                    'launch',
                    'robot_state_publisher.launch.py',
                ])
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'burger',
                '-file', model_path,
                '-x', x_pose,
                '-y', y_pose,
                '-z', '0.01',
            ],
            output='screen',
        ),
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            arguments=[
                '--ros-args',
                '-p',
                ['config_file:=', bridge_config],
            ],
            output='screen',
        ),
    ])
