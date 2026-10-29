import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import rclpy
from rclpy.node import Node


class SimpleObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)

        self.front_threshold = 0.25
        self.linear_speed = 0.2
        self.angular_speed = 0.5

    def scan_callback(self, scan: LaserScan):
        left_vals = [r for r in scan.ranges[:31] if math.isfinite(r)]
        left_avg = sum(left_vals)/len(left_vals) if left_vals else 0.0

        right_vals = [r for r in scan.ranges[-30:] if math.isfinite(r)]
        right_avg = sum(right_vals)/len(right_vals) if right_vals else 0.0

        front_vals = left_vals + right_vals
        front_min = min(front_vals) if front_vals else float('inf')

        twist = TwistStamped()

        if front_min > self.front_threshold:
            twist.twist.linear.x = 0.15
            twist.twist.angular.z = 0.0
        else:
            twist.twist.linear.x = 0.0
            twist.twist.angular.z = self.angular_speed if left_avg > right_avg else -self.angular_speed

        self.cmd_pub.publish(twist)


def main():
    rclpy.init()
    node = SimpleObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()