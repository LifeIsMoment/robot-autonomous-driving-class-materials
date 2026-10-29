import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from tf_transformations import euler_from_quaternion


class SimpleYawObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_yaw_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)

        self.state = "MOVE"

        self.front_threshold = 0.25
        self.linear_speed = 0.2
        self.angular_speed = 0.5
        
        self.current_yaw = 0.0
        self.target_yaw = 0.0
        self.yaw_tolerance = 0.05
        self.rotation_angle = math.pi / 6

    def odom_callback(self, msg: Odometry):
        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        _, _, self.current_yaw = euler_from_quaternion(quat)

    def scan_callback(self, scan: LaserScan):
        left_vals = [r for r in scan.ranges[:31] if math.isfinite(r)]
        left_avg = sum(left_vals)/len(left_vals) if left_vals else 0.0

        right_vals = [r for r in scan.ranges[-30:] if math.isfinite(r)]
        right_avg = sum(right_vals)/len(right_vals) if right_vals else 0.0

        front_vals = left_vals + right_vals
        front_min = min(front_vals) if front_vals else float('inf')

        twist = TwistStamped()

        if self.state == "TURN":
            angle_diff = self.normalize_angle(self.target_yaw - self.current_yaw)

            if abs(angle_diff) > self.yaw_tolerance:
                twist.twist.linear.x = 0.0
                twist.twist.angular.z = self.angular_speed * (1 if angle_diff > 0 else -1)
            else:
                self.state = "MOVE"

        else:
            if front_min > self.front_threshold:
                twist.twist.linear.x = self.linear_speed
                twist.twist.angular.z = 0.0
            else:
                self.state = "TURN"

                turn_dir = 1 if left_avg > right_avg else -1
                self.target_yaw = self.normalize_angle(
                    self.current_yaw + turn_dir * self.rotation_angle
                )

                twist.twist.linear.x = 0.0
                twist.twist.angular.z = self.angular_speed * turn_dir

        self.cmd_pub.publish(twist)

    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))


def main():
    rclpy.init()
    node = SimpleYawObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()