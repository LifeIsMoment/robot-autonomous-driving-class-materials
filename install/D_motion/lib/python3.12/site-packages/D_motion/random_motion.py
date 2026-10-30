import random

import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node


class RandomMotion(Node):
    def __init__(self):
        super().__init__('random_motion')
        self.publisher = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(0.2, self.publish_command)

    def publish_command(self):
        message = TwistStamped()
        message.header.stamp = self.get_clock().now().to_msg()
        message.twist.linear.x = 0.3
        message.twist.angular.z = random.uniform(-2.5, 1.8)
        self.publisher.publish(message)


def main(args=None):
    rclpy.init(args=args)
    node = RandomMotion()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            stop = TwistStamped()
            stop.header.stamp = node.get_clock().now().to_msg()
            node.publisher.publish(stop)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
