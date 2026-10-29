import os

from launch import LaunchDescription
from launch.actions import ExecuteProcess, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution


def generate_launch_description():

    # 1. Burger 모델
    set_model = SetEnvironmentVariable(
        name='TURTLEBOT3_MODEL',
        value='burger'
    )

    # 2. Turtlebot3 Gazebo (Custom World)
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('E_gazebo'),
                'launch',
                'my_world.launch.py'
            ])
        )
    )

    # ───────────────────────────────────────────
    # [추가] EKF 센서 융합 노드
    from launch_ros.actions import Node
    
    ekf_config_path = PathJoinSubstitution([
        FindPackageShare('F_sensor_fusion'),
        'config',
        'ekf.yaml'
    ])

    robot_localization_node = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[ekf_config_path],
    )
    # ───────────────────────────────────────────

    # 3. SLAM Toolbox
    slam_toolbox = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('slam_toolbox'),
                'launch',
                'online_async_launch.py'
            ])
        )
    )

    # 4. RViz2 실행 (config 포함)
    rviz = ExecuteProcess(
        cmd=[
            'rviz2',
            '-d',
            os.path.expanduser('~/.rviz2/mapping.rviz')
        ],
        output='screen'
    )

    # 5. 로봇 주행 노드 실행
    navigate = ExecuteProcess(
        cmd=[
            'gnome-terminal', '--', 'bash', '-c',
            'source ~/robot_navigation/colcon_ws/install/setup.bash; '
            'ros2 run B_lidar 주행파일이름'
            'exec bash'
        ],
        output='screen'
    )

    return LaunchDescription([
        set_model,
        gazebo,
        robot_localization_node,  # <--- 추가
        slam_toolbox,
        rviz,
        navigate,
    ])