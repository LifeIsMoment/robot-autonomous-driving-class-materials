import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution


def generate_launch_description():
    package_share = get_package_share_directory('E_gazebo')
    turtlebot_share = get_package_share_directory('turtlebot3_gazebo')
    ros_gz_sim_share = get_package_share_directory('ros_gz_sim')

    world_name = LaunchConfiguration('world')
    model = LaunchConfiguration('model')
    use_sim_time = LaunchConfiguration('use_sim_time')
    x_pose = LaunchConfiguration('x_pose')
    y_pose = LaunchConfiguration('y_pose')
    world_path = PathJoinSubstitution([package_share, 'worlds', world_name])
    turtlebot_launch = os.path.join(turtlebot_share, 'launch')

    return LaunchDescription([
        DeclareLaunchArgument(
            'world',
            default_value='custom_world.world',
            description='World file installed in E_gazebo/worlds',
        ),
        DeclareLaunchArgument('model', default_value='waffle'),
        DeclareLaunchArgument('use_sim_time', default_value='true'),
        DeclareLaunchArgument('x_pose', default_value='0.0'),
        DeclareLaunchArgument('y_pose', default_value='0.0'),
        SetEnvironmentVariable('TURTLEBOT3_MODEL', model),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            os.path.join(turtlebot_share, 'models'),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={
                'gz_args': ['-r -s -v2 ', world_path],
                'on_exit_shutdown': 'true',
            }.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(ros_gz_sim_share, 'launch', 'gz_sim.launch.py')
            ),
            launch_arguments={
                'gz_args': '-g -v2 ',
                'on_exit_shutdown': 'true',
            }.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(turtlebot_launch, 'robot_state_publisher.launch.py')
            ),
            launch_arguments={'use_sim_time': use_sim_time}.items(),
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(turtlebot_launch, 'spawn_turtlebot3.launch.py')
            ),
            launch_arguments={
                'x_pose': x_pose,
                'y_pose': y_pose,
            }.items(),
        ),
    ])
