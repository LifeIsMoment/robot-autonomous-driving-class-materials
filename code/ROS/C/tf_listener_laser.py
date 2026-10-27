import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from tf2_geometry_msgs import PointStamped
import tf2_ros
import math


# LaserTFListener 클래스는 ROS2 노드로, 레이저 스캔 데이터를 수신하고 각 포인트를 'hello_base_link' 프레임으로 변환하여 로그에 출력합니다.
class LaserTFListener(Node):
    def __init__(self):
        super().__init__('laser_tf')

        self.tf_buffer = tf2_ros.Buffer()
        self.tf_listener = tf2_ros.TransformListener(self.tf_buffer, self)
        self.sub = self.create_subscription(...)  # /scan 토픽에서 LaserScan 메시지를 구독하는 서브스크립션 생성

    # 레이저 스캔 데이터를 처리하고 각 포인트를 로봇 절대 좌표계로 변환합니다.
    def scan_callback(self, msg: LaserScan):
        i = 0        # 포인트 인덱스를 초기화합니다.
        angle = ...  # 레이저 스캔의 시작 각도를 초기화합니다.

        # 레이저 스캔의 각 거리 값을 반복합니다.
        for distance in ...:
            # 거리 값이 무한대이거나 NaN이면 다음 포인트로 넘어갑니다.
            if distance == float('inf') or math.isnan(distance):
                angle += msg.angle_increment
                continue

            # 레이저 스캔의 거리 데이터를 좌표로 변환합니다.
            x = ...
            y = ...

            # PointStamped 메시지를 생성하고 레이저 스캔 포인트를 설정합니다.
            point = PointStamped()
            point.header = ...   # LaserScan 데이터의 부모 프레임을 설정합니다.
            point.point.x = ...
            point.point.y = ...
            point.point.z = ...

            try:
                transformed = self.tf_buffer.transform(...)  # 포인트를 로봇 좌표계(프레임)으로 변환합니다.
                self.get_logger().info(
                    f"[{i}] TF point: x={transformed.point.x:.2f}, y={transformed.point.y:.2f}, z={transformed.point.z:.2f}"
                )
                i += 1  # 포인트 인덱스를 증가시킵니다.
            except Exception as e:
                self.get_logger().warn(f"TF not ready: {e}")

            angle += ...  # 레이저 스캔의 각도를 증가시킵니다.

def main():
    rclpy.init()
    node = LaserTFListener()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()