# 필요한 라이브러리 및 메시지 타입을 임포트
import math
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import TwistStamped
import rclpy
from rclpy.node import Node



# -------------------------------------------------------------------------------------------------------------------------------------------------------------



# SimpleObstacleAvoider 클래스는 ROS2 노드로, 레이저 스캔 데이터를 기반으로 장애물을 피하는 간단한 로직을 구현합니다.
class SimpleObstacleAvoider(Node):
    def __init__(self):
        super().__init__('simple_obstacle_avoider')  # 노드 이름을 'simple_obstacle_avoider'로 설정

        self.cmd_pub = self.create_publisher(TwistStamped, '/cmd_vel', 10)                     # /cmd_vel 토픽에 TwistStamped 메시지를 발행하는 퍼블리셔 생성
        self.scan_sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)   # /scan 토픽에서 LaserScan 메시지를 구독하는 서브스크립션 생성

        self.front_threshold = 0.25  # 정면 장애물 감지 거리 임계값
        self.linear_speed = 0.2      # 전진 속도
        self.angular_speed = 0.5     # 회전 속도

    # LaserScan 메시지를 수신할 때 호출되는 callback 함수
    def scan_callback(self, scan: LaserScan):
        left_vals = [r for r in scan.ranges[:31] if math.isfinite(r)]       # left_vals: 레이저 스캔의 왼쪽 30도 거리 값 중 유한한 값만 필터링
        left_avg = sum(left_vals)/len(left_vals) if left_vals else 0.0      # left_avg: 왼쪽 거리 값의 평균 계산, 값이 없으면 0.0으로 설정

        right_vals = [r for r in scan.ranges[-30:] if math.isfinite(r)]     # right_vals: 레이저 스캔의 오른쪽 30도 거리 값 중 유한한 값만 필터링
        right_avg = sum(right_vals)/len(right_vals) if right_vals else 0.0  # right_avg: 오른쪽 거리 값의 평균 계산, 값이 없으면 0.0으로 설정

        front_vals = left_vals + right_vals                                 # front_vals: 왼쪽과 오른쪽 거리 값의 합
        front_min = min(front_vals) if front_vals else float('inf')         # front_min: 정면 거리 값의 최솟값 계산, 값이 없으면 무한대로 설정

        twist = TwistStamped()  # TwistStamped 메시지 객체 생성

        twist.twist.linear.x = self.linear_speed    # 전진 속도를 설정
        twist.twist.angular.z = self.angular_speed  # 회전 속도를 설정
        
        self.cmd_pub.publish(twist)  # TwistStamped 메시지를 /cmd_vel 토픽에 publish하여 로봇을 제어



# -------------------------------------------------------------------------------------------------------------------------------------------------------------



# 실행 함수
def main():
    rclpy.init()
    node = SimpleObstacleAvoider()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


# 실제 실행
if __name__ == '__main__':
    main()