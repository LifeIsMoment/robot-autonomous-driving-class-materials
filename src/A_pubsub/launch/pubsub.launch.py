from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='a_pubsub',
            executable='subscriber',
            output='screen',
        ),
        Node(
            package='a_pubsub',
            executable='processor',
            output='screen',
        ),
        Node(
            package='a_pubsub',
            executable='publisher',
            output='screen',
        ),
    ])
