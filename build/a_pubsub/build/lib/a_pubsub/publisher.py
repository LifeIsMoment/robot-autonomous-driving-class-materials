import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String


class DirectionPublisher(Node):
    def __init__(self):
        super().__init__('get_dir')
        self.pub = self.create_publisher(String, '/direction', 10)

    def run(self):
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.1)
            direction = input('Input Direction (w,s,a,d): ').lower()
            msg = String()
            msg.data = direction
            self.pub.publish(msg)
            self.get_logger().info(f'Published: {direction}')


def main():
    rclpy.init()
    node = DirectionPublisher()
    try:
        node.run()
    except (KeyboardInterrupt, ExternalShutdownException):
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
