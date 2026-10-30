import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import Int16MultiArray


class LocationSubscriber(Node):
    def __init__(self):
        super().__init__('my_loc')
        self.sub = self.create_subscription(Int16MultiArray, '/location', self.callback, 10)

    def callback(self, msg):
        x, y = msg.data
        self.get_logger().info(f'New location: {x}, {y}')


def main():
    rclpy.init()
    node = LocationSubscriber()
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
