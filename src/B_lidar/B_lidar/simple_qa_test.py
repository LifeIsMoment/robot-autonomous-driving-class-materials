import math
import time

from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import rclpy
from rclpy.node import Node


class SimpleObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )

        self.front_threshold = 0.40
        self.linear_speed = 0.15
        self.angular_speed = 0.5
        self.front_half_angle = math.radians(15.0)
        self.side_inner_angle = math.radians(30.0)
        self.side_outer_angle = math.radians(90.0)
        self.scan_timeout = 0.5
        self.last_scan_time = None
        self.stale_stop_sent = False

        self.watchdog = self.create_timer(0.1, self.check_scan_timeout)

    @staticmethod
    def sector_min(scan: LaserScan, start_angle: float, end_angle: float):
        distances = []

        for index, distance in enumerate(scan.ranges):
            angle = math.atan2(
                math.sin(scan.angle_min + index * scan.angle_increment),
                math.cos(scan.angle_min + index * scan.angle_increment),
            )
            if not start_angle <= angle <= end_angle:
                continue

            if math.isinf(distance) and distance > 0:
                distances.append(scan.range_max)
            elif (
                math.isfinite(distance)
                and scan.range_min <= distance <= scan.range_max
            ):
                distances.append(distance)

        return min(distances) if distances else None

    def publish_cmd(self, linear: float, angular: float):
        command = TwistStamped()
        command.header.stamp = self.get_clock().now().to_msg()
        command.twist.linear.x = linear
        command.twist.angular.z = angular
        self.cmd_pub.publish(command)

    def scan_callback(self, scan: LaserScan):
        self.last_scan_time = time.monotonic()
        self.stale_stop_sent = False

        front_min = self.sector_min(
            scan, -self.front_half_angle, self.front_half_angle
        )
        left_min = self.sector_min(
            scan, self.side_inner_angle, self.side_outer_angle
        )
        right_min = self.sector_min(
            scan, -self.side_outer_angle, -self.side_inner_angle
        )

        if front_min is None:
            self.get_logger().warning(
                '정면 LiDAR 데이터가 없어 정지합니다.', throttle_duration_sec=2.0
            )
            self.publish_cmd(0.0, 0.0)
            return

        if front_min < self.front_threshold:
            if left_min is None or right_min is None:
                self.get_logger().warning(
                    '좌우 LiDAR 데이터가 부족해 정지합니다.',
                    throttle_duration_sec=2.0,
                )
                self.publish_cmd(0.0, 0.0)
                return

            turn_direction = 1.0 if left_min >= right_min else -1.0
            self.publish_cmd(0.0, turn_direction * self.angular_speed)
            return

        speed_scale = min(
            1.0,
            (front_min - self.front_threshold) / self.front_threshold,
        )
        self.publish_cmd(self.linear_speed * speed_scale, 0.0)

    def check_scan_timeout(self):
        if self.last_scan_time is None:
            return

        if (
            time.monotonic() - self.last_scan_time > self.scan_timeout
            and not self.stale_stop_sent
        ):
            self.get_logger().error(
                'LiDAR 스캔이 끊겨 정지 명령을 보냅니다.'
            )
            self.publish_cmd(0.0, 0.0)
            self.stale_stop_sent = True


def main():
    rclpy.init()
    node = SimpleObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()