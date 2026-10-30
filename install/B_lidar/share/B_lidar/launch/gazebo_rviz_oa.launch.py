from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    AppendEnvironmentVariable,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    turtlebot_share = get_package_share_directory('turtlebot3_gazebo')
    ros_gz_share = get_package_share_directory('ros_gz_sim')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    world = PathJoinSubstitution([
        FindPackageShare('B_lidar'),
        'worlds',
        'turtlebot3_dqn_stage2_slow.world',
    ])

    rviz_config = (
        get_package_share_directory('B_lidar')
        + '/rviz/tb3_gazebo_slow_view.rviz'
    )

    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                ros_gz_share,
                'launch',
                'gz_sim.launch.py',
            ])
        ),
        launch_arguments={'gz_args': ['-r -s -v4 ', world]}.items(),
    )
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                ros_gz_share,
                'launch',
                'gz_sim.launch.py',
            ])
        ),
        launch_arguments={'gz_args': '-g -v4'}.items(),
    )

    robot_state_publisher = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'robot_state_publisher.launch.py',
            ])
        ),
        launch_arguments={'use_sim_time': use_sim_time}.items(),
    )
    spawn_robot = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('turtlebot3_gazebo'),
                'launch',
                'spawn_turtlebot3.launch.py',
            ])
        ),
        launch_arguments={
            'x_pose': x_pose,
            'y_pose': y_pose,
        }.items(),
    )

    return LaunchDescription([
        SetEnvironmentVariable('TURTLEBOT3_MODEL', 'waffle'),
        AppendEnvironmentVariable(
            'GZ_SIM_RESOURCE_PATH',
            turtlebot_share + '/models',
        ),
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        spawn_robot,
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
