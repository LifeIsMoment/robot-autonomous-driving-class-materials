import math
import time

import rclpy
from geometry_msgs.msg import TwistStamped
from rclpy.node import Node
from sensor_msgs.msg import LaserScan


class CornerEscapeObstacleAvoider(Node):
    def __init__(self):
        super().__init__('corner_escape_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)
        self.scan_sub = self.create_subscription(
            LaserScan, '/scan', self.scan_callback, 10
        )

        self.front_threshold = 0.45
        self.linear_speed = 0.10
        self.reverse_speed = 0.06
        self.angular_speed = 0.5
        self.scan_timeout = 2.0
        self.turn_timeout = 4.0
        self.reverse_duration = 0.6

        self.latest_scan = None
        self.last_scan_time = None
        self.state = 'MOVE'
        self.turn_direction = 1.0
        self.state_started = time.monotonic()
        self.stale_stop_sent = False

        self.create_timer(0.1, self.control_loop)

    @staticmethod
    def sector_min(scan: LaserScan, start_angle: float, end_angle: float):
        distances = []
        for index, distance in enumerate(scan.ranges):
            angle = scan.angle_min + index * scan.angle_increment
            angle = math.atan2(math.sin(angle), math.cos(angle))
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

    def scan_callback(self, scan: LaserScan):
        self.latest_scan = scan
        self.last_scan_time = time.monotonic()
        self.stale_stop_sent = False

    def publish_cmd(self, linear: float, angular: float):
        command = TwistStamped()
        command.header.stamp = self.get_clock().now().to_msg()
        command.twist.linear.x = linear
        command.twist.angular.z = angular
        self.cmd_pub.publish(command)

    def enter_state(self, state: str):
        self.state = state
        self.state_started = time.monotonic()

    def control_loop(self):
        now = time.monotonic()
        if (
            self.latest_scan is None
            or self.last_scan_time is None
            or now - self.last_scan_time > self.scan_timeout
        ):
            if not self.stale_stop_sent:
                self.get_logger().error(
                    'LiDAR 스캔이 없어 정지 명령을 보냅니다.'
                )
                self.publish_cmd(0.0, 0.0)
                self.stale_stop_sent = True
            return

        scan = self.latest_scan
        front_min = self.sector_min(
            scan, -math.radians(15), math.radians(15)
        )
        left_min = self.sector_min(
            scan, math.radians(30), math.radians(100)
        )
        right_min = self.sector_min(
            scan, -math.radians(100), -math.radians(30)
        )
        rear_min = self.sector_min(
            scan, math.radians(165), math.radians(180)
        )
        rear_other_min = self.sector_min(
            scan, -math.radians(180), -math.radians(165)
        )
        if rear_min is None:
            rear_min = rear_other_min
        elif rear_other_min is not None:
            rear_min = min(rear_min, rear_other_min)

        if front_min is None:
            self.publish_cmd(0.0, 0.0)
            self.get_logger().warning(
                '정면 LiDAR 데이터가 없어 정지합니다.',
                throttle_duration_sec=2.0,
            )
            return

        if self.state == 'MOVE':
            if front_min <= self.front_threshold:
                left_clearance = left_min or 0.0
                right_clearance = right_min or 0.0
                self.turn_direction = (
                    1.0 if left_clearance >= right_clearance else -1.0
                )
                self.enter_state('TURN')
                self.publish_cmd(0.0, self.turn_direction * self.angular_speed)
            else:
                speed_scale = min(
                    1.0,
                    (front_min - self.front_threshold) / self.front_threshold,
                )
                self.publish_cmd(self.linear_speed * speed_scale, 0.0)
            return

        if self.state == 'TURN':
            if front_min > self.front_threshold + 0.15:
                self.enter_state('MOVE')
                self.publish_cmd(self.linear_speed, 0.0)
            elif now - self.state_started >= self.turn_timeout:
                if rear_min is not None and rear_min > self.front_threshold:
                    self.enter_state('BACKUP')
                    self.publish_cmd(-self.reverse_speed, 0.0)
                else:
                    self.turn_direction *= -1.0
                    self.enter_state('TURN')
                    self.publish_cmd(
                        0.0, self.turn_direction * self.angular_speed
                    )
            else:
                self.publish_cmd(0.0, self.turn_direction * self.angular_speed)
            return

        if now - self.state_started >= self.reverse_duration:
            self.turn_direction *= -1.0
            self.enter_state('TURN')
            self.publish_cmd(0.0, self.turn_direction * self.angular_speed)
        elif rear_min is not None and rear_min > self.front_threshold:
            self.publish_cmd(-self.reverse_speed, 0.0)
        else:
            self.enter_state('TURN')
            self.turn_direction *= -1.0
            self.publish_cmd(0.0, self.turn_direction * self.angular_speed)


def main(args=None):
    rclpy.init(args=args)
    node = CornerEscapeObstacleAvoider()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.publish_cmd(0.0, 0.0)
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
