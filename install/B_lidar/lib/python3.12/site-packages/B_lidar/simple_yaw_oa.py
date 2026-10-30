import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
from nav_msgs.msg import Odometry
import rclpy
from rclpy.node import Node
from tf_transformations import euler_from_quaternion


# SimpleYawObstacleAvoider 클래스는 ROS2 노드로, 레이저 스캔 데이터와 오도메트리 데이터를 기반으로 장애물을 피하면서 목표 방향으로 회전하는 로직을 구현합니다.
class SimpleYawObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_yaw_obstacle_avoider')

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)                    # /cmd_vel 토픽에 제어 명령 메시지를 발행하는 퍼블리셔 생성
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)  # /scan 토픽에서 LaserScan 메시지를 구독
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)   # /odom 토픽에서 Odometry 메시지를 구독

        self.state = "MOVE"  # 현재 상태를 나타내는 변수, "MOVE"는 전진 상태, "TURN"은 회전 상태를 의미

        self.front_threshold = 0.25  # 정면 장애물 감지 거리 임계값
        self.linear_speed = 0.2      # 전진 속도
        self.angular_speed = 0.5     # 회전 속도
        
        self.current_yaw = 0.0             # 현재 로봇의 yaw(회전) 각도
        self.target_yaw = 0.0              # 목표 yaw(회전) 각도
        self.yaw_tolerance = 0.05          # 목표 yaw 각도 허용 오차
        self.rotation_angle = math.pi / 6  # 회전할 각도 (30도)

    # odom_callback 함수는 Odometry 메시지를 수신할 때 호출되며, 로봇의 현재 yaw 각도를 업데이트합니다.
    def odom_callback(self, msg: Odometry):
        q = msg.pose.pose.orientation
        quat = [q.x, q.y, q.z, q.w]
        _, _, self.current_yaw = euler_from_quaternion(quat)

    # scan_callback 함수는 LaserScan 메시지를 수신할 때 호출되며, 장애물 감지 및 회전 로직을 수행합니다.
    def scan_callback(self, scan: LaserScan):
        left_vals = [r for r in scan.ranges[:31] if math.isfinite(r)]
        left_avg = sum(left_vals)/len(left_vals) if left_vals else 0.0

        right_vals = [r for r in scan.ranges[-30:] if math.isfinite(r)]
        right_avg = sum(right_vals)/len(right_vals) if right_vals else 0.0

        front_vals = left_vals + right_vals
        front_min = min(front_vals) if front_vals else float('inf')

        twist = TwistStamped()

        # 장애물이 감지되면 회전 상태로 전환하고, 목표 yaw 각도를 설정합니다. 그렇지 않으면 전진 상태를 유지합니다.
        if self.state == "TURN":
            angle_diff = self.normalize_angle(self.target_yaw - self.current_yaw)  # 현재 yaw와 목표 yaw의 차이를 계산하여 회전 방향을 결정합니다.

            # 회전 상태에서 목표 yaw 각도에 도달하지 못했으면 회전 명령을 발행하고, 도달하면 전진 상태로 전환합니다.
            if abs(angle_diff) > self.yaw_tolerance:
                twist.twist.linear.x = 0.0
                twist.twist.angular.z = self.angular_speed * (1 if angle_diff > 0 else -1)
            # 회전 상태에서 목표 yaw 각도에 도달하면 전진 상태로 전환합니다.
            else:
                self.state = "MOVE"

        # 전진 상태에서 장애물이 감지되면 회전 상태로 전환하고, 목표 yaw 각도를 설정합니다. 그렇지 않으면 전진 명령을 발행합니다.
        else:
            # 장애물이 감지되지 않으면 전진 명령을 발행합니다.
            if ...:
                twist.twist.linear.x = ...
                twist.twist.angular.z = ...
            # 장애물이 감지되면 회전 상태로 전환하고, 목표 yaw 각도를 설정합니다.
            else:  
                ...  # 전진 상태에서 장애물이 감지되면 회전 상태로 전환합니다.

                # 회전 방향을 결정하고 목표 yaw 각도를 설정합니다.
                turn_dir = 1 if left_avg > right_avg else -1
                self.target_yaw = self.normalize_anself.current_yaw + turn_dir * self.rotation_angle

                # 회전 상태에서 회전 명령을 발행합니다.
                twist.twist.linear.x = ...
                twist.twist.angular.z = ...

        self.cmd_pub.publish(twist)  # TwistStamped 메시지를 /cmd_vel 토픽에 publish하여 로봇을 제어합니다.

    # normalize_angle 함수는 각도를 -π에서 π 범위로 정규화합니다.
    def normalize_angle(self, angle):
        return math.atan2(math.sin(angle), math.cos(angle))



# -------------------------------------------------------------------------------------------------------------------------------------------------------------



def main():
    rclpy.init()
    node = SimpleYawObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()