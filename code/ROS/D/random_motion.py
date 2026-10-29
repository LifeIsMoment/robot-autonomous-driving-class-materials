import rclpy
from rclpy.node import Node
from geometry_msgs.msg import TwistStamped
import random

class RandomMotion(Node):
    def __init__(self):
        super().__init__('random_motion')
        self.pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.timer = self.create_timer(0.2, self.update)

    def update(self):
        msg = TwistStamped()

        msg.twist.linear.x = 0.3
        msg.twist.angular.z = random.uniform(-2.5, 1.8)

        self.pub.publish(msg)

def main():
    rclpy.init()
    node = RandomMotion()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()